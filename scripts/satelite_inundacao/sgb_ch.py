# Carta de suscetibilidade a inundação do SGB — Chapada dos Guimarães (RIGeo doc/25797), camada Inundacao_A
import sys,collections; sys.path.insert(0,'/home/claude/x'); sys.path.insert(0,'/home/claude/f')
from s2lib import *
from geo import read_gpkg
F,H=load_atlas()
recs=read_gpkg('sgbch_suscetibilidade.gpkg','Inundacao_A',['CLASSE','PROCESSO','MUNICIPIO','FONTE','EXECUCAO','PROJETO'])
print(len(recs),collections.Counter((a['CLASSE'],a['PROCESSO']) for g,a in recs)); print(recs[0][1])
CL={'Baixa':1,'Média':2,'Media':2,'Alta':3}
allx=np.concatenate([r[:,0] for g,a in recs for p in g for r in p]); ally=np.concatenate([r[:,1] for g,a in recs for p in g for r in p])
print('extensão UTM',allx.min(),allx.max(),ally.min(),ally.max())
RS=10; E0=int(allx.min()//100*100)-100; N1=int(ally.max()//100*100)+200; W=int((allx.max()-E0)/RS)+20; Hh=int((N1-ally.min())/RS)+20
G=np.zeros((Hh,W),np.uint8)
for g,a in recs:
    c=CL.get((a['CLASSE'] or '').strip())
    if not c: continue
    for p in g:
        rings=[np.stack([(r[:,0]-E0)/RS,(N1-r[:,1])/RS],-1) for r in p]
        al=np.concatenate(rings); x0=max(0,int(al[:,0].min())-1); y0=max(0,int(al[:,1].min())-1); x1=min(W,int(al[:,0].max())+2); y1=min(Hh,int(al[:,1].max())+2)
        m=np.zeros((y1-y0,x1-x0),np.uint8); off=np.array([x0,y0])
        cv2.fillPoly(m,[np.round((rings[0]-off)*8).astype(np.int32)],1,shift=3)
        for h in rings[1:]: cv2.fillPoly(m,[np.round((h-off)*8).astype(np.int32)],0,shift=3)
        sub=G[y0:y1,x0:x1]; np.maximum(sub,m*c,out=sub)
np.save('sgbch_grid.npy',G); json.dump({'E0':E0,'N1':N1,'RS':RS,'W':W,'H':Hh},open('sgbch_grid.json','w'))
km=lambda c: (G==c).sum()*RS*RS/1e6
print('km2 baixa %.1f média %.1f alta %.1f'%(km(1),km(2),km(3)))
out={}
for f in F:
    p=f['properties']
    if p['mun']!='Chapada dos Guimarães': continue
    xs=[];ys=[]
    for pg in polys(f['geometry']):
        r=np.asarray(pg[0]); x,y=ll2utm(r[:,0],r[:,1]); xs+=[x.min(),x.max()]; ys+=[y.min(),y.max()]
    c0=int((min(xs)-E0)/RS)-1; c1=int((max(xs)-E0)/RS)+2; r0=int((N1-max(ys))/RS)-1; r1=int((N1-min(ys))/RS)+2
    if (r1-r0)*(c1-c0)<8e6: m=rastc((r1-r0,c1-c0),E0+c0*RS,N1-r0*RS,RS,f['geometry'])
    else: m=rast((r1-r0,c1-c0),E0+c0*RS,N1-r0*RS,RS,f['geometry'])==1
    n=int(m.sum())
    if n==0: out[p['id']]=dict(sgb_alta=None); continue
    g=np.zeros((r1-r0,c1-c0),np.uint8); a0=max(0,c0); a1=min(W,c1); b0=max(0,r0); b1=min(Hh,r1)
    if a1>a0 and b1>b0: g[b0-r0:b1-r0,a0-c0:a1-c0]=G[b0:b1,a0:a1]
    g=g[m]; a=100*float((g==3).mean()); am=100*float((g>=2).mean())
    out[p['id']]=dict(sgb_alta=round(a,1),sgb_am=round(am,1),sgb_alta_pop=round(p['pop']*round(a,1)/100),n=n,area_ratio=round(n*RS*RS/1e6/p['area'],3))
json.dump(out,open('sgbch_out.json','w'))
v=[o for o in out.values() if o['sgb_alta'] is not None]
print(len(out),len(v),'alta média %.1f máx %.1f; pop em alta %d; razão de área mediana %.3f'%(np.mean([o['sgb_alta'] for o in v]),max(o['sgb_alta'] for o in v),sum(o['sgb_alta_pop'] for o in v),np.median([o['area_ratio'] for o in v])))
U=[(o['sgb_alta'],f['properties']['inund']) for f in F for o in [out.get(f['properties']['id'])] if o and o['sgb_alta'] is not None and f['properties'].get('inund') is not None]
print('urbanos com HAND',len(U),'corr sgb_alta × inund %.2f'%np.corrcoef(*zip(*U))[0,1])
print('campos existentes (exemplo Cuiabá):',{k:F[0]['properties'].get(k) for k in ('sgb_alta','sgb_alta_pop','sgb_am')})
