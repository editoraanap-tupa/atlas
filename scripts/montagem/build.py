import json, math, collections, sys
import numpy as np, cv2
from shp import *
from calc import indicators, T

NEWM={'5100102':'Acorizal','5102678':'Campo Verde','5103007':'Chapada dos Guimarães','5106109':'Nossa Senhora do Livramento','5107800':'Santo Antônio de Leverger'}
L=open('../atlas_orig.html').read().split('\n')
def js(i,pref): return json.loads(L[i][len(pref):].rstrip().rstrip(';'))
DATA=js(510,'<script>const DATA = '); HIDRO=js(511,'const HIDRO = '); EQUIP=js(512,'const EQUIP = ')

# ---------- geometry helpers ----------
def dp(pts,eps):
    if len(pts)<3: return pts
    a=np.array(pts); keep=np.zeros(len(a),bool); keep[0]=keep[-1]=True; st=[(0,len(a)-1)]
    while st:
        i,j=st.pop()
        if j<=i+1: continue
        p,q=a[i],a[j]; d=q-p; n=np.hypot(*d)
        seg=a[i+1:j]
        dist=np.abs(d[0]*(seg[:,1]-p[1])-d[1]*(seg[:,0]-p[0]))/n if n>0 else np.hypot(*(seg-p).T)
        k=int(np.argmax(dist))
        if dist[k]>eps: keep[i+1+k]=True; st+= [(i,i+1+k),(i+1+k,j)]
    return [tuple(x) for x in a[keep]]
def simp_ring(r,eps):
    s=dp(r,eps)
    if len(s)<4: s=r if len(r)<8 else dp(r,eps/4)
    return [[round(x,5),round(y,5)] for x,y in s]
def geom(rings,eps):
    polys=to_geojson(rings)
    out=[[simp_ring(r,eps) for r in poly if len(r)>=4] for poly in polys]
    out=[p for p in out if p and len(p[0])>=4]
    if len(out)==1: return {'type':'Polygon','coordinates':out[0]}
    return {'type':'MultiPolygon','coordinates':out}
def centroid(rings):
    best=max(to_geojson(rings),key=lambda p:abs(ring_area(p[0])))[0]
    A=0;cx=0;cy=0
    for i in range(len(best)-1):
        x0,y0=best[i];x1,y1=best[i+1];c=x0*y1-x1*y0;A+=c;cx+=(x0+x1)*c;cy+=(y0+y1)*c
    if A==0: return best[0]
    return (cx/(3*A),cy/(3*A))
def hav(a,b):
    R=6371008.8; la1,la2=math.radians(a[1]),math.radians(b[1]); dl=math.radians(b[0]-a[0])
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))

# ---------- setores ----------
rows=read_dbf('shp/MT_setores_CD2022.dbf'); G=read_shp('shp/MT_setores_CD2022.shp')
NEWF=[]
for r,gm in zip(rows,G):
    if r['CD_MUN'] not in NEWM: continue
    cd=r['CD_SETOR']; urb=r['SITUACAO']=='Urbana'
    p={'id':cd,'mun':r['NM_MUN'],'sit':r['SITUACAO'],'bairro':r['NM_BAIRRO'],'dist':r['NM_DIST'],'fcu':r['NM_FCU'],
       'area':round(float(r['AREA_KM2']),3)}
    ind=indicators(cd,None)
    p['pop']=ind.pop('pop'); p['dens']=round(p['pop']/float(r['AREA_KM2']),1) if float(r['AREA_KM2'])>0 else None
    p['dppo']=ind.pop('dppo'); p.update(ind)
    for k in ['ivsa','ivsa_n','inund','inund2','inund_pop','ndvi','verde','lst','lst_anom','c1974','c1974_pop','alerta','app_pct','app_pop']: p[k]=None
    eps=0.00004 if urb else 0.0004
    NEWF.append({'type':'Feature','properties':p,'geometry':geom(gm[1],eps),'_rings':gm[1],'_c':centroid(gm[1])})
print('novos setores',len(NEWF), collections.Counter((f['properties']['mun'],f['properties']['sit']) for f in NEWF))

# ---------- municipios ----------
M=json.load(open('municipios.json'))
MUN={'type':'FeatureCollection','features':[]}
def sim_any(c,eps):
    if isinstance(c[0][0],(int,float)): return simp_ring(c,eps)
    return [sim_any(x,eps) for x in c]
order=['Cuiabá','Várzea Grande','Nossa Senhora do Livramento','Santo Antônio de Leverger','Acorizal','Chapada dos Guimarães','Campo Verde']
for nome in order:
    f=[x for x in M['features'] if x['properties']['nome']==nome][0]
    MUN['features'].append({'type':'Feature','properties':{'nome':nome},'geometry':{'type':f['geometry']['type'],'coordinates':sim_any(f['geometry']['coordinates'],0.0002)}})
def pip(pt,poly):
    x,y=pt; ins=False
    for ring in poly:
        for i in range(len(ring)-1):
            x0,y0=ring[i];x1,y1=ring[i+1]
            if (y0>y)!=(y1>y) and x<(x1-x0)*(y-y0)/(y1-y0)+x0: ins=not ins
    return ins
def in_mun(pt,nome):
    g=[f for f in MUN['features'] if f['properties']['nome']==nome][0]['geometry']
    polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
    return any(pip(pt,p) for p in polys)
def which_mun(pt):
    for n in order:
        if in_mun(pt,n): return n
    return None

# ---------- equipamentos novos ----------
NEWEQ=[]
cn=json.load(open('cnes.json'))
for r in cn:
    n=(r['n'] or '').title(); pt=(round(r['x'],5),round(r['y'],5))
    if 'Cadeia' in n: continue
    if which_mun(pt) not in NEWM.values(): continue
    c=None
    if r['t'] in (1,2): c='ubs'
    elif r['t'] in (73,20,21): c='upa'
    elif r['t'] in (5,7) and r['sus']=='SIM': c='hosp'
    if c: NEWEQ.append({'c':c,'n':n,'x':pt[0],'y':pt[1],'f':'CNES'})
osm=json.load(open('osm_equip.json'))['elements']
for e in osm:
    t=e.get('tags',{});
    if 'lat' in e: pt=(e['lon'],e['lat'])
    elif 'center' in e: pt=(e['center']['lon'],e['center']['lat'])
    else: continue
    pt=(round(pt[0],5),round(pt[1],5))
    c=None
    if t.get('amenity') in ('school','kindergarten'): c='esc'
    elif t.get('leisure') in ('park','garden'): c='parque'
    elif t.get('leisure')=='nature_reserve' or t.get('boundary')=='protected_area': c='uc'
    if not c: continue
    if which_mun(pt) not in NEWM.values(): continue
    NEWEQ.append({'c':c,'n':t.get('name',''),'x':pt[0],'y':pt[1],'f':'OSM'})
print('novos equipamentos',collections.Counter(e['c'] for e in NEWEQ))
ALLEQ=EQUIP+NEWEQ

# distancias
cat={'d_ubs':['ubs'],'d_saude':['upa','hosp'],'d_esc':['esc'],'d_parque':['parque','uc']}
for f in NEWF:
    c=f['_c']
    for k,cs in cat.items():
        pts=[(e['x'],e['y']) for e in ALLEQ if e['c'] in cs]
        d=min(hav(c,q) for q in pts) if pts else None
        f['properties'][k]=int(round(d/10)*10) if d is not None else None

json.dump({'NEWF':[{k:v for k,v in f.items() if not k.startswith('_')} for f in NEWF],'NEWEQ':NEWEQ,'MUN':MUN},open('stage1.json','w'),ensure_ascii=False)
import pickle; pickle.dump([(f['properties']['id'],f['_rings'],f['properties']['sit']) for f in NEWF],open('rings.pkl','wb'))
