import struct, hashlib, sys
sys.path.insert(0, sys.argv[0].rsplit('/',1)[0])
from espimg import Img
src, dst = sys.argv[1], sys.argv[2]
im = Img(src)
d = bytearray(im.d)

def foff(addr):
    for a, l, o in im.segs:
        if a <= addr < a + l:
            return o + addr - a
    raise ValueError(hex(addr))

# 1) Rename name table entry "OUYA Game Controller" -> "8BitDo NGC Modkit"
i = d.find(b'OUYA Game Controller\0')
assert i > 0 and d.count(b'OUYA Game Controller\0') == 1
typ, sub, flags = struct.unpack_from('<iII', d, i + 252)
print('entry type %d subtype %d flags %#x' % (typ, sub, flags))
assert flags == 1 << 18
name = b'8BitDo NGC Modkit'
d[i:i + 249] = name + b'\0' * (249 - len(name))

# 2) mask literal of the OUYA quirk 0xBB1F0FFF -> 0xFF1F0FFF
lit = foff(0x400d184c)
assert struct.unpack_from('<I', d, lit)[0] == 0xBB1F0FFF
struct.pack_into('<I', d, lit, 0xFF1F0FFF)

# 3) Replace OUYA button remap (memset + btns) with the 8bitdo GC Modkit quirk
start, end = 0x400e66e0, 0x400e6730
o = foff(start)
assert bytes(d[o:o + 3]) == bytes.fromhex('a2c220')            # addi a10, a2, 0x20
assert bytes(d[foff(end):foff(end) + 2]) == bytes.fromhex('1df0')  # retw.n
def l32i(t, s, off): return bytes([(t << 4) | 2, (2 << 4) | s, off // 4])
def s32i(t, s, off): return bytes([(t << 4) | 2, (6 << 4) | s, off // 4])
def movi(t, imm): return bytes([(t << 4) | 2, 0xA0 | ((imm >> 8) & 0xF), imm & 0xFF])
B = lambda idx: 0x20 + idx * 4
RB_LEFT, RB_RIGHT, MS, LM, LS, LT, RM, RS, RT = 16, 17, 21, 24, 25, 26, 28, 29, 30
code = b''.join([
    l32i(3, 2, B(RB_LEFT)), l32i(4, 2, B(RB_RIGHT)),
    s32i(4, 2, B(RB_LEFT)), s32i(3, 2, B(RB_RIGHT)),
    l32i(3, 2, B(MS)), s32i(3, 2, B(RS)),
    movi(3, 0x100), s32i(3, 2, B(LT)),
    movi(3, 0x200), s32i(3, 2, B(RT)),
    movi(3, 0),
    s32i(3, 2, B(MS)), s32i(3, 2, B(LM)), s32i(3, 2, B(RM)), s32i(3, 2, B(LS)),
    bytes.fromhex('1df0'),  # retw.n
])
assert len(code) <= end - start
code += b'\x1d\xf0' * ((end - start - len(code)) // 2)  # unreachable filler
d[o:o + len(code)] = code

# 4) Rumble for the 8bitdo GC Modkit (report 0xA5: 0xDB, lf, hf like BlueRetro v24.10)
def j(pc, target):
    off = target - (pc + 4)
    assert -131072 <= off < 131072
    off &= 0x3FFFF
    return bytes([((off & 3) << 6) | 0x06, (off >> 2) & 0xFF, (off >> 10) & 0xFF])
def s8i(t, s, off): return bytes([(t << 4) | 2, (4 << 4) | s, off])
def bbsi(s, bit, pc, target):
    off = target - (pc + 4)
    assert 0 <= off < 256 and bit < 32
    return bytes([((bit & 0xF) << 4) | 7, ((0xE | (bit >> 4)) << 4) | s, off])
def movnez(r, s, t): return bytes([(t << 4), (r << 4) | s, 0x93])

# 4a) Disable the Stadia quirk block (beqz -> j) and use it as code cave
stadia_chk, stadia_end = 0x400e6661, 0x400e66bd
o = foff(stadia_chk)
assert bytes(d[o:o + 3]) == bytes.fromhex('168a05')  # beqz a10, 0x400e66bd
d[o:o + 3] = j(stadia_chk, stadia_end)
cave = 0x400e6664

# 4b) Hook hid_fb_from_generic: first instr after entry l32i a5, a3, 0xd4
hook = 0x400e4bbf
o = foff(hook)
assert bytes(d[o:o + 3]) == bytes.fromhex('522335')
d[o:o + 3] = j(hook, cave)

pc = cave
code = bytearray()
def emit(b):
    global pc
    code.extend(b); pc += len(b)
emit(l32i(4, 3, 8))                       # a4 = bt_data->base.flags[PAD]
bbsi_pc = pc; emit(b'\0\0\0')             # bbsi a4, 18 (OUYA bit = NGC Modkit), gc
emit(l32i(5, 3, 0xd4))                    # displaced instruction
emit(j(pc, hook + 3))                     # back to hid_fb_from_generic
gc = pc
code[bbsi_pc - cave:bbsi_pc - cave + 3] = bbsi(4, 18, bbsi_pc, gc)
emit(movi(4, 0xA5)); emit(s8i(4, 3, 0xA8))                      # report_id
emit(movi(4, 3)); emit(s8i(4, 3, 0xA9))                         # report_size = 3
emit(movi(4, 0)); emit(s8i(4, 3, 0xAA)); emit(s8i(4, 3, 0xAB)); emit(s8i(4, 3, 0xAC))
emit(movi(4, 0xDB)); emit(s8i(4, 3, 0x50))                      # state[0]
emit(l32i(5, 2, 4))                                             # fb_data->state
emit(movi(4, 0)); emit(movi(6, 0xFF)); emit(movnez(4, 6, 5))    # on ? 0xFF : 0
emit(s8i(4, 3, 0x51)); emit(s8i(4, 3, 0x52))                    # lf, hf
emit(bytes.fromhex('1df0'))                                     # retw.n
assert pc <= stadia_end, hex(pc)
o = foff(cave)
d[o:o + len(code)] = code

# 4c) bt_hid_cmd_generic_rumble: send report_size bytes instead of sizeof() = 0x5d
o = foff(0x400de3d7)
assert bytes(d[o:o + 3]) == bytes.fromhex('e2a05d')  # movi a14, 0x5d
d[o:o + 3] = bytes([0xE2, 0x03, 0x59])               # l8ui a14, a3, 0x59 (report_size)

# 5) Fix image checksum and SHA256
off = 24
for a, l, so in im.segs:
    off = so + l
chk = 0xEF
for a, l, so in im.segs:
    for b in d[so:so + l]:
        chk ^= b
pad = (16 - ((off + 1) % 16)) % 16
off += pad
d[off] = chk
off += 1
assert d[23] == 1
d[off:off + 32] = hashlib.sha256(bytes(d[:off])).digest()
open(dst, 'wb').write(bytes(d[:off + 32]))
print('written', dst, off + 32)
