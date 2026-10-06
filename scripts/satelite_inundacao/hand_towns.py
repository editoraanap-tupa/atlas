# Suscetibilidade a inundação nas sedes e distritos dos 5 municípios novos
# Mesmo método da camada da conurbação (reconstituído e conferido em hand_cal*.py):
#   altura do terreno (Copernicus GLO-30) acima da drenagem mais próxima em linha reta (rede OSM: rios e córregos);
#   cota da drenagem = mínimo 3x3 do MDS na célula de drenagem; classes 2/5/8 m (córregos) e 4/8/12 m (Rio Cuiabá);
#   só manchas ligadas à drenagem.
import sys; sys.path.insert(0,'/home/claude/x')
from handlib import *
from common import *
from scipy import ndimage as ndi
from skimage.draw import polygon as skp
F,Hh=load_atlas(); R=1/3600
i=Hh.find('const HIDRO = '); HID,_=json.JSONDecoder().raw_decode(Hh[i+len('const HIDRO = '):])
W=json.load(open('windows.json'))
NEW=('Acorizal','Campo Verde','Chapada dos Guimarães','Nossa Senhora do Livramento','Santo Antônio de Leverger')
out={}; RAS={}; info=[]
for wi,w in enumerate(W):
    h,Z=rd_dem('w%d'%wi); NY,NX=Z.shape; lon0,lat0=h['lon0'],h['lat0']
    px=lambda c: np.round(np.stack([(np.asarray(c,float)[:,0]-lon0)/R,(lat0-np.asarray(c,float)[:,1])/R],-1)).astype(np.int32)
    d=np.zeros((NY,NX),np.uint8); nl=0
    for f in HID['features']:
        p=f['properties']; g=f['geometry']
        if g['type']=='LineString' and p.get('t') in ('r','s'):
            a=np.asarray(g['coordinates'])
            if ((a[:,0]>=lon0)&(a[:,0]<=lon0+NX*R)&(a[:,1]<=lat0)&(a[:,1]>=lat0-NY*R)).any(): nl+=1; cv2.polylines(d,[px(a)],False,1,1)
    for f in HID['features']:
        p=f['properties']; g=f['geometry']
        if g['type']=='LineString' and p.get('n')=='Rio Cuiabá': cv2.polylines(d,[px(g['coordinates'])],False,2,1)
    b=w['bbox']; core=(slice(max(0,int((lat0-b[3])/R)),int((lat0-b[1])/R)+1),slice(max(0,int((b[0]-lon0)/R)),int((b[2]-lon0)/R)+1))
    info.append(dict(w=wi,mun=w['mun'],linhas=nl,dren_px=int((d>0).sum())))
    if (d>0).sum()==0:
        C=None
    else:
        dist,(iy,ix)=ndi.distance_transform_edt(d==0,return_indices=True); dc=d[iy,ix]
        Zm=cv2.erode(Z.astype(np.float32),np.ones((3,3),np.uint8)).astype(np.float64)
        hd=(Z-Zm[iy,ix]).astype(np.float32); hd[hd<0]=0
        C=classes(hd,dc,d)
        RAS[wi]=dict(lon0=lon0+core[1].start*R,lat0=lat0-core[0].start*R,C=C[core].copy())
    for f in F:
        p=f['properties']
        if p['mun'] not in NEW or p['sit']!='Urbana': continue
        bb=fbbox(f['geometry'])
        if bb[0]<b[0]-1e-6 or bb[2]>b[2]+1e-6 or bb[1]<b[1]-1e-6 or bb[3]>b[3]+1e-6: continue
        if p['id'] in out and out[p['id']].get('inund') is not None: continue
        if C is None: out[p['id']]=dict(inund=None,inund2=None,w=wi,motivo='sem rede de drenagem no OSM'); continue
        c0=max(0,int((bb[0]-lon0)/R)-1); c1=int((bb[2]-lon0)/R)+2; r0=max(0,int((lat0-bb[3])/R)-1); r1=int((lat0-bb[1])/R)+2
        m=np.zeros((r1-r0,c1-c0),bool)
        for pg in polys(f['geometry']):
            for j,r in enumerate(pg):
                r=np.asarray(r); rr,cc=skp((lat0-r[:,1])/R-r0,(r[:,0]-lon0)/R-c0,m.shape); m[rr,cc]=(j==0)
        if m.sum()==0:
            cy=int(round((lat0-(bb[1]+bb[3])/2)/R))-r0; cx=int(round(((bb[0]+bb[2])/2-lon0)/R))-c0; m[cy,cx]=True
        c=C[r0:r1,c0:c1][m]
        out[p['id']]=dict(inund=round(100*float((c==1).mean()),1),inund2=round(100*float(((c==1)|(c==2)).mean()),1),w=wi,n=int(m.sum()))
json.dump(out,open('hand_out.json','w')); np.save('hand_ras.npy',RAS,allow_pickle=True); json.dump(info,open('hand_info.json','w'),ensure_ascii=False)
for x in info: print(x)
import collections
c=collections.Counter(); tot=collections.Counter()
for f in F:
    p=f['properties']
    if p['mun'] in NEW and p['sit']=='Urbana':
        tot[p['mun']]+=1; o=out.get(p['id'])
        c[(p['mun'],'fora de janela' if o is None else ('sem dado' if o['inund'] is None else 'ok'))]+=1
print(dict(tot)); 
for k,v in sorted(c.items()): print(k,v)
v=[o['inund'] for o in out.values() if o['inund'] is not None]; print('inund média %.1f mediana %.1f máx %.1f; >=20%%: %d de %d'%(np.mean(v),np.median(v),max(v),sum(x>=20 for x in v),len(v)))
