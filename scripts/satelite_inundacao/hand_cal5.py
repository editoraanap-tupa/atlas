import sys; sys.path.insert(0,'/home/claude/x')
from hand_cal2 import *
k=msk>0
def rep(nm,C): 
    s=score(C,O,msk); fr=[(C[k]==c).mean() for c in (1,2,3)]
    print(nm,'concord %.3f IoUalta %.3f IoUqq %.3f'%s[:3],'frac %.3f %.3f %.3f'%tuple(fr)); return s
def run(off=(144,144),ks=3,types=('r','s'),areas=False,conn=True,sub=0.5,thick=1,zsrc='min'):
    Zb=np.ascontiguousarray(Z[off[1]:off[1]+NY,off[0]:off[0]+NX])
    d=np.zeros((NY,NX),np.uint8)
    def px(c): c=np.asarray(c,float); return np.round(np.stack([(c[:,0]-RB[0])/R-sub,(RB[1]-c[:,1])/R-sub],-1)).astype(np.int32)
    for f in HID['features']:
        p=f['properties']; t=p.get('t'); g=f['geometry']
        if g['type']=='LineString' and t in types: cv2.polylines(d,[px(g['coordinates'])],False,1,thick)
        elif areas and t=='a':
            for pg in ([g['coordinates']] if g['type']=='Polygon' else g['coordinates']): cv2.fillPoly(d,[px(pg[0])],1)
    for f in HID['features']:
        p=f['properties']; g=f['geometry']
        if g['type']=='LineString' and p.get('n') in ('Rio Cuiabá','Rio Coxipó'): cv2.polylines(d,[px(g['coordinates'])],False,2,thick)
    dist,(iy,ix)=ndi.distance_transform_edt(d==0,return_indices=True); dc=d[iy,ix]
    Zm=cv2.erode(Zb.astype(np.float32),np.ones((ks,ks),np.uint8)).astype(np.float64) if ks>1 else Zb
    hd=(Zb-Zm[iy,ix]).astype(np.float32); hd[hd<0]=0
    return classes(hd,dc,d,conn=conn),d,hd,dc
if __name__=='__main__':
    for off in [(144,144),(143,144),(145,144),(144,143),(144,145),(143,143),(145,145)]: rep('off %s'%(off,),run(off)[0])
    for sub in (0,1): rep('sub %s'%sub,run(sub=sub)[0])
    rep('thick2 k1',run(ks=1,thick=2)[0]); rep('thick3 k1',run(ks=1,thick=3)[0]); rep('thick2 k3',run(ks=3,thick=2)[0])
    rep('areas',run(areas=True)[0]); rep('tipos rsc',run(types=('r','s','c'))[0]); rep('sem conn',run(conn=False)[0])
