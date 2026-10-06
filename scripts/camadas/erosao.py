import json, numpy as np, cv2, collections, base64, io, math
from PIL import Image
exec(open('env.py').read().split('# municipios')[0])
mun=np.load('mun.npy'); sl=np.load('sl.npy'); solo=np.load('solo.npy'); geo=np.load('geo.npy'); vgs=np.load('vgs.npy')
inR=mun>0
# ---- relevo (IBGE geomorfologia; matriz de dissecação de Crepani et al., 2001)
DD={'muito baixa':1.0,'baixa':1.5,'média':2.0,'alta':2.5,'muito alta':3.0}
AI={'muito fraco':1.0,'fraco':1.5,'médio':2.0,'forte':2.5,'muito forte':3.0}
def rel(p):
    nat=p['natureza']; fo=p['forma'] or ''
    if nat=='acumulação': return 1.5 if 'coluvial' in fo else 1.0
    if nat=='aplanamento': return 1.0 if p['categoria'] and 'desnudado' not in p['categoria'] else 1.2
    if nat=='dissecação':
        if 'encosta íngreme' in fo: return 3.0
        d=DD.get(p['dens_dren']); a=AI.get((p['aprof_inci'] or '').split(':')[0].strip()) if p['aprof_inci'] else None
        base={'topo tabular':1.3,'topo convexo':1.7,'topo aguçado':2.2}.get(fo,1.7)
        v=[x for x in (d,a) if x is not None]
        return round((sum(v)/len(v)+base)/2 if v else base,2)
    return None
rr=np.zeros((H,W),np.uint8)
for x in json.load(open('ibge_geom_area.json'))['features']:
    v=rel(x['properties'])
    if v: fill(rr,x['geometry'],int(round(v*10)))
# ---- solos: escore; area urbana/agua = sem dado
SOLO_S={1:1.0,2:2.0,3:2.5,4:3.0,5:3.0,6:2.0,7:3.0,8:3.0,9:3.0,10:3.0}
ss=np.zeros(256,np.uint8)
for k,v in SOLO_S.items(): ss[k]=int(v*10)
sls=ss[solo]
# 'ÁREA URBANA' foi classificada em OUTROS(10): refaz com legenda
L2i=json.load(open('solo2_leg.json')); solo2=np.load('solo2.npy')
sls[solo2==L2i.get('ÁREA URBANA',255)]=0
C=2.0
V=np.full((H,W),np.nan,np.float32)
for y0 in range(0,H,1000):
    sl_=slice(y0,min(H,y0+1000))
    st=np.stack([geo[sl_],rr[sl_],sls[sl_],vgs[sl_]]).astype(np.float32)/10
    va=st>0; n=va.sum(0)
    v=np.where(n>=3,(np.where(va,st,0).sum(0)+C)/(n+1),np.nan).astype(np.float32)
    v[~inR[sl_]]=np.nan; V[sl_]=v
del geo; import gc; gc.collect()
print('V',np.nanmin(V),np.nanmax(V),np.nanmean(V))
# classes Crepani
edges=[1.35,1.75,2.25,2.65]
cls=np.digitize(V,edges)+1; cls[np.isnan(V)]=0
print('classes km2',{k:round(float((cls==k).sum()*PXA)) for k in range(1,6)})
np.save('ero_cls.npy',cls.astype(np.uint8))
# ---- por setor
F_ids=[f['properties']['id'] for f in F]
Vf=np.nan_to_num(V,nan=0); ok=~np.isnan(V)
cnt=np.bincount(sl[ok],minlength=len(F)+1).astype(float)
sm=np.bincount(sl[ok],weights=Vf[ok],minlength=len(F)+1)
hi=np.bincount(sl[ok&(V>=2.25)],minlength=len(F)+1).astype(float)
# solo predominante por setor
SOLN={1:'Latossolo',2:'Argissolo',3:'Cambissolo',4:'Neossolo',5:'Plintossolo',6:'Planossolo',7:'Gleissolo',8:'Vertissolo',9:'Organossolo',10:'Afloramento / outros'}
inv={v:k for k,v in L2i.items()}
per={}
for k,fid in enumerate(F_ids):
    d={}
    if cnt[k+1]>0: d['erosao']=round(float(sm[k+1]/cnt[k+1]),2); d['eros_alta']=round(100*hi[k+1]/cnt[k+1],1)
    else: d['erosao']=None; d['eros_alta']=None
    per[fid]=d
# solo predominante (moda de solo2) — por ordenação
order=np.argsort(sl.ravel(),kind='stable'); sv=sl.ravel()[order]; s2=solo2.ravel()[order]
b=np.searchsorted(sv,np.arange(len(F)+2))
for k,fid in enumerate(F_ids):
    v=s2[b[k+1]:b[k+2]]; v=v[v>0]
    if len(v):
        c=inv[int(np.bincount(v).argmax())]
        per[fid]['solo']=c.capitalize().replace('Vermelho-amarelo','Vermelho-Amarelo')
json.dump(per,open('ero_per.json','w'),ensure_ascii=False)
# ---- municipios
MUNS=[m['properties']['nome'] for m in MUN['features']]
mt={}
for k,nmn in enumerate(MUNS):
    m=(mun==k+1)
    c=np.bincount(cls[m],minlength=6)[1:].astype(float); t=c.sum()
    s2c=np.bincount(solo2[m],minlength=len(L2i)+1); top=[(inv[i],round(100*s2c[i]/s2c[1:].sum(),1)) for i in np.argsort(-s2c) if i>0 and s2c[i]>0][:3]
    mt[nmn]={'ero':[round(100*x/t,1) for x in c],'vmed':round(float(np.nanmean(V[m])),2),'solos':top}
json.dump(mt,open('ero_mun.json','w'),ensure_ascii=False)
print(json.dumps(mt,ensure_ascii=False)[:1500])
