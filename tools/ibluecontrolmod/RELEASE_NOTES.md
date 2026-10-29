Aktuelles BlueRetro (Stand v25.10-beta) für das AliExpress-Board **„iBlueControlMod“**,
das interne Bluetooth-Controllerport-Board für die GameCube (Platinenaufdruck „V1.1“).

## Neu gegenüber der Original-Firmware des Boards

* **8BitDo GameCube Mod Kit:** wird erkannt, mit analogen Schultertasten und Rumble
* Alle Verbesserungen von BlueRetro seit v1.9, auf der die Original-Firmware basiert
* **Rumble ab Werk eingeschaltet**
* **Schlafmodus** (Reset-Taste beim Einschalten 3 s halten), z. B. für Final Fantasy
  Crystal Chronicles mit GBA als Controller
* **GBA-Link** mit BT-Controller, z. B. Pokémon Colosseum ↔ Pokémon Blattgrün

## Getestet

Start und Bild, Flashen per Bluetooth und Rückweg per 30 s Reset, 8BitDo GameCube Mod Kit
inkl. analoger Trigger und Rumble, Xbox-One-Controller inkl. Rumble, Schlafmodus,
GBA-Link mit Final Fantasy Crystal Chronicles (Schlafmodus) und Pokémon Colosseum ↔
Blattgrün (mit BT-Controller).

## Installation

1. `BlueRetro_iblue_gc.bin` herunterladen.
2. Konsole einschalten, BT-Controller aus.
3. In Chrome/Edge https://blueretro.io/ota.html öffnen, **Connect BlueRetro**, Datei
   auswählen, **Update Firmware**. Danach Konsole aus- und einschalten.

**Zurück zur Original-Firmware:** Reset-Taste der Konsole 30 s gedrückt halten. Die
Original-Firmware wird nie überschrieben.

Ausführliche Anleitung, Notfall-Wiederherstellung per Kabel und alle Unterschiede zur
chinesischen Firmware: [tools/ibluecontrolmod/README.md](https://github.com/konsolenschatz/BlueRetro-iBlueControlMod/blob/master/tools/ibluecontrolmod/README.md)

## Dateien

| Datei | Wofür |
|---|---|
| `BlueRetro_iblue_gc.bin` | **Normale Firmware**, für alle |
| `BlueRetro_iblue_gc_safe.bin` | Nur falls das Board neu startet oder Bluetooth ständig abreißt: geringere Sendeleistung, Brownout-Schutz aus |
| `otadata_ota0.bin` | Nur für das Flashen per Kabel (an `0xd000`, Firmware an `0x110000`) |
| `otadata_leer.bin` | Nur für die Notfall-Wiederherstellung per Kabel (an `0xd000`) |

**Unterstützen:** Wenn dir das Projekt hilft, freue ich mich über eine kleine Spende per
[PayPal](https://www.paypal.biz/PDHBeats). Mehr Retro-Mods gibt es auf meinem YouTube-Kanal
[Konsolenschatz](https://www.youtube.com/@Konsolenschatz).

---

**English:** Current BlueRetro for the AliExpress "iBlueControlMod" internal GameCube board,
with 8BitDo GameCube Mod Kit support (analog triggers, rumble), rumble on by default, sleep
mode (hold reset while powering on) and working GBA link. Flash `BlueRetro_iblue_gc.bin` with
https://blueretro.io/ota.html; hold the console reset button for 30 s to return to the stock
firmware.
