import json, math, re, sys, collections, statistics as stt
import numpy as np
sys.path.insert(0,'/home/claude/d'); import os; os.chdir('/home/claude/d')
from calc import indicators, T
s=open('/home/claude/d/atlas_rmvrc.html').read()
def grab(pref):
    i=s.index(pref); j=s.index('\n',i); return json.loads(s[i+len(pref):j].rstrip().rstrip(';'))
D=grab('<script>const DATA = '); F=D['features']; P=[f['properties'] for f in F]
MUN=grab('const MUN = '); EQ=grab('const EQUIP = '); MICRO=grab('const MICRO = '); SUB=grab('const SUBBACIAS = '); BAC=grab('const BACIAS = ')
R={}
OFF={'Cuiabá':(650877,4327.448),'Várzea Grande':(300078,724.279),'Nossa Senhora do Livramento':(12940,5537.413),'Santo Antônio de Leverger':(15246,9469.139),'Acorizal':(5014,850.763),'Chapada dos Guimarães':(18990,6603.252),'Campo Verde':(44585,4770.631)}
MCODE={'Cuiabá':'5103403','Várzea Grande':'5108402','Nossa Senhora do Livramento':'5106109','Santo Antônio de Leverger':'5107800','Acorizal':'5100102','Chapada dos Guimarães':'5103007','Campo Verde':'5102678'}
# 1. população x IBGE oficial
pm=collections.Counter(); nm=collections.Counter()
for p in P: pm[p['mun']]+=p['pop']; nm[p['mun']]+=1
R['pop']={m:(pm[m],OFF[m][0],pm[m]-OFF[m][0]) for m in OFF}
# 2. recálculo dos indicadores censitários
keys=['pop','dppo','mor','idosos','criancas','mulheres','negros','indig','agua','agua_enc','esgoto','esg_prec','lixo','sem_banh','renda','renda_med','analf','pav','arvore','arv5','luz','calcada','bueiro','onibus']
dif=collections.Counter(); ex={}
for p in P:
    n=indicators(p['id'],None)
    for k in keys:
        a,b=p.get(k),n.get(k)
        if a is None and b is None: continue
        if a is None or b is None or abs(a-b)>0.051: dif[k]+=1; ex.setdefault(k,(p['id'],a,b))
R['recalc']=(dict(dif),ex)
# 3. coerência interna
iss=collections.defaultdict(list)
pct=['idosos','criancas','mulheres','negros','indig','agua','agua_enc','esgoto','esg_prec','lixo','sem_banh','analf','pav','arvore','arv5','luz','calcada','bueiro','onibus','app_pct','inund','c1974','sgb_alta','a1974','alerta','verde','veg_nat','eros_alta']
for p in P:
    for k in pct:
        v=p.get(k)
        if v is not None and not (0<=v<=100.0001): iss['fora_0_100'].append((p['id'],k,v))
    if p.get('esgoto') is not None and p.get('esg_prec') is not None and p['esgoto']+p['esg_prec']>100.2: iss['esgoto+precario>100'].append((p['id'],p['esgoto'],p['esg_prec']))
    if p.get('arv5') is not None and p.get('arvore') is not None and p['arv5']>p['arvore']+0.05: iss['arv5>arvore'].append(p['id'])
    for k,b in [('app_pop','app_pct'),('inund_pop','inund'),('c1974_pop','c1974'),('sgb_alta_pop','sgb_alta'),('a1974_pop','a1974')]:
        v=p.get(k)
        if v is not None and v>p['pop']+0.5: iss['moradores_em_risco>pop'].append((p['id'],k,v,p['pop']))
        if v is not None and p.get(b) is not None and abs(v-p['pop']*p[b]/100)>1.01: iss['pop_x_fracao_incoerente'].append((p['id'],k,v,p['pop'],p[b]))
    if p.get('pm') and abs(sum(p['pm'])+sum(p['pf'])-p['pop'])>max(3,0.02*p['pop']): iss['piramide≠pop'].append((p['id'],sum(p['pm'])+sum(p['pf']),p['pop']))
    if p.get('dens') is not None and p['area'] and abs(p['dens']-p['pop']/p['area'])/max(1,p['dens'])>0.02: iss['densidade≠pop/area'].append((p['id'],p['dens'],round(p['pop']/p['area'],1)))
    if p.get('ndvi') is not None and not (-1<=p['ndvi']<=1): iss['ndvi_fora'].append(p['id'])
    if p.get('lst') is not None and not (15<=p['lst']<=65): iss['lst_implausivel'].append((p['id'],p['lst']))
    if p.get('lst') is not None and p.get('lst_anom') is not None and abs(p['lst']-39.1-p['lst_anom'])>0.11: iss['anomalia≠lst-39,1'].append((p['id'],p['lst'],p['lst_anom']))
    if p.get('erosao') is not None and not (1<=p['erosao']<=3): iss['erosao_fora_1_3'].append(p['id'])
    for k in ('d_ubs','d_saude','d_esc','d_parque'):
        v=p.get(k)
        if v is not None and (v<0 or v>150000): iss['distancia_implausivel'].append((p['id'],k,v))
    if not p['id'].startswith(MCODE[p['mun']]): iss['codigo≠municipio'].append(p['id'])
    if p.get('renda') is not None and p.get('renda_med') is not None and p['renda_med']>p['renda']*1.6: iss['mediana>>media'].append((p['id'],p['renda'],p['renda_med']))
R['coer']={k:(len(v),v[:5]) for k,v in iss.items()}
ids=[p['id'] for p in P]; R['dup_ids']=len(ids)-len(set(ids))
# 4. geometria: área do polígono x AREA_KM2; centróide no município
def ring_area_km2(r):
    lat=math.radians(sum(c[1] for c in r)/len(r)); kx=111.320*math.cos(lat); ky=110.574
    return abs(sum((r[i][0]*kx)*(r[i+1][1]*ky)-(r[i+1][0]*kx)*(r[i][1]*ky) for i in range(len(r)-1)))/2
def polys(g): return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
def garea(g): return sum(ring_area_km2(p[0])-sum(ring_area_km2(h) for h in p[1:]) for p in polys(g))
def pip(pt,poly):
    x,y=pt; ins=False
    for ring in poly:
        for i in range(len(ring)-1):
            x0,y0=ring[i];x1,y1=ring[i+1]
            if (y0>y)!=(y1>y) and x<(x1-x0)*(y-y0)/(y1-y0)+x0: ins=not ins
    return ins
mp={m['properties']['nome']:polys(m['geometry']) for m in MUN['features']}
aerr=[]; fora=[]
for f in F:
    p=f['properties']; a=garea(f['geometry'])
    if p['area']>0: aerr.append(abs(a-p['area'])/p['area'])
    # ponto interior: centróide do maior anel (aprox.)
    big=max(polys(f['geometry']),key=lambda q:ring_area_km2(q[0]))[0]
    c=(sum(x for x,y in big)/len(big),sum(y for x,y in big)/len(big))
    if not any(pip(c,q) for q in mp[p['mun']]):
        # testa se cai em outro município
        other=[n for n,qs in mp.items() if any(pip(c,q) for q in qs)]
        fora.append((p['id'],p['mun'],other[:1],round(p['area'],3)))
aerr=np.array(aerr)
R['area_geom']={'mediana_%':round(100*np.median(aerr),2),'p95_%':round(100*np.percentile(aerr,95),2),'max_%':round(100*aerr.max(),1),'n>5%':int((aerr>0.05).sum())}
R['centroide_fora_mun']=(len(fora),fora[:8])
# área municipal do mapa x oficial
R['area_mun']={m:(round(sum(garea({'type':'MultiPolygon','coordinates':mp[m]} ) for _ in [0]),1),OFF[m][1]) for m in mp}
# 5. IVSA (réplica do cálculo da página)
WC=[('analf',1,0),('esgoto',-1,0),('lixo',-1,0),('agua',-1,0),('renda',-1,1),('arvore',-1,0),('pav',-1,0)]
NR={}
for k,sg,lg in WC:
    xs=[p[k] for p in P if p['pop']>=50 and p.get(k) is not None]
    if lg: xs=[math.log(x) for x in xs if x>0]
    NR[k]=(np.percentile(xs,2),np.percentile(xs,98))
iv=[]; cob=collections.Counter()
for p in P:
    if p['pop']<50: cob['pop<50']+=1; continue
    s_=0; w=0
    for k,sg,lg in WC:
        x=p.get(k)
        if x is None or (lg and x<=0): continue
        if lg: x=math.log(x)
        lo,hi=NR[k]; z=min(1,max(0,(x-lo)/((hi-lo) or 1)));
        if sg<0: z=1-z
        s_+=z; w+=1
    if w>=0.6*len(WC): iv.append((p['id'],p['mun'],p['sit'],round(100*s_/w,1),w))
    else: cob['sem_indice(<60%)']+=1
R['ivsa']={'com_indice':len(iv),'sem':dict(cob),'por_mun':{m:round(np.average([x[3] for x in iv if x[1]==m],weights=[next(q['pop'] for q in P if q['id']==x[0]) for x in iv if x[1]==m]),1) for m in OFF},
 'rural_sem_entorno':sum(1 for x in iv if x[4]<7)}
# 6. correlações de plausibilidade
def corr(a,b,flt=lambda p:True):
    xs=[(p[a],p[b]) for p in P if flt(p) and p.get(a) is not None and p.get(b) is not None]
    if len(xs)<10: return None
    x,y=np.array(xs).T; return (round(float(np.corrcoef(x,y)[0,1]),2),len(xs))
urb=lambda p:p['sit']=='Urbana'
R['corr']={'ndvi×verde':corr('ndvi','verde',urb),'ndvi×lst':corr('ndvi','lst',urb),'verde×veg_nat':corr('verde','veg_nat',urb),'arvore×verde':corr('arvore','verde',urb),
 'inund×sgb_alta':corr('inund','sgb_alta'),'c1974×a1974':corr('c1974','a1974'),'renda×analf':corr('renda','analf',urb),'renda×esgoto':corr('renda','esgoto',urb),'esgoto×esg_prec':corr('esgoto','esg_prec',urb),'d_ubs×dens':corr('d_ubs','dens',urb)}
R['lst_media_urb']=round(float(np.mean([p['lst'] for p in P if urb(p) and p.get('lst') is not None])),2)
# 7. distâncias: recálculo de d_ubs com os equipamentos publicados
def hav(a,b):
    R_=6371008.8; la1,la2=math.radians(a[1]),math.radians(b[1]); dl=math.radians(b[0]-a[0])
    return 2*R_*math.asin(math.sqrt(math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin(dl/2)**2))
ubs=[(e['x'],e['y']) for e in EQ if e['c']=='ubs']
dd=[]
import random; random.seed(1)
for f in random.sample(F,200):
    p=f['properties']
    if p.get('d_ubs') is None: continue
    big=max(polys(f['geometry']),key=lambda q:ring_area_km2(q[0]))[0]
    c=(sum(x for x,y in big)/len(big),sum(y for x,y in big)/len(big))
    d=min(hav(c,u) for u in ubs); dd.append(abs(d-p['d_ubs']))
R['d_ubs_recalc']={'n':len(dd),'mediana_dif_m':round(float(np.median(dd))),'p90_dif_m':round(float(np.percentile(dd,90)))}
# 8. equipamentos
c=collections.Counter((e['c'],e['f']) for e in EQ); dupe=collections.Counter((e['c'],round(e['x'],4),round(e['y'],4)) for e in EQ)
R['equip']={'total':len(EQ),'por_tipo':{f'{a}/{b}':n for (a,b),n in c.items()},'duplicados_mesmo_ponto':sum(n-1 for n in dupe.values() if n>1),
 'sem_nome':sum(1 for e in EQ if not e['n'])}
inside=0
for e in EQ:
    if any(any(pip((e['x'],e['y']),q) for q in qs) for qs in mp.values()): inside+=1
R['equip']['dentro_rmvrc']=inside
# 9. bacias / microbacias
R['bacias']={'bacias_km2':sum(f['properties']['area_rm'] for f in BAC['features']),'sub_km2':sum(f['properties']['area_rm'] for f in SUB['features']),'rmvrc_oficial_km2':round(sum(v[1] for v in OFF.values()),1),
 'micro_n':len(MICRO['features']),'micro_sem_nome':sum(1 for f in MICRO['features'] if f['properties']['nome']=='Microbacia sem nome')}
# 10. cobertura de dados por indicador
cov={}
for k in ['renda','analf','arvore','pav','ndvi','lst','inund','app_pct','veg_nat','erosao','d_ubs','sgb_alta','a1974']:
    cov[k]={m:round(100*sum(1 for p in P if p['mun']==m and p.get(k) is not None)/nm[m]) for m in OFF}
R['cobertura_%']=cov
json.dump(R,open('/home/claude/d/audit_result.json','w'),ensure_ascii=False,indent=1,default=str)
print(json.dumps(R,ensure_ascii=False,indent=1,default=str)[:12000])
