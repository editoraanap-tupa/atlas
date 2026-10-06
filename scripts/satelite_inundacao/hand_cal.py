import sys; sys.path.insert(0,'/home/claude/x')
from handlib import *
from common import *
import time
F,Hh=load_atlas()
a=np.load('inund_orig_rgba.npy'); O=np.zeros(a.shape[:2],np.uint8)
O[(a[...,0]==8)&(a[...,3]>0)]=1; O[(a[...,0]==107)&(a[...,3]>0)]=2; O[(a[...,0]==198)&(a[...,3]>0)]=3
i=Hh.find('const MUN = '); MUN,_=json.JSONDecoder().raw_decode(Hh[i+len('const MUN = '):])
RB=[-56.32,-15.3,-55.84,-15.8]; NX,NY=1728,1800; R=1/3600
msk=np.zeros((NY,NX),np.uint8)
for m in MUN['features']:
    if m['properties']['nome'] in ('Cuiabá','Várzea Grande'):
        for p in polys(m['geometry']):
            r=np.asarray(p[0]); cv2.fillPoly(msk,[np.round(np.stack([(r[:,0]-RB[0])/R,(RB[1]-r[:,1])/R],-1)).astype(np.int32)],1)
print('orig classes',np.bincount(O.ravel()), 'mask',msk.sum(), 'orig fora da máscara',int(((O>0)&(msk==0)).sum()))
h,Z=rd_dem('cvg'); print(h['lon0'],h['lat0'],Z.shape)
np.save('cal_O.npy',O); np.save('cal_msk.npy',msk)
def run(Zb,d8,A,AR,thr={1:(2,5,8),2:(4,8,12)},conn=True,ret=False):
    key=(id(Zb),d8)
    if key not in run.c: run.c[key]=flood(Zb,d8)
    fill,rec,order,acc=run.c[key]; ca=30.87*30.87*np.cos(np.radians(15.55))/1e6
    drain=np.zeros(Zb.shape,np.uint8); drain[acc*ca>=A]=1; drain[acc*ca>=AR]=2
    hd,dc=hand(Zb,rec,order,drain); return classes(hd,dc,drain,thr,conn),drain,hd
run.c={}
def score(C,O,m):
    k=m>0; agree=(C[k]==O[k]).mean(); iou=lambda c:(((C==c)&(O==c)&k).sum()/max(1,(((C==c)|(O==c))&k).sum()))
    return agree,iou(1),((C>0)&(O>0)&k).sum()/max(1,(((C>0)|(O>0))&k).sum()),(C[k]==1).mean(),(O[k]==1).mean()
if __name__=='__main__':
    for off in [(144,144)]:
        Zb=np.ascontiguousarray(Z[off[1]:off[1]+NY,off[0]:off[0]+NX])
        for d8 in (0,1):
            for A in (0.1,0.25,0.5,1,2,4):
                for AR in (300,1000):
                    t=time.time(); C,_,_=run(Zb,d8,A,AR); s=score(C,O,msk)
                    print('d8',d8,'A',A,'AR',AR,'concord %.3f IoU alta %.3f IoU qualquer %.3f  alta%% %.3f (orig %.3f)'%s)
