# NDVI e cobertura vegetal por setor — Sentinel-2 L2A (Earth Search), RMVRC
# Regras: NDVI=(B8-B4)/(B8+B4); pixels válidos = fora de água (SCL 6), nuvem/sombra (SCL 3,8,9,10) e sem dado (SCL 0,1)
# 10 m onde o setor cabe inteiro num recorte de 10 m (conurbação e sedes/distritos); 40 m (reamostragem do próprio COG) nos demais
import sys,glob,os,time; sys.path.insert(0,'/home/claude/x')
from s2lib import *
import cv2
F,H=load_atlas()
BAD=[0,1,3,6,8,9,10]
R10=[]
# conurbação
h,b=rd('s2box_cvg.bin'); w,hh=h['w'],h['h']
v=np.frombuffer(b,np.int8,w*hh).reshape(hh,w); scl=np.frombuffer(b,np.uint8,h['sw']*h['sh'],offset=w*hh).reshape(h['sh'],h['sw']); scl=np.repeat(np.repeat(scl,2,0),2,1)
R10.append(dict(name='cvg',e0=h['e0'],n1=h['n1'],w=w,h=hh,nd=v.astype(np.float32)/100+0.005,gt=v>=45,ok=(v>-128)&~np.isin(scl,BAD),nod=(v==-128),date='23/08/2026',used=h['used']))
print('cvg',h['used'],'nodata',int((v==-128).sum()))
for i in range(17):
    h,red,nir,scl=rdwin('w%d'%i); nd=(nir-red)/np.maximum(nir+red,1)
    R10.append(dict(name='w%d'%i,e0=h['e0'],n1=h['n1'],w=h['w'],h=h['h'],nd=nd,gt=nd>=0.45,ok=~np.isin(scl,BAD),nod=(red==0)&(nir==0),date=h['date'][8:10]+'/08/2026'))
# mosaico 40 m na malha de 20 m
E0,E1,N0,N1=475000,777000,8078000,8389500; MW=(E1-E0)//20; MH=(N1-N0)//20
M=np.full((MH,MW),-128,np.int8); SRC=np.zeros((MH,MW),np.uint8)
fl=sorted(glob.glob(UP+'s2ndvi40_*0823*'))+sorted(glob.glob(UP+'s2ndvi40_*0817*'))
for fn in fl:
    h,b=rd(os.path.basename(fn)); a=np.frombuffer(b,np.int8).reshape(h['h'],h['w']); a=np.repeat(np.repeat(a,2,0),2,1)
    c0=int((h['e0']-E0)//20); r0=int((N1-h['n0'])//20)
    assert (h['e0']-E0)%20==0 and (N1-h['n0'])%20==0
    # recorta à malha
    y0=max(0,r0); x0=max(0,c0); y1=min(MH,r0+a.shape[0]); x1=min(MW,c0+a.shape[1])
    sub=M[y0:y1,x0:x1]; new=a[y0-r0:y1-r0,x0-c0:x1-c0]
    k=((sub==-128)|(sub==-126))&(new!=-128)&~((sub==-126)&(new==-126))
    sub[k]=new[k]; SRC[y0:y1,x0:x1][k]=1 if '0823' in fn else 2
    print(os.path.basename(fn)[9:-4],int(k.sum()))
np.save('mos40.npy',M); np.save('mos40_src.npy',SRC)
out={}; t0=time.time()
def bboxutm(g):
    xs=[];ys=[]
    for p in polys(g):
        r=np.asarray(p[0]); x,y=ll2utm(r[:,0],r[:,1]); xs+=[x.min(),x.max()]; ys+=[y.min(),y.max()]
    return min(xs),min(ys),max(xs),max(ys)
for f in F:
    p=f['properties']; x0,y0,x1,y1=bboxutm(f['geometry']); done=False
    for R in R10:
        if x0>=R['e0']+10 and x1<=R['e0']+R['w']*10-10 and y0>=R['n1']-R['h']*10+10 and y1<=R['n1']-10:
            c0=int((x0-R['e0'])/10)-1; c1=int((x1-R['e0'])/10)+2; r0=int((R['n1']-y1)/10)-1; r1=int((R['n1']-y0)/10)+2
            c0=max(c0,0); r0=max(r0,0)
            m=rastc((r1-r0,c1-c0),R['e0']+c0*10,R['n1']-r0*10,10,f['geometry'])
            if m.sum()==0 or R['nod'][r0:r1,c0:c1][m].any(): continue
            ok=R['ok'][r0:r1,c0:c1][m]; n=int(m.sum()); nv=int(ok.sum())
            if nv==0: out[p['id']]=dict(ndvi=None,verde=None,res=10,n=n,nv=0,date=R['date']); done=True; break
            nd=R['nd'][r0:r1,c0:c1][m][ok]; gt=R['gt'][r0:r1,c0:c1][m][ok]
            out[p['id']]=dict(ndvi=round(float(nd.mean()),3),verde=round(100*float(gt.mean()),1),res=10,n=n,nv=nv,date=R['date']); done=True; break
    if done: continue
    c0=max(0,int((x0-E0)/20)-1); c1=min(MW,int((x1-E0)/20)+2); r0=max(0,int((N1-y1)/20)-1); r1=min(MH,int((N1-y0)/20)+2)
    if (r1-r0)*(c1-c0)<6e6: m=rastc((r1-r0,c1-c0),E0+c0*20,N1-r0*20,20,f['geometry'])
    else: m=rast((r1-r0,c1-c0),E0+c0*20,N1-r0*20,20,f['geometry'])==1
    n=int(m.sum())
    if n==0:
        out[p['id']]=dict(ndvi=None,verde=None,res=40,n=0,nv=0,date=None); continue
    a=M[r0:r1,c0:c1][m]; s=SRC[r0:r1,c0:c1][m]; ok=a>=-100; nv=int(ok.sum()); nnod=int((a==-128).sum())
    if nv==0 or nnod>0.5*n:
        out[p['id']]=dict(ndvi=None,verde=None,res=40,n=n,nv=nv,date=None); continue
    f17=float((s[ok]==2).mean())
    out[p['id']]=dict(ndvi=round(float(a[ok].mean())/100+0.005,3),verde=round(100*float((a[ok]>=45).mean()),1),res=40,n=n,nv=nv,date='23/08/2026' if f17<0.05 else ('17/08/2026' if f17>0.95 else '17 e 23/08/2026'),f17=round(f17,3))
json.dump(out,open('ndvi_out.json','w'))
print('ok',len(out),round(time.time()-t0),'s')
