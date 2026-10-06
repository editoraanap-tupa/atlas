import json, math, sys, collections
import numpy as np, cv2
from sklearn.isotonic import IsotonicRegression
from scipy import ndimage
sys.path.insert(0,'/home/claude/d')
B=[-56.32,-15.3,-55.84,-15.8]; FAC=3; W,H=1728*FAC,1800*FAC
dx=(B[2]-B[0])/W; dy=(B[1]-B[3])/H
lat0=math.radians(-15.55); PXA=(dx*111320*math.cos(lat0))*(dy*110574)/1e6
def pix(c): c=np.asarray(c); return np.stack([(c[:,0]-B[0])/dx,(B[1]-c[:,1])/dy],-1)
def ipts(xy): return np.round(xy*8).astype(np.int32)
Z=np.load('anadem_grid.npy'); sgb=np.load('sgb_grid.npy')

s=open('/home/claude/d/atlas_rmvrc.html').read()
def grab(name):
    i=s.index('const '+name+' = '); j=s.index('\n',i); return json.loads(s[i+len('const '+name+' = '):j].rstrip().rstrip(';'))
i=s.index('const DATA = '); j=s.index('\n',i); DATA=json.loads(s[i+len('const DATA = '):j].rstrip(';'))
HID=grab('HIDRO')
# ---- rio Cuiabá rasterizado
riv=np.zeros((H,W),np.uint8)
for f in HID['features']:
    p=f['properties']
    if p.get('t')=='r' and p.get('n')=='Rio Cuiabá':
        cv2.polylines(riv,[ipts(pix(f['geometry']['coordinates']))],False,1,thickness=1,shift=3)
print('rio px',riv.sum())
# componente principal
n,lab=cv2.connectedComponents(riv,connectivity=8); big=np.bincount(lab.ravel())[1:].argmax()+1; riv=(lab==big).astype(np.uint8)
ys,xs=np.nonzero(riv)
# distancia ao longo do rio a partir do ponto mais ao norte (montante)
start=np.argmin(ys)
from collections import deque
idx={ (y,x):k for k,(y,x) in enumerate(zip(ys,xs)) }
dist=np.full(len(ys),np.inf); dist[start]=0; dq=deque([start])
while dq:
    k=dq.popleft(); y,x=ys[k],xs[k]
    for ddy in (-1,0,1):
        for ddx in (-1,0,1):
            if ddy==ddx==0: continue
            q=idx.get((y+ddy,x+ddx))
            if q is not None and dist[q]==np.inf:
                dist[q]=dist[k]+math.hypot(ddx*10,ddy*10.2); dq.append(q)
ok=np.isfinite(dist); print('rio km',dist[ok].max()/1000)
# cota do leito/lamina: minimo do MDT num raio de ~45 m
zmin=ndimage.minimum_filter(np.nan_to_num(Z,nan=9999),size=9)
zr=zmin[ys,xs]
iso=IsotonicRegression(increasing=False).fit(dist[ok],zr[ok])
surf=np.full(len(ys),np.nan); surf[ok]=iso.predict(dist[ok])
# suaviza
order=np.argsort(dist); sm=surf.copy()
w=51; ker=np.ones(w)/w; tmp=np.convolve(np.pad(surf[order],(w//2,w//2),mode='edge'),ker,'valid'); sm[order]=tmp
# regua de Cuiaba
st=np.array([[-56.1086,-15.6156]]); sx,sy=pix(st)[0]
kreg=np.argmin((xs-sx)**2+(ys-sy)**2); print('regua dist m',math.hypot(xs[kreg]-sx,ys[kreg]-sy)*10, 'lamina modelo',sm[kreg], 'queda', sm[ok].max()-sm[ok].min())
ZERO=139.36
# rotulo do pixel de rio mais proximo
inv=np.ones((H,W),np.uint8); inv[ys,xs]=0
D,L=cv2.distanceTransformWithLabels(inv,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL)
# mapear label -> indice k
labk=np.zeros(L.max()+1,np.int64); labk[L[ys,xs]]=np.arange(len(ys))
near=labk[L]; D=D*10
SURF=sm[near]
Zf=np.nan_to_num(Z,nan=9999)
CEN={'alerta':8.50,'emerg':9.50,'c1995':10.36,'c1974':10.85,'calam':11.00}
def flood(regua,delta):
    lvl=SURF+(ZERO+regua-sm[kreg])+delta
    m=((Zf<lvl)&(D<12000)).astype(np.uint8); m[ys,xs]=1
    n,lab=cv2.connectedComponents(m,connectivity=8)
    keep=np.zeros(n,bool); keep[np.unique(lab[ys,xs])]=True; keep[0]=False
    return keep[lab]
# ---- setores/bairros
F=[f for f in DATA['features'] if f['properties']['mun'] in ('Cuiabá','Várzea Grande')]
sl=np.zeros((H,W),np.int32)
def polys(g): return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
for k,f in enumerate(F):
    for p in polys(f['geometry']):
        cv2.fillPoly(sl,[ipts(pix(p[0]))],k+1,shift=3)
        for h in p[1:]: cv2.fillPoly(sl,[ipts(pix(h))],0,shift=3)
npx=np.bincount(sl.ravel(),minlength=len(F)+1).astype(float)
pop=np.array([0]+[f['properties']['pop'] for f in F],float)
urb=np.array([0]+[f['properties']['sit']=='Urbana' for f in F],bool)
BAI=[('Terceiro','Cuiabá'),('Porto','Cuiabá'),('Praeirinho','Cuiabá'),('Cristo Rei','Várzea Grande'),('Passagem da Conceição','Várzea Grande'),('Bom Sucesso','Várzea Grande')]
bai_ids={b:[k+1 for k,f in enumerate(F) if f['properties']['bairro']==b[0] and f['properties']['mun']==b[1]] for b in BAI}
def stats(m):
    fp=np.bincount(sl[m],minlength=len(F)+1).astype(float); frac=np.divide(fp,npx,out=np.zeros_like(fp),where=npx>0)
    mor=(frac*pop)[1:].sum()
    bai={b[0]:round(100*fp[ids].sum()/max(1,npx[ids].sum()),1) for b,ids in bai_ids.items()}
    return frac,mor,bai
res={}
for delta in [0,0.5,1,1.5,2,2.5,3]:
    row={}
    for c in ('c1995','c1974'):
        m=flood(CEN[c],delta); frac,mor,bai=stats(m); row[c]=(int(mor),bai,round(m.sum()*PXA,1))
    res[delta]=row
    print(delta, 'mor95',row['c1995'][0],'mor74',row['c1974'][0],'km2_74',row['c1974'][2],'| 74:',row['c1974'][1],'| 95:',row['c1995'][1])
json.dump({str(k):v for k,v in res.items()},open('calib.json','w'),ensure_ascii=False)
np.save('river_idx.npy',np.stack([ys,xs])); np.save('surf.npy',sm)
import pickle; pickle.dump(dict(kreg=int(kreg),F_ids=[f['properties']['id'] for f in F]),open('meta.pkl','wb'))
np.save('setor_lab.npy',sl); np.save('near.npy',near.astype(np.int32)); np.save('D.npy',D.astype(np.float32))
