# Camada de demarcação de APP e nascentes (Lei 12.651/2012, art. 4º) em vetor, nos 7 municípios
# classes dos corpos d'água: /home/claude/x/app_cls.py -> app_cls.json
import json
H=open('/home/claude/d/atlas_rmvrc.html').read()
def rep(a,b,n=1):
    global H
    c=H.count(a); assert c>=1 and (n is None or c==n),(c,a[:90]); H=H.replace(a,b)
dec=json.JSONDecoder()
# ---- 1. classes nos polígonos da hidrografia
pref='const HIDRO = '; i=H.index(pref); HID,j=dec.raw_decode(H[i+len(pref):]); CL=json.load(open('/home/claude/x/app_cls.json'))
for k,c in CL.items():
    p=HID['features'][int(k)]['properties']; assert p['t']=='a'; p['ap']=c['ap']; p['ak']=c['ak']
H=H[:i+len(pref)]+json.dumps(HID,ensure_ascii=False,separators=(',',':'))+H[i+len(pref)+j:]
# ---- 2. sai a imagem raster da APP (a camada passa a ser vetorial)
pref='const RAST = '; i=H.index(pref); RAST,j=dec.raw_decode(H[i+len(pref):]); RAST['img'].pop('app')
H=H[:i+len(pref)]+json.dumps(RAST,ensure_ascii=False)+H[i+len(pref)+j:]
# ---- 3. desenho
a=H.index("const outR=c=>!(c[0]>=RB[0]"); b=H.index("const gSG = g.append('g').attr('display','none');")
assert "RAST.img.app" in H[a:b]
NEW=r"""// ------- demarcação de APP (Lei 12.651/2012, art. 4º): vetor, com contorno, nos 7 municípios -------
gA.attr('pointer-events','none');
const APPCOL={30:'#63c98d',50:'#2fa866',100:'#15803d',200:'#0b5d2c',500:'#063f1e'};
const gcol=fs=>path({type:'GeometryCollection',geometries:fs.map(f=>f.geometry)});
const HAA=HIDRO.features.filter(f=>f.properties.t==='a');
const appSets=[];
for(const w of [30,50,100,200,500]){ const fs=HIDRO.features.filter(f=>{ const q=f.properties; return ((q.t==='r'||q.t==='s')&&q.app===w)||(q.t==='a'&&q.ak==='rio'&&q.ap===w); }); if(fs.length) appSets.push([w,'rio',fs]); }
for(const w of [30,50,100]){ const fs=HAA.filter(f=>f.properties.ak==='lago'&&f.properties.ap===w); if(fs.length) appSets.push([w,'lago',fs]); }
const APPW=[...new Set(appSets.filter(s=>s[1]==='rio').map(s=>s[0]))];
const appC=appSets.map(([w,t,fs])=>[gA.append('path').attr('class','appc').attr('d',gcol(fs)),w]);
appSets.forEach(([w,t,fs])=>gA.append('path').attr('class','appf').attr('d',gcol(fs)).attr('stroke',t==='lago'?'#38b2a3':APPCOL[w]).attr('stroke-width',2*w*upm));
gA.append('path').attr('class','appw').attr('d',gcol(HAA.filter(f=>f.properties.ap>0)));
const appR=gA.append('path').attr('class','appr').attr('d',gcol(HAA.filter(f=>f.properties.ak==='res')));
// nascentes presumidas (início de cada córrego) e APP de 50 m de raio (art. 4º, IV)
const gNa=g.append('g').attr('display','none').attr('pointer-events','none');
const NASC=HIDRO.features.filter(f=>f.properties.t==='n').map(f=>proj(f.geometry.coordinates)), rNa=50*upm;
const nasC=gNa.append('path').attr('class','nasc').attr('d',NASC.map(([x,y])=>`M${(x-rNa).toFixed(3)},${y.toFixed(3)}a${rNa},${rNa} 0 1,0 ${2*rNa},0a${rNa},${rNa} 0 1,0 ${-2*rNa},0`).join(''));
const nasP=gNa.append('path').attr('class','nasp').attr('d',NASC.map(([x,y])=>`M${x.toFixed(3)},${y.toFixed(3)}l0.0001,0`).join(''));
function placeApp(k){ const e=2.6/k; for(const [el,w] of appC) el.attr('stroke-width',2*w*upm+e); appR.attr('stroke-width',3.2/k).attr('stroke-dasharray',`${5/k} ${3.5/k}`); nasC.attr('stroke-width',1.3/k).attr('stroke-dasharray',`${3.5/k} ${2.5/k}`); nasP.attr('stroke-width',5.5/k); }
placeApp(1);
window.__app={APPW,APPCOL};
"""
H=H[:a]+NEW+H[b:]
rep("placeLabels(e.transform.k); placeEq(e.transform.k);","placeLabels(e.transform.k); placeEq(e.transform.k); placeApp(e.transform.k);")
rep("gA.attr('opacity', OPA.app/100);","gA.attr('opacity', OPA.app/100); gNa.attr('opacity', OPA.app/100);")
rep("document.getElementById('app-on').addEventListener('change',e=>{ gA.attr('display',e.target.checked?null:'none'); document.getElementById('appleg').hidden=!e.target.checked; });",
    "document.getElementById('app-on').addEventListener('change',e=>{ gA.attr('display',e.target.checked?null:'none'); document.getElementById('appleg').hidden=!e.target.checked; });\ndocument.getElementById('nas-on').addEventListener('change',e=>{ gNa.attr('display',e.target.checked?null:'none'); });")
rep("[['set','Setores (indicador)'],['ras','Fundo de satélite / modelo'],['app','APP'],","[['set','Setores (indicador)'],['ras','Fundo de satélite / modelo'],['app','APP e nascentes'],")
# ---- 4. controles
rep('<label class="opt" for="app-on"><input type="checkbox" id="app-on"><span>APP<small>faixas do Código Florestal</small></span></label>',
    '<label class="opt" for="app-on"><input type="checkbox" id="app-on"><span>APP de rios, córregos e lagos<small>demarcação · Código Florestal, art. 4º</small></span></label>\n      <label class="opt" for="nas-on"><input type="checkbox" id="nas-on"><span>Nascentes<small>APP com raio de 50 m · art. 4º, IV</small></span></label>')
rep('<span><i style="width:14px;height:10px;background:rgba(0,150,90,.8);border-radius:2px"></i>APP (faixa marginal e nascentes)</span>',
    '<span><i style="width:14px;height:10px;background:#2fa866;border:1.5px solid #0a4f2b;border-radius:2px"></i>APP de curso d’água e de lago (Lei 12.651/2012, art. 4º)</span>')
# ---- 5. legenda dinâmica
rep("    if(on('app-on')) L.push(it(bx('rgba(0,150,90,.8)'),'APP (faixa marginal e nascentes)'));",
"""    if(on('app-on')){ const {APPW,APPCOL}=window.__app||{APPW:[],APPCOL:{}}; const AW={30:'leito de até 10 m',50:'leito de 10 a 50 m',100:'leito de 50 a 200 m',200:'leito de 200 a 600 m',500:'leito acima de 600 m'};
      for(const w of APPW) L.push(it(bx(APPCOL[w],'#0a4f2b'),'APP de curso d’água · '+w+' m ('+AW[w]+')'));
      L.push(it(bx('#38b2a3','#0a4f2b'),'APP de lago ou lagoa · 30 m em área urbana; 50 ou 100 m em área rural'));
      L.push(it(ln('#4b5d7a',1.6,'4 3'),'Reservatório, açude ou tanque · faixa definida no licenciamento (não demarcada)')); }
    if(on('nas-on')) L.push(it('<svg width="20" height="14"><circle cx="10" cy="7" r="6" fill="rgba(234,88,12,.22)" stroke="#c2410c" stroke-width="1.2" stroke-dasharray="2.5 2"/><circle cx="10" cy="7" r="2" fill="#c2410c"/></svg>','Nascente presumida (início de córrego) e APP de 50 m de raio'));""")
# ---- 6. legenda e fontes na exportação (PNG/PDF)
rep("  if(on('app-on')){ ctx.globalAlpha=OPA.app/100; sw('rgba(0,150,90,.85)',y); ctx.globalAlpha=1; ctx.fillStyle='#0f1d3a'; ctx.fillText('APP (faixas e nascentes)', cx+48, y); y+=32; }",
"""  if(on('app-on')){ const AW={30:'leito até 10 m',50:'leito de 10 a 50 m',100:'leito de 50 a 200 m',200:'leito de 200 a 600 m',500:'leito acima de 600 m'};
    for(const w of APPW){ sw(APPCOL[w],y,'#0a4f2b'); ctx.fillStyle='#0f1d3a'; ctx.fillText('APP de curso d’água · '+w+' m ('+AW[w]+')', cx+48, y); y+=32; }
    sw('#38b2a3',y,'#0a4f2b'); ctx.fillStyle='#0f1d3a'; ctx.fillText('APP de lago ou lagoa · 30 m urbano; 50 ou 100 m rural', cx+48, y); y+=32;
    ctx.strokeStyle='#4b5d7a'; ctx.lineWidth=2; ctx.setLineDash([7,5]); ctx.strokeRect(cx+1,y-17,32,20); ctx.setLineDash([]); ctx.fillStyle='#0f1d3a'; ctx.fillText('Reservatório ou açude · faixa definida no licenciamento', cx+48, y); y+=32; }
  if(on('nas-on')){ ctx.fillStyle='rgba(234,88,12,.22)'; ctx.strokeStyle='#c2410c'; ctx.lineWidth=1.6; ctx.setLineDash([4,3]); ctx.beginPath(); ctx.arc(cx+17,y-7,11,0,2*Math.PI); ctx.fill(); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle='#c2410c'; ctx.beginPath(); ctx.arc(cx+17,y-7,3.5,0,2*Math.PI); ctx.fill(); ctx.fillStyle='#0f1d3a'; ctx.fillText('Nascente presumida e APP de 50 m de raio', cx+48, y); y+=32; }""")
rep("  if(on('app-on')) f.push('APP: Lei 12.651/2012 sobre hidrografia OpenStreetMap');",
    "  if(on('app-on')||on('nas-on')) f.push('APP e nascentes: demarcação pela Lei 12.651/2012, art. 4º, sobre hidrografia OpenStreetMap');")
# ---- 7. estilos
CSS='''
.appc{fill:none;stroke:#0a4f2b;stroke-linejoin:round;stroke-linecap:round}
.appf{fill:none;stroke-linejoin:round;stroke-linecap:round}
.appw{fill:var(--water);stroke:none}
.appr{fill:none;stroke:#4b5d7a;stroke-linejoin:round}
.nasc{fill:rgba(234,88,12,.22);stroke:#c2410c}
.nasp{fill:none;stroke:#c2410c;stroke-linecap:round}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .appc{stroke:#d7f7e2} :root:not([data-theme="light"]) .appr{stroke:#b8c4dc} :root:not([data-theme="light"]) .nasc{stroke:#ffb37a;fill:rgba(255,150,80,.25)} :root:not([data-theme="light"]) .nasp{stroke:#ffb37a}}
:root[data-theme="dark"] .appc{stroke:#d7f7e2} :root[data-theme="dark"] .appr{stroke:#b8c4dc} :root[data-theme="dark"] .nasc{stroke:#ffb37a;fill:rgba(255,150,80,.25)} :root[data-theme="dark"] .nasp{stroke:#ffb37a}
'''
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSS+H[k:]
# ---- 8. textos
rep("Suscetibilidade a inundação, APP e microbacias cobrem as áreas urbanas (conurbação, sedes e distritos).","A demarcação de APP e de nascentes cobre toda a hidrografia mapeada. Suscetibilidade a inundação, indicador de área em APP e microbacias cobrem as áreas urbanas (conurbação, sedes e distritos).")
a=H.index("<li><b>APP</b>: faixas do Código Florestal (Lei 12.651/2012, art. 4º) sobre a rede do OpenStreetMap:"); b=H.index("</li>",a)+5
OLD=H[a:b]
NEWLI=OLD.replace("<li><b>APP</b>: faixas","<li><b>Área em APP (indicador)</b>: faixas")+"""
      <li><b>Demarcação de APP e nascentes (camada do mapa)</b>: desenho vetorial das Áreas de Preservação Permanente da Lei 12.651/2012, art. 4º, sobre a hidrografia do OpenStreetMap, nos 7 municípios. <b>Cursos d’água</b> (inciso I): quando a calha está desenhada como polígono, a faixa parte da margem e a largura do leito é estimada por 2 × área ÷ perímetro do polígono — 30 m (leito de até 10 m), 50 m (10 a 50 m), 100 m (50 a 200 m) e 200 m (200 a 600 m); rios e córregos desenhados só como linha recebem a faixa mínima de 30 m (Rio Cuiabá, 100 m; Rio Coxipó, 50 m). <b>Lagos e lagoas naturais</b> com 1 ha ou mais (inciso II): 30 m em setor urbano; em setor rural, 50 m até 20 ha e 100 m acima disso. <b>Reservatórios artificiais, açudes e tanques</b> (inciso III): a faixa é definida na licença ambiental e por isso não é demarcada; aparecem só com contorno tracejado. Acumulações com menos de 1 ha são dispensadas de faixa (§ 4º). <b>Nascentes</b> (inciso IV): raio de 50 m em torno do início de cada córrego mapeado, tomado como nascente presumida. Canais artificiais ficam de fora. Não estão demarcadas as APPs de encosta acima de 45°, borda de chapada, topo de morro e vereda (incisos V, VIII, IX e XI). A classificação de lago, lagoa ou reservatório é a do OpenStreetMap, e a situação urbana ou rural é a do setor censitário do IBGE: a camada orienta o planejamento e não substitui a delimitação em campo nem o Cadastro Ambiental Rural. O indicador “Área em APP” segue a regra do item anterior, mais simples (30 m em torno de todo corpo d’água), e só nos setores urbanos.</li>"""
H=H[:a]+NEWLI+H[b:]
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('app ok',len(H))
