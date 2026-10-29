import struct, capstone, sys, re
class Img:
    def __init__(s,path):
        d=open(path,'rb').read(); s.d=d
        n=d[1]; off=24; s.segs=[]
        for i in range(n):
            a,l=struct.unpack('<II',d[off:off+8]); s.segs.append((a,l,off+8)); off+=8+l
    def read(s,addr,n):
        for a,l,o in s.segs:
            if a<=addr<a+l: return s.d[o+addr-a:o+addr-a+n]
        return None
    def u32(s,a):
        b=s.read(a,4); return struct.unpack('<I',b)[0] if b and len(b)==4 else None
    def cstr(s,a):
        b=s.read(a,200)
        if not b: return None
        b=b.split(b'\0')[0]
        try:
            t=b.decode()
            if len(t)>=3 and all(32<=ord(c)<127 or c in '\n\r\t\x1b' for c in t): return t
        except: pass
        return None
    def find_str(s,t):
        res=[]
        for a,l,o in s.segs:
            seg=s.d[o:o+l]; i=seg.find(t.encode())
            while i!=-1: res.append(a+i); i=seg.find(t.encode(),i+1)
        return res
    def code_segs(s):
        return [(a,l,o) for a,l,o in s.segs if 0x40000000<=a<0x40400000]
def md():
    m=capstone.Cs(capstone.CS_ARCH_XTENSA, capstone.CS_MODE_LITTLE_ENDIAN if not hasattr(capstone,'CS_MODE_XTENSA_ESP32') else capstone.CS_MODE_XTENSA_ESP32)
    m.skipdata=True
    return m
