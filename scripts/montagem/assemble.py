import json, re
L=open('../atlas_orig.html').read().split('\n')
def js(i,pref): return json.loads(L[i][len(pref):].rstrip().rstrip(';'))
DATA=js(510,'<script>const DATA = '); HIDRO=js(511,'const HIDRO = '); EQUIP=js(512,'const EQUIP = ')
S1=json.load(open('stage1.json')); APP=json.load(open('app_new.json')); HN=json.load(open('hidro_new.json'))
for f in S1['NEWF']:
    p=f['properties']; a=APP.get(p['id'])
    if a is not None: p['app_pct']=a; p['app_pop']=int(round(p['pop']*a/100))
    p['cob']=0  # sem camadas de satelite/modelo
def sa(r):
    return sum(r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1] for i in range(len(r)-1))/2
def rewind_poly(poly):
    out=[]
    for j,r in enumerate(poly):
        a=sa(r)
        if (j==0 and a>0) or (j>0 and a<0): r=r[::-1]
        out.append(r)
    return out
def rewind(g):
    if g['type']=='Polygon': g['coordinates']=rewind_poly(g['coordinates'])
    elif g['type']=='MultiPolygon': g['coordinates']=[rewind_poly(p) for p in g['coordinates']]
# checa convencao do original
o=[f for f in HIDRO['features'] if f['geometry']['type']=='Polygon'][0]['geometry']['coordinates'][0]
print('orig area sign',sa(o))
for f in HN:
    if f['geometry']['type'] in ('Polygon','MultiPolygon'): rewind(f['geometry'])
for f in S1['MUN']['features']: rewind(f['geometry'])
for f in S1['NEWF']: rewind(f['geometry'])
RES=json.load(open('/home/claude/f/resultado.json'))
for f in DATA['features']:
    f['properties'].update(RES['per'].get(f['properties']['id'],{}))
for f in S1['NEWF']:
    for k in ('sgb_alta','sgb_alta_pop','sgb_am','a1974','a1974_pop','aalerta'): f['properties'][k]=None
_veg=json.load(open('/home/claude/g/veg.json')); _ero=json.load(open('/home/claude/g/ero_per.json')); _bac=json.load(open('/home/claude/g/bacias_out.json')); _mic=json.load(open('/home/claude/g/micro_out.json'))
for f in DATA['features']+S1['NEWF']:
    _i=f['properties']['id']; f['properties']['veg_nat']=_veg.get(_i)
    _e=_ero.get(_i,{}); f['properties']['erosao']=_e.get('erosao'); f['properties']['eros_alta']=_e.get('eros_alta'); f['properties']['solo']=_e.get('solo','')
    f['properties']['micro']=_mic['per'].get(_i,'')
    f['properties']['bac']=_bac['per_bacias'].get(_i,''); f['properties']['subbac']=_bac['per_sub'].get(_i,'')
FEAT=DATA['features']+S1['NEWF']
ORD=['Cuiabá','Várzea Grande','Nossa Senhora do Livramento','Santo Antônio de Leverger','Acorizal','Chapada dos Guimarães','Campo Verde']
DATA['features']=FEAT
HIDRO['features']+=HN
EQ=EQUIP+S1['NEWEQ']
_seen=set(); _eq=[]
for _e in EQ:
    _k=(_e['c'],round(_e['x'],4),round(_e['y'],4))
    if _k in _seen: continue
    _seen.add(_k); _eq.append(_e)
EQ=_eq
def _cent(g):
    _ps=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']; A=cx=cy=0
    for _p in _ps:
        r=_p[0]
        for i in range(len(r)-1):
            x0,y0=r[i];x1,y1=r[i+1];c=x0*y1-x1*y0;A+=c;cx+=(x0+x1)*c;cy+=(y0+y1)*c
    return (cx/(3*A),cy/(3*A))
def _hav(a,b):
    import math as _m
    R_=6371008.8; la1,la2=_m.radians(a[1]),_m.radians(b[1]); dl=_m.radians(b[0]-a[0])
    return 2*R_*_m.asin(_m.sqrt(_m.sin((la2-la1)/2)**2+_m.cos(la1)*_m.cos(la2)*_m.sin(dl/2)**2))
_cat={'d_ubs':['ubs'],'d_saude':['upa','hosp'],'d_esc':['esc'],'d_parque':['parque','uc']}
_pts={k:[(e['x'],e['y']) for e in EQ if e['c'] in v] for k,v in _cat.items()}
_upd=0
for _f in FEAT:
    _c=_cent(_f['geometry'])
    for k,pts in _pts.items():
        d=int(round(min(_hav(_c,q) for q in pts)/10)*10); old=_f['properties'].get(k)
        if old is None or d<old-200: _f['properties'][k]=d; _upd+=1
print('distancias atualizadas',_upd)
MUN=S1['MUN']
dumps=lambda o: json.dumps(o,ensure_ascii=False,separators=(',',':'))
L[510]='<script>const DATA = '+dumps(DATA)+';'
L[511]='const HIDRO = '+dumps(HIDRO)+';'
L[512]='const EQUIP = '+dumps(EQ)+';'
L[513]='const MUN = '+dumps(MUN)+';'
H='\n'.join(L)
NSET=len(FEAT); NPOP=sum(f['properties']['pop'] for f in FEAT)
def fmt(n): return f'{n:,}'.replace(',','.')
print('setores',NSET,'pop',NPOP)

cnt={}
def rep(old,new,n=1):
    global H
    c=H.count(old)
    assert c>=1, ('NAO ACHEI',old[:90])
    if n and c!=n: raise AssertionError(('contagem',c,n,old[:90]))
    H=H.replace(old,new)
LOGO=open('../logo.b64').read()

# ---------------- CSS: identidade PPGAU-UNIVAG ----------------
rep('<title>Atlas Socioambiental Cuiabá–VG</title>','<title>Atlas Socioambiental RMVRC</title>')
rep('family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Source+Sans+3','family=Montserrat:wght@500;600;700;800&family=Source+Sans+3')
rep('''  --bg:#ecefe9; --panel:#fbfcf9; --panel-2:#f3f6f1; --fg:#14221f; --muted:#56665f; --line:#d4dcd4;
  --accent:#0b6b5a; --accent-soft:#d5ebe3; --ochre:#a8661c; --nodata:#c9cfca; --hover:#111;''',
'''  --bg:#f2f4f8; --panel:#ffffff; --panel-2:#f1f4fa; --fg:#0f1d3a; --muted:#56607a; --line:#d9dfeb;
  --accent:#002060; --accent-soft:#e3e9f6; --ochre:#9a6f00; --gold:#ffc000; --navy:#002060; --nodata:#cdd3de; --hover:#111;''')
rep('''  --hero-bg:#0d2628; --hero-bg2:#123a3a; --hero-fg:#edf4f0; --hero-muted:#a3bcb4; --hero-line:rgba(237,244,240,.14); --hero-river:#49b3d6; --hero-ochre:#e0a257;
  --shadow:0 1px 2px rgba(20,34,31,.06),0 6px 20px rgba(20,34,31,.07);
  --f-display:"Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;''',
'''  --hero-bg:#001640; --hero-bg2:#0b3585; --hero-fg:#ffffff; --hero-muted:#bfcbe6; --hero-line:rgba(255,255,255,.16); --hero-river:#7fc4ff; --hero-ochre:#ffc000;
  --shadow:0 1px 2px rgba(0,32,96,.06),0 6px 20px rgba(0,32,96,.08);
  --f-display:"Montserrat", "Segoe UI", system-ui, sans-serif;''')
dark_old='''  --bg:#0c1311; --panel:#141d1a; --panel-2:#18231f; --fg:#e4ebe7; --muted:#95a59e; --line:#28352f;
  --accent:#4fc2a5; --accent-soft:#193831; --ochre:#e0a257; --nodata:#3a4541; --hover:#fff; --water:#23506f; --water-line:#6fb3e8; --water-text:#9fd0f5;'''
dark_new='''  --bg:#060e20; --panel:#0d1830; --panel-2:#12203d; --fg:#e8edf7; --muted:#9aa6c2; --line:#233253;
  --accent:#ffc000; --accent-soft:#2e2a14; --ochre:#ffc000; --gold:#ffc000; --navy:#8fb0f0; --nodata:#34405a; --hover:#fff; --water:#1f4a70; --water-line:#6fb3e8; --water-text:#9fd0f5;'''
rep(dark_old,dark_new,2)
rep('--men:#7ea6d4; --women:#e08aa2; --hero-bg:#081716; --hero-bg2:#0e2a29;','--men:#7ea6d4; --women:#e08aa2; --hero-bg:#000c26; --hero-bg2:#082a6b;',2)

extra_css='''
/* ---- identidade PPGAU-UNIVAG ---- */
.hero::before{content:"";position:absolute;inset:0 0 auto 0;height:5px;background:var(--gold)}
.hero::after{content:"";position:absolute;inset:auto 0 0 0;height:3px;background:var(--gold);opacity:.9}
.inst{display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px;margin-bottom:6px}
.inst .logo{display:inline-flex;background:#fff;border-radius:12px;padding:8px 14px;box-shadow:0 6px 24px rgba(0,0,0,.25)}
.inst .logo img{height:58px;width:auto;display:block}
.inst .itx{font:600 13px/1.5 var(--f-body);color:var(--hero-muted)}
.inst .itx .nw{white-space:nowrap}
@media (max-width:560px){.inst .itx .nw{white-space:normal}}
.inst .itx a{color:var(--hero-fg);text-decoration:none;border-bottom:1px solid var(--gold)}
.inst .itx a:hover{color:var(--gold)}
.hero h1{font-weight:800;letter-spacing:-.03em}
.hero h1 .gold{color:var(--gold)}
.hero-in{grid-template-columns:minmax(0,1fr)}
.credits{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));gap:10px 28px;max-width:1100px;margin-top:4px;padding:14px 0 0;border-top:1px solid var(--hero-line)}
.credits .ck{font:700 10.5px var(--f-body);letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:3px}
.credits .cv{font:600 14.5px/1.4 var(--f-body);color:var(--hero-fg)}
.credits .cv,.credits .ck{text-shadow:0 0 6px #001640,0 0 14px #001640}.credits .cv.ptit{font-style:italic}.credits .cv.ptit span{font-style:normal;margin-top:3px}
.credits .cv span{display:block;font-weight:400;color:var(--hero-muted);font-size:13px}
.bar{border-bottom:3px solid var(--gold)}
.bar .brand{font-weight:800}
.bar .brand i{color:var(--ochre)}
.bar .brand small{font:700 10.5px var(--f-body);letter-spacing:.1em;color:var(--muted);margin-left:6px;text-transform:uppercase}
select.munsel{font:600 13px var(--f-body);padding:7px 30px 7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--panel) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2356607a'/%3E%3C/svg%3E") right 10px center/10px no-repeat;color:var(--fg);appearance:none;-webkit-appearance:none;max-width:100%;cursor:pointer}
.sec-h .kick{color:var(--ochre)}
.sec-h h2{font-weight:800}
.sec-h h2::after{content:"";display:block;width:56px;height:4px;background:var(--gold);border-radius:2px;margin-top:10px}
.cobnote{font-size:11.5px;color:var(--muted);background:var(--panel-2);border:1px dashed var(--line);border-radius:8px;padding:6px 9px;margin:4px 0 8px;line-height:1.35}
.about{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:28px;align-items:start}
@media (max-width:900px){.about{grid-template-columns:minmax(0,1fr)}}
.about h3{font:800 12px var(--f-display);letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0 0 10px}
.about p{margin:0 0 10px;max-width:70ch}
.people{display:grid;gap:10px}
.person{display:grid;grid-template-columns:46px minmax(0,1fr);gap:12px;align-items:center;border:1px solid var(--line);border-radius:12px;padding:10px 12px;background:var(--panel-2)}
.person .av{width:46px;height:46px;border-radius:50%;background:var(--navy);color:var(--gold);display:grid;place-items:center;font:800 15px var(--f-display)}
:root[data-theme="dark"] .person .av{background:#0b3585}
.person b{display:block;font:700 15px var(--f-display);color:var(--fg)}
.person span{font-size:13px;color:var(--muted)}
.cite{font:13px/1.5 var(--f-body);background:var(--panel-2);border-left:4px solid var(--gold);border-radius:0 10px 10px 0;padding:10px 14px;margin-top:10px}
.mtab{width:100%;border-collapse:collapse;font-size:13px}
.mtab th,.mtab td{padding:5px 8px;border-bottom:1px solid var(--line);text-align:right}
.mtab th:first-child,.mtab td:first-child{text-align:left}
.mtab th{color:var(--muted);font-size:12px;font-weight:700}
.pbadge{display:inline-block;font:700 10.5px var(--f-body);letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:99px;background:var(--navy);color:#fff}
.pbadge.g{background:var(--gold);color:#1a1400}
footer .inst-f{display:flex;align-items:center;gap:10px}
footer .inst-f img{height:34px;width:auto;background:#fff;border-radius:6px;padding:3px 6px}
footer a{color:var(--accent)}
.bar nav a{padding:6px 7px}
.bar .search input{width:190px}
@media (max-width:1560px){.bar .brand small{display:none}}
@media (max-width:1320px){.bar .brand{display:none}}
'''
rep('@media (prefers-reduced-motion:reduce){*{transition:none!important}}','@media (prefers-reduced-motion:reduce){*{transition:none!important}}'+extra_css)

# ---------------- HERO ----------------
old_hero_start=H.index('    <div class="eyebrow">Instituto ANAP')
old_hero_end=H.index('    <div class="kpis" id="kpis"></div>')
new_hero=f'''    <div class="inst">
      <a class="logo" href="https://www.univag-ppgau.com/" target="_blank" rel="noopener" aria-label="PPGAU-UNIVAG — site do programa"><img alt="PPGAU — Programa de Pós-Graduação Stricto Sensu em Arquitetura e Urbanismo" src="data:image/webp;base64,{LOGO}"></a>
      <div class="itx"><span class="nw">Programa de Pós-Graduação <i>Stricto Sensu</i> em Arquitetura e Urbanismo</span><br><a class="nw" href="https://www.univag-ppgau.com/" target="_blank" rel="noopener">PPGAU · UNIVAG — Centro Universitário de Várzea Grande</a></div>
    </div>
    <div class="eyebrow">Censo IBGE 2022 · {fmt(NSET)} setores censitários · 7 municípios</div>
    <h1>Região Metropolitana do <span class="gold">Vale do Rio Cuiabá</span><small>Atlas Socioambiental da RMVRC</small></h1>
    <p class="lede">Quem mora onde, com que saneamento, renda, verde e calor, e quem vive perto dos rios e das áreas que alagam, nos sete municípios do núcleo metropolitano: Cuiabá, Várzea Grande, Nossa Senhora do Livramento, Santo Antônio de Leverger, Acorizal, Chapada dos Guimarães e Campo Verde. <b>Escolha um indicador, clique num setor</b> e ajuste com a equipe os pesos do índice de vulnerabilidade.</p>
    <div class="credits">
      <div><div class="ck">Elaboração</div><div class="cv">Prof. Dr. Ricardo Miranda dos Santos<br>Profa. Dra. Sandra Medina Benini</div></div>
      <div><div class="ck">Pesquisa de Pós-Doutorado · 2025–2026</div><div class="cv ptit">“Indicadores ambientais como ferramenta para a sustentabilidade urbana: estudo de caso na Região Metropolitana do Vale do Rio Cuiabá (RMVRC)”<span>Resultado da pesquisa de Pós-Doutorado do Prof. Dr. Ricardo Miranda dos Santos, supervisionada pela Profa. Dra. Sandra Medina Benini, docente do PPGAU-UNIVAG</span></div></div>
    </div>
'''
H=H[:old_hero_start]+new_hero+H[old_hero_end:]

# ---------------- barra ----------------
rep('<span class="brand">Atlas <i>Cuiabá–VG</i></span>','<span class="brand">Atlas <i>RMVRC</i><small>PPGAU · UNIVAG</small></span>')
opts=''.join(f'<option value="{m}">{m}</option>' for m in ORD)
rep('''    <div class="seg" role="group" aria-label="Município">
      <button id="m-all" data-m="all" aria-pressed="true">Conurbação</button>
      <button id="m-cba" data-m="Cuiabá" aria-pressed="false">Cuiabá</button>
      <button id="m-vg" data-m="Várzea Grande" aria-pressed="false">Várzea Grande</button>
    </div>''',f'''    <select id="munsel" class="munsel" aria-label="Município"><option value="all">RMVRC · 7 municípios</option><option value="conurb">Conurbação Cuiabá–VG</option>{opts}</select>''')
rep('<a href="#metodo">Método</a></nav>','<a href="#metodo">Método</a><a href="#sobre">Sobre</a></nav>')

# ---------------- camadas: nota de cobertura ----------------
rep('<div class="grp-t">Fundo do mapa</div>','<div class="grp-t">Fundo do mapa</div>\n      <div class="cobnote">Vegetação, temperatura, inundação, cheias, setores de risco e FCU cobrem a conurbação Cuiabá–Várzea Grande. APP e rede hídrica cobrem também as sedes dos demais municípios.</div>')

# ---------------- secao validacao: recorte ----------------
rep('<span class="kick">Controle de qualidade</span><h2>Validação da mancha de inundação</h2>','<span class="kick">Controle de qualidade · conurbação Cuiabá–Várzea Grande</span><h2>Validação da mancha de inundação</h2>')

# ---------------- metodo: fontes ----------------
rep('<li>Malha: <code>MT_setores_CD2022</code> (malha com atributos, IBGE).</li>','<li>Recorte: núcleo da Região Metropolitana do Vale do Rio Cuiabá, com os sete municípios definidos pelas Leis Complementares Estaduais 359/2009 (Cuiabá, Várzea Grande, Nossa Senhora do Livramento e Santo Antônio de Leverger), 577/2016 (Acorizal e Chapada dos Guimarães) e 796/2024 (Campo Verde). O entorno metropolitano (Barão de Melgaço, Jangada, Nobres, Nova Brasilândia, Planalto da Serra, Poconé e Rosário Oeste) não está incluído.</li>\n      <li>Malha: <code>MT_setores_CD2022</code> (malha com atributos, IBGE).</li>')
rep('<li>Divisa municipal: malha municipal do IBGE (API de malhas, qualidade máxima).</li>','<li>Divisa municipal: malha municipal do IBGE (API de malhas, qualidade máxima, simplificada a ≈20 m).</li>\n      <li>Ampliação para a RMVRC (30/09/2026): mesmos agregados e mesmas fórmulas; os indicadores de Cuiabá e Várzea Grande foram recalculados e conferem com a versão anterior. Rede hídrica dos novos municípios pelo OpenStreetMap (rios em toda a região; córregos, canais e lagoas nas sedes e distritos urbanos). Equipamentos de saúde pelo CNES (API de dados abertos do Ministério da Saúde) e escolas e praças pelo OpenStreetMap.</li>\n      <li>Normalização do IVSA: percentis 2 e 98 calculados sobre todos os setores da RMVRC com 50 ou mais moradores; por isso os valores de Cuiabá e Várzea Grande podem diferir levemente da versão só da conurbação.</li>')
rep('<p>Extração em 29/09/2026 a partir de ftp.ibge.gov.br.</p>','<p>Extração em 29/09/2026 (Cuiabá–VG) e 30/09/2026 (demais municípios) a partir de ftp.ibge.gov.br.</p>')
rep('<li><span class="status next">próximo</span>Obter a mancha oficial','<li><span class="status ok">feito</span>Ampliação para os 7 municípios do núcleo da RMVRC (indicadores censitários, APP, acesso a serviços)</li>\n      <li><span class="status next">próximo</span>Estender NDVI, temperatura de superfície e modelo HAND aos municípios fora da conurbação</li>\n      <li><span class="status next">próximo</span>Obter a mancha oficial')
rep('<li><b>APP</b>: faixas do Código Florestal','<li><b>Cobertura</b>: vegetação, temperatura, suscetibilidade a inundação, cheias do Rio Cuiabá, setores de risco do SGB e FCU existem apenas para Cuiabá e Várzea Grande. Nos demais municípios esses campos ficam sem dado e não entram no IVSA.</li>\n      <li><b>APP</b>: faixas do Código Florestal')
rep('<li><b>Moradores em APP ou em área de inundação</b>:','<li><b>APP nos novos municípios</b>: calculada só para setores urbanos (sedes e distritos), com as mesmas faixas, em grade de 5 m; nos setores rurais extensos a rede de córregos do OpenStreetMap é incompleta e o campo fica sem dado.</li>\n      <li><b>Moradores em APP ou em área de inundação</b>:')

# ---------------- secao Sobre + rodape ----------------
about=f'''<div class="sec-h" id="sobre" style="scroll-margin-top:calc(var(--tb) + 12px)"><span class="kick">Ficha técnica</span><h2>Sobre o Atlas</h2><p>Produto de pesquisa vinculado ao Programa de Pós-Graduação <i>Stricto Sensu</i> em Arquitetura e Urbanismo do Centro Universitário de Várzea Grande (PPGAU-UNIVAG).</p></div>
<section class="block">
  <div class="about">
    <div>
      <h3>Apresentação</h3>
      <p>O <b>Atlas Socioambiental da Região Metropolitana do Vale do Rio Cuiabá</b> reúne, na escala do setor censitário, indicadores demográficos, de saneamento, renda, entorno urbano, ambiente e acesso a serviços para os sete municípios do núcleo metropolitano. Ele integra dados do Censo Demográfico 2022 do IBGE a camadas de sensoriamento remoto, hidrografia e equipamentos públicos, e propõe um Índice de Vulnerabilidade Socioambiental (IVSA) com pesos ajustáveis, construído de forma colaborativa.</p>
      <p>Este Atlas é resultado da pesquisa de Pós-Doutorado do <b>Prof. Dr. Ricardo Miranda dos Santos</b>, intitulada <i>“Indicadores ambientais como ferramenta para a sustentabilidade urbana: estudo de caso na Região Metropolitana do Vale do Rio Cuiabá (RMVRC)”</i>, desenvolvida no PPGAU-UNIVAG no período de <b>2025 a 2026</b>, sob a supervisão da <b>Profa. Dra. Sandra Medina Benini</b>, docente do Programa.</p>
      <h3 style="margin-top:16px">Recorte territorial</h3>
      <table class="mtab"><thead><tr><th>Município</th><th>Lei (RMVRC)</th><th>Setores</th><th>Moradores</th></tr></thead><tbody>{''.join(f"<tr><td>{m}</td><td>{'LC 359/2009' if m in ORD[:4] else ('LC 577/2016' if m in ORD[4:6] else 'LC 796/2024')}</td><td class='num'>{fmt(sum(1 for f in FEAT if f['properties']['mun']==m))}</td><td class='num'>{fmt(sum(f['properties']['pop'] for f in FEAT if f['properties']['mun']==m))}</td></tr>" for m in ORD)}<tr style="font-weight:700"><td>RMVRC (núcleo)</td><td></td><td class='num'>{fmt(NSET)}</td><td class='num'>{fmt(NPOP)}</td></tr></tbody></table>
    </div>
    <div>
      <h3>Elaboração</h3>
      <div class="people">
        <div class="person"><div class="av">RM</div><div><b>Prof. Dr. Ricardo Miranda dos Santos</b><span>Pesquisador de Pós-Doutorado · PPGAU-UNIVAG (2025–2026)</span></div></div>
        <div class="person"><div class="av">SB</div><div><b>Profa. Dra. Sandra Medina Benini</b><span>Supervisora da pesquisa de Pós-Doutorado · Docente do PPGAU-UNIVAG</span></div></div>
      </div>
      <h3 style="margin-top:16px">Vínculo institucional</h3>
      <p><span class="pbadge">PPGAU</span> <span class="pbadge g">UNIVAG</span></p>
      <p>Programa de Pós-Graduação <i>Stricto Sensu</i> em Arquitetura e Urbanismo · Centro Universitário de Várzea Grande · <a href="https://www.univag-ppgau.com/" target="_blank" rel="noopener">www.univag-ppgau.com</a></p>
      <h3 style="margin-top:16px">Como citar</h3>
      <div class="cite">SANTOS, Ricardo Miranda dos; BENINI, Sandra Medina. <b>Atlas Socioambiental da Região Metropolitana do Vale do Rio Cuiabá (RMVRC)</b>. Várzea Grande: PPGAU-UNIVAG, 2026. Atlas digital interativo. Resultado da pesquisa de Pós-Doutorado “Indicadores ambientais como ferramenta para a sustentabilidade urbana: estudo de caso na Região Metropolitana do Vale do Rio Cuiabá (RMVRC)” (2025–2026).</div>
    </div>
  </div>
</section>
'''
rep('<footer><span>Fontes:',about+'<footer><span class="inst-f"><img alt="PPGAU-UNIVAG" src="data:image/webp;base64,'+LOGO+'"><span>© 2026 PPGAU-UNIVAG · Elaboração: Prof. Dr. Ricardo Miranda dos Santos e Profa. Dra. Sandra Medina Benini · Pós-Doutorado 2025–2026</span></span><span>Fontes:')
rep('Landsat 9 (USGS, via Microsoft Planetary Computer). Elaboração: Instituto ANAP.</span><span>Versão de 29/09/2026</span>','Landsat 9 (USGS, via Microsoft Planetary Computer).</span><span>Versão de 30/09/2026</span>')

# ---------------- JS ----------------
js_start=H.index('<script>\n(function(){')
head,body=H[:js_start],H[js_start:]
def jrep(old,new,n=1):
    global body
    c=body.count(old); assert c>=1,('JS NAO ACHEI',old[:90])
    if n and c!=n: raise AssertionError(('JS contagem',c,n,old[:90]))
    body=body.replace(old,new)
jrep("localStorage.getItem('atlas-cvg')","localStorage.getItem('atlas-rmvrc')")
jrep("localStorage.setItem('atlas-cvg',","localStorage.setItem('atlas-rmvrc',")
jrep("'atlas-cvg-w'","'atlas-rmvrc-w'",2)
jrep("'atlas-cvg-opa'","'atlas-rmvrc-opa'",3)
jrep("const st = {ind:'ivsa', mun:'all',","const CONURB=['Cuiabá','Várzea Grande'];\nconst MUNS=MUN.features.map(m=>m.properties.nome);\nconst inSel=m=>st.mun==='all'||(st.mun==='conurb'?CONURB.includes(m):m===st.mun);\nconst st = {ind:'ivsa', mun:'all',")
jrep("function visible(){ return F.filter(f=>(st.mun==='all'||f.properties.mun===st.mun)&&","function visible(){ return F.filter(f=>inSel(f.properties.mun)&&")
# projecao: permite afastar ate a RMVRC inteira
jrep("const zoom = d3.zoom().scaleExtent([.4,40])","const zoom = d3.zoom().scaleExtent([.04,60])")
jrep("const k=Math.min(40,.92/Math.max(dx/W,dy/H));","const k=Math.min(60,.92/Math.max(dx/W,dy/H));")
# rotulos de municipio: sede = maior aglomerado urbano
jrep("const munLab = gM.selectAll('text').data(MUN.features.map(m=>{ const fs=F.filter(f=>f.properties.mun===m.properties.nome&&f.properties.sit==='Urbana');",
     "const munLab = gM.selectAll('text').data(MUN.features.map(m=>{ let fs=F.filter(f=>f.properties.mun===m.properties.nome&&f.properties.sit==='Urbana'); const dm=d3.rollups(fs,v=>d3.sum(v,f=>f.properties.pop),f=>f.properties.dist).sort((a,b)=>b[1]-a[1])[0]; if(dm) fs=fs.filter(f=>f.properties.dist===dm[0]);")
jrep("return {n:m.properties.nome.toUpperCase(),x:c[0],y:c[1]}; }))","return {n:m.properties.nome.toUpperCase(),x:c[0],y:c[1],big:CONURB.includes(m.properties.nome)}; }))")
jrep("munLab.attr('font-size',18/k).attr('stroke-width',4/k); }","munLab.attr('font-size',d=>(d.big?18:13)/k).attr('stroke-width',4/k); }")
# APP vetorial nos novos municipios (fora do raster da conurbacao)
jrep("gA.append('image').attr('href',RAST.img.app)",
"""const upm=(()=>{ const c=proj.invert([W/2,H/2]), a=proj(c), b=proj([c[0],c[1]+0.001]); return Math.abs(b[1]-a[1])/111.32; })();
const outR=c=>!(c[0]>=RB[0]&&c[0]<=RB[2]&&c[1]<=RB[1]&&c[1]>=RB[3]);
const APPL=HIDRO.features.filter(f=>(f.properties.t==='r'||f.properties.t==='s')&&f.properties.app&&f.geometry.coordinates.some(outR));
gA.selectAll('path.appv').data(APPL).join('path').attr('d',path).attr('fill','none').attr('stroke','rgba(0,150,90,.55)').attr('stroke-linecap','round').attr('stroke-width',f=>2*f.properties.app*upm);
gA.selectAll('circle.appn').data(HIDRO.features.filter(f=>f.properties.t==='n'&&outR(f.geometry.coordinates))).join('circle').attr('cx',f=>proj(f.geometry.coordinates)[0]).attr('cy',f=>proj(f.geometry.coordinates)[1]).attr('r',50*upm).attr('fill','rgba(0,150,90,.55)');
gA.append('image').attr('href',RAST.img.app)""")
# comparativo municipal
old_cmp=body[body.index('function renderCmp(){'):body.index('// ------- ficha do setor -------')]
new_cmp='''function renderCmp(){
  const i=byK[st.ind], A=st.area==='all'?F:F.filter(f=>f.properties.sit==='Urbana');
  const rows=[['RMVRC',A], ...MUNS.map(m=>[m,A.filter(f=>f.properties.mun===m)])];
  const ab={'Nossa Senhora do Livramento':'N. Sra. do Livramento','Santo Antônio de Leverger':'Sto. Ant. de Leverger','Chapada dos Guimarães':'Chapada dos Guimarães'};
  const sec=i.k==='ivsa'?byK.renda:byK.ivsa;
  document.getElementById('cmp').innerHTML = `<tr><th>Município</th><th>${i.n.length>22?i.n.slice(0,21)+'…':i.n}</th><th>${sec.n.split(' ')[0]==='Renda'?'Renda':'IVSA'}</th></tr>` +
   rows.map(([n,fs],j)=>`<tr${j===0?' style="font-weight:700"':''}${n===st.mun||(st.mun==='conurb'&&CONURB.includes(n))?' style="background:var(--accent-soft)"':''}><td>${ab[n]||n}</td><td class="num">${fv(i.k,agg(fs,i))}</td><td class="num">${fv(sec.k,agg(fs,sec))}</td></tr>`).join('');
}
'''
body=body.replace(old_cmp,new_cmp)
# KPIs: indicar cobertura das camadas ambientais
jrep("'moradores, suscetibilidade alta', '#49b3d6'","'moradores, susc. alta (Cuiabá–VG)', '#49b3d6'")
jrep("'média em 13/08/2026, 10h45', '#e0a257'","'média 13/08/2026 (Cuiabá–VG)', '#ffc000'")
# tabela de equipamentos: municipio
jrep("const inMun = e=>{ if(st.mun==='all') return true; const m=MUN.features.find(m=>m.properties.nome===st.mun); return d3.geoContains(m,[e.x,e.y]); };",
     "const munOf = e=>{ const m=MUN.features.find(m=>d3.geoContains(m,[e.x,e.y])); return m?m.properties.nome:'—'; };\n    const inMun = e=>inSel(munOf(e));")
jrep("mun:d3.geoContains(MUN.features[0],[e.x,e.y])?'Cuiabá':(d3.geoContains(MUN.features[1],[e.x,e.y])?'Várzea Grande':'—')","mun:munOf(e)")
slug="(st.mun==='all'?'rmvrc':st.mun==='conurb'?'conurbacao_cuiaba_vg':st.mun.normalize('NFD').replace(/[^A-Za-z0-9]+/g,'_').toLowerCase())"
jrep("const tag = () => (st.mun==='all'?'conurbacao':st.mun==='Cuiabá'?'cuiaba':'varzea_grande')+","const tag = () => "+slug+"+")
jrep("_${st.mun==='all'?'conurbacao':st.mun==='Cuiabá'?'cuiaba':'varzea_grande'}`","_${"+slug+"}`")
jrep("${st.mun==='all'?'Conurbação Cuiabá–Várzea Grande':st.mun}","${st.mun==='all'?'Região Metropolitana do Vale do Rio Cuiabá (7 municípios)':st.mun==='conurb'?'Conurbação Cuiabá–Várzea Grande':st.mun}")
AUT='Elaboração: Prof. Dr. Ricardo Miranda dos Santos e Profa. Dra. Sandra Medina Benini · PPGAU-UNIVAG'
jrep("'ATLAS SOCIOAMBIENTAL · CUIABÁ E VÁRZEA GRANDE · INSTITUTO ANAP'","'ATLAS SOCIOAMBIENTAL DA RMVRC · PPGAU-UNIVAG'")
jrep("IVSA com os pesos em uso nesta página. Elaboração: Instituto ANAP. Mapa gerado em","IVSA com os pesos em uso nesta página. "+AUT+". Mapa gerado em")
jrep("para('ATLAS SOCIOAMBIENTAL · CUIABÁ E VÁRZEA GRANDE',{size:9,bold:true,color:'0.66 0.40 0.11',gap:2});",
     "para('ATLAS SOCIOAMBIENTAL DA REGIÃO METROPOLITANA DO VALE DO RIO CUIABÁ · PPGAU-UNIVAG',{size:9,bold:true,color:'0.00 0.13 0.38',gap:2});")
jrep("para(`Instituto ANAP · documento gerado em ${hoje()} · recorte: ${filtroTxt()}`,{size:9,color:'0.34 0.40 0.37',gap:10});",
     "para(`"+AUT+"`,{size:9.5,bold:true,color:'0.06 0.11 0.23',gap:2});\n  para('Resultado da pesquisa de Pós-Doutorado do Prof. Dr. Ricardo Miranda dos Santos, “Indicadores ambientais como ferramenta para a sustentabilidade urbana: estudo de caso na Região Metropolitana do Vale do Rio Cuiabá (RMVRC)” (2025–2026), supervisionada pela Profa. Dra. Sandra Medina Benini, docente do Programa de Pós-Graduação Stricto Sensu em Arquitetura e Urbanismo do Centro Universitário de Várzea Grande (PPGAU-UNIVAG).',{size:9,color:'0.34 0.38 0.48',gap:2});\n  para(`Documento gerado em ${hoje()} · recorte: ${filtroTxt()}`,{size:9,color:'0.34 0.38 0.48',gap:10});")
jrep("ops.push(`0.66 0.40 0.11 RG 1 w","ops.push(`1 0.75 0 RG 2 w")
jrep("`Atlas Socioambiental Cuiabá–Várzea Grande · Instituto ANAP · página ${j+1} de ${pages.length}`","`Atlas Socioambiental da RMVRC · PPGAU-UNIVAG · página ${j+1} de ${pages.length}`")
jrep("saveFile('metodologia_fontes_atlas_cuiaba_vg.pdf',","saveFile('metodologia_fontes_atlas_rmvrc.pdf',")
jrep("const ATLAS_NOME='Cuiabá e Várzea Grande';","const ATLAS_NOME='Região Metropolitana do Vale do Rio Cuiabá';")
jrep("ctx.fillText(`Elaboração: Instituto ANAP · gerado em ${hoje()}`, RM, RH-48);","ctx.fillText(`"+AUT+" · gerado em ${hoje()}`, RM, RH-48);")
# textos "conurbação" -> RMVRC
for a,b in [("pior situação da conurbação","pior situação da RMVRC"),("perfil da conurbação","perfil da RMVRC"),("Mediana da conurbação","Mediana da RMVRC"),("20% piores da conurbação","20% piores da RMVRC"),("mediana da conurbação","mediana da RMVRC"),("mediana dos setores da conurbação","mediana dos setores da RMVRC"),("tracejado = perfil da conurbação","tracejado = perfil da RMVRC")]:
    body=body.replace(a,b)
# cores fixas dos canvases
body=body.replace("'#14221f'","'#0f1d3a'").replace("'#56665f'","'#56607a'").replace("'#a8661c'","'#9a6f00'").replace("'#f3f6f1'","'#f1f4fa'")
# seletor de municipio
jrep("segs('[data-m]','mun',()=>fitTo(visible()));","document.getElementById('munsel').addEventListener('change',e=>{ st.mun=e.target.value; render(); fitTo(visible()); });")
# arte da abertura: RMVRC inteira
jrep("const pj=d3.geoMercator().fitExtent([[w*.02,h*.04],[w*1.05,h*1.02]], core), pa=d3.geoPath(pj);","const pj=d3.geoMercator().fitExtent([[w*.04,h*.06],[w*.98,h*.98]], MUN), pa=d3.geoPath(pj);")
jrep("hs.append('g').selectAll('path').data(F.filter(f=>f.properties.fcu)).join('path').attr('class','set').attr('d',pa);","hs.append('g').selectAll('path').data(F.filter(f=>f.properties.sit==='Urbana')).join('path').attr('class','set').attr('d',pa);")
jrep("attr('stroke-width',f=>f.properties.n==='Rio Cuiabá'?3.2:1.6)","attr('stroke-width',f=>f.properties.n==='Rio Cuiabá'?2.4:.9)")
# enquadramento inicial: area urbana da RMVRC
jrep("placeLabels(1); placeEq(1); scaleBar(1);","placeLabels(1); placeEq(1); scaleBar(1);\nsetTimeout(()=>fitTo(visible()),60);")
H=head+body
# AX cores alinhadas a paleta (mantem distincao)
open('/home/claude/d/atlas_rmvrc.html','w').write(H)
print('ok',len(H)/1e6,'MB')

# ================= camada independente de nomes dos cursos d'agua =================
H=open('/home/claude/d/atlas_rmvrc.html').read()
def r2(old,new,n=1):
    global H
    c=H.count(old); assert c==n,(c,old[:80]); H=H.replace(old,new)
r2('''<label class="opt" for="hid-on"><input type="checkbox" id="hid-on" checked><span>Rede hídrica<small>OpenStreetMap</small></span></label>''',
'''<label class="opt" for="hid-on"><input type="checkbox" id="hid-on" checked><span>Rede hídrica<small>OpenStreetMap</small></span></label>
      <label class="opt" for="nmr-on"><input type="checkbox" id="nmr-on" checked><span>Nomes de rios e ribeirões<small>rótulos independentes da rede</small></span></label>
      <label class="opt" for="nmc-on"><input type="checkbox" id="nmc-on" checked><span>Nomes de córregos e canais<small>aparecem conforme o zoom</small></span></label>''')
a=H.index("// rótulos dos principais cursos d'água"); b=H.index("document.getElementById('hid-on')")
NEWLAB=r'''// ------- nomes dos cursos d'água: camada própria, liga/desliga sem depender da rede -------
const gN = g.append('g').attr('class','hid hidn');
const segLen=s=>d3.sum(s.slice(1),(p,i)=>Math.hypot(p[0]-s[i][0],p[1]-s[i][1]));
const labels = [];
for(const [nome,fs] of d3.group(HL.filter(f=>f.properties.n), f=>f.properties.n)){
  const rank = /^Rio\b/.test(nome)?0:(/^Ribeir/.test(nome)?1:2);
  for(const f of fs){ const s=f.geometry.coordinates.map(c=>proj(c)); const Ls=segLen(s); if(Ls<1.5) continue;
    const n=Math.max(1,Math.floor(Ls/90));
    for(let q=0;q<n;q++){ const half=Ls*(q+.5)/n; let acc=0;
      for(let i=1;i<s.length;i++){ const d=Math.hypot(s[i][0]-s[i-1][0],s[i][1]-s[i-1][1]);
        if(acc+d>=half){ const t=d?(half-acc)/d:0, x=s[i-1][0]+t*(s[i][0]-s[i-1][0]), y=s[i-1][1]+t*(s[i][1]-s[i-1][1]);
          let ang=Math.atan2(s[i][1]-s[i-1][1],s[i][0]-s[i-1][0])*180/Math.PI; if(ang>90)ang-=180; if(ang<-90)ang+=180;
          labels.push({nome,x,y,a:ang,rank,L:Ls/n,big:rank===0,cor:f.properties.t!=='r'}); break; } acc+=d; } } }
}
labels.sort((p,q)=>p.rank-q.rank||q.L-p.L);
const lab = gN.selectAll('text').data(labels).join('text').attr('text-anchor','middle').attr('dy','-0.45em').text(d=>d.nome).attr('display','none');
let labK=1, labRaf=0;
function placeLabels(k){ labK=k; if(labRaf) return; labRaf=requestAnimationFrame(()=>{ labRaf=0; layoutLabels(labK); }); }
function layoutLabels(k){
  const t=d3.zoomTransform(svg.node()), showR=document.getElementById('nmr-on').checked, showC=document.getElementById('nmc-on').checked;
  const boxes=[], last=new Map(), cell=60, grid=new Map();
  const hit=(b)=>{ const x0=Math.floor(b[0]/cell),x1=Math.floor(b[2]/cell),y0=Math.floor(b[1]/cell),y1=Math.floor(b[3]/cell);
    for(let gx=x0;gx<=x1;gx++) for(let gy=y0;gy<=y1;gy++){ const arr=grid.get(gx+','+gy); if(arr) for(const o of arr) if(b[0]<o[2]&&b[2]>o[0]&&b[1]<o[3]&&b[3]>o[1]) return true; }
    for(let gx=x0;gx<=x1;gx++) for(let gy=y0;gy<=y1;gy++){ const key=gx+','+gy; (grid.get(key)||grid.set(key,[]).get(key)).push(b); } return false; };
  lab.each(function(d){
    let on=false;
    const fsz=d.rank===0?13:(d.rank===1?12:11);
    if((d.rank<2?showR:showC)){
      const sx=t.x+k*d.x, sy=t.y+k*d.y;
      if(sx>-50&&sx<W+50&&sy>-20&&sy<H+20){
        const w=d.nome.length*fsz*.56;
        if(d.L*k>=w*.9 || (d.rank===0&&d.L*k>=w*.5)){
          const prev=last.get(d.nome)||[];
          if(!prev.some(p=>Math.hypot(p[0]-sx,p[1]-sy)<Math.max(260,w*2.2))){
            const r=d.a*Math.PI/180, bw=Math.abs(w*Math.cos(r))+Math.abs(fsz*Math.sin(r)), bh=Math.abs(w*Math.sin(r))+Math.abs(fsz*Math.cos(r))+4;
            const b=[sx-bw/2,sy-bh/2-fsz*.4,sx+bw/2,sy+bh/2-fsz*.4];
            if(!hit(b)){ on=true; prev.push([sx,sy]); last.set(d.nome,prev); }
          }
        }
      }
    }
    const el=d3.select(this);
    if(on) el.attr('display',null).attr('font-size',fsz/k).attr('stroke-width',3/k).attr('transform',`translate(${d.x},${d.y}) rotate(${d.a})`);
    else el.attr('display','none');
  });
}
for(const id of ['nmr-on','nmc-on']) document.getElementById(id).addEventListener('change',()=>layoutLabels(d3.zoomTransform(svg.node()).k));
'''
H=H[:a]+NEWLAB+H[b:]
# nomes por cima da divisa municipal, abaixo dos equipamentos
r2("document.getElementById('mun-on').addEventListener('change',e=>gM.attr('display',e.target.checked?null:'none'));",
   "document.getElementById('mun-on').addEventListener('change',e=>gM.attr('display',e.target.checked?null:'none'));\ngN.raise();")
open('/home/claude/d/atlas_rmvrc.html','w').write(H)
print('nomes ok')

exec(open('/home/claude/d/refino.py').read())
exec(open('/home/claude/d/layers.py').read())
exec(open('/home/claude/d/vhab.py').read())
exec(open('/home/claude/d/metodo.py').read())
exec(open('/home/claude/d/fontes.py').read())
exec(open('/home/claude/d/final.py').read())

exec(open('/home/claude/d/site.py').read())

exec(open('/home/claude/d/sat7.py').read())
exec(open('/home/claude/d/lic.py').read())
exec(open('/home/claude/d/sgbch.py').read())
exec(open('/home/claude/d/app.py').read())
exec(open('/home/claude/d/rep2.py').read())
