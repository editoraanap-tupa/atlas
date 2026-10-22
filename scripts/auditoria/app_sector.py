# Área em APP por setor (Lei 12.651/2012, art. 4º) com as faixas da camada vetorial do Atlas, nos 1.940 setores
import json, sys, numpy as np, math
sys.path.insert(0,'/home/claude/x')
from common import ll2utm, polys
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
s=open('/home/claude/d/atlas_rmvrc.html').read()
dec=json.JSONDecoder()
i=s.index('<script>const DATA = ')+len('<script>const DATA = '); D,_=dec.raw_decode(s[i:])
i=s.index('const HIDRO = ')+len('const HIDRO = '); HID,_=dec.raw_decode(s[i:])
# feições: (tipo, faixa, coords UTM, bbox)
FE=[]
def utm(c):
    a=np.asarray(c,float); x,y=ll2utm(a[:,0],a[:,1]); return np.stack([x,y],-1)
for f in HID['features']:
    p=f['properties']; g=f['geometry']; t=p['t']
    if t in('r','s') and p.get('app'): FE.append(('L',p['app'],[utm(g['coordinates'])]))
    elif t=='a':
        rings=[utm(r) for r in g['coordinates']]
        FE.append(('W',p.get('ap',0) if p.get('ak') in('rio','lago') else 0,rings))
    elif t=='n': FE.append(('P',50,[utm([g['coordinates']])]))
for k,f in enumerate(FE):
    a=np.concatenate(f[2]); FE[k]=f+((a[:,0].min(),a[:,1].min(),a[:,0].max(),a[:,1].max()),)
PAD=260
out={}
for n,feat in enumerate(D['features']):
    p=feat['properties']; area=p['area']
    res=5 if area<3 else 10 if area<40 else 20 if area<400 else 30
    rings=[[utm(r) for r in pg] for pg in polys(feat['geometry'])]
    a=np.concatenate([r[0] for r in rings]); x0,y0,x1,y1=a[:,0].min()-PAD,a[:,1].min()-PAD,a[:,0].max()+PAD,a[:,1].max()+PAD
    W=int(math.ceil((x1-x0)/res)); H=int(math.ceil((y1-y0)/res))
    tp=lambda r:[((x-x0)/res,(y1-y)/res) for x,y in r]
    def poly_mask(rr):
        im=Image.new('1',(W,H),0); d=ImageDraw.Draw(im)
        for pg in rr:
            d.polygon(tp(pg[0]),fill=1)
            for hole in pg[1:]: d.polygon(tp(hole),fill=0)
        return np.array(im,bool)
    sec=poly_mask(rings)
    near=[f for f in FE if not(f[3][2]<x0 or f[3][0]>x1 or f[3][3]<y0 or f[3][1]>y1)]
    water=np.zeros((H,W),bool); app=np.zeros((H,W),bool)
    wm=[f for f in near if f[0]=='W']
    if wm: water=poly_mask([f[2] for f in wm])
    for w in sorted({f[1] for f in near if f[1]}):
        im=Image.new('1',(W,H),0); d=ImageDraw.Draw(im); any_=False
        for f in near:
            if f[1]!=w: continue
            any_=True
            if f[0]=='L': d.line(tp(f[2][0]),fill=1,width=1)
            elif f[0]=='P':
                (px,py),=tp(f[2][0]); d.point((px,py),fill=1)
            else:
                d.polygon(tp(f[2][0]),fill=1)
                for hole in f[2][1:]: d.polygon(tp(hole),fill=0)
                d.line(tp(f[2][0]),fill=1,width=1)
        if not any_: continue
        m=np.array(im,bool)
        if m.any(): app|=ndi.distance_transform_edt(~m)*res<=w
    den=(sec&~water).sum(); num=(sec&~water&app).sum()
    out[p['id']]=round(100*num/den,1) if den>0 else None
    if n%200==0: print(n,p['id'],res,W,H,out[p['id']],p.get('app_pct'),flush=True)
json.dump(out,open('/home/claude/aud/app_sector.json','w'))
print('ok',len(out))
