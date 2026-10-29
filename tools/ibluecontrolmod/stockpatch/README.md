# 8BitDo NGC Modkit patch for the stock iBlueControlMod firmware

Binary patch of the stock app (BlueRetro v1.9 based, built 2024-01-15, factory
partition of `iblueretro_stock-fw_8M.bin`, sha256 of the extracted app
`67caef65...`). Only the OUYA controller entry is repurposed:

* name table entry "OUYA Game Controller" -> "8BitDo NGC Modkit" (HID generic, quirk bit 18)
* OUYA quirk mask literal 0xBB1F0FFF -> 0xFF1F0FFF
* OUYA quirk button remap replaced by the 8bitdo GC Modkit remap from BlueRetro v24.10 (5f9608f)
* rumble: hid_fb_from_generic hooked (code cave in the disabled Stadia quirk block,
  Stadia controllers keep working without their special remap) to build the
  8bitdo vendor rumble report 0xA5 {0xDB, lf, hf}
* bt_hid_cmd_generic_rumble sends report_size bytes instead of a fixed 0x5D (like fc7da9e)
* image checksum and SHA256 recomputed

Usage (`stock_app.bin` = factory partition trimmed to the image size, 566512 bytes):

    python3 patch_stock.py stock_app.bin BlueRetro_stock_8bitdo_ngc.bin

Flash the result with https://blueretro.io/ota.html.
