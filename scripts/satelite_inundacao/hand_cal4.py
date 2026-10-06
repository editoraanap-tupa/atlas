import sys; sys.path.insert(0,'/home/claude/x')
from hand_cal2 import *
k=msk>0
def rep(nm,C): 
    s=score(C,O,msk); fr=[(C[k]==c).mean() for c in (1,2,3)]
    print(nm,'concord %.3f IoUalta %.3f IoUqq %.3f'%s[:3],'frac %.3f %.3f %.3f'%tuple(fr)); return s
dosm=drainmap(('r','s'))
dist,(iy,ix)=ndi.distance_transform_edt(dosm==0,return_indices=True); dc=dosm[iy,ix]
for ks in (1,3,5,7,9,13):
    Zm=cv2.erode(Zb.astype(np.float32),np.ones((ks,ks),np.uint8)).astype(np.float64) if ks>1 else Zb
    hd=(Zb-Zm[iy,ix]).astype(np.float32); hd[hd<0]=0
    rep('eucl OSM zmin k=%d'%ks,classes(hd,dc,dosm))
    Zc=cv2.erode(Zb.astype(np.float32),np.ones((ks,ks),np.uint8)).astype(np.float64) if ks>1 else Zb
    hd=(Zc-Zm[iy,ix]).astype(np.float32); hd[hd<0]=0
    rep('  ambos zmin k=%d'%ks,classes(hd,dc,dosm))
