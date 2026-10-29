# BlueRetro für das AliExpress „iBlueControlMod“ GameCube-Board (V1.1)

Aktuelles [BlueRetro](https://github.com/darthcloud/BlueRetro) (Stand v25.10-beta) für das
interne Bluetooth-Controllerport-Board „iBlueControlMod“ von AliExpress
(ESP32-WROOM-32E, 8 MB Flash, Platinenaufdruck „V1.1“). Das Board ersetzt die
Controllerport-Platine der GameCube, inklusive Reset-Taste und Uhr-Batterie.

> **English summary:** Current BlueRetro for the AliExpress "iBlueControlMod" internal
> GameCube board. Flash `BlueRetro_iblue_gc.bin` over Bluetooth with
> https://blueretro.io/ota.html. The stock firmware stays in the factory slot; holding the
> console reset button for 30 s always brings it back. The vendor's warning that BlueRetro
> damages the board comes from two pin changes (power off on IO17, console enable on IO13
> that must be held high) which this build takes care of.

**Unterstützen:** Wenn dir das Projekt hilft, freue ich mich über eine kleine Spende per
[PayPal](https://www.paypal.biz/PDHBeats). Mehr Retro-Mods gibt es auf meinem YouTube-Kanal
[Konsolenschatz](https://www.youtube.com/@Konsolenschatz).

## Inhalt

* [Was funktioniert (getestet)](#was-funktioniert-getestet)
* [Flashen per Bluetooth](#flashen-per-bluetooth)
* [Zurück zur Original-Firmware](#zurück-zur-original-firmware)
* [Reset-Taste und Schlafmodus](#reset-taste-und-schlafmodus)
* [GBA-Link](#gba-link)
* [Notfall: Wiederherstellung per Kabel (UART)](#notfall-wiederherstellung-per-kabel-uart)
* [Was die chinesische Firmware vom Original unterscheidet](#was-die-chinesische-firmware-vom-original-unterscheidet)
* [Wie die Firmware portiert wurde](#wie-die-firmware-portiert-wurde)
* [Selbst bauen](#selbst-bauen)

## Was funktioniert (getestet)

Getestet auf einer GameCube mit PicoBoot, Bild über den Analog-Ausgang.

| Funktion | Ergebnis |
|---|---|
| Start und Bild | ✅ |
| Flashen per Bluetooth (blueretro.io/ota.html) und Rückweg per 30 s Reset | ✅ |
| **8BitDo GameCube Mod Kit**: Erkennung, analoge Schultertasten, **Rumble** | ✅ |
| Xbox-One-Controller inkl. Rumble | ✅ |
| Rumble ab Werk eingeschaltet (Advanced Config → Accessories) | ✅ |
| **Schlafmodus** (Reset-Taste beim Einschalten 3 s halten) | ✅ |
| GBA-Link im Schlafmodus: Final Fantasy Crystal Chronicles mit GBA als Controller | ✅ |
| GBA-Link mit BT-Controller: Pokémon Colosseum ↔ Pokémon Blattgrün | ✅ |

Nicht eigens getestet, sollte aber wie im normalen BlueRetro funktionieren: alle anderen
von BlueRetro unterstützten Controller (PS3/PS4/PS5, Switch Pro/Joy-Con, Wii U Pro, …),
mehrere Controller gleichzeitig und die Web-Konfiguration auf https://blueretro.io.

## Flashen per Bluetooth

Die Original-Firmware bringt den OTA-Mechanismus von BlueRetro v1.9 mit, die offizielle
Update-Seite funktioniert deshalb direkt. Du brauchst Chrome oder Edge am PC oder Chrome
unter Android (Web Bluetooth).

1. Aus dem [Release](../../releases) `BlueRetro_iblue_gc.bin` herunterladen.
2. Alle Bluetooth-Controller ausschalten, Konsole einschalten.
3. https://blueretro.io/ota.html öffnen, **Connect BlueRetro** klicken und das Gerät
   `BlueRetro…` auswählen.
4. `BlueRetro_iblue_gc.bin` auswählen und **Update Firmware** klicken.
   Das dauert einige Minuten, die Konsole dabei nicht ausschalten.
5. Nach „OTA FW Update sucessfull!“ die Konsole aus- und wieder einschalten.

Bricht das Update ab, bleibt die bisherige Firmware aktiv. Die neue wird erst nach
erfolgreicher Prüfung als Startpartition gesetzt.

**Welche Datei?**

| Datei | Wofür |
|---|---|
| `BlueRetro_iblue_gc.bin` | **Normale Firmware**, für alle |
| `BlueRetro_iblue_gc_safe.bin` | Nur falls das Board mit der normalen Firmware neu startet oder Bluetooth ständig abreißt: geringere Sendeleistung, Brownout-Schutz aus, 20 s keine Kopplungssuche nach dem Start |
| `otadata_ota0.bin` | Nur für das Flashen per Kabel (siehe unten) |
| `otadata_leer.bin` | Nur für die Notfall-Wiederherstellung per Kabel |

Die Dateien heißen bewusst nicht „hw2“: Die Update-Seite hält die Original-Firmware
(Version „1“) für HW1 und würde eine „hw2“-Datei mit „Hardware and firmware mismatch!“
ablehnen.

## Zurück zur Original-Firmware

Die Original-Firmware wird nie überschrieben. Sie liegt im Factory-Bereich, BlueRetro
landet im Bereich `ota_0`.

* **Reset-Taste der Konsole 30 s gedrückt halten** (Konsole an). BlueRetro löscht seine
  Einstellungen und die Startauswahl, danach startet wieder die Original-Firmware.
* Danach kannst du jederzeit wieder BlueRetro per Bluetooth aufspielen.

## Reset-Taste und Schlafmodus

| Reset-Taste halten (Konsole an) | Wirkung | Port-LEDs während des Haltens |
|---|---|---|
| kurz (< 3 s) | Konsole zurücksetzen (wie die originale Reset-Taste) | an |
| 3–6 s | Alle BT-Controller trennen bzw. Kopplungssuche beenden | blinken langsam |
| 6–9 s | Kopplungssuche starten | blinken schneller |
| > 9 s | BlueRetro-Einstellungen und Kopplungen löschen | blinken schnell |
| 30 s | Zusätzlich zurück zur Original-Firmware | |

**Schlafmodus:** Reset-Taste gedrückt halten, **während** du die Konsole einschaltest, und
nach etwa 3 s loslassen. Bluetooth geht aus, die Platine greift nicht mehr in die
Controller-Ports ein und die Konsole startet normal. Gedacht für Zubehör, das sich mit
BlueRetro nicht verträgt, zum Beispiel den GBA als Controller in Final Fantasy Crystal
Chronicles. Zum Steuern dann einen Original-Controller mit Kabel benutzen.
Normalbetrieb: Konsole aus- und ohne gedrückte Taste wieder einschalten.

## GBA-Link

Das Board treibt einen Controller-Port nur, wenn dort ein Bluetooth-Controller
zugeordnet ist. Ein eingestecktes GBA-Link-Kabel erkennt das Board nicht als Controller,
deshalb:

* **Pokémon Colosseum/XD ↔ GBA:** Einen BT-Controller verbinden (landet auf Port 1), den
  GBA an einen anderen Port stecken. Keinen weiteren BT-Controller verbinden, sonst
  bekommt dieser den Port des GBA.
* **Final Fantasy Crystal Chronicles** und andere Spiele, in denen alle Spieler einen GBA
  benutzen: im **Schlafmodus** starten.

## Notfall: Wiederherstellung per Kabel (UART)

Nur nötig, falls eine Firmware gar nicht mehr startet und weder Bluetooth noch die
Reset-Taste reagieren. Bootloader und Original-Firmware werden dabei nicht verändert.

Du brauchst einen USB-Seriell-Adapter mit **3,3 V**-Pegel (getestet: DSD TECH SH-U09B3,
CP2102N) und Chrome oder Edge.

**Debug-Header** neben dem ESP32 (6 Löcher, das eckige Pad ist Loch 1):

| Loch | Signal | Adapter |
|---|---|---|
| 1 (eckig) | GND | GND |
| 2 | IO1 / TX | RXD |
| 3 | IO3 / RX | TXD |
| 4 | EN | frei |
| 5 | IO0 | nur zum Flashen auf GND (z. B. Metallgehäuse eines Controllerports) |
| 6 | 3V3 | **frei**, das Board bekommt Strom von der Konsole |

5V0, RTS und CTS des Adapters bleiben frei.

1. Konsole aus, Kabel anschließen, IO0 auf GND brücken.
2. Konsole einschalten. Der ESP32 startet im Download-Modus.
3. https://espressif.github.io/esptool-js/ öffnen, Baudrate 115200, **Connect**.
   Kommt keine Verbindung, TXD und RXD tauschen.
4. Flash Address **`0xd000`**, Datei **`otadata_leer.bin`**, **Program**.
   **Nicht „Erase Flash“ drücken**, das würde auch die Original-Firmware löschen.
5. Konsole aus, IO0-Brücke entfernen, Konsole ein: Die Original-Firmware läuft wieder.

**Boot-Log mitlesen:** gleiche Verkabelung ohne IO0-Brücke, z. B. mit
https://serial.huhn.me/ und **921600 Baud**, Monitor verbinden und dann die Konsole einschalten.

**BlueRetro per Kabel flashen** (statt Bluetooth): wie oben, aber zwei Dateien schreiben:
`otadata_ota0.bin` an `0xd000` und `BlueRetro_iblue_gc.bin` an `0x110000`.

## Was die chinesische Firmware vom Original unterscheidet

Die Original-Firmware des Boards (Dump im Repo
[zeus86/blueretro-gc-internal-hw2-aliexpress](https://github.com/zeus86/blueretro-gc-internal-hw2-aliexpress))
ist ein leicht angepasstes **BlueRetro v1.9 / v1.9.1-beta** (Stand 2023), gebaut mit
ESP-IDF v5.1.1, App-Version „1“. Partitionstabelle, Bluetooth-Konfigurationsdienst und
OTA sind mit BlueRetro identisch. Unterschiede:

| Funktion | BlueRetro HW2 | iBlueControlMod |
|---|---|---|
| Konsole AUS (Power off) | IO16 | **IO17** |
| Konsole AN (IO13) | 20-ms-Puls nur bei Bedarf | **1 s nach dem Start HIGH und dauerhaft halten**, sonst bleibt das Bild schwarz |
| Reset-Taste (Eingang) | IO0 | **IO16** (interner Pull-up nötig) |
| Status-LED | IO17 (PWM) | RGB-LED, aktiv-low: grün IO22, blau IO23, rot IO18 |
| Port-LEDs P1..P4 | IO2, IO4, IO12, IO15 | **IO15, IO4, IO2, IO12** |
| Reset / Power-Sense | IO14 / IO39 | gleich |
| Port-Erkennung P1..P4 | IO35, IO36, IO32, IO33 | gleich |
| Controller-Daten P1..P4 | IO19, IO5, IO26, IO27 | gleich |
| Reset-Taste Schwellen | 1 s / 3 s / 6 s | 3 s / 6 s / 9 s |
| Reset-Taste beim Einschalten | Deep Sleep | eigene Schlaf-Task |

Dazu kommen nur chinesische Log-Ausgaben. Funktional ist der Rest BlueRetro v1.9.
Insbesondere fehlt der Original-Firmware alles, was BlueRetro seitdem dazugelernt hat,
zum Beispiel die Unterstützung für das 8BitDo GameCube Mod Kit (analoge Schultertasten
und Rumble).

**Warum originales BlueRetro das Board „beschädigt“ (Herstellerwarnung):** Original-BlueRetro
für HW2 benutzt IO17 als blinkende Status-LED. Auf diesem Board hängt an IO17 aber die
Leitung zum Ausschalten der Konsole. Außerdem setzt es IO13 nicht dauerhaft auf HIGH,
die Konsole bleibt dann schwarz. Kaputt geht dabei nichts, mit 30 s Reset bzw. per Kabel
kommt man immer zurück.

## Wie die Firmware portiert wurde

1. **Analyse der Original-Firmware:** Die App-Partition wurde aus dem Flash-Dump
   extrahiert und disassembliert (Capstone, Xtensa). Anhand der Text-Strings und des
   bekannten BlueRetro-v1.9-Quellcodes wurden die Funktionen zugeordnet und die
   Pin-Belegung oben abgeleitet.
2. **Board-Variante im aktuellen BlueRetro:** `CONFIG_BLUERETRO_HW2_IBLUECONTROLMOD`
   (`configs/hw2/gamecube_ibluecontrolmod`) setzt die Pins, die Reset-Taste auf IO16 mit
   Pull-up, die Schwellen 3/6/9 s und Hotplug (ein Port wird erst angesteuert, wenn dort
   ein BT-Controller verbunden ist; das hält Ports für den GBA frei).
3. **Fehlersuche „kein Bild“:** Die ersten Builds starteten, aber die Konsole blieb
   schwarz. Ein Funktions- und Datenvergleich zwischen der Original-Firmware und einem
   eigenen v1.9-Rebuild zeigte keinen Unterschied in der Programmlogik. Erst der Vergleich
   der seriellen Boot-Logs zeigte, dass die Original-Firmware 1 s nach dem Start IO13
   (Konsole AN) auf HIGH setzt und hält. Das ist jetzt nachgebaut, auch im Schlafmodus.
4. **Komfort:** Rumble ist ab Werk eingeschaltet. Die Original-Firmware legt nach einem
   Reset ihre Konfiguration mit Rumble aus neu an, deshalb schaltet BlueRetro es beim ersten
   Start einmalig ein. Eine spätere eigene Einstellung bleibt erhalten.
5. **OTA-kompatibel:** Der Dateiname enthält kein „hw2“, damit blueretro.io/ota.html das
   Update von der Original-Firmware aus akzeptiert.

Im Ordner `stockpatch/` liegt außerdem ein älterer Binär-Patch, der der Original-Firmware
nur die 8BitDo-Mod-Kit-Unterstützung hinzufügt. Mit dieser Firmware wird er nicht mehr
gebraucht.

## Selbst bauen

GitHub Actions: Workflow „ibluecontrolmod“ läuft bei jedem Push auf `main`. Manuell über
„Run workflow“ mit ausgefülltem `release_tag` (z. B. `v25.10-iblue.2`) entsteht zusätzlich
ein Release-Entwurf mit allen Dateien.

Lokal (ESP-IDF 5.5):

    cp configs/hw2/gamecube_ibluecontrolmod sdkconfig
    BR_HW=_iblue BR_SYS=_gc idf.py reconfigure build
    python3 tools/ibluecontrolmod/gen_otadata_ota0.py build/otadata_ota0.bin

Lizenz: Apache-2.0 wie BlueRetro. Danke an Jacques Gagnon (darthcloud) für BlueRetro und an
zeus86 für Dump und Fotos des Boards.
