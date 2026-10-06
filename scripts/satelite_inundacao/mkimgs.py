import sys,io,base64,math; sys.path.insert(0,'/home/claude/x')
from s2lib import *
from PIL import Image
F,Hh=load_atlas()
i=Hh.find('const MUN = '); MUN,_=json.JSONDecoder().raw_decode(Hh[i+len('const MUN = '):])
def ramp(stops,v0,v1):
    c=np.array([[int(s[i:i+2],16) for i in (1,3,5)] for s in stops],float); n=len(c)-1
    def f(v):
        t=np.clip((v-v0)/(v1-v0),0,1)*n; i=np.minimum(t.astype(int),n-1); fr=(t-i)[...,None]
        return (c[i]*(1-fr)+c[i+1]*fr).round().astype(np.uint8)
    return f
RN=ramp(['#8c510a','#d8b365','#f6e8c3','#c7e9c0','#74c476','#238b45','#00441b'],-0.1,0.8)
RL=ramp(['#313695','#4575b4','#abd9e9','#ffffbf','#fdae61','#d73027','#67001f'],30,46)
def enc(rgba,q=80,lossless=False):
    b=io.BytesIO(); Image.fromarray(rgba,'RGBA').save(b,'WEBP',quality=q,lossless=lossless,method=6,exact=False); return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
def munmask(lon,lat):  # lon[], lat[] centros (grade regular em lon; lat arbitrária monotônica)
    NX,NY=len(lon),len(lat); m=np.zeros((NY,NX),np.uint8); dx=lon[1]-lon[0]
    for mu in MUN['features']:
        for p in polys(mu['geometry']):
            r=np.asarray(p[0]); x=(r[:,0]-lon[0])/dx; y=np.interp(-r[:,1],-lat,np.arange(NY))
            cv2.fillPoly(m,[np.round(np.stack([x,y],-1)).astype(np.int32)],1)
    return m>0
def merc_lats(lat_top,lat_bot,n):
    mer=lambda la: math.log(math.tan(math.pi/4+math.radians(la)/2)); yT,yB=mer(lat_top),mer(lat_bot)
    return np.array([math.degrees(2*math.atan(math.exp(yT+(yB-yT)*(i+.5)/n))-math.pi/2) for i in range(n)])
# ---------- fontes
E0,E1,N0,N1=475000,777000,8078000,8389500
M=np.load('mos40.npy')                      # malha 20 m
T=np.load('lst60_T.npy')                    # malha 60 m
def blockmean_ndvi(M,k):
    H,W=M.shape; H2,W2=H//k*k,W//k*k; a=M[:H2,:W2].reshape(H2//k,k,W2//k,k); ok=a>=-100
    s=np.where(ok,a,0).astype(np.float32).sum((1,3)); n=ok.sum((1,3)); out=np.full(n.shape,np.nan,np.float32); g=n>=(k*k*0.5); out[g]=s[g]/n[g]/100+0.005; return out
def blockmean(T,k):
    H,W=T.shape; H2,W2=H//k*k,W//k*k; a=T[:H2,:W2].reshape(H2//k,k,W2//k,k); ok=~np.isnan(a); s=np.where(ok,a,0).sum((1,3)); n=ok.sum((1,3)); out=np.full(n.shape,np.nan,np.float32); g=n>0; out[g]=s[g]/n[g]; return out
def sample(A,res,lon,lat,e0=E0,n1=N1):
    LO,LA=np.meshgrid(lon,lat); X,Y=ll2utm(LO,LA); c=np.floor((X-e0)/res).astype(int); r=np.floor((n1-Y)/res).astype(int)
    ok=(c>=0)&(c<A.shape[1])&(r>=0)&(r<A.shape[0]); out=np.full(LO.shape,np.nan,np.float32); out[ok]=A[r[ok],c[ok]]; return out
def img(v,rf,mask,q=80):
    rgba=np.zeros(v.shape+(4,),np.uint8); ok=~np.isnan(v)&mask; rgba[ok,:3]=rf(v[ok]); rgba[ok,3]=255; return enc(rgba,q)
OUT={}
# ---------- regional (limites do RAST2)
RB2=[-57.25008221457918,-14.54974316229865,-54.399907481124764,-17.400187390338303]; NR_=2200
lon=RB2[0]+(np.arange(NR_)+.5)*(RB2[2]-RB2[0])/NR_; lat=merc_lats(RB2[1],RB2[3],NR_); mk=munmask(lon,lat)
N120=blockmean_ndvi(M,6); T120=blockmean(T,2)
OUT['reg']={'ndvi':img(sample(N120,120,lon,lat),RN,mk,72),'lst':img(sample(T120,120,lon,lat),RL,mk,72)}
print('reg',{k:len(v)//1024 for k,v in OUT['reg'].items()})
# ---------- conurbação (limites do RAST), 1728x1800
RB=[-56.32,-15.3,-55.84,-15.8]; NX,NY=1728,1800
lon=RB[0]+(np.arange(NX)+.5)*(RB[2]-RB[0])/NX; lat=merc_lats(RB[1],RB[3],NY); mk=munmask(lon,lat)
h,b=rd('s2box_cvg.bin'); w,hh=h['w'],h['h']; v=np.frombuffer(b,np.int8,w*hh).reshape(hh,w); scl=np.frombuffer(b,np.uint8,h['sw']*h['sh'],offset=w*hh).reshape(h['sh'],h['sw']); scl=np.repeat(np.repeat(scl,2,0),2,1)
vv=np.where((v>-128)&~np.isin(scl,[0,1,3,6,8,9,10]),v,-128).astype(np.int8); N30=blockmean_ndvi(vv,3)
ndc=sample(N30,30,lon,lat,h['e0'],h['n1'])
hl,bl=rd('lsbox_wcvg.bin'); a=np.frombuffer(bl,np.uint16).reshape(hl['h'],hl['w']); t=np.where(a>1,a*0.00341802+149.0-273.15,np.nan).astype(np.float32)
ltc=sample(t,30,lon,lat,hl['e0'],hl['n0']+1e7)
OUT['cvg']={'ndvi':img(ndc,RN,mk,74),'lst':img(ltc,RL,mk,76)}
print('cvg',{k:len(v)//1024 for k,v in OUT['cvg'].items()}, 'nan ndvi',int(np.isnan(ndc[mk]).sum()),'nan lst',int(np.isnan(ltc[mk]).sum()))
# ---------- recortes das sedes e distritos
W=json.load(open('windows.json')); RAS=np.load('hand_ras.npy',allow_pickle=True).item(); P=[]
IC=np.array([[0,0,0,0],[8,81,156,220],[107,174,214,190],[198,219,239,150]],np.uint8)
DW,DN=4.01,1.96
for wi,wd in enumerate(W):
    b=wd['bbox']; d=0.0002; nx=int(round((b[2]-b[0])/d)); ny=int(round((b[3]-b[1])/d))
    lon=b[0]+(np.arange(nx)+.5)*d; lat=b[3]-(np.arange(ny)+.5)*d; mk=munmask(lon,lat)
    h,red,nir,scl=rdwin('w%d'%wi); nd=(nir-red)/np.maximum(nir+red,1); nd[np.isin(scl,[0,1,3,6,8,9,10])]=np.nan
    k=2; H2,W2=nd.shape[0]//k*k,nd.shape[1]//k*k; a=nd[:H2,:W2].reshape(H2//k,k,W2//k,k); ok=~np.isnan(a); s=np.where(ok,a,0).sum((1,3)); n=ok.sum((1,3)); n2=np.full(n.shape,np.nan,np.float32); n2[n>=2]=s[n>=2]/n[n>=2]
    e={'b':[round(b[0],5),round(b[3],5),round(b[2],5),round(b[1],5)],'ndvi':img(sample(n2,20,lon,lat,h['e0'],h['n1']),RN,mk,82)}
    nm,adj={14:('w14_oeste',DW),6:('w6_n70',DN)}.get(wi,('w%d'%wi,0))
    hl,bl=rd('lsbox_%s.bin'%nm); a=np.frombuffer(bl,np.uint16).reshape(hl['h'],hl['w']); t=np.where(a>1,a*0.00341802+149.0-273.15+adj,np.nan).astype(np.float32)
    e['lst']=img(sample(t,30,lon,lat,hl['e0'],hl['n0']+1e7),RL,mk,82)
    if wi in RAS:
        C=RAS[wi]['C']; R=1/3600; ci=np.round((lon-RAS[wi]['lon0'])/R).astype(int); ri=np.round((RAS[wi]['lat0']-lat)/R).astype(int)
        okc=(ci>=0)&(ci<C.shape[1]); okr=(ri>=0)&(ri<C.shape[0]); cc=np.zeros((ny,nx),np.uint8); cc[np.ix_(okr,okc)]=C[np.ix_(ri[okr],ci[okc])]; cc[~mk]=0
        um=np.zeros((ny,nx),np.uint8)
        for f in F:
            p=f['properties']
            if p['sit']!='Urbana' or p['mun'] in ('Cuiabá','Várzea Grande'): continue
            for pg in polys(f['geometry']):
                r=np.asarray(pg[0])
                if r[:,0].max()<b[0] or r[:,0].min()>b[2] or r[:,1].max()<b[1] or r[:,1].min()>b[3]: continue
                cv2.fillPoly(um,[np.round(np.stack([(r[:,0]-b[0])/d,(b[3]-r[:,1])/d],-1)).astype(np.int32)],1)
        um=cv2.dilate(um,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(27,27)))   # margem de ~300 m em torno dos setores urbanos
        cc[um==0]=0
        e['inund']=enc(IC[cc],lossless=True)
    P.append(e)
OUT['patches']=P
print('patches KB',sum(len(v) for e in P for k,v in e.items() if k!='b')//1024,[ {k:len(v)//1024 for k,v in e.items() if k!='b'} for e in P[:3]])
json.dump(OUT,open('rast_new.json','w'))
# prévias
def prev(uri,fn,sz=900):
    im=Image.open(io.BytesIO(base64.b64decode(uri.split(',')[1]))).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); bg.convert('RGB').resize((sz,int(sz*im.size[1]/im.size[0]))).save(fn)
prev(OUT['reg']['ndvi'],'pv_reg_ndvi.png'); prev(OUT['reg']['lst'],'pv_reg_lst.png'); prev(OUT['cvg']['ndvi'],'pv_cvg_ndvi.png',700); prev(OUT['cvg']['lst'],'pv_cvg_lst.png',700)
prev(P[0]['ndvi'],'pv_w0_ndvi.png',500); prev(P[0]['lst'],'pv_w0_lst.png',500); prev(P[15]['inund'],'pv_w15_inund.png',800)
