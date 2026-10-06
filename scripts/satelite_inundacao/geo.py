import math, struct, sqlite3
import numpy as np
A=6378137.0; F=1/298.257222101; E2=F*(2-F); K0=0.9996
def utm2ll(E,N,zone=21,south=True):
    E=np.asarray(E,float); N=np.asarray(N,float)
    x=E-500000.0; y=N-(10000000.0 if south else 0)
    e1=(1-math.sqrt(1-E2))/(1+math.sqrt(1-E2)); ep2=E2/(1-E2)
    M=y/K0; mu=M/(A*(1-E2/4-3*E2**2/64-5*E2**3/256))
    p1=mu+(3*e1/2-27*e1**3/32)*np.sin(2*mu)+(21*e1**2/16-55*e1**4/32)*np.sin(4*mu)+(151*e1**3/96)*np.sin(6*mu)+(1097*e1**4/512)*np.sin(8*mu)
    C1=ep2*np.cos(p1)**2; T1=np.tan(p1)**2; N1=A/np.sqrt(1-E2*np.sin(p1)**2); R1=A*(1-E2)/(1-E2*np.sin(p1)**2)**1.5; D=x/(N1*K0)
    lat=p1-(N1*np.tan(p1)/R1)*(D**2/2-(5+3*T1+10*C1-4*C1**2-9*ep2)*D**4/24+(61+90*T1+298*C1+45*T1**2-252*ep2-3*C1**2)*D**6/720)
    lon=(D-(1+2*T1+C1)*D**3/6+(5-2*C1+28*T1-3*C1**2+8*ep2+24*T1**2)*D**5/120)/np.cos(p1)
    lon0=math.radians(-183+6*zone)
    return np.degrees(lon0+lon), np.degrees(lat)

def wkb_polys(b,o=0):
    """returns list of polygons (list of rings as Nx2 arrays), offset"""
    bo=b[o]; e='<' if bo==1 else '>'; t=struct.unpack(e+'I',b[o+1:o+5])[0]; o+=5
    t=t%1000 if t<1000000 else t
    hasz = (t>1000 and t<2000) or t in (1003,1006)
    base=t%1000
    dim=3 if hasz else 2
    if base==3:
        nr=struct.unpack(e+'I',b[o:o+4])[0]; o+=4; rings=[]
        for _ in range(nr):
            n=struct.unpack(e+'I',b[o:o+4])[0]; o+=4
            a=np.frombuffer(b[o:o+8*dim*n],dtype=e+'f8').reshape(n,dim)[:,:2]; o+=8*dim*n; rings.append(a)
        return [rings],o
    if base==6:
        n=struct.unpack(e+'I',b[o:o+4])[0]; o+=4; out=[]
        for _ in range(n):
            p,o=wkb_polys(b,o); out+=p
        return out,o
    raise ValueError(t)
def gpkg_geom(blob):
    b=bytes(blob); flags=b[3]; env=(flags>>1)&7; el={0:0,1:32,2:48,3:48,4:64}[env]
    return wkb_polys(b,8+el)[0]
def read_gpkg(path,table,cols):
    c=sqlite3.connect(path)
    return [(gpkg_geom(r[0]),dict(zip(cols,r[1:]))) for r in c.execute(f'select geom,{",".join(cols)} from "{table}"') if r[0]]
