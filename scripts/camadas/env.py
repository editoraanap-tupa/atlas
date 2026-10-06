import json, gzip, math, collections, sys
import numpy as np, cv2
raw=open('mapbiomas_c9_2023_rmvrc.bin','rb').read(); MH=json.loads(raw[:512])
MB=np.frombuffer(gzip.decompress(raw[512:]),np.uint8).reshape(MH['h'],MH['w'])
W,H=MH['w'],MH['h']; L0,T0,RES=MH['lon0'],MH['lat0'],MH['res']
def pix(c): c=np.asarray(c,float); return np.stack([(c[:,0]-L0)/RES,(T0-c[:,1])/RES],-1)
def ipts(xy): return np.round(xy*8).astype(np.int32)
def polys(g): return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
def fill(arr,geom,val):
    for p in polys(geom):
        rings=[pix(r) for r in p if len(r)>=3]
        if not rings: continue
        a=np.concatenate(rings); x0=max(0,int(a[:,0].min())-1); y0=max(0,int(a[:,1].min())-1); x1=min(W,int(a[:,0].max())+2); y1=min(H,int(a[:,1].max())+2)
        if x1<=x0 or y1<=y0: continue
        m=np.zeros((y1-y0,x1-x0),np.uint8); off=np.array([x0,y0])
        cv2.fillPoly(m,[ipts(rings[0]-off)],1,shift=3)
        for h in rings[1:]: cv2.fillPoly(m,[ipts(h-off)],0,shift=3)
        sub=arr[y0:y1,x0:x1]; sub[m==1]=val
lat_c=math.radians(-15.9); PXA=(RES*111320*math.cos(lat_c))*(RES*110574)/1e6
s=open('/home/claude/d/atlas_rmvrc.html').read()
def grab(name,pref=None):
    pref=pref or ('const '+name+' = '); i=s.index(pref); j=s.index('\n',i); return json.loads(s[i+len(pref):j].rstrip().rstrip(';'))
DATA=grab('DATA','<script>const DATA = '); MUN=grab('MUN')
F=DATA['features']
# municipios
mun=np.zeros((H,W),np.uint8); MUNS=[m['properties']['nome'] for m in MUN['features']]
for k,m in enumerate(MUN['features']): fill(mun,m['geometry'],k+1)
# setores
sl=np.zeros((H,W),np.int16)
for k,f in enumerate(F): fill(sl,f['geometry'],k+1)
cnt=np.bincount(sl.ravel(),minlength=len(F)+1)
# setores sem pixel: centroide
cent=[]
for k,f in enumerate(F):
    p=polys(f['geometry'])[0][0]; c=np.mean(np.array(p),0); cent.append(c)
print('setores sem pixel',int((cnt[1:]==0).sum()))
np.save('mun.npy',mun); np.save('sl.npy',sl)
# ---- solos
SOLO_ORD={'LATOSSOLO':1,'ARGISSOLO':2,'CAMBISSOLO':3,'NEOSSOLO':4,'PLINTOSSOLO':5,'PLANOSSOLO':6,'GLEISSOLO':7,'VERTISSOLO':8,'ORGANOSSOLO':9,'OUTROS':10}
SOLO_S={1:1.0,2:2.0,3:2.5,4:3.0,5:3.0,6:2.0,7:3.0,8:3.0,9:3.0,10:3.0}
solo=np.zeros((H,W),np.uint8); solo2=np.zeros((H,W),np.uint8)
L2=sorted({x['properties']['legenda_2'] for x in json.load(open('ibge_pedo_area.json'))['features']})
L2i={n:i+1 for i,n in enumerate(L2)}
for x in json.load(open('ibge_pedo_area.json'))['features']:
    pr=x['properties']; o=SOLO_ORD.get(pr['leg_ordem'])
    if pr['legenda_2']=='AFLORAMENTO': o=10
    if o: fill(solo,x['geometry'],o)
    fill(solo2,x['geometry'],L2i[pr['legenda_2']])
np.save('solo.npy',solo); np.save('solo2.npy',solo2); json.dump(L2i,open('solo2_leg.json','w'),ensure_ascii=False)
# ---- geologia (Crepani et al., 2001: estabilidade das rochas)
GEO={'Depósitos Aluvionares Holocênicos':3.0,'Terraços Holocênicos':3.0,'Pantanal':3.0,'Pantanal - Fácies Depósitos Coluvionares':3.0,'Depósitos Coluviais Pleistocênicos':3.0,
 'Xaraiés':2.9,'Cobertura Detrito-Laterítica Neogênica':2.8,'Cobertura Detrito-Laterítica Neo-Pleistocênica':2.8,
 'Marília':2.5,'Salto das Nuvens':2.5,'Utiariti':2.4,'Botucatu':2.4,'Furnas':2.4,'Aquidauana':2.5,'Ponta Grossa':2.7,'Palermo':2.7,'Rio Ivaí':2.4,
 'Serra Geral':1.5,'Tapirapuã':1.5,'Intrusivas Ponta do Morro':1.2,'Cuiabá':1.7,'Moenda':2.4,'Raizama':2.4,'Sepotuba':2.7,'Diamantino':2.6,'Araras':2.9,'Bauxi':2.2,
 'Granito São Vicente':1.1,'Vulcânicas de Mimoso':1.5}
geo=np.zeros((H,W),np.uint8); miss=collections.Counter()
for x in json.load(open('ibge_geol_area.json'))['features']:
    n=x['properties']['nm_unidade']; v=GEO.get(n)
    if v is None: miss[n]+=1; continue
    fill(geo,x['geometry'],int(round(v*10)))
print('geo sem escore',miss)
np.save('geo.npy',geo)
# ---- vegetacao (MapBiomas) escores
VEG={3:1.2,4:1.7,5:1.2,6:1.2,49:1.7,11:2.2,12:2.2,50:2.2,9:2.0,15:2.8,21:2.6,20:2.9,39:2.9,40:2.9,41:2.9,62:2.9,46:2.6,47:2.6,48:2.6,24:2.5,25:3.0,29:3.0,30:3.0,23:3.0}
vg=np.zeros(256,np.uint8)
for k,v in VEG.items(): vg[k]=int(round(v*10))
vgs=vg[MB]
np.save('vgs.npy',vgs)
NAT=np.zeros(256,bool); NAT[[3,4,5,6,11,12,49,50]]=True
nat=NAT[MB]; agua=np.isin(MB,[33,31])
# vegetacao por setor (fora da agua)
land=~agua
nl=np.bincount(sl[land].ravel(),minlength=len(F)+1).astype(float)
nn=np.bincount(sl[nat].ravel(),minlength=len(F)+1).astype(float)
veg={}
for k,f in enumerate(F):
    if nl[k+1]>0: veg[f['properties']['id']]=round(100*nn[k+1]/nl[k+1],1)
    else:
        x,y=pix([cent[k]])[0].astype(int)
        veg[f['properties']['id']]=100.0 if (0<=x<W and 0<=y<H and nat[y,x]) else 0.0
json.dump(veg,open('veg.json','w'))
# municipio
mv={}
for k,n in enumerate(MUNS):
    m=(mun==k+1)&land; mv[n]={'veg':round(100*float((nat&m).sum())/float(m.sum()),1),'km2':round(float((mun==k+1).sum()*PXA),0)}
    # classes de uso
    c=np.bincount(MB[mun==k+1],minlength=256); mv[n]['uso']={int(i):round(100*c[i]/c.sum(),1) for i in np.nonzero(c)[0]}
json.dump(mv,open('mun_veg.json','w'),ensure_ascii=False)
print(json.dumps({k:v['veg'] for k,v in mv.items()},ensure_ascii=False))
