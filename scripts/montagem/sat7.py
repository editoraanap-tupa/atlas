# Extensão das camadas de satélite e de inundação aos 7 municípios (01/10/2026)
# Dados gerados em /home/claude/x: ndvi_all.py, lst_prep.py + lst_all.py, hand_towns.py, mkimgs.py
import json
H=open('/home/claude/d/atlas_rmvrc.html').read()
def rep(a,b,n=None):
    global H
    c=H.count(a); assert c>=1 and (n is None or c==n),(c,a[:90]); H=H.replace(a,b)
dec=json.JSONDecoder()
def getc(name):
    pref='const '+name+' = '; i=H.index(pref); obj,j=dec.raw_decode(H[i+len(pref):]); return obj,i+len(pref),i+len(pref)+j
# ---------- 1. dados por setor
D=json.load(open('/home/claude/x/sat7_data.json')); SGBCH=json.load(open('/home/claude/x/sgbch_out.json'))
DATA,a,b=getc('DATA'); n=0
for f in DATA['features']:
    p=f['properties']; d=D[p['id']]
    for k in ('ndvi','verde','lst','lst_anom'): p[k]=d[k]
    for k in ('inund','inund2','inund_pop'):
        if k in d: p[k]=d[k]
    for k in ('vr','vd','lr','ld'):
        if k in d: p[k]=d[k]
    if p['id'] in SGBCH and SGBCH[p['id']]['sgb_alta'] is not None:
        for k in ('sgb_alta','sgb_am','sgb_alta_pop'): p[k]=SGBCH[p['id']][k]
    n+=1
H=H[:a]+json.dumps(DATA,ensure_ascii=False,separators=(',',':'))+H[b:]
# ---------- 2. imagens
R=json.load(open('/home/claude/x/rast_new.json'))
RAST,a,b=getc('RAST'); RAST['img']['ndvi']=R['cvg']['ndvi']; RAST['img']['lst']=R['cvg']['lst']
H=H[:a]+json.dumps(RAST,ensure_ascii=False)+H[b:]
RAST2,a,b=getc('RAST2'); RAST2['img']['ndvi_r']=R['reg']['ndvi']; RAST2['img']['lst_r']=R['reg']['lst']
H=H[:a]+json.dumps(RAST2,ensure_ascii=False,separators=(',',':'))+';\nconst RAST3 = '+json.dumps(R['patches']+[json.load(open('/home/claude/x/rast_sgbch.json'))],ensure_ascii=False,separators=(',',':'))+H[b:]
rep("for(const k of ['ndvi','lst','inund','cheias','sgbc','cheias2']) rimg[k]=gR.append('image').attr('href',RAST.img[k]).attr('x',ix0).attr('y',iy0).attr('width',ix1-ix0).attr('height',iy1-iy0).attr('preserveAspectRatio','none').attr('display','none');",
"""const mkImg=(par,href,bb)=>{ const [a0,b0]=proj([bb[0],bb[1]]), [a1,b1]=proj([bb[2],bb[3]]); return par.append('image').attr('href',href).attr('x',a0).attr('y',b0).attr('width',a1-a0).attr('height',b1-b0).attr('preserveAspectRatio','none'); };
// regional (7 municípios) por baixo, conurbação em 30 m por cima, recortes das sedes e distritos por último
for(const k of ['ndvi','lst','inund','cheias','sgbc','cheias2']){ const gk=gR.append('g').attr('display','none'); if(RAST2.img[k+'_r']) mkImg(gk,RAST2.img[k+'_r'],RB2); mkImg(gk,RAST.img[k],RB); for(const t of RAST3) if(t[k]) mkImg(gk,t[k],t.b); rimg[k]=gk; }""",1)
# ---------- 3. procedência por setor (imagem e grade) — vai para a ficha, o relatório e o CSV
rep("const F = DATA.features;","""const F = DATA.features;
const SAT_VD=['23/08/2026','17/08/2026','17 e 23/08/2026'], SAT_LD=['13/08/2026','12/08/2026, ajustada','12 e 13/08/2026','14/08/2026, ajustada','13 e 14/08/2026','04/08/2026, ajustada','04 e 13/08/2026'];
F.forEach(f=>{ const p=f.properties; p.sat_veg = p.ndvi==null?null:'Sentinel-2 de '+SAT_VD[p.vd||0]+', pixels de '+(p.vr||10)+' m'; p.sat_lst = p.lst==null?null:'Landsat de '+SAT_LD[p.ld||0]+', '+(p.lr?'amostra de 120 m':'pixels de 30 m'); });
function satNote(p){ const a=[]; if(p.vr||p.vd) a.push('vegetação: '+p.sat_veg); if(p.lr||p.ld) a.push('temperatura: '+p.sat_lst); if(p.inund==null&&p.sit==='Urbana'&&!CONURB_N.includes(p.mun)) a.push('suscetibilidade a inundação sem dado: não há córregos mapeados no OpenStreetMap'); return a.length?'Satélite neste setor — '+a.join('; ')+'.':''; }
const CONURB_N=['Cuiabá','Várzea Grande'];
window.__sat=()=>({F,satNote});""",1)
rep("const ALLCOLS = [['id','Setor'],['mun','Município'],['sit','Situação'],['bairro','Bairro'],['fcu','FCU'],['area','Área (km²)'],...IND.map(i=>[i.k, i.n+(i.u&&i.u!=='hab.'?' ('+i.u+')':'')])];",
    "const ALLCOLS = [['id','Setor'],['mun','Município'],['sit','Situação'],['bairro','Bairro'],['fcu','FCU'],['area','Área (km²)'],...IND.map(i=>[i.k, i.n+(i.u&&i.u!=='hab.'?' ('+i.u+')':'')]),['sat_veg','Vegetação: imagem e grade'],['sat_lst','Temperatura: imagem e grade']];",1)
rep("""const ctxl=[p.fcu?'Favela ou comunidade urbana: '+p.fcu:'', p.solo?'Solo predominante: '+p.solo:'', p.micro?'Microbacia: '+p.micro:'', p.subbac?'Sub-bacia: '+p.subbac.replace(/^Bacia (do |da |de )?/,''):'', p.bac||''].filter(Boolean).join(' · ');""",
    """const ctxl=[p.fcu?'Favela ou comunidade urbana: '+p.fcu:'', p.solo?'Solo predominante: '+p.solo:'', p.micro?'Microbacia: '+p.micro:'', p.subbac?'Sub-bacia: '+p.subbac.replace(/^Bacia (do |da |de )?/,''):'', p.bac||'', satNote(p).replace(/\\.$/,'')].filter(Boolean).join(' · ');""",1)
# ---------- 4. textos
rep("NDVI, temperatura, HAND, cheias, carta do SGB, setores de risco e FCU cobrem só a conurbação Cuiabá–Várzea Grande. Solos, erosão, cobertura da terra, bacias, rede hídrica e divisas cobrem os 7 municípios; APP e microbacias, as áreas urbanas.",
    "Vegetação (NDVI), temperatura, solos, erosão, cobertura da terra, bacias, rede hídrica e divisas cobrem os 7 municípios. Suscetibilidade a inundação, APP e microbacias cobrem as áreas urbanas (conurbação, sedes e distritos). Carta do SGB: Cuiabá, Várzea Grande e Chapada dos Guimarães. Cheias do Rio Cuiabá, setores de risco e FCU: só a conurbação Cuiabá–Várzea Grande.",1)
rep("<small>Sentinel-2 · 23/08/2026</small>","<small>Sentinel-2 · 17 e 23/08/2026</small>",1)
rep("<small>Landsat 9 · 13/08/2026</small>","<small>Landsat 9 · 13/08/2026 · 7 municípios</small>",1)
rep("<small>modelo HAND · Copernicus</small>","<small>altura acima da drenagem · áreas urbanas</small>",1)
S2A="Copernicus Sentinel-2 MSI Nível 2A, imagem de 23/08/2026 (via Earth Search/Element 84)."
S2B="Copernicus Sentinel-2 MSI Nível 2A, imagens de 23/08/2026 (órbita relativa oeste) e, a leste de 55,1° O, de 17/08/2026 (via Earth Search/Element 84)."
rep(S2A,S2B)
L9A="Landsat 9 OLI/TIRS Collection 2 Level-2 (ST_B10), imagem de 13/08/2026 (via Microsoft Planetary Computer)."
L9B="Landsat 9 OLI/TIRS Collection 2 Level-2 (ST_B10), órbita 226, imagem de 13/08/2026; nas bordas, fora dessa faixa, Landsat 8 de 12/08 e 14/08/2026 e Landsat 9 de 04/08/2026 (via Microsoft Planetary Computer)."
rep(L9A,L9B)
rep("Imagem Sentinel-2 L2A (23/08/2026)","Imagens Sentinel-2 L2A (17 e 23/08/2026)")
rep("Imagem Landsat 9 C2 L2 (13/08/2026)","Imagens Landsat 8 e 9 C2 L2 (13/08/2026 e datas vizinhas)")
rep("<li><b>Suscetibilidade a inundação</b>: modelo HAND (altura acima da drenagem mais próxima) com o MDS Copernicus GLO-30. Alta: até 2 m acima de córregos ou 4 m acima dos rios Cuiabá e Coxipó; média: até 5 m / 8 m; baixa: até 8 m / 12 m; só manchas ligadas à drenagem. É uma triagem, não uma mancha oficial: o MDS inclui prédios e copas, e canais cobertos não aparecem.</li>",
    "<li><b>Suscetibilidade a inundação</b>: altura do terreno (MDS Copernicus GLO-30) acima do rio ou córrego mais próximo em linha reta (rede do OpenStreetMap), uma forma simplificada do modelo HAND. Alta: até 2 m acima de córregos ou 4 m acima dos rios Cuiabá e Coxipó; média: até 5 m / 8 m; baixa: até 8 m / 12 m; só manchas ligadas à drenagem. Calculada na conurbação e nas sedes e distritos dos outros cinco municípios (127 de 130 setores urbanos; 3 distritos sem córregos mapeados ficam sem dado). É uma triagem, não uma mancha oficial: o MDS inclui prédios e copas, canais cobertos não aparecem, e onde o OpenStreetMap não mapeia um córrego o modelo não o enxerga.</li>",1)
rep("<li><b>Vegetação</b>: NDVI do Sentinel-2 (23/08/2026, estiagem), média por setor sem espelhos d'água; cobertura vegetal = área com NDVI ≥ 0,45.</li>",
    "<li><b>Vegetação</b>: NDVI do Sentinel-2 na estiagem (23/08/2026; a leste de 55,1° O, 17/08/2026), média por setor sem água, nuvem e sombra, segundo a classificação de cena do próprio produto; cobertura vegetal = área com NDVI ≥ 0,45. Pixels de 10 m na conurbação e nas sedes e distritos; de 40 m nos 246 setores que não cabem nesses recortes, quase todos rurais.</li>",1)
rep("<li><b>Temperatura de superfície</b>: Landsat 9, banda termal (13/08/2026, 10h45 local). Anomalia = diferença para a média dos setores urbanos (39,1 °C). Não é temperatura do ar.</li>",
    "<li><b>Temperatura de superfície</b>: Landsat 9, banda termal, 13/08/2026, 9h45 no horário de Mato Grosso (13h45 UTC). Pixels de 30 m na conurbação e nas sedes e distritos; amostra de 120 m nos demais setores (a banda termal tem 100 m de resolução original). Em 21 setores das bordas, fora da faixa dessa imagem, usam-se as de 12/08, 14/08 e 04/08/2026, ajustadas à de 13/08 pela diferença média na faixa comum. Anomalia = diferença para a média dos setores urbanos de Cuiabá e Várzea Grande (39,1 °C). Não é temperatura do ar.</li>",1)
rep("com as bandas B8 e B4 do Sentinel-2 L2A de 23/08/2026 (estiagem, reflectância de superfície, 10 m). NDVI do setor = média dos pixels, excluídos espelhos d’água.</li>",
    "com as bandas B8 e B4 do Sentinel-2 L2A (reflectância de superfície, estiagem): imagem de 23/08/2026 e, a leste de 55,1° O, onde ela não alcança, de 17/08/2026. NDVI do setor = média dos pixels cujo centro cai dentro do setor, excluídos os de água (classe 6 da classificação de cena, SCL), nuvem e sombra (classes 3, 8, 9 e 10) e sem dado. Pixels de 10 m quando o setor cabe inteiro num recorte de 10 m (conurbação, sedes e distritos: 1.694 setores); nos outros 246, pixels de 40 m, média 4 × 4 da mesma imagem.</li>",1)
rep("produto de temperatura de superfície Landsat 9 Collection 2 Nível 2, banda ST_B10 (30 m), imagem de 13/08/2026, 10h45: LST(°C) = ST_B10 × 0,00341802 + 149,0 − 273,15. LST do setor = média dos pixels.",
    "produto de temperatura de superfície Landsat 9 Collection 2 Nível 2, banda ST_B10, órbita 226, imagem de 13/08/2026, 13h45 UTC (9h45 em Mato Grosso): LST(°C) = ST_B10 × 0,00341802 + 149,0 − 273,15. LST do setor = média dos pixels sem nuvem nem sombra (QA_PIXEL): de 30 m na conurbação e nas sedes e distritos, e amostra de 120 m nos demais setores. Fora da faixa dessa imagem (21 setores), LST = LST da imagem vizinha + Δ, sendo Δ a diferença média para a imagem de 13/08 na faixa comum: +4,0 °C (Landsat 8, 12/08), −0,7 °C (Landsat 8, 14/08) e +2,0 °C (Landsat 9, 04/08).",1)
rep("<li><b>HAND</b> (Height Above Nearest Drainage; Rennó et al., 2008; Nobre et al., 2011): para cada célula do MDS Copernicus GLO-30, HAND = z(célula) − z(célula de drenagem para onde escoa). Classes: alta ≤ 2 m (córregos) ou ≤ 4 m (rios Cuiabá e Coxipó); média ≤ 5 m / 8 m; baixa ≤ 8 m / 12 m; só manchas conectadas à drenagem.</li>",
    "<li><b>Altura acima da drenagem</b> (forma simplificada do HAND, Height Above Nearest Drainage; Rennó et al., 2008; Nobre et al., 2011): para cada célula do MDS Copernicus GLO-30, H = z(célula) − z<sub>d</sub>, em que z<sub>d</sub> é a menor cota na vizinhança 3 × 3 da célula de drenagem mais próxima em linha reta, e a drenagem são os rios e córregos do OpenStreetMap. O HAND original usa a drenagem alcançada pelo caminho do escoamento; aqui usa-se a mais próxima em distância. Classes: alta ≤ 2 m (córregos) ou ≤ 4 m (rios Cuiabá e Coxipó; fora da conurbação, só o Rio Cuiabá); média ≤ 5 m / 8 m; baixa ≤ 8 m / 12 m; só manchas conectadas à drenagem. Abrangência: conurbação e sedes e distritos dos outros cinco municípios.</li>",1)
rep("calcula-se a altura acima da drenagem mais próxima para onde a água escoa (HAND).</li>","calcula-se a altura acima do rio ou córrego mais próximo em linha reta (forma simplificada do HAND).</li>",1)
rep("<dd>Modelo de superfície de 30 m e rede de drenagem derivada</dd>","<dd>Modelo de superfície de 30 m; rios e córregos do OpenStreetMap</dd>",1)
rep("Copernicus GLO-30 (ESA); método HAND (Rennó et al., 2008)","Copernicus GLO-30 (ESA); OpenStreetMap; HAND simplificado (Rennó et al., 2008)")
rep("<li>Calcula-se o NDVI em cada pixel de 10 m da imagem Sentinel-2 de 23/08/2026.</li>","<li>Calcula-se o NDVI em cada pixel da imagem Sentinel-2 (23/08/2026; a leste de 55,1° O, 17/08/2026): 10 m nas áreas urbanas, 40 m nos setores rurais extensos.</li>",1)
rep("<li>Divide-se pelo total de pixels do setor, fora da água.</li>","<li>Divide-se pelo total de pixels do setor, fora da água, de nuvem e de sombra.</li>",1)
rep("<li>Calcula-se o índice em cada pixel de 10 m.</li><li>Faz-se a média dos pixels do setor, excluindo espelhos d’água.</li>","<li>Calcula-se o índice em cada pixel (10 m nas áreas urbanas, 40 m nos setores rurais extensos).</li><li>Faz-se a média dos pixels do setor, excluindo água, nuvem e sombra.</li>",1)
rep("<dd>Copernicus Sentinel-2 L2A, 23/08/2026</dd>","<dd>Copernicus Sentinel-2 L2A, 17 e 23/08/2026</dd>",1)
rep('"ndvi": "Copernicus Sentinel-2 L2A, 23/08/2026"','"ndvi": "Copernicus Sentinel-2 L2A, 17 e 23/08/2026"',1)
rep("banda ST_B10, de 13/08/2026 às 10h45.</li>","banda ST_B10, de 13/08/2026 às 9h45 (horário de Mato Grosso); em 21 setores das bordas, imagens de datas vizinhas ajustadas a essa.</li>",1)
rep("<li>Faz-se a média dos pixels de 30 m do setor.</li>","<li>Faz-se a média dos pixels do setor (30 m nas áreas urbanas; amostra de 120 m nos setores rurais extensos).</li>",1)
rep("<dd>USGS – Landsat 9 Collection 2 Level-2</dd>","<dd>USGS – Landsat 8 e 9 Collection 2 Level-2</dd>",1)
rep('"lst": "USGS – Landsat 9 Collection 2 Level-2"','"lst": "USGS – Landsat 8 e 9 Collection 2 Level-2"',1)
rep("d:'Parte da área do setor com NDVI ≥ 0,45 (Sentinel-2, 23/08/2026).'","d:'Parte da área do setor com NDVI ≥ 0,45 (Sentinel-2, 17 e 23/08/2026).'",1)
rep("d:'Índice de vegetação médio do setor, de −1 a 1 (Sentinel-2, 23/08/2026).'","d:'Índice de vegetação médio do setor, de −1 a 1 (Sentinel-2, 17 e 23/08/2026).'",1)
rep("d:'Temperatura média da superfície no setor (Landsat 9, 13/08/2026, 10h45).'","d:'Temperatura média da superfície no setor (Landsat 9, 13/08/2026, 9h45 em Mato Grosso).'",1)
rep("d:'Diferença para a média dos setores urbanos (39,1 °C). Positivo = ilha de calor.'","d:'Diferença para a média dos setores urbanos de Cuiabá e Várzea Grande (39,1 °C). Positivo = ilha de calor.'",1)
rep("d:'Parte da área do setor na classe alta do modelo HAND.'","d:'Parte da área do setor até 2 m acima do córrego mais próximo (4 m no Rio Cuiabá e no Coxipó). Só áreas urbanas.'",1)
rep("ndvi:'Vegetação: NDVI Sentinel-2 (Copernicus/ESA), 23/08/2026',lst:'Temperatura de superfície: Landsat 9 (USGS), 13/08/2026',inund:'Suscetibilidade a inundação: modelo HAND sobre Copernicus GLO-30 (ESA)',",
    "ndvi:'Vegetação: NDVI Sentinel-2 (Copernicus/ESA), 17 e 23/08/2026',lst:'Temperatura de superfície: Landsat 9 (USGS), 13/08/2026; bordas: Landsat 8 e 9 de datas vizinhas',inund:'Suscetibilidade a inundação: altura acima da drenagem (OpenStreetMap) sobre Copernicus GLO-30 (ESA)',",1)
rep("bgName={ndvi:'Vegetação (NDVI) · Sentinel-2, 23/08/2026', lst:'Temperatura de superfície · Landsat 9, 13/08/2026', inund:'Suscetibilidade a inundação · modelo HAND (Copernicus GLO-30)',",
    "bgName={ndvi:'Vegetação (NDVI) · Sentinel-2, 17 e 23/08/2026', lst:'Temperatura de superfície · Landsat 9, 13/08/2026', inund:'Suscetibilidade a inundação · altura acima da drenagem (Copernicus GLO-30)',",1)
rep("'média 13/08/2026 (Cuiabá–VG)'","'média dos setores · 13/08/2026'",1)
rep("'moradores, susc. alta (Cuiabá–VG)'","'moradores, susc. alta (áreas urbanas)'",1)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('sat7 ok',n,len(H))
