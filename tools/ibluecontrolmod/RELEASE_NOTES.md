Current BlueRetro (v25.10-beta) for the AliExpress **"iBlueControlMod"** board, the internal
Bluetooth controller port board for the GameCube (PCB marking "V1.1").

## New compared to the board's stock firmware

* **8BitDo GameCube Mod Kit:** detected, with analog triggers and rumble
* **Nintendo Switch 2 / NSO GameCube controller** fixes from RyanCopley/BlueRetro (several pads at once, no more lock-outs after a bad pairing)
* All BlueRetro improvements since v1.9, which the stock firmware is based on
* **Rumble enabled out of the box**
* **Sleep mode** (hold the reset button for 3 s while powering on), e.g. for Final Fantasy
  Crystal Chronicles with the GBA as controller
* **GBA link** with a BT controller, e.g. Pokémon Colosseum ↔ Pokémon LeafGreen

## Tested

Boot and video, flashing over Bluetooth and going back with a 30 s reset, 8BitDo GameCube Mod
Kit incl. analog triggers and rumble, Xbox One controller incl. rumble, sleep mode, GBA link
with Final Fantasy Crystal Chronicles (sleep mode) and Pokémon Colosseum ↔ LeafGreen (with a
BT controller).

## Installation

1. Download `BlueRetro_iblue_gc.bin`.
2. Switch on the console, BT controllers off.
3. In Chrome/Edge open https://blueretro.io/ota.html, **Connect BlueRetro**, select the file,
   **Update Firmware**. Then switch the console off and on.

**Back to the stock firmware:** hold the console reset button for 30 s. The stock firmware is
never overwritten.

Full guide, cable recovery with pinout photos and all differences to the Chinese firmware:
[English](https://github.com/konsolenschatz/BlueRetro-iBlueControlMod/blob/master/tools/ibluecontrolmod/README.md) ·
[Deutsch](https://github.com/konsolenschatz/BlueRetro-iBlueControlMod/blob/master/tools/ibluecontrolmod/README.de.md)

## Files

| File | Purpose |
|---|---|
| `BlueRetro_iblue_gc.bin` | **Regular firmware**, for everyone |
| `BlueRetro_iblue_gc_safe.bin` | Only if the board reboots or Bluetooth keeps dropping: lower TX power, brownout detection off |
| `otadata_ota0.bin` | Only for flashing over a cable (at `0xd000`, firmware at `0x110000`) |
| `otadata_leer.bin` | Only for emergency recovery over a cable (at `0xd000`) |

**Support:** If this project helps you, a small donation via
[PayPal](https://www.paypal.biz/PDHBeats) is very welcome. More retro mods on my YouTube
channel [Konsolenschatz](https://www.youtube.com/@Konsolenschatz).

---

**Deutsch:** Aktuelles BlueRetro für das AliExpress-Board „iBlueControlMod“ mit Unterstützung
für das 8BitDo GameCube Mod Kit (analoge Schultertasten, Rumble), Fixes für den NSO-GameCube-Controller, Rumble ab Werk, Schlafmodus
(Reset-Taste beim Einschalten 3 s halten) und funktionierendem GBA-Link. `BlueRetro_iblue_gc.bin`
über https://blueretro.io/ota.html flashen; zurück zur Original-Firmware mit 30 s Reset-Taste.
[Ausführliche Anleitung auf Deutsch](https://github.com/konsolenschatz/BlueRetro-iBlueControlMod/blob/master/tools/ibluecontrolmod/README.de.md)
