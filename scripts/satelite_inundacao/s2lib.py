import json,gzip,numpy as np,cv2,sys
sys.path.insert(0,'/home/claude/x')
from common import *
UP='/mnt/user-data/uploads/Downloads/'
def rd(fn):
    raw=open(UP+fn,'rb').read(); h=json.loads(raw[:512]); return h,gzip.decompress(raw[512:])
def rdwin(name):
    h,b=rd('s2win_%s.bin'%name); w,hh=h['w'],h['h']
    a=np.frombuffer(b,np.uint16,w*hh*2); red=a[:w*hh].reshape(hh,w).astype(np.float32); nir=a[w*hh:].reshape(hh,w).astype(np.float32)
    scl=np.frombuffer(b,np.uint8,h['sw']*h['sh'],offset=w*hh*4).reshape(h['sh'],h['sw'])
    scl=np.repeat(np.repeat(scl,2,0),2,1)
    return h,red,nir,scl
def rast(shape,e0,n1,res,geom,sub=8):
    """máscara do polígono na grade UTM (e0,n1 = canto superior esquerdo)"""
    Hh,Ww=shape; m=np.zeros(shape,np.uint8)
    for p in polys(geom):
        rings=[]
        for r in p:
            r=np.asarray(r); x,y=ll2utm(r[:,0],r[:,1]); rings.append(np.stack([(x-e0)/res,(n1-y)/res],-1))
        cv2.fillPoly(m,[np.round(rings[0]*sub).astype(np.int32)],1,shift=3)
        for hl in rings[1:]: cv2.fillPoly(m,[np.round(hl*sub).astype(np.int32)],0,shift=3)
    return m
from skimage.draw import polygon as _skpoly
def rastc(shape,e0,n1,res,geom):
    """máscara por centro de pixel (pixel pertence ao setor se o centro está dentro)"""
    m=np.zeros(shape,bool)
    for p in polys(geom):
        for k,r in enumerate(p):
            r=np.asarray(r); x,y=ll2utm(r[:,0],r[:,1])
            rr,cc=_skpoly((n1-y)/res-0.5,(x-e0)/res-0.5,shape)
            m[rr,cc]=(k==0)
    return m
