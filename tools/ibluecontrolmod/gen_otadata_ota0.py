#!/usr/bin/env python3
# Generate an otadata partition image (0x2000 bytes) that boots the ota_0 slot.
# The factory slot (stock iBlueControlMod FW) stays untouched, erasing otadata
# (BlueRetro 30s button hold or esptool erase_region 0xd000 0x2000) boots it again.
import binascii
import struct
import sys

seq = 1  # ota_seq 1 -> ota_0
entry = struct.pack('<I', seq) + b'\xff' * 20 + struct.pack('<I', 0xFFFFFFFF)
entry += struct.pack('<I', binascii.crc32(struct.pack('<I', seq), 0xFFFFFFFF) & 0xFFFFFFFF)
otadata = bytearray(b'\xff' * 0x2000)
otadata[0:len(entry)] = entry
with open(sys.argv[1] if len(sys.argv) > 1 else 'otadata_ota0.bin', 'wb') as f:
    f.write(otadata)
