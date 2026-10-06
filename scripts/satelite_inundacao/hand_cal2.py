import sys; sys.path.insert(0,'/home/claude/x')
from hand_cal import *
from scipy import ndimage as ndi
i=Hh.find('const HIDRO = '); HID,_=json.JSONDecoder().raw_decode(Hh[i+len('const HIDRO = '):])
import collections
print(collections.Counter(f['properties'].get('t') for f in HID['features']), collections.Counter(f['geometry']['type'] for f in HID['features']))
print([ (k,v) for k,v in collections.Counter(f['properties'].get('n') for f in HID['features'] if f['properties'].get('t')=='r').most_common(12)])
Zb=np.ascontiguousarray(Z[144:144+NY,144:144+NX])
def px(c): c=np.asarray(c,float); return np.round(np.stack([(c[:,0]-RB[0])/R-0.5,(RB[1]-c[:,1])/R-0.5],-1)).astype(np.int32)
def drainmap(types=('r','s'),rivers=('Rio Cuiabá','Rio Coxipó'),areas=False):
    d=np.zeros((NY,NX),np.uint8)
    for f in HID['features']:
        p=f['properties']; t=p.get('t'); g=f['geometry']
        if g['type']=='LineString' and t in types:
            cv2.polylines(d,[px(g['coordinates'])],False,2 if (p.get('n') in rivers) else 1,1)
        elif areas and t=='a':
            for pg in ([g['coordinates']] if g['type']=='Polygon' else g['coordinates']): cv2.fillPoly(d,[px(pg[0])],1)
    # rios por cima
    for f in HID['features']:
        p=f['properties']; g=f['geometry']
        if g['type']=='LineString' and p.get('n') in rivers: cv2.polylines(d,[px(g['coordinates'])],False,2,1)
    return d
def eucl(Zb,d,maxd=None):
    dist,(iy,ix)=ndi.distance_transform_edt(d==0,return_indices=True)
    hd=(Zb-Zb[iy,ix]).astype(np.float32); hd[hd<0]=0; dc=d[iy,ix].copy()
    if maxd: dc[dist>maxd]=0
    return hd,dc
if __name__=='__main__':
    for types in [('r','s'),('r','s','c')]:
        for areas in (False,True):
            d=drainmap(types,areas=areas)
            for maxd in (None,):
                hd,dc=eucl(Zb,d,maxd)
                for conn in (True,False):
                    C=classes(hd,dc,d,conn=conn); print('eucl',types,'areas',areas,'conn',conn,'concord %.3f IoU alta %.3f IoU qualquer %.3f  alta%% %.3f (orig %.3f)'%score(C,O,msk))
            # caminho de fluxo com drenagem OSM
            for d8 in (0,1):
                fill,rec,order,acc=flood(Zb,d8); hd,dc=hand(Zb,rec,order,d); C=classes(hd,dc,d); print('fluxo OSM d8',d8,types,'areas',areas,'concord %.3f IoU alta %.3f IoU qualquer %.3f  alta%% %.3f (orig %.3f)'%score(C,O,msk))
