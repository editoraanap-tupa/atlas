# Regenera a pasta dados/ do repositório a partir do Atlas publicado (mesmos números da página)
import json, math, numpy as np, csv, io
R='/home/claude/repo/atlas-rmvrc/dados/'
s=open('/home/claude/d/atlas_rmvrc.html').read(); dec=json.JSONDecoder()
def grab(pref):
    i=s.index(pref)+len(pref); v,_=dec.raw_decode(s[i:]); return v
D=grab('<script>const DATA = '); F=D['features']; P=[f['properties'] for f in F]
# IVSA como a página calcula ao abrir (7 componentes do Censo, peso 1; normalização P2–P98 dos setores com 50+ moradores)
WC=[('analf',1,0),('esgoto',-1,0),('lixo',-1,0),('agua',-1,0),('renda',-1,1),('arvore',-1,0),('pav',-1,0)]
NR={}
for k,sg,lg in WC:
    xs=[p[k] for p in P if p['pop']>=50 and p.get(k) is not None]
    if lg: xs=[math.log(x) for x in xs if x>0]
    NR[k]=(np.percentile(xs,2),np.percentile(xs,98))
dif=[]
for p in P:
    old=p.get('ivsa')
    if p['pop']<50: p['ivsa']=None; p['ivsa_n']=None; continue
    sm=0; n=0
    for k,sg,lg in WC:
        x=p.get(k)
        if x is None or (lg and x<=0): continue
        if lg: x=math.log(x)
        lo,hi=NR[k]; z=min(1,max(0,(x-lo)/((hi-lo) or 1)));
        if sg<0: z=1-z
        sm+=z; n+=1
    p['ivsa']=round(1000*sm/n)/10 if n>=0.6*len(WC) else None; p['ivsa_n']=n if p['ivsa'] is not None else None
    if old is not None and p['ivsa'] is not None: dif.append(abs(old-p['ivsa']))
print('ivsa: setores',sum(p['ivsa'] is not None for p in P),'parciais',sum(1 for p in P if p['ivsa_n'] and p['ivsa_n']<7),'dif. máx. com o gravado',max(dif) if dif else None)
RT=json.load(open('/home/claude/aud/runtime_props.json'))
mx=0
for q in P:
    r=RT[q['id']]
    if (r['ivsa'] is None)!=(q['ivsa'] is None) or (r['ivsa'] is not None and abs(r['ivsa']-q['ivsa'])>0.051): mx+=1
    q['ivsa']=r['ivsa']; q['verde_hab']=round(r['verde_hab'],1) if r['verde_hab'] is not None else None; q['sat_veg']=r['sat_veg']; q['sat_lst']=r['sat_lst']
print('IVSA python × página: divergências',mx)
COLS=['id','mun','sit','bairro','dist','fcu','area','pop','dens','dppo','mor','idosos','criancas','mulheres','negros','indig','agua','agua_enc','esgoto','esg_prec','lixo','sem_banh','renda','renda_med','analf','pav','arvore','arv5','luz','calcada','bueiro','onibus','ivsa','ivsa_n','app_pct','app_pop','inund','inund2','inund_pop','ndvi','verde','lst','d_ubs','d_saude','d_esc','d_parque','lst_anom','c1974','c1974_pop','alerta','sgb_alta','sgb_alta_pop','sgb_am','a1974','a1974_pop','aalerta','veg_nat','erosao','eros_alta','solo','micro','bac','subbac','verde_hab','w15','went','wr','sat_veg','sat_lst']
miss=[c for c in COLS if c not in P[0]]; print('colunas ausentes na base:',miss)
def fmt(v):
    if v is None: return ''
    if isinstance(v,float): return (('%.4f'%v).rstrip('0').rstrip('.')).replace('.',',')
    return str(v)
b=io.StringIO(); w=csv.writer(b,delimiter=';',lineterminator='\n'); w.writerow(COLS)
for p in P: w.writerow([fmt(p.get(c)) for c in COLS])
open(R+'setores_rmvrc_indicadores.csv','w',encoding='utf-8-sig').write(b.getvalue())
G={'type':'FeatureCollection','features':[{'type':'Feature','properties':{c:f['properties'].get(c) for c in COLS},'geometry':f['geometry']} for f in F]}
json.dump(G,open(R+'setores_rmvrc.geojson','w'),ensure_ascii=False,separators=(',',':'))
for pref,fn in [('const MUN = ','mun.geojson'),('const HIDRO = ','hidro.geojson'),('const BACIAS = ','bacias.geojson'),('const SUBBACIAS = ','subbacias.geojson'),('const MICRO = ','micro.geojson'),('const SGB = ','sgb.geojson'),('const EQUIP = ','equipamentos.json'),('const SAUDE=','saude_municipios.json'),('const LENS=','lentes_prioridade.json')]:
    try: v=grab(pref)
    except ValueError: print('não achei',pref); continue
    json.dump(v,open(R+fn,'w'),ensure_ascii=False,separators=(',',':')); print(fn,'ok')
