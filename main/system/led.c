/*
 * Copyright (c) 2019-2024, Jacques Gagnon
 * SPDX-License-Identifier: Apache-2.0
 */

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <soc/efuse_reg.h>
#include "zephyr/atomic.h"
#include "system/gpio.h"
#include "driver/gpio.h"
#include "driver/ledc.h"
#include "esp_rom_gpio.h"
#include "soc/gpio_sig_map.h"
#include "adapter/config.h"
#include "led.h"

#ifdef CONFIG_BLUERETRO_SYSTEM_SEA_BOARD
#define ERR_LED_PIN 32
#elif defined(CONFIG_BLUERETRO_HW2_IBLUECONTROLMOD)
/* IO17 is the console power off line on this board, never drive it as LED! */
/* Top RGB LED, active low: green IO22 (status like the stock FW), blue IO23, red IO18 */
#define ERR_LED_PIN 22
#define ERR_LED_INV 1
#define STATUS_LED_BLUE_PIN 23
#define STATUS_LED_RED_PIN 18
#else
#define ERR_LED_PIN 17
#endif
#ifndef ERR_LED_INV
#define ERR_LED_INV 0
#endif
#define PICO_ERR_LED_PIN 20

/* LED flags */
enum {
    ERR_LED_SET = 0,
};

static atomic_t led_flags = 0;
static TaskHandle_t err_led_task_hdl;
static uint8_t err_led_pin = ERR_LED_PIN;

#ifdef CONFIG_BLUERETRO_HW2_IBLUECONTROLMOD
static void status_led_set_pin(uint8_t pin, uint32_t on) {
    esp_rom_gpio_connect_out_signal(pin, SIG_GPIO_OUT_IDX, false, false);
    gpio_set_level(pin, !on);
}

/* Like the stock FW: solid green while the console is on, whether a BT */
/* controller is connected or not (pairing is shown by the pulsing port LED), */
/* red on error and while sleeping */
static void status_led_update(void) {
    if (atomic_test_bit(&led_flags, ERR_LED_SET)) {
        status_led_set_pin(ERR_LED_PIN, 0);
        status_led_set_pin(STATUS_LED_BLUE_PIN, 0);
        status_led_set_pin(STATUS_LED_RED_PIN, 1);
    }
    else {
        status_led_set_pin(ERR_LED_PIN, 1);
        status_led_set_pin(STATUS_LED_BLUE_PIN, 0);
    }
}

void err_led_refresh(void) {
    status_led_update();
}

void err_led_sleep(void) {
    /* Red while sleeping, like the stock FW */
    status_led_set_pin(ERR_LED_PIN, 0);
    status_led_set_pin(STATUS_LED_BLUE_PIN, 0);
    status_led_set_pin(STATUS_LED_RED_PIN, 1);
    gpio_hold_en(ERR_LED_PIN);
    gpio_hold_en(STATUS_LED_BLUE_PIN);
    gpio_hold_en(STATUS_LED_RED_PIN);
}
#else
void err_led_refresh(void) {
}

void err_led_sleep(void) {
}
#endif

static void err_led_task(void *param) {
    while (1) {
        if (!atomic_test_bit(&led_flags, ERR_LED_SET)) {
            ledc_set_fade_time_and_start(LEDC_HIGH_SPEED_MODE, LEDC_CHANNEL_0, hw_config.led_pulse_duty_max,
                hw_config.led_pulse_fade_time_ms, LEDC_FADE_NO_WAIT);
            vTaskDelay(hw_config.led_pulse_fade_cycle_delay_ms / portTICK_PERIOD_MS);
            ledc_set_fade_time_and_start(LEDC_HIGH_SPEED_MODE, LEDC_CHANNEL_0, hw_config.led_pulse_duty_min,
                hw_config.led_pulse_fade_time_ms, LEDC_FADE_NO_WAIT);
            vTaskDelay(hw_config.led_pulse_fade_cycle_delay_ms / portTICK_PERIOD_MS);
        }
        else {
            vTaskSuspend(err_led_task_hdl);
        }
    }
}

void err_led_init(uint32_t package) {
    ledc_timer_config_t ledc_timer = {
        .duty_resolution = LEDC_TIMER_13_BIT,
        .freq_hz = hw_config.led_pulse_hz,
        .speed_mode = LEDC_HIGH_SPEED_MODE,
        .timer_num = LEDC_TIMER_0,
        .clk_cfg = LEDC_AUTO_CLK,
    };
    ledc_channel_config_t ledc_channel = {
        .channel    = LEDC_CHANNEL_0,
        .duty       = hw_config.led_pulse_off_duty_cycle,
        .gpio_num   = ERR_LED_PIN,
        .speed_mode = LEDC_HIGH_SPEED_MODE,
        .hpoint     = 0,
        .timer_sel  = LEDC_TIMER_0,
        .flags.output_invert = ERR_LED_INV,
    };

    if (package == EFUSE_RD_CHIP_VER_PKG_ESP32PICOV302) {
        ledc_channel.gpio_num = PICO_ERR_LED_PIN;
        err_led_pin = PICO_ERR_LED_PIN;
    }

    ledc_timer_config(&ledc_timer);
    ledc_channel_config(&ledc_channel);
    ledc_fade_func_install(0);
    ledc_set_duty_and_update(LEDC_HIGH_SPEED_MODE, LEDC_CHANNEL_0, hw_config.led_pulse_off_duty_cycle, 0);

#ifdef CONFIG_BLUERETRO_HW2_IBLUECONTROLMOD
    gpio_config_t io_conf = {
        .pin_bit_mask = BIT64(STATUS_LED_BLUE_PIN) | BIT64(STATUS_LED_RED_PIN),
        .mode = GPIO_MODE_OUTPUT,
    };
    gpio_set_level(STATUS_LED_BLUE_PIN, 1);
    gpio_set_level(STATUS_LED_RED_PIN, 1);
    gpio_config(&io_conf);
#endif

    xTaskCreatePinnedToCore(&err_led_task, "err_led_task", 768, NULL, 5, &err_led_task_hdl, 0);
    err_led_clear();
    err_led_refresh();
}

void err_led_cfg_update(void) {
    ledc_set_freq(LEDC_HIGH_SPEED_MODE, LEDC_TIMER_0, hw_config.led_pulse_hz);
}

void err_led_set(void) {
    vTaskSuspend(err_led_task_hdl);
    ledc_set_duty_and_update(LEDC_HIGH_SPEED_MODE, LEDC_CHANNEL_0, hw_config.led_pulse_on_duty_cycle, 0);
    atomic_set_bit(&led_flags, ERR_LED_SET);
    err_led_refresh();
}

void err_led_clear(void) {
    /* When error is set it stay on until power cycle */
    if (!atomic_test_bit(&led_flags, ERR_LED_SET)) {
        vTaskSuspend(err_led_task_hdl);
        ledc_set_duty_and_update(LEDC_HIGH_SPEED_MODE, LEDC_CHANNEL_0, hw_config.led_pulse_off_duty_cycle, 0);
    }
}

void err_led_pulse(void) {
    vTaskResume(err_led_task_hdl);
}

uint32_t err_led_get_pin(void) {
    return err_led_pin;
}

uint32_t err_led_get_inv(void) {
    return ERR_LED_INV;
}
