# Série histórica municipal (Censos 1991, 2000, 2010, 2022) a partir das tabelas do SIDRA/IBGE
# Entrada: sidra_serie_historica_rmvrc.json (consulta à API de agregados v3 do IBGE, com URL de cada tabela)
# Saída: hist.json (contagens por município e ano) e serie_historica_municipios.csv (dados abertos)
import json, csv
D='./'
o=json.load(open(D+'sidra_serie_historica_rmvrc.json'))
R={}
for k,c,m,p,v in o['rows']:
    R[(k,c,m,p)]=0 if v in ('-',) else int(round(float(v))) if k!='alf22t' else float(v)
MUN={'5103403':'Cuiabá','5108402':'Várzea Grande','5100102':'Acorizal','5102678':'Campo Verde','5103007':'Chapada dos Guimarães','5106109':'Nossa Senhora do Livramento','5107800':'Santo Antônio de Leverger'}
Y=['1991','2000','2010','2022']
g=lambda *a: R[a]
out={}
for m,nome in MUN.items():
    r={}
    r['pop']=[g('pop','1:0|2:0',m,y) for y in Y[:3]]+[g('pop22','1:6795',m,'2022')]
    r['popu']=[g('pop','1:1|2:0',m,y) for y in Y[:3]]+[g('pop22','1:1',m,'2022')]
    r['dom']=[g('agua91','1:0|61:0',m,'1991'),g('agua00','1:0|11557:0|61:0',m,'2000'),g('agua10','61:0|299:0|67:0|309:0',m,'2010'),g('agua22','301:72053|1817:72125',m,'2022')]
    r['agua']=[g('agua91','1:0|61:1033',m,'1991')+g('agua91','1:0|61:1035',m,'1991'),g('agua00','1:0|11557:0|61:92853',m,'2000'),g('agua10','61:92853|299:0|67:0|309:0',m,'2010'),g('agua22','301:31471|1817:72125',m,'2022')]
    r['esg']=[sum(g('esg91','1:0|1612:'+c,m,'1991') for c in ['120451','120460','120453','120462']),g('esg00','1:0|11557:0|11558:92855',m,'2000'),g('esg10p','299:10941',m,'2010'),g('esg22','11558:72110',m,'2022')]
    r['esg91_rede']=g('esg91','1:0|1612:120451',m,'1991')+g('esg91','1:0|1612:120460',m,'1991')
    r['esg22_fossa']=g('esg22','11558:46290',m,'2022')
    r['lixo']=[g('lixo91','1:0|67:2520',m,'1991'),g('lixo00','1:0|11557:0|67:2520',m,'2000'),g('lixo10','61:0|299:0|67:2520|309:0',m,'2010'),g('lixo22','67:2520',m,'2022')]
    A=[];T=[]
    for y in ['1991','2000']:
        T.append(g('alf9100','59:0|58:0',m,y)-g('alf9100','59:0|58:1141',m,y)-g('alf9100','59:0|58:1142',m,y))
        A.append(g('alf9100','59:1023|58:0',m,y)-g('alf9100','59:1023|58:1141',m,y)-g('alf9100','59:1023|58:1142',m,y))
    T.append(g('alf10','86:0|59:93024|1:0|287:0',m,'2010')-sum(g('alf10','86:0|59:93024|1:0|287:'+c,m,'2010') for c in ['7817','2659','93085']))
    A.append(g('alf10','86:0|59:1023|1:0|287:0',m,'2010')-sum(g('alf10','86:0|59:1023|1:0|287:'+c,m,'2010') for c in ['7817','2659','93085']))
    T.append(g('alf22','59:93024|2:6794|86:95251|287:100362',m,'2022')); A.append(g('alf22','59:1023|2:6794|86:95251|287:100362',m,'2022'))
    r['p15']=T; r['alf']=A
    # conferências
    for y,t in [(0,g('esg91','1:0|1612:0',m,'1991')),(2,g('esg10p','299:2942',m,'2010')),(3,g('esg22','11558:46292',m,'2022')),(3,g('lixo22','67:10972',m,'2022')),(0,g('lixo91','1:0|67:0',m,'1991')),(1,g('esg00','1:0|11557:0|11558:0',m,'2000')),(2,g('lixo10','61:0|299:0|67:0|309:0',m,'2010'))]:
        assert t==r['dom'][y],(nome,y)
    assert abs(100*A[3]/T[3]-g('alf22t','2:6794|86:95251|287:100362',m,'2022'))<0.01, nome
    out[nome]=r
# tabelas de origem (para citar e conferir)
TAB={'pop':{'1991':202,'2000':202,'2010':202,'2022':9923},'dom':{'1991':179,'2000':1442,'2010':3218,'2022':6804},
     'agua':{'1991':179,'2000':1442,'2010':3218,'2022':6804},'esg':{'1991':180,'2000':1444,'2010':3154,'2022':6805},
     'lixo':{'1991':182,'2000':1447,'2010':3218,'2022':6892},'alf':{'1991':204,'2000':204,'2010':1379,'2022':9542}}
H={'anos':[1991,2000,2010,2022],'mun':out,'tab':TAB,'consulta':o['consultado_em'][:10]}
json.dump(H,open(D+'hist.json','w'),ensure_ascii=False,separators=(',',':'))
# CSV aberto
with open(D+'serie_historica_municipios.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['municipio','codigo_ibge','ano','populacao','populacao_urbana','taxa_urbanizacao_pct','domicilios','dom_agua_rede','agua_rede_pct','dom_esgoto_rede_ou_pluvial','esgoto_rede_pct','dom_lixo_coletado','lixo_coletado_pct','pessoas_15mais','alfabetizadas_15mais','alfabetizacao_15mais_pct','tabelas_sidra'])
    cod={v:k for k,v in MUN.items()}
    for nome,r in out.items():
        for i,y in enumerate(Y):
            pc=lambda a,b: round(100*a/b,1)
            w.writerow([nome,cod[nome],y,r['pop'][i],r['popu'][i],pc(r['popu'][i],r['pop'][i]),r['dom'][i],r['agua'][i],pc(r['agua'][i],r['dom'][i]),r['esg'][i],pc(r['esg'][i],r['dom'][i]),r['lixo'][i],pc(r['lixo'][i],r['dom'][i]),r['p15'][i],r['alf'][i],pc(r['alf'][i],r['p15'][i]),
                        ' '.join(sorted({str(TAB[k][y]) for k in TAB}, key=int))])
print('ok', len(json.dumps(H)))
