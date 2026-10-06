import sys,glob,os,time; sys.path.insert(0,'/home/claude/x')
from s2lib import *
E0,E1,N0,N1=475000,777000,8078000,8389500; RS=60; MW=(E1-E0)//RS; MH=(N1-N0)//RS
xc=E0+(np.arange(MW)+.5)*RS; yc=N1-(np.arange(MH)+.5)*RS-1e7   # UTM 21N (norte negativo)
def scene(key):
    h,b=rd('ls_%s_2.bin'%key); a=np.frombuffer(b,np.uint16).reshape(h['h'],h['w'])
    ci=np.floor((xc-h['e0'])/h['resx']).astype(int); ri=np.floor((h['n0']-yc)/h['resy']).astype(int)
    okc=(ci>=0)&(ci<h['w']); okr=(ri>=0)&(ri<h['h'])
    out=np.zeros((MH,MW),np.uint16); out[np.ix_(okr,okc)]=a[np.ix_(ri[okr],ci[okc])]
    return out,h
G={}
for grp,keys in [('p',['p71','p70','p72']),('w',['w71','w72']),('e',['e71','e70','e72']),('a',['alt72']),('n',['n70'])]:
    M=np.zeros((MH,MW),np.uint16)
    for k in keys:
        s,h=scene(k); m=(M<=1)&(s>M); M[m]=s[m]; print(grp,k,h['date'][:16],'validos',int((s>1).sum()),'nuvem',int((s==1).sum()))
    G[grp]=M; np.save('lst60_%s.npy'%grp,M)
C=lambda d: d*0.00341802+149.0-273.15
for a,b in [('p','w'),('p','e'),('p','a'),('w','a'),('e','a'),('p','n'),('w','n')]:
    k=(G[a]>1)&(G[b]>1)
    if k.sum()<1000: print(a,b,'sem sobreposição',int(k.sum())); continue
    x=C(G[a][k].astype(float)); y=C(G[b][k].astype(float)); print(a,b,'n',int(k.sum()),'médias %.2f %.2f  dif(b-a) %.2f  dp dif %.2f  r %.3f'%(x.mean(),y.mean(),(y-x).mean(),(y-x).std(),np.corrcoef(x,y)[0,1]))
