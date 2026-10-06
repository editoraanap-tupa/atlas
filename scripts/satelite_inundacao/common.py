import json, math, numpy as np
A=6378137.0; F_=1/298.257222101; E2=F_*(2-F_); K0=0.9996
def ll2utm(lon,lat,zone=21,south=True):
    lon=np.asarray(lon,float); lat=np.asarray(lat,float)
    ph=np.radians(lat); lam=np.radians(lon)-math.radians(-183+6*zone)
    ep2=E2/(1-E2); N=A/np.sqrt(1-E2*np.sin(ph)**2); T=np.tan(ph)**2; C=ep2*np.cos(ph)**2; Aa=np.cos(ph)*lam
    e4=E2*E2; e6=e4*E2
    M=A*((1-E2/4-3*e4/64-5*e6/256)*ph-(3*E2/8+3*e4/32+45*e6/1024)*np.sin(2*ph)+(15*e4/256+45*e6/1024)*np.sin(4*ph)-(35*e6/3072)*np.sin(6*ph))
    x=K0*N*(Aa+(1-T+C)*Aa**3/6+(5-18*T+T*T+72*C-58*ep2)*Aa**5/120)+500000.0
    y=K0*(M+N*np.tan(ph)*(Aa**2/2+(5-T+9*C+4*C*C)*Aa**4/24+(61-58*T+T*T+600*C-330*ep2)*Aa**6/720))
    if south: y=y+10000000.0
    return x,y
def load_atlas():
    H=open('/home/claude/d/atlas_rmvrc.html').read()
    i=H.find('const DATA = ')+len('const DATA = '); D,_=json.JSONDecoder().raw_decode(H[i:])
    return D['features'], H
def polys(g): return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
def fbbox(g):
    a=np.concatenate([np.array(p[0]) for p in polys(g)]); return a[:,0].min(),a[:,1].min(),a[:,0].max(),a[:,1].max()
