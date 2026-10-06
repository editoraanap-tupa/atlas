# ================= refinamento: carta SGB + ANADEM =================
import json as _j
H=open('/home/claude/d/atlas_rmvrc.html').read()
RES=_j.load(open('/home/claude/f/resultado.json')); IM=_j.load(open('/home/claude/f/imgs.json')); V=RES['V']
def br(x,d=1): return (f'{x:,.{d}f}').replace(',','#').replace('.',',').replace('#','.')
def bi(x): return f'{int(x):,}'.replace(',','.')
def r3(old,new,n=1):
    global H
    c=H.count(old); assert c==n,(c,old[:90]); H=H.replace(old,new)
DL=br(RES['delta'])
# RAST
i=H.index('const RAST = '); k=H.index('"img": {',i)+len('"img": {')
H=H[:k]+'"sgbc": "'+IM['sgbc']+'", "cheias2": "'+IM['cheias2']+'", '+H[k:]
# radios
r3('<label class="opt" for="bg-cheias">','<label class="opt" for="bg-sgbc"><input type="radio" name="bg" id="bg-sgbc" value="sgbc"><span>Carta de suscetibilidade SGB<small>oficial · 1:25.000 · Cuiabá e VG</small></span><i class="sw2" style="background:linear-gradient(90deg,#fee08b 0 33%,#f46d43 33% 66%,#a50026 66%)"></i></label>\n      <label class="opt" for="bg-cheias2"><input type="radio" name="bg" id="bg-cheias2" value="cheias2"><span>Cheias do Rio Cuiabá · MDT ANADEM<small>terreno sem vegetação · recalibrado</small></span><i class="sw2" style="background:linear-gradient(90deg,#3f007d,#6a51a3,#bcbddc)"></i></label>\n      <label class="opt" for="bg-cheias">')
# JS
r3("for(const k of ['ndvi','lst','inund','cheias']) rimg[k]","for(const k of ['ndvi','lst','inund','cheias','sgbc','cheias2']) rimg[k]")
r3(",cheias:'Na cheia de 1974: '+fv('c1974',p.c1974)+' da área'}[st.bg]",",cheias:'Na cheia de 1974: '+fv('c1974',p.c1974)+' da área',cheias2:'Na cheia de 1974 (ANADEM): '+fv('a1974',p.a1974)+' da área',sgbc:'Carta SGB, classe alta: '+fv('sgb_alta',p.sgb_alta)+' da área'}[st.bg]")
r3("    inund:['Suscetibilidade','linear-gradient(90deg,rgba(198,219,239,.8) 0 33%,rgba(107,174,214,.9) 33% 66%,rgb(8,81,156) 66%)','baixa','alta']};",
   "    inund:['Suscetibilidade','linear-gradient(90deg,rgba(198,219,239,.8) 0 33%,rgba(107,174,214,.9) 33% 66%,rgb(8,81,156) 66%)','baixa','alta'],\n    sgbc:['Carta de suscetibilidade a inundação · SGB','linear-gradient(90deg,#fee08b 0 33%,#f46d43 33% 66%,#a50026 66%)','baixa','alta']};")
r3("  if(bgr&&st.bg==='cheias'){","  if(bgr&&st.bg==='cheias2'){ rp.innerHTML=`<b>Cheias do Rio Cuiabá · MDT ANADEM (ajuste +"+DL+" m)</b><div class=\"chl\"><span><i style=\"background:#3f007d\"></i>8,50 m · alerta</span><span><i style=\"background:#54278f\"></i>9,50 m · emergência</span><span><i style=\"background:#6a51a3\"></i>10,36 m · 1995</span><span><i style=\"background:#807dba\"></i>10,85 m · 1974</span><span><i style=\"background:#bcbddc\"></i>11,00 m · calamidade</span></div>`; }\n  else if(bgr&&st.bg==='cheias'){")
r3("      inund:[['#c6dbef','#6baed6','#08519c'],'baixa','alta']}[st.bg];","      inund:[['#c6dbef','#6baed6','#08519c'],'baixa','alta'],\n      sgbc:[['#fee08b','#f46d43','#a50026'],'baixa','alta'],\n      cheias2:[['#3f007d','#6a51a3','#bcbddc'],'alerta (8,50 m)','calamidade (11,00 m)']}[st.bg];")
r3("cheias:'Cheias do Rio Cuiabá · cotas históricas, modelo calibrado'}[st.bg];","cheias:'Cheias do Rio Cuiabá · cotas históricas, modelo calibrado', cheias2:'Cheias do Rio Cuiabá · cotas históricas, MDT ANADEM recalibrado', sgbc:'Suscetibilidade a inundação · carta oficial do SGB (1:25.000)'}[st.bg];")
# indicadores
r3(" {k:'alerta',ax:'amb',", " {k:'sgb_alta',ax:'amb',n:'Suscetibilidade alta · carta SGB',u:'%',pol:'r',d:'Parte da área do setor na classe alta da Carta de Suscetibilidade a Inundação do Serviço Geológico do Brasil (1:25.000; Cuiabá e Várzea Grande, 2021).',w:'area'},\n"
   " {k:'sgb_alta_pop',ax:'amb',n:'Moradores em suscet. alta (SGB)',u:'hab.',pol:'r',d:'População do setor × fração da área na classe alta da carta do SGB.',w:'sum'},\n"
   " {k:'a1974',ax:'amb',n:'Área na cheia de 1974 (ANADEM)',u:'%',pol:'r',d:'Parte da área do setor abaixo do nível da cheia de 1974 no modelo refeito com o MDT ANADEM (terreno sem vegetação) e ajuste de +"+DL+" m.',w:'area'},\n"
   " {k:'a1974_pop',ax:'amb',n:'Moradores na cheia de 1974 (ANADEM)',u:'hab.',pol:'r',d:'População do setor × fração da área abaixo do nível da cheia de 1974 (modelo ANADEM).',w:'sum'},\n"
   " {k:'alerta',ax:'amb',")
r3("  {k:'inund', n:'Suscetibilidade a inundação', s:1, env:1},","  {k:'inund', n:'Suscetibilidade a inundação', s:1, env:1},\n  {k:'sgb_alta', n:'Suscetibilidade (carta SGB)', s:1, env:1},")
# roteiro
r3('<li><span class="status next">próximo</span>Obter a mancha oficial da Defesa Civil e levantamento topográfico (LiDAR) para refinar os cenários</li>',
 '<li><span class="status ok">feito</span>Carta oficial de suscetibilidade a inundação do SGB (Cuiabá e VG) integrada e comparada com os modelos</li>\n      <li><span class="status ok">feito</span>Cenários de cheia refeitos com o MDT ANADEM (terreno sem vegetação) e recalibrados</li>\n      <li><span class="status next">próximo</span>Solicitar à Defesa Civil de Cuiabá, de Várzea Grande e à SEDEC-MT a mancha oficial das cheias (Lei de Acesso à Informação)</li>\n      <li><span class="status next">próximo</span>Levantamento LiDAR da planície do Rio Cuiabá e nivelamento geodésico da régua 66260001</li>')
T=RES['tab']; Bq=RES['bai']; cal=RES['calib']
cal_rows=''.join("<tr%s><td class='num'>+%s m</td><td class='num'>%s%%</td><td class='num'>%s%%</td><td class='num'>%s%%</td><td class='num'>%s</td><td class='num'>%s</td></tr>"%(' style="font-weight:700"' if float(d)==RES['delta'] else '',br(float(d)),br(v['c1974'][1]['Terceiro']),br(v['c1995'][1]['Praeirinho']),br(v['c1974'][1]['Porto']),bi(v['c1995'][0]),bi(v['c1974'][0])) for d,v in cal.items())
tab_rows=''.join("<tr><td class='l'>%s</td><td class='num'>%s m</td><td class='num'>%s km²</td><td class='num'>%s</td></tr>"%(t['nome'],br(t['regua'],2),br(t['km2']),bi(t['mor'])) for t in T)
bai_rows=''.join("<tr><td class='l'>%s</td><td class='l'>%s</td><td class='num'>%s</td><td class='num'>%s%%</td><td class='num'>%s%%</td><td class='num'>%s%%</td></tr>"%(b['b'],b['mun'],b['ano'],br(b['a74']),br(b['sgbA']),br(b['sgbAM'])) for b in Bq)
sec=f"""<div class="sec-h" id="refino" style="scroll-margin-top:calc(var(--tb) + 12px)"><span class="kick">Refinamento dos cenários · setembro de 2026</span><h2>Carta oficial do SGB e terreno sem vegetação</h2><p>Duas bases públicas foram incorporadas para refinar os cenários: a Carta de Suscetibilidade a Movimentos Gravitacionais de Massa e Inundação do Serviço Geológico do Brasil (1:25.000, validada em campo em 2021) para Cuiabá e Várzea Grande, e o MDT ANADEM (ANA/UFRGS, 30 m), que remove a vegetação do modelo Copernicus. Com elas os cenários de cheia foram refeitos e comparados.</p></div>
<section class="block">
  <div class="kpis vk">
    <div class="kpi"><div class="lab">Área urbana em suscet. alta (SGB)</div><div class="val">{br(V['sgbA_urb_pct'])}%</div><div class="sub">{br(V['sgbA_urb_km2'])} km² · HAND: {br(V['handA_urb_pct'])}%</div></div>
    <div class="kpi"><div class="lab">Moradores em suscet. alta (SGB)</div><div class="val">{bi(V['mor_sgbA'])}</div><div class="sub">{bi(V['mor_sgbAM'])} em alta ou média</div></div>
    <div class="kpi"><div class="lab">Cheia de 1974 dentro da carta</div><div class="val">{br(V['a74_in_sgbAM'])}%</div><div class="sub">da mancha urbana em alta/média (SGB)</div></div>
    <div class="kpi"><div class="lab">ANADEM × modelo anterior</div><div class="val">{br(V['g74_in_a74'])}%</div><div class="sub">da mancha de 1974 anterior confirmada</div></div>
  </div>
  <div class="split" style="margin-top:18px">
    <div>
      <h3>Cenários refeitos com o MDT ANADEM (ajuste +{DL} m)</h3>
      <div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th class="l">Cenário</th><th>Régua de Cuiabá</th><th>Área alagada</th><th>Moradores hoje abaixo do nível</th></tr></thead><tbody>{tab_rows}</tbody></table></div>
      <h3 style="margin-top:16px">Calibração com os bairros atingidos</h3>
      <div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th>Ajuste</th><th>Terceiro (1974)</th><th>Praeirinho (1995)</th><th>Porto (1974)</th><th>Moradores 1995</th><th>Moradores 1974</th></tr></thead><tbody>{cal_rows}</tbody></table></div>
      <p class="msg" style="margin-top:8px">Mesmo com o terreno sem vegetação, o modelo só reproduz o Terceiro submerso em 1974 com ajuste de +{DL} m (o modelo anterior precisou de +2 m). A diferença, portanto, não vem da vegetação: vem do tamanho do pixel (30 m), de aterros e diques que o satélite não distingue e, possivelmente, da diferença entre o referencial altimétrico da régua e o do modelo. Só um levantamento LiDAR e o nivelamento geodésico da régua resolvem essa incerteza.</p>
    </div>
    <div>
      <h3>Bairros atingidos: modelo × carta oficial</h3>
      <div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th class="l">Bairro / distrito</th><th class="l">Município</th><th>Cheia</th><th>Na cheia de 1974 (ANADEM)</th><th>Suscet. alta (SGB)</th><th>Alta ou média (SGB)</th></tr></thead><tbody>{bai_rows}</tbody></table></div>
      <h3 style="margin-top:16px">O que a comparação mostra</h3>
      <ul class="msg" style="padding-left:18px;margin:0">
        <li>A carta do SGB e o modelo HAND apontam extensões parecidas de área urbana em suscetibilidade alta ({br(V['sgbA_urb_pct'])}% e {br(V['handA_urb_pct'])}%); {br(V['sgbA_in_handAM'])}% da classe alta do SGB cai nas classes média ou alta do HAND.</li>
        <li>{br(V['a74_in_sgbAM'])}% da mancha urbana da cheia de 1974 (ANADEM) está nas classes alta ou média da carta oficial; {br(V['a74_in_sgbA'])}% está na classe alta.</li>
        <li>Dos {V['risco_n']} setores de risco de inundação e alagamento mapeados pelo SGB com a Defesa Civil, {V['risco_toca_sgbA']} tocam a classe alta da carta e {V['risco_toca_sgbAM']} tocam alta ou média.</li>
        <li>As manchas de 1974 do modelo anterior (Copernicus GLO-30) e do novo (ANADEM) coincidem em {br(V['iou_74'])}% (interseção sobre união); a nova é um pouco maior ({br(T[3]['km2'])} km²).</li>
        <li>A carta do SGB passa a ser a referência oficial de suscetibilidade no Atlas; os cenários por cota seguem como a única estimativa de alcance por nível de cheia até a Defesa Civil disponibilizar a mancha oficial.</li>
      </ul>
    </div>
  </div>
</section>
"""
r3('<div class="sec-h" id="metodo"',sec+'<div class="sec-h" id="metodo"')
r3('<a href="#validacao">Validação</a>','<a href="#validacao">Validação</a><a href="#refino">Refinamento</a>')
r3('<li>Rede hídrica: OpenStreetMap','<li>Carta de suscetibilidade a inundação: SGB/CPRM, Cartas de Suscetibilidade a Movimentos Gravitacionais de Massa e Inundação, 1:25.000 — Cuiabá (2021, publicada em 2022) e Várzea Grande; vetores em SIRGAS 2000/UTM 21S convertidos para coordenadas geográficas e rasterizados a 10 m.</li>\n      <li>MDT ANADEM v1 (ANA/UFRGS, 30 m, terreno sem vegetação), recorte lido diretamente do arquivo em nuvem (tile 21L). Régua fluviométrica Cuiabá, código ANA 66260001 (lat −15,6156; lon −56,1086).</li>\n      <li>Rede hídrica: OpenStreetMap')
open('/home/claude/d/atlas_rmvrc.html','w').write(H)
print('refino ok', len(H)/1e6)
