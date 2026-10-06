# LST por setor — Landsat 8/9 C2 L2 ST_B10 (Planetary Computer)
import sys,glob,os,time; sys.path.insert(0,'/home/claude/x')
from s2lib import *
F,H=load_atlas()
C=lambda d: d*0.00341802+149.0-273.15
DW,DE,DN=4.01,-0.68,1.96   # ajuste das datas vizinhas à imagem de 13/08 (diferença média na faixa comum)
E0,E1,N0,N1=475000,777000,8078000,8389500; RS=60; MW=(E1-E0)//RS; MH=(N1-N0)//RS
P=np.load('lst60_p.npy'); Wm=np.load('lst60_w.npy'); Em=np.load('lst60_e.npy'); Nm=np.load('lst60_n.npy')
T=np.full((MH,MW),np.nan,np.float32); SRC=np.zeros((MH,MW),np.uint8)
k=P>1; T[k]=C(P[k].astype(np.float32)); SRC[k]=1
k=(SRC==0)&(P==0)&(Wm>1); T[k]=C(Wm[k].astype(np.float32))+DW; SRC[k]=2     # só onde 13/08 não cobre (não onde há nuvem)
k=(SRC==0)&(P==0)&(Em>1); T[k]=C(Em[k].astype(np.float32))+DE; SRC[k]=3
k=(SRC==0)&(P==0)&(Nm>1); T[k]=C(Nm[k].astype(np.float32))+DN; SRC[k]=4
CLD=(P==1)
np.save('lst60_T.npy',T); np.save('lst60_src.npy',SRC)
R30=[]
def box(name,adj=0,date='13/08/2026'):
    h,b=rd('lsbox_%s.bin'%name); a=np.frombuffer(b,np.uint16).reshape(h['h'],h['w']); t=np.where(a>1,C(a.astype(np.float32))+adj,np.nan).astype(np.float32)
    R30.append(dict(name=name,e0=h['e0'],n1=h['n0']+1e7,w=h['w'],h=h['h'],t=t,date=date,adj=adj))
box('wcvg')
for i in range(17):
    if i==14: box('w14_oeste',DW,'12/08/2026')
    elif i==6: box('w6_n70',DN,'04/08/2026')
    else: box('w%d'%i)
def bboxutm(g):
    xs=[];ys=[]
    for p in polys(g):
        r=np.asarray(p[0]); x,y=ll2utm(r[:,0],r[:,1]); xs+=[x.min(),x.max()]; ys+=[y.min(),y.max()]
    return min(xs),min(ys),max(xs),max(ys)
out={}
for f in F:
    p=f['properties']; x0,y0,x1,y1=bboxutm(f['geometry']); done=False
    for R in R30:
        if x0>=R['e0'] and x1<=R['e0']+R['w']*30 and y0>=R['n1']-R['h']*30 and y1<=R['n1']:
            c0=max(0,int((x0-R['e0'])/30)-1); c1=int((x1-R['e0'])/30)+2; r0=max(0,int((R['n1']-y1)/30)-1); r1=int((R['n1']-y0)/30)+2
            m=rastc((r1-r0,c1-c0),R['e0']+c0*30,R['n1']-r0*30,30,f['geometry']); sub=R['t'][r0:r1,c0:c1]
            if m.sum()==0:   # setor menor que um pixel: pixel do centro
                cy=int((R['n1']-(y0+y1)/2)/30)-r0; cx=int(((x0+x1)/2-R['e0'])/30)-c0; m[cy,cx]=True
            v=sub[m[:sub.shape[0],:sub.shape[1]]]; ok=~np.isnan(v)
            if ok.sum()>=max(1,0.5*len(v)):
                out[p['id']]=dict(lst=round(float(v[ok].mean()),1),res=30,n=int(len(v)),nv=int(ok.sum()),date=R['date'],adj=R['adj']); done=True
            break
    if done: continue
    c0=max(0,int((x0-E0)/RS)-1); c1=min(MW,int((x1-E0)/RS)+2); r0=max(0,int((N1-y1)/RS)-1); r1=min(MH,int((N1-y0)/RS)+2)
    m=rastc((r1-r0,c1-c0),E0+c0*RS,N1-r0*RS,RS,f['geometry'])
    if m.sum()==0:
        cy=min(r1-r0-1,int((N1-(y0+y1)/2)/RS)-r0); cx=min(c1-c0-1,int(((x0+x1)/2-E0)/RS)-c0); m[cy,cx]=True
    v=T[r0:r1,c0:c1][m]; s=SRC[r0:r1,c0:c1][m]; cl=CLD[r0:r1,c0:c1][m]; ok=~np.isnan(v); n=int(m.sum())
    if ok.sum()<0.5*n:
        out[p['id']]=dict(lst=None,res=120,n=n,nv=int(ok.sum()),cloud=round(float(cl.mean()),2),date=None); continue
    fw=float((s[ok]==2).mean()); fe=float((s[ok]==3).mean()); fn=float((s[ok]==4).mean())
    date=('04/08/2026' if fn>0.95 else '04 e 13/08/2026') if fn>=0.05 and fn>=fw else '13/08/2026' if fw+fe<0.05 else ('12/08/2026' if fw>0.95 else ('14/08/2026' if fe>0.95 else ('12 e 13/08/2026' if fw>fe else '13 e 14/08/2026')))
    out[p['id']]=dict(lst=round(float(v[ok].mean()),1),res=120,n=n,nv=int(ok.sum()),cloud=round(float(cl.mean()),2),date=date,fw=round(fw,2),fe=round(fe,2),fn=round(fn,2))
json.dump(out,open('lst_out.json','w'))
import collections
c=collections.Counter()
for f in F:
    p=f['properties']; o=out[p['id']]; c[(p['mun'],o['res'],o['date'])]+=1
for k,v in sorted(c.items(),key=str): print(k,v)
A=np.array([[f['properties']['lst'],out[f['properties']['id']]['lst'],out[f['properties']['id']]['res']] for f in F if f['properties'].get('lst') is not None and out[f['properties']['id']]['lst'] is not None])
for r in (30,120):
    B=A[A[:,2]==r]; d=B[:,1]-B[:,0]; print(r,len(B),'bias %.3f mae %.3f max %.2f r %.4f'%(d.mean(),abs(d).mean(),abs(d).max(),np.corrcoef(B[:,0],B[:,1])[0,1]))
urb=[out[f['properties']['id']]['lst'] for f in F if f['properties']['mun'] in ('Cuiabá','Várzea Grande') and f['properties']['sit']=='Urbana' and out[f['properties']['id']]['lst'] is not None]
print('média urbana Cuiabá-VG',np.mean(urb),len(urb), 'antiga', np.mean([f['properties']['lst'] for f in F if f['properties']['mun'] in ('Cuiabá','Várzea Grande') and f['properties']['sit']=='Urbana' and f['properties'].get('lst') is not None]))
cl=[(f['properties']['mun'],f['properties']['id'],o['cloud'],o['lst']) for f in F for o in [out[f['properties']['id']]] if o.get('cloud',0)>0.1]
print('setores com nuvem >10%',len(cl),cl[:20])
