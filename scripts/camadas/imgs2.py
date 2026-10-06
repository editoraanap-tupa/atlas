import json, numpy as np, base64, io, math, gzip
from PIL import Image
exec(open('env.py').read().split('# municipios')[0])
mun=np.load('mun.npy'); inR=mun>0
OUT=1800
R_=L0+W*RES; B_=T0-H*RES
def merc(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
yT,yB=merc(T0),merc(B_)
# linhas igualmente espaçadas em Mercator -> linha da grade original
rows=[]
for i in range(OUT):
    ym=yT+(yB-yT)*(i+.5)/OUT; lat=math.degrees(2*math.atan(math.exp(ym))-math.pi/2)
    rows.append(min(H-1,max(0,int((T0-lat)/RES))))
rows=np.array(rows); cols=np.clip(((np.arange(OUT)+.5)*W/OUT).astype(int),0,W-1)
def samp(a): return a[rows][:,cols]
def webp(a,lossless=True,q=90):
    b=io.BytesIO(); Image.fromarray(a,'RGBA').save(b,'WEBP',lossless=lossless,quality=q,method=6); return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
msk=samp(inR)
def hx(h,a=255): h=h.lstrip('#'); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),a)
imgs={}; leg={}
# ---- solos (legenda_2)
L2i=json.load(open('solo2_leg.json')); s2=samp(np.load('solo2.npy'))
SC={'LATOSSOLO VERMELHO':'#b8412f','LATOSSOLO VERMELHO-AMARELO':'#e0863a','LATOSSOLO AMARELO':'#f2c14e','ARGISSOLO VERMELHO-AMARELO':'#e7a0a0','ARGISSOLO VERMELHO':'#c9657a',
 'CAMBISSOLO HÁPLICO':'#a88b5b','NEOSSOLO LITÓLICO':'#9b8fb0','NEOSSOLO QUARTZARÊNICO':'#f5ecb0','NEOSSOLO FLÚVICO':'#7fb3c9','PLINTOSSOLO PÉTRICO':'#7d5a8c','PLINTOSSOLO ARGILÚVICO':'#b48ec4',
 'PLANOSSOLO HÁPLICO':'#8fc9b2','PLANOSSOLO NÁTRICO':'#5fa58c','GLEISSOLO HÁPLICO':'#6f8fb8','GLEISSOLO MELÂNICO':'#3f5f8a','VERTISSOLO HIDROMÓRFICO':'#4f4f4f','VERTISSOLO EBÂNICO':'#2f2f2f',
 'ORGANOSSOLO HÁPLICO':'#1b1b1b','AFLORAMENTO':'#c8c8c8','ÁREA URBANA':'#e2e2e2',"CORPO D'ÁGUA CONTINENTAL":'#9cc7e6'}
rgb=np.zeros((OUT,OUT,4),np.uint8); area={}
for n,i in L2i.items():
    m=(s2==i)&msk
    if m.any(): rgb[m]=hx(SC.get(n,'#cccccc'),215); area[n]=int(m.sum())
imgs['solos']=webp(rgb)
leg['solos']=[[n.capitalize().replace('-amarelo','-Amarelo').replace("d'água","d'água"),SC.get(n,'#ccc')] for n,_ in sorted(area.items(),key=lambda x:-x[1])]
# ---- erosao (continua 1,3–2,8)
cls=np.load('ero_cls.npy')
# refaz V continuo a partir das classes? usa classes (5) -> cores
EC={1:'#1a9850',2:'#91cf60',3:'#fee08b',4:'#fc8d59',5:'#d73027'}
e=samp(cls); rgb=np.zeros((OUT,OUT,4),np.uint8)
for k,c in EC.items(): rgb[(e==k)&msk]=hx(c,205)
imgs['erosao']=webp(rgb)
# ---- MapBiomas
MBC={3:('Formação florestal','#1f8d49'),4:('Formação savânica','#7dc975'),6:('Floresta alagável','#026975'),11:('Campo alagado e área pantanosa','#519799'),12:('Formação campestre','#d6bc74'),
 9:('Silvicultura','#7a5900'),15:('Pastagem','#edde8e'),21:('Mosaico de usos','#ffefc3'),39:('Soja','#f5b3c8'),20:('Cana','#db7093'),41:('Outras lavouras temporárias','#f54ca9'),62:('Algodão','#ff69b4'),
 24:('Área urbanizada','#d4271e'),25:('Outras áreas não vegetadas','#db4d4f'),29:('Afloramento rochoso','#ffaa5f'),30:('Mineração','#9c0027'),33:('Rio, lago e oceano','#2532e4'),31:('Aquicultura','#091077')}
mb=samp(MB); rgb=np.zeros((OUT,OUT,4),np.uint8); a2={}
for k,(n,c) in MBC.items():
    m=(mb==k)&msk
    if m.any(): rgb[m]=hx(c,215); a2[k]=int(m.sum())
imgs['mbveg']=webp(rgb)
leg['mbveg']=[[MBC[k][0],MBC[k][1]] for k,_ in sorted(a2.items(),key=lambda x:-x[1])]
json.dump({'bounds':[L0,T0,R_,B_],'img':imgs,'leg':leg},open('rast2.json','w'),ensure_ascii=False)
print({k:len(v)//1024 for k,v in imgs.items()}, leg['solos'][:5])
