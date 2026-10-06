import struct
def read_dbf(path, enc='utf-8'):
    f=open(path,'rb'); h=f.read(32)
    n=struct.unpack('<I',h[4:8])[0]; hl=struct.unpack('<H',h[8:10])[0]; rl=struct.unpack('<H',h[10:12])[0]
    fields=[]
    while True:
        d=f.read(32)
        if d[0]==0x0D: break
        name=d[:11].split(b'\0')[0].decode(); fields.append((name,chr(d[11]),d[16]))
    f.seek(hl); rows=[]
    for i in range(n):
        r=f.read(rl); p=1; o={}
        for name,t,l in fields:
            v=r[p:p+l]; p+=l
            try: s=v.decode(enc).strip()
            except: s=v.decode('latin1').strip()
            o[name]=s
        rows.append(o)
    return rows

def read_shp(path):
    b=open(path,'rb').read(); pos=100; out=[]
    while pos<len(b):
        rn,cl=struct.unpack('>ii',b[pos:pos+8]); pos+=8; c=b[pos:pos+cl*2]; pos+=cl*2
        st=struct.unpack('<i',c[:4])[0]
        if st==0: out.append(None); continue
        bbox=struct.unpack('<4d',c[4:36]); np_,npt=struct.unpack('<ii',c[36:44])
        parts=list(struct.unpack('<%di'%np_,c[44:44+4*np_])); o=44+4*np_
        pts=struct.unpack('<%dd'%(2*npt),c[o:o+16*npt])
        pts=[(pts[2*i],pts[2*i+1]) for i in range(npt)]
        rings=[pts[parts[i]:(parts[i+1] if i+1<np_ else npt)] for i in range(np_)]
        out.append((bbox,rings))
    return out

def ring_area(r):
    s=0
    for i in range(len(r)-1): s+=r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1]
    return s/2

def to_geojson(rings):
    # shapefile: outer rings clockwise (negative area in std math), holes ccw
    polys=[]
    for r in rings:
        if ring_area(r)<0: polys.append([r])
        else:
            if polys: polys[-1].append(r)
            else: polys.append([r])
    return polys
