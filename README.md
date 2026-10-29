# BlueRetro für das AliExpress „iBlueControlMod“ GameCube-Board

Aktuelles [BlueRetro](https://github.com/darthcloud/BlueRetro) für das interne
Bluetooth-Controllerport-Board „iBlueControlMod“ von AliExpress (Platinenaufdruck „V1.1“).
Mit 8BitDo-GameCube-Mod-Kit-Unterstützung inklusive analoger Schultertasten und Rumble,
Schlafmodus und funktionierendem GBA-Link.

* **Download:** [Releases](../../releases), Datei `BlueRetro_iblue_gc.bin`
* **Anleitung** (Flashen per Bluetooth, Rückweg zur Original-Firmware, Reset-Taste, GBA-Link,
  Unterschiede zur chinesischen Firmware): [tools/ibluecontrolmod/README.md](tools/ibluecontrolmod/README.md)

> **English:** Current BlueRetro for the AliExpress "iBlueControlMod" internal GameCube board.
> Get `BlueRetro_iblue_gc.bin` from the releases and flash it with https://blueretro.io/ota.html.
> Holding the console reset button for 30 s returns to the stock firmware.
> Support the project: [PayPal](https://www.paypal.biz/PDHBeats) · YouTube: [Konsolenschatz](https://www.youtube.com/@Konsolenschatz)
> Details (German, with English summary): [tools/ibluecontrolmod/README.md](tools/ibluecontrolmod/README.md)

**Unterstützen:** Wenn dir das Projekt hilft, freue ich mich über eine kleine Spende per
[PayPal](https://www.paypal.biz/PDHBeats). Mehr Retro-Mods gibt es auf meinem YouTube-Kanal
[Konsolenschatz](https://www.youtube.com/@Konsolenschatz).

Unabhängiges Community-Projekt, nicht verbunden mit dem Hersteller des Boards oder mit
dem BlueRetro-Projekt. Nutzung auf eigene Gefahr.

Below is the original BlueRetro README.

---

**This repository has been archived and is no longer under active development or maintenance.**

```
After 6 years working on BlueRetro, the time has come for me to move on
and focus on my family and my real job.

The code remains available as-is for reference, learning, and community use,
but no new features, bug fixes, or pull requests will be accepted.

Thank you to everyone who contributed, tested, reported issues,
or supported the project over the years.
Your involvement made BlueRetro what it is today.

If you are looking to build upon this work, please feel free to
fork the repository in accordance with the license.

Thank you,
Jacques Gagnon
```

# BlueRetro

<p align="center"><img src="/static/PNGs/BRE_Logo_Color_Outline.png" width="600"/></p>
<br>
<p align="justify">BlueRetro is a multiplayer Bluetooth controllers adapter for various retro game consoles & computers. Lost or broken controllers? Reproduction too expensive? Need those rare and obscure accessories? Just use the Bluetooth devices you already got! The project is open source hardware & software under the CERN-OHL-P-2.0 & Apache-2.0 licenses respectively. It's built for the popular ESP32 chip. Wii, Switch, PS3, PS4, PS5, Xbox One, Xbox Series X|S & generic HID Bluetooth (BR/EDR & LE) devices are supported. Parallel 1P (Computers, NeoGeo, Supergun, JAMMA, Handheld, etc), Parallel 2P (Atari 2600/7800, Master System, Computers, etc), NES, PCE / TG16, Mega Drive / Genesis, SNES, CD-i, 3DO, Jaguar, Saturn, PSX, PC-FX, JVS (Arcade), Virtual Boy, N64, Dreamcast, PS2, GameCube & Wii extension are supported with simultaneous 4+ players using a single adapter.</p>

## READ THIS FIRST
* [Project documentation](https://github.com/darthcloud/BlueRetro/wiki)

## Need help?
* [Open a GitHub discussion](https://github.com/darthcloud/BlueRetro/discussions)

## Makers sponsoring BlueRetro
Buying BlueRetro adapters from these makers helps support the continued development of the BlueRetro firmware!\
Thanks to all sponsors!

* [Laser Bear Industries](https://www.laserbear.net)
* [Humble Bazooka](https://www.humblebazooka.com)
* [RetroOnyx](https://www.retroonyx.com/)
* [RetroTime](https://8bitmods.com/retrotime)

## Community Contribution
* BlueRetro PS1/2 Receiver by [mi213](https://twitter.com/mi213ger): 3D printed case & PCB for building DIY PS1/2 dongle.\
  https://github.com/Micha213/BlueRetro-PS1-2-Receiver
* N64 BlueRetro Mount by [reventlow64](https://twitter.com/reventlow): 3d printed mount for ESP32-DevkitC for N64.\
  https://www.prusaprinters.org/prints/90275-nintendo-64-blueretro-bluetooth-receiver-mount
* BlueRetro Adapter Case by [Sigismond0](https://twitter.com/Sigismond0): 3d printed case for ESP32-DevkitC.\
  https://www.prusaprinters.org/prints/116729-blueretro-bluetooth-controller-adapter-case
* BlueRetro AIO by [pmgducati](https://github.com/pmgducati): BlueRetro Through-hole base and cable PCBs.\
  https://github.com/pmgducati/Blue-Retro-AIO-Units
* BlueRetro HW2 internal guides by [Nostalgic Indulgences](https://twitter.com/nosIndulgences): Internal install guides\
  https://github.com/nostalgic-indulgences/BlueRetro_Internal_Installation
* BlueRetro latency test by [GamingNJncos](https://twitter.com/GamingNJncos): Documentation on how to run BlueRetro latency test\
  https://github.com/GamingNJncos/BLE-3D-Saturn-Public/tree/main/BlueRetro_Latency_Testing
* BR4N64 by [TharathielCB](https://github.com/TharathielCB): Internal BlueRetro Flex-PCB for Nintendo 64\
  https://github.com/TharathielCB/BR4N64
* BlueMemCard by [ChrispyNugget](https://github.com/ChrispyNugget): Replacement PCB for PSX memory card that incorporates PicoMemcard and BlueRetro support\
  https://github.com/ChrispyNugget/BlueMemCard
* BlueRetro HW2 QSB for GameCube by [Arthrimus](https://github.com/Arthrimus): Internal Blueretro PCB with CurrentTrigger for GameCube\
  https://github.com/Arthrimus/BlueRetro-HW2-GameCube

<br><p align="center"><img src="https://cdn.hackaday.io/images/4560691598833898038.png" height="200"/></p>
