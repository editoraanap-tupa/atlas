import ctypes,numpy as np,cv2,json,gzip
L=ctypes.CDLL('/home/claude/x/pflood.so')
dp=np.ctypeslib.ndpointer(np.float64,flags='C'); ip=np.ctypeslib.ndpointer(np.int32,flags='C'); up=np.ctypeslib.ndpointer(np.uint8,flags='C'); fp=np.ctypeslib.ndpointer(np.float32,flags='C')
L.pflood.argtypes=[dp,ctypes.c_int,ctypes.c_int,dp,ip,ip,ctypes.c_int]; L.accum.argtypes=[ip,ip,ctypes.c_long,dp]; L.handc.argtypes=[dp,ip,ip,up,ctypes.c_long,fp,up]
def flood(Z,d8=1):
    Z=np.ascontiguousarray(Z,np.float64); H,W=Z.shape; fill=np.empty(H*W); rec=np.empty(H*W,np.int32); order=np.empty(H*W,np.int32)
    L.pflood(Z.ravel(),H,W,fill,rec,order,d8); acc=np.empty(H*W); L.accum(rec,order,H*W,acc)
    return fill.reshape(H,W),rec,order,acc.reshape(H,W)
def hand(Z,rec,order,drain):
    Z=np.ascontiguousarray(Z,np.float64); N=Z.size; h=np.empty(N,np.float32); c=np.zeros(N,np.uint8)
    L.handc(Z.ravel(),rec,order,np.ascontiguousarray(drain,np.uint8).ravel(),N,h,c); return h.reshape(Z.shape),c.reshape(Z.shape)
def classes(h,dc,drain,thr={1:(2,5,8),2:(4,8,12)},conn=True):
    """1 alta, 2 média, 3 baixa, 0 fora; thr por classe de drenagem (1 córrego, 2 rio)"""
    out=np.zeros(h.shape,np.uint8)
    for d,(a,m,b) in thr.items():
        k=(dc==d)&(h>=0)
        out[k&(h<=b)]=3; out[k&(h<=m)]=2; out[k&(h<=a)]=1
    if conn:
        for lev in (3,2,1):
            msk=((out>0)&(out<=lev)).astype(np.uint8); n,lab=cv2.connectedComponents(msk,connectivity=8)
            keep=np.zeros(n,bool); keep[np.unique(lab[(drain>0)&(msk>0)])]=True; keep[0]=False
            drop=(msk>0)&~keep[lab]
            if lev==3: out[drop]=0
            else: out[drop&(out<=lev)]=lev+1
    return out
def rd_dem(name):
    raw=open('/mnt/user-data/uploads/Downloads/dem_%s.bin'%name,'rb').read(); h=json.loads(raw[:512]); Z=np.frombuffer(gzip.decompress(raw[512:]),np.float32).reshape(h['h'],h['w']).astype(np.float64); return h,Z
