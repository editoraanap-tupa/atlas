import json, math, sys, collections, pickle
import numpy as np, cv2
sys.path.insert(0,'/home/claude/d')
from shp import read_dbf, read_shp, to_geojson
from geo import utm2ll, read_gpkg

B=[-56.32,-15.3,-55.84,-15.8]  # lon0, lat_top, lon1, lat_bot
FAC=3; W0,H0=1728,1800; W,H=W0*FAC,H0*FAC
dx=(B[2]-B[0])/W; dy=(B[1]-B[3])/H
def pix(lon,lat): return np.stack([(np.asarray(lon)-B[0])/dx,(B[1]-np.asarray(lat))/dy],-1)
def ipts(xy): return np.round(xy*8).astype(np.int32)  # subpixel shift=3
lat0=math.radians(-15.55); PXA=(dx*111320*math.cos(lat0))*(dy*110574)/1e6  # km2 per fine pixel
print('px m',dx*111320*math.cos(lat0),dy*110574)

# ---------------- SGB (Cuiabá shp + VG gpkg) ----------------
CL={'Baixa':1,'Média':2,'Media':2,'Alta':3}
sgb=np.zeros((H,W),np.uint8)
recs=[]
rows=read_dbf('sgbcba_Inundacao_A.dbf'); G=read_shp('sgbcba_Inundacao_A.shp')
for r,g in zip(rows,G):
    if g is None: continue
    c=CL.get(r['CLASSE'].strip())
    polys=to_geojson(g[1])
    recs.append((c,[[np.array(ring) for ring in p] for p in polys]))
for geom,attrs in read_gpkg('sgbvg_suscetibilidade.gpkg','Inundacao_A',['CLASSE']):
    recs.append((CL.get((attrs['CLASSE'] or '').strip()),geom))
print('sgb polys',len(recs),collections.Counter(c for c,_ in recs))
for c,polys in recs:
    if not c: continue
    for p in polys:
        rings=[]
        for ring in p:
            lo,la=utm2ll(ring[:,0],ring[:,1]); rings.append(pix(lo,la))
        allp=np.concatenate(rings); x0=max(0,int(allp[:,0].min())-1); y0=max(0,int(allp[:,1].min())-1)
        x1=min(W,int(allp[:,0].max())+2); y1=min(H,int(allp[:,1].max())+2)
        if x1<=x0 or y1<=y0: continue
        m=np.zeros((y1-y0,x1-x0),np.uint8)
        off=np.array([x0,y0])
        cv2.fillPoly(m,[ipts(rings[0]-off)],1,shift=3)
        for h in rings[1:]: cv2.fillPoly(m,[ipts(h-off)],0,shift=3)
        sub=sgb[y0:y1,x0:x1]; np.maximum(sub,m*c,out=sub)
np.save('sgb_grid.npy',sgb)
print('sgb px',[int((sgb==c).sum()*PXA) for c in (1,2,3)],'km2')

# ---------------- ANADEM ----------------
raw=open('anadem_cuiaba.bin','rb').read(); hdr=json.loads(raw[:512].decode().strip())
dem=np.frombuffer(raw[512:],np.float32).reshape(hdr['h'],hdr['w'])
X=np.arange(W)+.5; Y=np.arange(H)+.5
lon=B[0]+X*dx; lat=B[1]-Y*dy
ci=np.clip(((lon-hdr['lon0'])/hdr['res']).astype(int),0,hdr['w']-1); ri=np.clip(((hdr['lat0']-lat)/hdr['res']).astype(int),0,hdr['h']-1)
Z=dem[ri[:,None],ci[None,:]].astype(np.float32)
Z[Z<-1000]=np.nan
np.save('anadem_grid.npy',Z)
print('dem', np.nanmin(Z), np.nanmax(Z))
