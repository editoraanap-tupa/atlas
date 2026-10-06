# ================= metodologia detalhada: fórmulas e bases de cálculo =================
import json as _j, html as _h
H=open('/home/claude/d/atlas_rmvrc.html').read()
def r5(old,new,n=1):
    global H
    c=H.count(old); assert c==n,(c,old[:100]); H=H.replace(old,new)
RES=_j.load(open('/home/claude/f/resultado.json'))
DL=str(RES['delta']).replace('.',',')
P='Percentual'
# fórmula, variáveis e fonte de cada indicador
FORM={
 'ivsa':('IVSA = 100 × Σ(wⱼ·zᵢⱼ) / Σwⱼ — ver quadro do IVSA','Componentes normalizados do próprio Atlas','Elaboração própria'),
 'pop':('POP = V0001','V0001 = total de pessoas residentes no setor','IBGE, Censo 2022 – Agregados por setores, Básico'),
 'dens':('DENS = V0001 / ÁREA','ÁREA = AREA_KM2 da malha de setores (km²)','IBGE, Censo 2022 – Básico e malha de setores'),
 'criancas':('100 × (V01031 + V01032) / V0001','V01031 = 0 a 4 anos; V01032 = 5 a 9 anos','IBGE, Censo 2022 – Demografia'),
 'idosos':('100 × (V01040 + V01041) / V0001','V01040 = 60 a 69 anos; V01041 = 70 anos ou mais','IBGE, Censo 2022 – Demografia'),
 'negros':('100 × (V01318 + V01320) / V0001','V01318 = cor ou raça preta; V01320 = parda','IBGE, Censo 2022 – Cor ou raça'),
 'indig':('100 × V01321 / V0001','V01321 = cor ou raça indígena','IBGE, Censo 2022 – Cor ou raça'),
 'mor':('MOR = V0005','V0005 = média de moradores em domicílios particulares permanentes ocupados (DPPO)','IBGE, Censo 2022 – Básico'),
 'agua':('100 × V00111 / V0007','V00111 = DPPO que utilizam rede geral de distribuição; V0007 = total de DPPO','IBGE, Censo 2022 – Características do domicílio 2'),
 'agua_enc':('100 × V00199 / V0007','V00199 = DPPO com água encanada até dentro da casa','IBGE, Censo 2022 – Características do domicílio 2'),
 'esgoto':('100 × (V00309 + V00310) / V0007','V00309 = esgoto na rede geral ou pluvial; V00310 = fossa séptica ligada à rede','IBGE, Censo 2022 – Características do domicílio 2'),
 'esg_prec':('100 × (V00312 + V00313 + V00314 + V00315 + V00316) / V0007','fossa rudimentar ou buraco; vala; rio, lago ou córrego; outra forma; sem banheiro nem sanitário','IBGE, Censo 2022 – Características do domicílio 2'),
 'lixo':('100 × (V00397 + V00398) / V0007','V00397 = coletado no domicílio; V00398 = depositado em caçamba do serviço de limpeza','IBGE, Censo 2022 – Características do domicílio 2'),
 'sem_banh':('100 × V00495 / V0007','V00495 = DPPO sem banheiro de uso exclusivo com chuveiro e vaso','IBGE, Censo 2022 – Características do domicílio 2'),
 'renda':('RENDA = V06004','V06004 = rendimento nominal médio mensal das pessoas responsáveis com rendimento (R$)','IBGE, Censo 2022 – Rendimento do responsável (2026)'),
 'renda_med':('RENDA_MED = V06006','V06006 = rendimento nominal mediano mensal das pessoas responsáveis com rendimento (R$)','IBGE, Censo 2022 – Rendimento do responsável (2026)'),
 'analf':('100 × V00901 / (V00900 + V00901)','V00900 = pessoas de 15 anos ou mais que sabem ler e escrever; V00901 = que não sabem','IBGE, Censo 2022 – Alfabetização'),
 'arvore':('100 × (V05231 + V05232 + V05233) / V05200','V05200 = moradores em DPPO do setor pesquisado no entorno; V05231–V05233 = moradores em face com 1–2, 3–4 e 5 ou mais árvores','IBGE, Censo 2022 – Entorno dos domicílios (moradores)'),
 'arv5':('100 × V05233 / V05200','V05233 = moradores em face com 5 ou mais árvores','IBGE, Censo 2022 – Entorno dos domicílios'),
 'pav':('100 × V05206 / V05200','V05206 = moradores em face com via pavimentada','IBGE, Censo 2022 – Entorno dos domicílios'),
 'calcada':('100 × V05221 / V05200','V05221 = moradores em face com calçada','IBGE, Censo 2022 – Entorno dos domicílios'),
 'bueiro':('100 × V05209 / V05200','V05209 = moradores em face com bueiro ou boca de lobo','IBGE, Censo 2022 – Entorno dos domicílios'),
 'luz':('100 × V05212 / V05200','V05212 = moradores em face com iluminação pública','IBGE, Censo 2022 – Entorno dos domicílios'),
 'onibus':('100 × V05215 / V05200','V05215 = moradores em face com ponto de ônibus ou van','IBGE, Censo 2022 – Entorno dos domicílios'),
 'app_pct':('100 × A(setor ∩ APP) / A(setor − água)','A = área; APP = faixas marginais da Lei 12.651/2012 sobre a hidrografia (ver quadro)','Elaboração própria; hidrografia OpenStreetMap'),
 'app_pop':('POP × app_pct / 100','Supõe ocupação uniforme dentro do setor','Elaboração própria'),
 'inund':('100 × A(setor ∩ HAND alta) / A(setor)','HAND alta: até 2 m acima do córrego ou 4 m acima dos rios Cuiabá e Coxipó','Elaboração própria; Copernicus GLO-30'),
 'inund_pop':('POP × inund / 100','Supõe ocupação uniforme','Elaboração própria'),
 'c1974':('100 × A(setor ∩ mancha 1974, GLO-30) / A(setor)','Mancha: terreno abaixo do nível da cheia de 1974 ligado ao rio (ver quadro das cheias)','Elaboração própria; Copernicus GLO-30; SUDEC-MT'),
 'c1974_pop':('POP × c1974 / 100','Supõe ocupação uniforme','Elaboração própria'),
 'sgb_alta':('100 × A(setor ∩ classe alta SGB) / A(setor)','Rasterização a 10 m dos polígonos da carta','SGB/CPRM, Cartas de Suscetibilidade 1:25.000'),
 'sgb_alta_pop':('POP × sgb_alta / 100','Supõe ocupação uniforme','Elaboração própria; SGB/CPRM'),
 'a1974':('100 × A(setor ∩ mancha 1974, ANADEM) / A(setor)','Mancha recalculada com o MDT ANADEM e ajuste de +'+DL+' m','Elaboração própria; ANADEM (ANA/UFRGS)'),
 'a1974_pop':('POP × a1974 / 100','Supõe ocupação uniforme','Elaboração própria'),
 'alerta':('100 × A(setor ∩ mancha da cota de alerta) / A(setor)','Cota de alerta = 8,50 m na régua (147,86 m de altitude)','Elaboração própria; SUDEC-MT'),
 'veg_nat':('100 × Nₙₐₜ / (N − Nₐ)','N = pixels de 30 m do setor; Nₙₐₜ = pixels das classes 3, 4, 5, 6, 11, 12, 49 e 50; Nₐ = pixels de água (classes 31 e 33)','MapBiomas coleção 9, 2023'),
 'erosao':('V = (G + R + S + Vg + C) / 5, média dos pixels do setor','G geologia, R relevo, S solos, Vg cobertura, C clima (escores de 1 a 3; ver quadro)','Elaboração própria; IBGE BDiA; MapBiomas'),
 'eros_alta':('100 × N(V ≥ 2,25) / N(V)','Pixels de 30 m com índice de vulnerabilidade à erosão ≥ 2,25','Elaboração própria'),
 'verde':('100 × N(NDVI ≥ 0,45) / (N − Nₐ)','Pixels de 10 m do setor fora de espelhos d’água','Sentinel-2, 23/08/2026'),
 'ndvi':('NDVI = (B8 − B4) / (B8 + B4); média dos pixels do setor','B8 = infravermelho próximo (842 nm); B4 = vermelho (665 nm)','Sentinel-2 L2A, 23/08/2026'),
 'lst':('LST = média dos pixels do setor de (ST_B10 × 0,00341802 + 149,0) − 273,15','ST_B10 = banda de temperatura de superfície (produto Nível 2), em °C','Landsat 9 Collection 2, 13/08/2026 10h45'),
 'lst_anom':('ΔT = LST_setor − 39,1 °C','39,1 °C = média da LST dos setores urbanos da conurbação','Elaboração própria; Landsat 9'),
 'd_ubs':('D = min 2R·asin√[sin²(Δφ/2) + cosφ₁·cosφ₂·sin²(Δλ/2)]','Distância de Haversine (R = 6.371 km) do centro do setor à USF/UBS mais próxima; arredondada a 10 m','CNES/DATASUS'),
 'd_saude':('D = min Haversine(centro do setor, UPA/pronto-socorro/hospital SUS)','Mesma fórmula; arredondada a 10 m','CNES/DATASUS'),
 'd_esc':('D = min Haversine(centro do setor, escola ou creche)','Mesma fórmula; arredondada a 10 m','OpenStreetMap'),
 'd_parque':('D = min Haversine(centro do setor, parque, praça ou reserva)','Mesma fórmula; arredondada a 10 m','OpenStreetMap'),
}
exec(open('/home/claude/d/dicio.py').read())
FORM={k:(v['formula'],v['vars'],v['fonte']) for k,v in DIC.items()}
FONTE_IND={k:v['fonte'] for k,v in DIC.items()}
# ---- JS: fórmula no cabeçalho do mapa e no PDF
i=H.index('const byK = Object.fromEntries')
H=H[:i]+'const FORM = '+_j.dumps({k:v[0] for k,v in FORM.items()},ensure_ascii=False)+';\nconst FONTE_IND = '+_j.dumps(FONTE_IND,ensure_ascii=False)+';\n'+H[i:]
r5("IND.filter(i=>i.ax===ax).forEach(i=>para(`${i.n}${i.u?` (${i.u})`:''}: ${i.d}`,{bullet:true,indent:6,size:9.5,gap:1}));",
   "IND.filter(i=>i.ax===ax).forEach(i=>{ para(`${i.n}${i.u?` (${i.u})`:''}: ${i.d}`,{bullet:true,indent:6,size:9.5,gap:0}); if(FORM[i.k]) para(`Fórmula: ${FORM[i.k]} · Fonte: ${FONTE_IND[i.k]}`,{indent:16,size:8.5,gap:2,color:'0.25 0.30 0.45'}); });")
# ---- seção HTML
AXN={'ind':'Índice composto','dem':'Demografia','san':'Saneamento','ren':'Renda e alfabetização','ent':'Entorno urbano','amb':'Ambiente e risco','ace':'Acesso a serviços'}
import re
a=H.index('const IND = ['); b=H.index('];',a)
inds=re.findall(r"\{k:'(\w+)',ax:'(\w+)',n:'([^']*)',u:'([^']*)',pol:'(\w)'",H[a:b])
POL={'b':'maior = melhor','r':'maior = pior','n':'neutro'}
POLT={'b':'Quanto maior, melhor','r':'Quanto maior, pior','n':'Indicador descritivo (neutro)'}
cards={}
for k,ax,n,u,pol in inds:
    d=DIC.get(k)
    if not d: continue
    passos=''.join(f"<li>{_h.escape(p)}</li>" for p in d['passos'])
    cards.setdefault(ax,[]).append(f"""<details class='dcard' data-k='{k}'><summary><b>{_h.escape(n)}</b><span>{u or 'índice'} · {POLT[pol]}</span></summary>
<dl><dt>O que mede</dt><dd>{_h.escape(d['mede'])}</dd>
<dt>Fórmula</dt><dd><code class='fml'>{_h.escape(d['formula'])}</code></dd>
<dt>Como é calculado</dt><dd><ol>{passos}</ol></dd>
<dt>Variáveis e bases</dt><dd>{_h.escape(d['vars'])}</dd>
<dt>Fonte oficial</dt><dd>{_h.escape(d['fonte'])}</dd>
<dt>Como interpretar</dt><dd>{_h.escape(d['ler'])}</dd></dl></details>""")
rows=''.join(f"<h4 class='dax'>{AXN[ax]}</h4>"+''.join(cards[ax]) for ax in ['ind','dem','san','ren','ent','amb','ace'] if ax in cards)
WROWS=''.join(f"<tr><td class='l'>{n}</td><td class='l'>{v}</td><td class='l'>{s}</td><td class='num'>{w}</td></tr>" for n,v,s,w in [
 ('Analfabetismo','analf','quanto maior, mais vulnerável','1'),('Esgoto fora da rede','esgoto','invertido (1 − z)','1'),('Lixo sem coleta','lixo','invertido','1'),('Água fora da rede','agua','invertido','1'),
 ('Renda baixa','renda (em log)','invertido','1'),('Falta de árvores na rua','arvore','invertido','1'),('Falta de pavimento','pav','invertido','1'),
 ('Suscetibilidade a inundação','inund','direto','0'),('Suscetibilidade (carta SGB)','sgb_alta','direto','0'),('Pouca vegetação nativa','veg_nat','invertido','0'),('Vulnerabilidade à erosão','erosao','direto','0'),
 ('Ocupação de APP','app_pct','direto','0'),('Calor de superfície','lst','direto','0'),('Pouca vegetação (NDVI)','verde','invertido','0'),('Longe da USF/UBS','d_ubs (em log)','direto','0')])
GTAB=[('Depósitos aluvionares, terraços, Formação Pantanal, depósitos coluviais','3,0'),('Formação Xaraiés (calcários tufáceos)','2,9'),('Coberturas detrito-lateríticas','2,8'),('Ponta Grossa, Palermo, Sepotuba (folhelhos e siltitos)','2,7'),('Diamantino (siltitos, arcóseos)','2,6'),('Marília, Salto das Nuvens, Aquidauana (arenitos e conglomerados)','2,5'),('Furnas, Botucatu, Utiariti, Rio Ivaí, Moenda, Raizama (arenitos)','2,4'),('Bauxi (metassedimentos)','2,2'),('Grupo Cuiabá (filitos, xistos, metarenitos)','1,7'),('Serra Geral, Tapirapuã, Vulcânicas de Mimoso (basaltos)','1,5'),('Intrusivas Ponta do Morro','1,2'),('Granito São Vicente','1,1')]
STAB=[('Latossolos','1,0'),('Argissolos, Planossolos','2,0'),('Cambissolos','2,5'),('Neossolos, Plintossolos, Gleissolos, Vertissolos, Organossolos, afloramentos','3,0')]
VTAB=[('Formação florestal, floresta alagável','1,2'),('Formação savânica','1,7'),('Silvicultura','2,0'),('Formação campestre, campo alagado','2,2'),('Área urbanizada','2,5'),('Mosaico de usos','2,6'),('Pastagem','2,8'),('Soja, cana, algodão, outras lavouras temporárias','2,9'),('Outras áreas não vegetadas, mineração, afloramento rochoso','3,0')]
RTAB=[('Planícies, terraços e planos de acumulação','1,0 (rampa de colúvio: 1,5)'),('Pediplanos (aplanamento)','1,0 (desnudados: 1,2)'),('Dissecação: média entre o escore do topo (tabular 1,3; convexo 1,7; aguçado 2,2) e a média dos escores de densidade de drenagem e de aprofundamento da incisão','1,0 a 3,0'),('Densidade de drenagem: muito baixa 1,0; baixa 1,5; média 2,0; alta 2,5; muito alta 3,0','—'),('Aprofundamento da incisão: muito fraco 1,0; fraco 1,5; médio 2,0; forte 2,5; muito forte 3,0','—'),('Encosta íngreme de erosão','3,0')]
tb=lambda rows,h1,h2: f"<div class='tblwrap' style='max-height:none'><table class='dt'><thead><tr><th class='l'>{h1}</th><th>{h2}</th></tr></thead><tbody>"+''.join(f"<tr><td class='l' style='white-space:normal'>{a}</td><td class='num'>{b}</td></tr>" for a,b in rows)+"</tbody></table></div>"
sec=f"""<div class="sec-h" id="formulas" style="scroll-margin-top:calc(var(--tb) + 12px)"><span class="kick">Descrição do método</span><h2>Metodologia detalhada: fórmulas e bases de cálculo</h2><p>Para que cada número do Atlas possa ser conferido e reproduzido, esta seção descreve a unidade de análise, a fórmula de cada indicador, as variáveis do IBGE e as bases usadas, e o passo a passo dos índices compostos e dos cruzamentos espaciais. As camadas apenas exibidas (hidrografia, divisas, bacias, solos, cobertura da terra) têm a fonte indicada no rodapé do mapa.</p></div>
<section class="block metodo">
  <div class="split">
    <div>
      <h3>1. Unidade de análise e convenções</h3>
      <ul class="msg" style="padding-left:18px;margin:0 0 12px">
        <li><b>Unidade:</b> setor censitário do Censo 2022 (malha <code>MT_setores_CD2022</code>), identificado pelo código de 15 dígitos. Os valores de cada setor vêm dos Agregados por Setores Censitários do IBGE e das bases espaciais listadas.</li>
        <li><b>Percentuais:</b> P = 100 × numerador / denominador. O denominador é o universo indicado na fórmula: pessoas (V0001), domicílios particulares permanentes ocupados – DPPO (V0007) ou moradores do setor pesquisado no entorno (V05200).</li>
        <li><b>Sigilo:</b> quando o IBGE publica <code>X</code> (sigilo estatístico), a célula é tratada como zero dentro de uma soma de categorias e como “sem dado” quando é o único termo do numerador.</li>
        <li><b>Cruzamentos espaciais:</b> as bases em polígono ou em imagem são convertidas em grade regular (10 m para a carta do SGB e o MDT; 30 m para MapBiomas e erosão; 5 m para APP nos novos municípios). A fração do setor é f = A(setor ∩ camada) / A(setor), medida pelo número de células da grade dentro do polígono do setor.</li>
        <li><b>Moradores estimados:</b> M = POP × f. Supõe distribuição uniforme da população dentro do setor; é uma estimativa, não uma contagem.</li>
        <li><b>Médias municipais e da RMVRC</b> (painel lateral e quadros): médias ponderadas Σ(xᵢ·wᵢ)/Σwᵢ, com peso w = moradores (indicadores de pessoas), DPPO (indicadores de domicílio) ou área (indicadores de território); somas para contagens; densidade = ΣPOP/ΣÁREA.</li>
        <li><b>Classes do mapa:</b> quintis (20% dos setores em cada classe) ou intervalos iguais entre o menor e o maior valor, à escolha do usuário.</li>
      </ul>
      <h3>2. Índice de Vulnerabilidade Socioambiental (IVSA)</h3>
      <p class="msg">Para cada setor i com 50 ou mais moradores e cada componente j:</p>
      <p class="fml">zᵢⱼ = min(1, max(0, (xᵢⱼ − P2ⱼ) / (P98ⱼ − P2ⱼ)))</p>
      <p class="msg">P2ⱼ e P98ⱼ são os percentis 2 e 98 do componente entre todos os setores da RMVRC com 50 ou mais moradores (limita o efeito de valores extremos). Renda e distância à USF/UBS entram em logaritmo natural (x = ln x). Quando o valor maior indica situação melhor (ex.: esgoto na rede), usa-se z′ = 1 − z; nos demais, z′ = z.</p>
      <p class="fml">IVSAᵢ = 100 × Σⱼ wⱼ·z′ᵢⱼ / Σⱼ wⱼ  (somando só os componentes com dado)</p>
      <p class="msg">O setor recebe índice apenas se os componentes com dado somarem pelo menos 60% do peso total. O IVSA vai de 0 (menor vulnerabilidade relativa) a 100 (maior). Os pesos wⱼ são ajustáveis na seção “Pesos do IVSA”; o padrão é:</p>
      <div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th class="l">Componente</th><th class="l">Variável</th><th class="l">Sentido</th><th>Peso padrão</th></tr></thead><tbody>{WROWS}</tbody></table></div>
      <p class="msg" style="margin-top:6px">Classificação na ficha: quintis do IVSA entre todos os setores com índice (muito baixa, baixa, média, alta, muito alta). Ranking: posição do setor em ordem decrescente de IVSA.</p>
    </div>
    <div>
      <h3>3. Vegetação e temperatura</h3>
      <ul class="msg" style="padding-left:18px;margin:0 0 12px">
        <li><b>NDVI</b> (Rouse et al., 1974): NDVI = (NIR − Red) / (NIR + Red), com as bandas B8 e B4 do Sentinel-2 L2A de 23/08/2026 (estiagem, reflectância de superfície, 10 m). NDVI do setor = média dos pixels, excluídos espelhos d’água.</li>
        <li><b>Cobertura vegetal (NDVI)</b> = % dos pixels com NDVI ≥ 0,45 (limiar de vegetação densa na estiagem).</li>
        <li><b>Vegetação nativa (MapBiomas)</b> = % dos pixels de 30 m do setor, excluída a água, nas classes naturais do MapBiomas coleção 9, ano 2023: 3 formação florestal, 4 formação savânica, 5 mangue, 6 floresta alagável, 11 campo alagado e área pantanosa, 12 formação campestre, 49 restinga arbórea, 50 restinga herbácea. Silvicultura (9), pastagem, lavouras e mosaico de usos não contam como vegetação nativa. Os totais municipais usam a mesma fórmula sobre todos os pixels do município.</li>
        <li><b>Temperatura de superfície (LST):</b> produto de temperatura de superfície Landsat 9 Collection 2 Nível 2, banda ST_B10 (30 m), imagem de 13/08/2026, 10h45: LST(°C) = ST_B10 × 0,00341802 + 149,0 − 273,15. LST do setor = média dos pixels. É a temperatura da superfície (telhados, asfalto, solo), não a do ar.</li>
        <li><b>Anomalia térmica:</b> ΔT = LST do setor − 39,1 °C, sendo 39,1 °C a média da LST dos setores urbanos de Cuiabá e Várzea Grande. ΔT &gt; 0 indica ilha de calor relativa.</li>
      </ul>
      <h3>4. Inundação, cheias e APP</h3>
      <ul class="msg" style="padding-left:18px;margin:0 0 12px">
        <li><b>HAND</b> (Height Above Nearest Drainage; Rennó et al., 2008; Nobre et al., 2011): para cada célula do MDS Copernicus GLO-30, HAND = z(célula) − z(célula de drenagem para onde escoa). Classes: alta ≤ 2 m (córregos) ou ≤ 4 m (rios Cuiabá e Coxipó); média ≤ 5 m / 8 m; baixa ≤ 8 m / 12 m; só manchas conectadas à drenagem.</li>
        <li><b>Cheias por cota:</b> altitude do nível na régua de Cuiabá (ANA 66260001): Z = 139,36 m + leitura (m). Ao longo do rio: N(s) = Z + [S(s) − S(s₀)] + Δ, onde S(s) é o perfil da lâmina d’água do modelo de terreno (mínimo do terreno no leito, ajustado por regressão isotônica decrescente para jusante e suavizado), s₀ é a posição da régua e Δ o ajuste de calibração (+2 m no GLO-30; +{DL} m no ANADEM). Uma célula está alagada se z(célula) &lt; N(s) do trecho de rio mais próximo e se estiver conectada ao rio por células também alagadas (até 12 km do rio).</li>
        <li><b>Calibração:</b> Δ foi escolhido testando valores de 0 a 3 m e comparando a área alagada com os bairros atingidos em 1974 (Terceiro, Porto) e 1995 (Praeirinho, Cristo Rei).</li>
        <li><b>APP:</b> faixas da Lei 12.651/2012, art. 4º, desenhadas sobre a hidrografia: 100 m (Rio Cuiabá), 50 m (Rio Coxipó), 30 m (demais rios e córregos), 30 m no entorno de lagos e lagoas e raio de 50 m nas nascentes. A área de água é excluída do denominador.</li>
        <li><b>Carta do SGB:</b> classes alta, média e baixa de suscetibilidade a inundação (1:25.000) rasterizadas a 10 m; fração e moradores pelas fórmulas do item 1.</li>
      </ul>
      <h3>5. Acesso a serviços</h3>
      <p class="msg">Distância em linha reta (Haversine, R = 6.371,0088 km) do centróide do polígono do setor até o equipamento mais próximo da categoria, arredondada a 10 m: d = 2R·asin√[sin²(Δφ/2) + cos φ₁ cos φ₂ sin²(Δλ/2)]. Não considera o sistema viário; é um indicador de proximidade, não de tempo de deslocamento.</p>
    </div>
  </div>
  <h3 style="margin-top:18px">6. Vulnerabilidade natural à erosão hídrica (Crepani et al., 2001)</h3>
  <p class="msg">Método da Ecodinâmica (Tricart, 1977) adaptado por Crepani et al. (INPE, 2001). Cada tema recebe um escore de estabilidade de 1,0 (estável, predomínio da pedogênese) a 3,0 (vulnerável, predomínio da morfogênese), e o índice de cada célula de 30 m é a média aritmética dos cinco temas:</p>
  <p class="fml">V = (G + R + S + Vg + C) / 5</p>
  <p class="msg">G = geologia (IBGE, Base Contínua de Geologia 1:250.000); R = relevo (IBGE, Base Contínua de Geomorfologia 1:250.000); S = solos (IBGE, Base Contínua de Pedologia 1:250.000); Vg = cobertura da terra (MapBiomas 2023); C = clima, adotado constante igual a 2,0 para a RMVRC (intensidade pluviométrica de ≈ 200–230 mm/mês na estação chuvosa, faixa média da tabela de Crepani). Se faltar um tema (água, área urbana sem solo mapeado), a média usa os temas disponíveis mais o clima, desde que existam ao menos três. Classes: estável 1,0–1,3; moderadamente estável 1,4–1,7; medianamente estável/vulnerável 1,8–2,2; moderadamente vulnerável 2,3–2,6; vulnerável 2,7–3,0. Indicadores do setor: média de V e percentual da área com V ≥ 2,25.</p>
  <div class="split" style="margin-top:8px">
    <div>{tb(GTAB,'Geologia (unidade litoestratigráfica)','G')}<div style="height:10px"></div>{tb(STAB,'Solos (ordem, SiBCS)','S')}</div>
    <div>{tb(RTAB,'Relevo (IBGE, geomorfologia)','R')}<div style="height:10px"></div>{tb(VTAB,'Cobertura da terra (MapBiomas)','Vg')}</div>
  </div>
  <h3 style="margin-top:18px">7. Bacias, sub-bacias e microbacias hidrográficas</h3>
  <p class="msg">Limites da base de Bacias Hidrográficas do IBGE (ottocodificação de Pfafstetter), recortados pelos limites municipais da RMVRC. Bacias: nível 4 (nível 3 ou 5 onde o nível 4 não cobre o território). Sub-bacias: nível 6 dentro da bacia correspondente; onde não há nível 6, usa-se o nível 5 e, na falta dele, a própria bacia (curso principal e interbacias). Cada setor recebe a bacia e a sub-bacia que ocupam a maior parte da sua área.</p>
  <p class="msg"><b>Microbacias urbanas</b> (elaboração própria): 1) recorte do MDT ANADEM (30 m) sobre as áreas urbanas; 2) “queima” da hidrografia do OpenStreetMap no terreno (rebaixamento de 5 m ao longo dos cursos d’água, para que a drenagem siga os córregos mapeados); 3) preenchimento de depressões e direções de escoamento pelo algoritmo priority-flood (Barnes et al., 2014), que também resolve áreas planas; 4) área de contribuição acumulada de cada célula; 5) exutórios: ponto mais a jusante de cada córrego ou ribeirão com nome (um por trecho contínuo) e confluências de afluentes sem nome com 2 km² ou mais que deságuam em cursos maiores; 6) cada célula é atribuída ao primeiro exutório a jusante, o que gera microbacias encaixadas (a microbacia de um afluente é descontada da do córrego principal); 7) mantêm-se as microbacias com pelo menos 0,05 km² de setores urbanos (afluentes sem nome: 1 km² de área total). Rios (Cuiabá, Coxipó etc.) não formam microbacia própria. Cada setor urbano recebe a microbacia que ocupa a maior parte da sua área. Limitação: pixel de 30 m e galerias pluviais não representadas; os limites são aproximados e devem ser conferidos com levantamentos municipais.</p>
  <h3 style="margin-top:18px">8. Dicionário completo dos indicadores</h3>
  <p class="msg">Clique em cada indicador para ver o que ele mede, a fórmula, o passo a passo do cálculo, as variáveis usadas, a fonte oficial e como interpretar o resultado. Os códigos V… são os nomes das variáveis nos arquivos de Agregados por Setores Censitários do IBGE, o que permite refazer qualquer cálculo a partir dos dados públicos.</p>
  <div class="dgrid">{rows}</div>
  <h3 style="margin-top:18px">Referências do método</h3>
  <ul class="msg" style="padding-left:18px;margin:0">
    <li>CREPANI, E. et al. <i>Sensoriamento remoto e geoprocessamento aplicados ao zoneamento ecológico-econômico e ao ordenamento territorial</i>. São José dos Campos: INPE, 2001.</li>
    <li>TRICART, J. <i>Ecodinâmica</i>. Rio de Janeiro: IBGE/SUPREN, 1977.</li>
    <li>RENNÓ, C. D. et al. HAND, a new terrain descriptor using SRTM-DEM. <i>Remote Sensing of Environment</i>, v. 112, 2008. NOBRE, A. D. et al. Height Above the Nearest Drainage. <i>Journal of Hydrology</i>, v. 404, 2011.</li>
    <li>BARNES, R.; LEHMAN, C.; MULLA, D. Priority-flood: an optimal depression-filling and watershed-labeling algorithm. <i>Computers &amp; Geosciences</i>, v. 62, 2014.</li>
    <li>ROUSE, J. W. et al. Monitoring vegetation systems in the Great Plains with ERTS. NASA, 1974.</li>
    <li>IBGE. Censo Demográfico 2022: Agregados por Setores Censitários — dicionário de dados. Rio de Janeiro: IBGE, 2025–2026.</li>
    <li>USGS. Landsat 8-9 Collection 2 Level-2 Science Product Guide. 2023. · MAPBIOMAS. Coleção 9 da Série Anual de Mapas de Cobertura e Uso da Terra do Brasil. 2024.</li>
    <li>BRASIL. Lei nº 12.651, de 25 de maio de 2012 (Código Florestal), art. 4º.</li>
  </ul>
</section>
"""
r5('<div class="sec-h" id="sobre"',sec+'<div class="sec-h" id="sobre"')
r5('<a href="#metodo">Método</a>','<a href="#formulas">Fórmulas</a><a href="#metodo">Fontes</a>')
H=H.replace('.fml{display:block;','.metodo code{font-size:12px;white-space:normal}\n.dgrid{margin-top:8px}\n.dax{font:800 12px var(--f-display);letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:16px 0 6px;padding-bottom:4px;border-bottom:2px solid var(--gold)}\n.dcard{border:1px solid var(--line);border-radius:10px;margin-bottom:6px;background:var(--panel)}\n.dcard summary{cursor:pointer;padding:9px 12px;display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;list-style:none}\n.dcard summary::-webkit-details-marker{display:none}\n.dcard summary::before{content:"\\25B8";color:var(--accent);margin-right:2px}\n.dcard[open] summary::before{content:"\\25BE"}\n.dcard summary span{font-size:12px;color:var(--muted)}\n.dcard dl{margin:0;padding:0 14px 12px;display:grid;grid-template-columns:150px minmax(0,1fr);gap:6px 14px;font-size:13.5px}\n.dcard dt{font-weight:700;color:var(--muted);font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;padding-top:2px}\n.dcard dd{margin:0}\n.dcard ol{margin:0;padding-left:18px}\n@media (max-width:640px){.dcard dl{grid-template-columns:minmax(0,1fr)}}\n.metodo td{vertical-align:top}\n.metodo .tblwrap td.l{white-space:normal}\np.fml{margin:6px 0}\n.fml{display:block;',1)
open('/home/claude/d/atlas_rmvrc.html','w').write(H)
print('metodo ok',len(H)/1e6)
