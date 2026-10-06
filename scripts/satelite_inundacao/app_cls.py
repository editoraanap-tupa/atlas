# Classes de APP dos corpos d'água em polígono (Lei 12.651/2012, art. 4º) — gera app_cls.json {índice do feature em HIDRO: {ap, ak, ...}}
import sys,collections; sys.path.insert(0,'/home/claude/x')
from common import *
from matplotlib.path import Path
F,H=load_atlas()
i=H.find('const HIDRO = '); HID,_=json.JSONDecoder().raw_decode(H[i+len('const HIDRO = '):])
def metr(ring):
    r=np.asarray(ring); x,y=ll2utm(r[:,0],r[:,1]); A=abs(np.sum(x[:-1]*y[1:]-x[1:]*y[:-1]))/2; P=np.sum(np.hypot(np.diff(x),np.diff(y))); return A,P,(x.mean(),y.mean())
# índice espacial simples dos setores
SB=[(fbbox(f['geometry']),f) for f in F]
def sit_at(lon,lat):
    for b,f in SB:
        if b[0]<=lon<=b[2] and b[1]<=lat<=b[3]:
            for pg in polys(f['geometry']):
                if Path(np.asarray(pg[0])).contains_point((lon,lat)): return f['properties']['sit'],f['properties']['mun']
    return None,None
def wclass(w): return 30 if w<10 else 50 if w<50 else 100 if w<200 else 200 if w<600 else 500
out={}; st=collections.Counter(); rows=[]
for k,f in enumerate(HID['features']):
    p=f['properties']
    if p['t']!='a': continue
    ring=f['geometry']['coordinates'][0]; A,P,_=metr(ring); holes=sum(metr(h)[0] for h in f['geometry']['coordinates'][1:]); A-=holes; ha=A/1e4
    r=np.asarray(ring); lon,lat=float(r[:,0].mean()),float(r[:,1].mean()); w=p.get('w') or ''; n=p.get('n') or ''
    if w in ('river','stream'):
        Wm=2*A/P
        ap=100 if n=='Rio Cuiabá' else 50 if n=='Rio Coxipó' else wclass(Wm); ak='rio'
        rows.append((n,round(ha,1),round(Wm,1),ap))
    elif w in ('reservoir','pond','basin') or 'Manso' in n:
        ap=0; ak='res'
    else:
        if ha<1: ap=0; ak='peq'
        else:
            sit,_=sit_at(lon,lat); ak='lago'
            ap=30 if sit=='Urbana' else (50 if ha<=20 else 100)
    out[k]=dict(ap=ap,ak=ak,ha=round(ha,2)); st[(ak,ap)]+=1
json.dump(out,open('app_cls.json','w'))
for k,v in sorted(st.items()): print(k,v)
print('polígonos de rio: largura média (2A/P) e faixa')
for r in sorted(rows,key=lambda x:-x[1])[:25]: print(' ',r)
print(collections.Counter(r[3] for r in rows), 'Rio Cuiabá larguras',[r[2] for r in rows if r[0]=='Rio Cuiabá'])
