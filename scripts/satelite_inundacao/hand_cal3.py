import sys; sys.path.insert(0,'/home/claude/x')
from hand_cal2 import *
k=msk>0
def rep(nm,C): 
    s=score(C,O,msk); fr=[(C[k]==c).mean() for c in (1,2,3)]
    print(nm,'concord %.3f IoUalta %.3f IoUqq %.3f'%s[:3],'frac %.3f %.3f %.3f'%tuple(fr))
print('orig frac',[(O[k]==c).mean() for c in (1,2,3)])
ca=30.87*30.87*np.cos(np.radians(15.55))/1e6
fill,rec,order,acc=flood(Zb,1)
dosm=drainmap(('r','s'))
for A in (0.5,1,2,5,10):
    d=np.zeros(Zb.shape,np.uint8); d[acc*ca>=A]=1; d[acc*ca>=300]=2
    hd,dc=eucl(Zb,d); rep('eucl DEM A=%s'%A,classes(hd,dc,d))
# euclidiano sobre DEM preenchido / suavizado
for nm,Zs in [('fill',fill),('blur3',cv2.blur(Zb,(3,3))),('med5',cv2.medianBlur(Zb.astype(np.float32),5).astype(np.float64))]:
    hd,dc=eucl(Zs,dosm); rep('eucl OSM '+nm,classes(hd,dc,dosm))
# limiares diferentes
hd,dc=eucl(Zb,dosm)
for thr in [{1:(1,3,5),2:(2,5,8)},{1:(1,2,5),2:(2,4,8)},{1:(2,5,8),2:(2,5,8)},{1:(1,2.5,4),2:(2,4,6)}]:
    rep('eucl OSM thr %s'%thr,classes(hd,dc,dosm,thr))
# histograma do HAND euclidiano dentro de cada classe original
for c in (1,2,3,0):
    m=k&(O==c); print('orig classe',c,'HAND eucl p10 p50 p90',np.percentile(hd[m],[10,50,90]).round(1), 'drain rio frac %.2f'%(dc[m]==2).mean())
