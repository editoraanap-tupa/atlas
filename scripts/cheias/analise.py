import json, math, sys, base64, io, collections, pickle
import numpy as np, cv2
from PIL import Image
exec(open('cheias.py').read().split('# ---- setores/bairros')[0].split("# ---- rio Cuiabá rasterizado")[0])
ys,xs=np.load('river_idx.npy'); sm=np.load('surf.npy'); meta=pickle.load(open('meta.pkl','rb')); kreg=meta['kreg']
sl=np.load('setor_lab.npy'); near=np.load('near.npy'); D=np.load('D.npy')
SURF=sm[near]; Zf=np.nan_to_num(Z,nan=9999); ZERO=139.36
DELTA=2.5
CEN=[('alerta','Cota de alerta',8.50),('emerg','Cota de emergência',9.50),('c1995','Cheia de fev/1995',10.36),('c1974','Cheia de mar/1974',10.85),('calam','Cota de calamidade',11.00)]
def flood(regua,delta=DELTA):
    lvl=SURF+(ZERO+regua-sm[kreg])+delta
    m=((Zf<lvl)&(D<12000)).astype(np.uint8); m[ys,xs]=1
    n,lab=cv2.connectedComponents(m,connectivity=8)
    keep=np.zeros(n,bool); keep[np.unique(lab[ys,xs])]=True; keep[0]=False
    return keep[lab]
s=open('/home/claude/d/atlas_rmvrc.html').read()
i=s.index('const DATA = '); j=s.index('\n',i); DATA=json.loads(s[i+len('const DATA = '):j].rstrip(';'))
i=s.index('const RAST = '); j=s.index('\n',i); RAST=json.loads(s[i+len('const RAST = '):j].rstrip(';'))
i=s.index('const SGB = '); j=s.index('\n',i); SGBR=json.loads(s[i+len('const SGB = '):j].rstrip(';'))
F=[f for f in DATA['features'] if f['properties']['mun'] in ('Cuiabá','Várzea Grande')]
N=len(F); npx=np.bincount(sl.ravel(),minlength=N+1).astype(float)
pop=np.array([0]+[f['properties']['pop'] for f in F],float)
urbid=np.array([0]+[f['properties']['sit']=='Urbana' for f in F],bool)
URB=urbid[sl]
def frac(m):
    fp=np.bincount(sl[m],minlength=N+1).astype(float); return np.divide(fp,npx,out=np.zeros_like(fp),where=npx>0)
# ---- cenarios ANADEM
cen={}; cenimg=np.zeros((H,W),np.uint8)
for n,(k,nome,r) in enumerate(CEN):
    m=flood(r); cen[k]=m
for n,(k,nome,r) in reversed(list(enumerate(CEN))): cenimg[cen[k]]=n+1
tab=[]
for k,nome,r in CEN:
    fr=frac(cen[k]); tab.append({'k':k,'nome':nome,'regua':r,'alt':round(ZERO+r,2),'km2':round(float(cen[k].sum()*PXA),1),'mor':int(round((fr*pop).sum()))})
print(tab)
# bairros (bairro ou distrito)
BAI=[('Terceiro','Cuiabá','1974'),('Porto','Cuiabá','1974'),('Praeirinho','Cuiabá','1995'),('Cristo Rei','Várzea Grande','1995'),('Passagem da Conceição','Várzea Grande','1974'),('Bom Sucesso','Várzea Grande','1974')]
sgbA=sgb==3; sgbAM=sgb>=2
bai=[]
for b,mu,ano in BAI:
    ids=[k+1 for k,f in enumerate(F) if f['properties']['mun']==mu and (f['properties']['bairro']==b or (not f['properties']['bairro'] and f['properties']['dist']==b) or (mu=='Várzea Grande' and f['properties']['dist']==b))]
    msk=np.isin(sl,ids); a=msk.sum()
    bai.append({'b':b,'mun':mu,'ano':ano,'a74':round(100*(cen['c1974']&msk).sum()/max(1,a),1),'sgbA':round(100*(sgbA&msk).sum()/max(1,a),1),'sgbAM':round(100*(sgbAM&msk).sum()/max(1,a),1),'n':len(ids)})
print(bai)
# ---- rasters antigos (GLO-30) decodificados
def dec(k):
    b=base64.b64decode(RAST['img'][k].split(',',1)[1]); a=np.array(Image.open(io.BytesIO(b)).convert('RGBA'))
    return a
ch=dec('cheias'); CHC={(8,48,107):1,(8,81,156):2,(33,113,181):3,(66,146,198):4,(107,174,214):5}
old=np.zeros(ch.shape[:2],np.uint8)
for c,v in CHC.items(): old[(ch[:,:,0]==c[0])&(ch[:,:,1]==c[1])&(ch[:,:,2]==c[2])&(ch[:,:,3]>0)]=v
old=np.kron(old,np.ones((3,3),np.uint8))[:H,:W]
g74=(old>=1)&(old<=4)
hd=dec('inund'); HC={(198,219,239):1,(107,174,214):2,(8,81,156):3}
hand=np.zeros(hd.shape[:2],np.uint8)
for c,v in HC.items(): hand[(hd[:,:,0]==c[0])&(hd[:,:,1]==c[1])&(hd[:,:,2]==c[2])&(hd[:,:,3]>0)]=v
hand=np.kron(hand,np.ones((3,3),np.uint8))[:H,:W]
a74=cen['c1974']
def pc(a,b): return round(100*float((a&b).sum())/max(1,float(b.sum())),1)
def iou(a,b): return round(100*float((a&b).sum())/max(1,float((a|b).sum())),1)
# área de análise: setores urbanos de Cuiabá e VG cobertos pela carta SGB (sgb>0 ou dentro dos municipios cobertos)
V={}
V['iou_74']=iou(a74,g74); V['a74_in_g74']=pc(g74,a74); V['g74_in_a74']=pc(a74,g74)
U=URB
V['urb_km2']=round(float(U.sum()*PXA),1)
V['sgbA_urb_km2']=round(float((sgbA&U).sum()*PXA),1); V['sgbAM_urb_km2']=round(float((sgbAM&U).sum()*PXA),1)
V['sgbA_urb_pct']=round(100*float((sgbA&U).sum())/float(U.sum()),1)
V['handA_urb_pct']=round(100*float(((hand==3)&U).sum())/float(U.sum()),1)
V['handA_in_sgbAM']=pc(sgbAM,(hand==3)&U)   # % da classe alta HAND (urbano) dentro de alta/media SGB
V['sgbA_in_handAM']=pc(hand>=2,sgbA&U)      # % da alta SGB coberta por HAND media/alta
V['a74_in_sgbA']=pc(sgbA,a74&U); V['a74_in_sgbAM']=pc(sgbAM,a74&U)
V['g74_in_sgbAM']=pc(sgbAM,g74&U)
# poligonos de risco do SGB (setorizacao) x carta
def polys(g): return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
tA=tAM=tot=0
for f in SGBR['features']:
    if not any(w in f['properties']['tipo'].lower() for w in ('inund','alag','enchente')): continue
    m=np.zeros((H,W),np.uint8)
    for p in polys(f['geometry']): cv2.fillPoly(m,[ipts(pix(p[0]))],1,shift=3)
    m=m.astype(bool); tot+=1
    if (m&sgbA).any(): tA+=1
    if (m&sgbAM).any(): tAM+=1
V['risco_n']=tot; V['risco_toca_sgbA']=tA; V['risco_toca_sgbAM']=tAM
# moradores em SGB alta
frA=frac(sgbA); frAM=frac(sgbAM)
V['mor_sgbA']=int(round((frA*pop).sum())); V['mor_sgbAM']=int(round((frAM*pop).sum()))
print(json.dumps(V,ensure_ascii=False))
# ---- por setor
fa74=frac(a74); fal=frac(cen['alerta'])
per={}
for k,f in enumerate(F):
    per[f['properties']['id']]={'sgb_alta':round(100*frA[k+1],1),'sgb_alta_pop':int(round(frA[k+1]*pop[k+1])),'sgb_am':round(100*frAM[k+1],1),
        'a1974':round(100*fa74[k+1],1),'a1974_pop':int(round(fa74[k+1]*pop[k+1])),'aalerta':round(100*fal[k+1],1)}
json.dump({'tab':tab,'bai':bai,'V':V,'delta':DELTA,'per':per,'calib':json.load(open('calib.json'))},open('resultado.json','w'),ensure_ascii=False)
# ---- imagens (1728x1800, ~30 m) — classe maxima no bloco 3x3
def down(a): return a.reshape(1800,3,1728,3).max(axis=(1,3))
sg=down(sgb); ci=np.where(cenimg>0,cenimg,0); ci=ci.reshape(1800,3,1728,3); ci=np.where(ci>0,ci,99).min(axis=(1,3)); ci[ci==99]=0
rgbS=np.zeros((1800,1728,4),np.uint8)
for v,c in {1:(254,224,139,120),2:(244,109,67,175),3:(165,0,38,215)}.items(): rgbS[sg==v]=c
rgbC=np.zeros((1800,1728,4),np.uint8)
for v,c in {1:(63,0,125,225),2:(84,39,143,215),3:(106,81,163,205),4:(128,125,186,195),5:(188,189,220,185)}.items(): rgbC[ci==v]=c
def webp(a):
    b=io.BytesIO(); Image.fromarray(a,'RGBA').save(b,'WEBP',lossless=True,quality=100,method=6); return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
imgs={'sgbc':webp(rgbS),'cheias2':webp(rgbC)}
json.dump(imgs,open('imgs.json','w'))
print('img KB',{k:len(v)//1024 for k,v in imgs.items()})
