import json
H=open('/home/claude/d/atlas_rmvrc.html').read()
i=H.find('const DATA = ')+len('const DATA = '); D,_=json.JSONDecoder().raw_decode(H[i:])
F=[f['properties'] for f in D['features']]
S=json.load(open('sih_rmvrc.json'))
def num(x): return 0 if x in ('-','') else int(x.replace('.',''))
def tab(rows):
    hdr=None; out={}
    for r in rows:
        if len(r)>1 and r[0] in ('Município','Lista Morb  CID-10','Município de residência','Ano/mês atendimento'): hdr=r; continue
        if hdr and len(r)==len(hdr): out[r[0]]={h:num(v) for h,v in zip(hdr[1:],r[1:])}
    return out
NM={'510010':'Acorizal','510267':'Campo Verde','510300':'Chapada dos Guimarães','510340':'Cuiabá','510610':'Nossa Senhora do Livramento','510780':'Santo Antônio de Leverger','510840':'Várzea Grande'}
CODE={'2':'510010','25':'510267','31':'510300','40':'510340','73':'510610','123':'510780','137':'510840'}
YRS=['2023','2024','2025']
pop={m:0 for m in NM.values()}
agg={m:{'esg':0,'agua':0,'lixo':0,'w':0,'ivsa':0,'wp':0} for m in NM.values()}
for p in F:
    m=p['mun']; pop[m]+=p['pop'] or 0
    w=p.get('dppo') or 0
    if all(p.get(k) is not None for k in ('esgoto','agua','lixo')) and w:
        a=agg[m]; a['esg']+=p['esgoto']*w; a['agua']+=p['agua']*w; a['lixo']+=p['lixo']*w; a['w']+=w
    if p.get('ivsa') is not None: agg[m]['ivsa']+=p['ivsa']*p['pop']; agg[m]['wp']+=p['pop']
def permun(t):
    out={}
    for k,v in t.items():
        c=k[:6]
        if c in NM: out[NM[c]]=[v.get(y,0) for y in YRS]
    return out
G=[('Feco-oral','diarreias, cólera e outras infecções intestinais',['Cólera','Febres tifóide','Shiguelose','Amebíase','Diarréia','Outras doenças infecciosas intestinais']),
   ('Inseto vetor','dengue, leishmaniose, malária, febre amarela, Chagas',['Outras febre p/arbovírus','Febre amarela','Leishmaniose','Malária','Tripanossomíase','Filariose']),
   ('Contato com a água','leptospirose, esquistossomose',['Outras doenças bacterianas','Leptospirose','Esquistossomose']),
   ('Higiene','micoses, tracoma, conjuntivite',['Micoses','Tracoma','Conjuntivite']),
   ('Geo-helmintos','ancilostomíase e outras helmintíases',['Ancilostomíase','Outras helmintíases'])]
drsai={}; gm={}; gy={g[0]:[0,0,0] for g in G}
for k,c in CODE.items():
    t=tab(S['drs_'+k]); m=NM[c]
    drsai[m]=[t.get('TOTAL',{}).get(y,0) for y in YRS]
    gm[m]={g[0]:0 for g in G}
    for row,v in t.items():
        if not row.startswith('..') or row.startswith('....'): continue
        name=row.lstrip('. ')
        for g,_,keys in G:
            if any(name.startswith(x) for x in keys):
                gm[m][g]+=sum(v.get(y,0) for y in YRS)
                for j,y in enumerate(YRS): gy[g][j]+=v.get(y,0)
    assert sum(gm[m].values())==sum(drsai[m]), (m,gm[m],drsai[m])
resp=permun(tab(S['resp'])); allint=permun(tab(S['all'])); asma=permun(tab(S['asma']))
deng=permun(tab(S['dengue']))
def mon(key):
    t=tab(S[key]); out=[]
    for row,v in t.items():
        r=row.lstrip('.')
        if '/' in r and r.split('/')[1] in YRS: out.append([r, v['Internações']])
    return out
MESES=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
def byyearmonth(key):
    acc={y:[0]*12 for y in YRS}
    for r,v in mon(key): mm,yy=r.split('/'); acc[yy][MESES.index(mm)]+=v
    return acc
def bymonth(key):
    acc=[0]*12
    for r,v in mon(key): acc[MESES.index(r.split('/')[0])]+=v
    return [round(x/3,1) for x in acc]
M=[]
for m in NM.values():
    P=pop[m]; a=agg[m]
    M.append(dict(mun=m,pop=P,
      drsai=round(sum(drsai[m])/3,1), drsai_tx=round(sum(drsai[m])/3/P*1e4,2),
      resp=round(sum(resp[m])/3,1), resp_tx=round(sum(resp[m])/3/P*1e4,1),
      asma=round(sum(asma[m])/3,1), asma_tx=round(sum(asma[m])/3/P*1e4,1),
      deng=round(sum(deng[m])/3,1), deng_tx=round(sum(deng[m])/3/P*1e5,0),
      allint=round(sum(allint[m])/3,1), drsai_pct=round(100*sum(drsai[m])/sum(allint[m]),2),
      anos_drsai=drsai[m], anos_resp=resp[m], anos_deng=deng[m], anos_asma=asma[m], anos_all=allint[m],
      grupos=gm[m],
      esgoto=round(a['esg']/a['w'],1), agua=round(a['agua']/a['w'],1), lixo=round(a['lixo']/a['w'],1)))
TOT=dict(pop=sum(pop.values()))
for k in ('drsai','resp','asma','deng','allint'): TOT[k]=round(sum(x[k] for x in M),1)
TOT['drsai_tx']=round(TOT['drsai']/TOT['pop']*1e4,2); TOT['resp_tx']=round(TOT['resp']/TOT['pop']*1e4,1); TOT['asma_tx']=round(TOT['asma']/TOT['pop']*1e4,1); TOT['deng_tx']=round(TOT['deng']/TOT['pop']*1e5,0); TOT['drsai_pct']=round(100*TOT['drsai']/TOT['allint'],2)
GR={g:sum(gm[m][g] for m in gm) for g,_,_ in G}
TOT['anos']={k:[sum(src[m][j] for m in src) for j in range(3)] for k,src in (('drsai',drsai),('resp',resp),('asma',asma),('deng',deng),('all',allint))}
OUT=dict(gy=gy,mes_ano_resp=byyearmonth('respmes'),mes_ano_drsai=byyearmonth('drsmes'),mun=M,tot=TOT,grupos=[[g,d,GR[g]] for g,d,_ in G],mes_resp=bymonth('respmes'),mes_drsai=bymonth('drsmes'),anos=YRS)
json.dump(OUT,open('saude.json','w'),ensure_ascii=False)
for x in M: print(x['mun'][:12],x['pop'],x['drsai_tx'],x['resp_tx'],x['asma_tx'],x['deng_tx'],x['drsai_pct'],x['esgoto'])
print(TOT); print(GR); print(OUT['mes_resp']); print(OUT['mes_drsai'])
