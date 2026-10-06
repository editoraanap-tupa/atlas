# gera afer_sec.html: aferição dos indicadores em duas camadas (didática e técnica)
import html as _h
ST={'ok':'conferido','cal':'calibrado','res':'com ressalva'}
IT=[
 dict(n='População e domicílios',s='moradores e domicílios de cada setor',st='ok',
  q='A população do Atlas é a mesma do IBGE?',
  simples='Sim. Somando os moradores de todos os setores de cada município, o total é idêntico ao número oficial do Censo 2022.',
  tec='Soma da variável V0001 (moradores) dos setores de cada município comparada com a população residente da tabela 4714 do SIDRA/IBGE.',
  res='Diferença zero nos 7 municípios: 1.047.730 habitantes.',
  refazer='Baixe o CSV dos setores em Dados abertos, some a coluna de moradores por município e compare com a tabela 4714 do SIDRA.',
  onde='IBGE, SIDRA, tabela 4714 · <a href="#tabelas">Dados abertos</a>'),
 dict(n='Indicadores do Censo',s='demografia, cor ou raça, água, esgoto, lixo, banheiro, renda, alfabetização e entorno (24 indicadores)',st='ok',
  q='As porcentagens de cada setor foram calculadas corretamente?',
  simples='Sim. Refizemos todas as contas do zero, a partir dos arquivos originais do IBGE, e comparamos com o que o Atlas mostra. Não houve nenhuma diferença.',
  tec='Recálculo independente dos 24 indicadores para os 1.940 setores com as fórmulas do dicionário e comparação valor a valor; testes de faixa (0–100%), de soma (esgoto na rede + esgoto precário ≤ 100%) e de unicidade dos códigos de setor.',
  res='46.560 comparações, nenhuma divergência acima de 0,05 ponto percentual; nenhum valor fora de 0–100%; nenhum código repetido.',
  refazer='Abra os Agregados por Setores do Censo 2022 (IBGE), aplique a fórmula do indicador (dicionário, item 8 da Metodologia) a um setor e compare com a ficha do setor no mapa.',
  onde='<a href="#formulas">Dicionário (item 8)</a> · CSV em <a href="#tabelas">Dados abertos</a>'),
 dict(n='Geometria',s='área dos setores e dos municípios, densidade',st='ok',
  q='O desenho dos setores no mapa corresponde ao tamanho real?',
  simples='Sim. O contorno é simplificado para o mapa ficar leve, mas a diferença de área é mínima, e as contas usam sempre a área oficial.',
  tec='Área medida no polígono do mapa comparada com AREA_KM2 da malha do IBGE (setores) e com a área territorial oficial (municípios, SIDRA, variável 6318).',
  res='Setores: diferença mediana de 0,28%, 95% abaixo de 1,44%. Municípios: 0,1% a 0,2%.',
  refazer='Compare a área mostrada na ficha de um setor com o atributo AREA_KM2 da malha de setores do IBGE.',
  onde='IBGE, malha de setores 2022 e SIDRA (variável 6318)'),
 dict(n='IVSA',s='Índice de Vulnerabilidade Socioambiental',st='ok',
  q='O índice de vulnerabilidade segue mesmo a fórmula publicada?',
  simples='Sim. O índice foi recalculado fora do Atlas com a fórmula da Metodologia, e as médias de cada município deram os mesmos valores.',
  tec='Reimplementação da fórmula (normalização P2–P98, média dos componentes, regra dos 60%) e comparação das médias municipais ponderadas pela população.',
  res='Médias coincidem com as do painel. 1.799 setores recebem índice; 86 ficam sem por terem menos de 50 moradores e 55 por falta de dados.',
  refazer='Siga o item 2 da Metodologia com os valores de um setor no CSV e compare com o IVSA da ficha.',
  onde='<a href="#formulas">Metodologia, item 2</a>'),
 dict(n='Moradores em áreas de risco',s='APP, suscetibilidade a inundação, cheias, carta do SGB',st='ok',
  q='O número de moradores em áreas de risco faz sentido?',
  simples='É uma estimativa: se 20% da área do setor está na mancha, contam-se 20% dos moradores. Conferimos que nenhum setor passa da própria população e que os totais citados são a soma dos setores.',
  tec='Teste da regra moradores = população × fração da área e soma dos setores comparada com os totais dos textos e painéis.',
  res='Nenhum setor com estimativa acima da população. Totais iguais à soma dos setores, com diferenças de 3 a 4 pessoas por arredondamento.',
  refazer='Multiplique os moradores de um setor pela porcentagem de área em risco mostrada na ficha.',
  onde='<a href="#formulas">Metodologia, item 4</a>'),
 dict(n='Suscetibilidade a inundação e cheias',s='altura acima da drenagem mais próxima e cenários por cota do Rio Cuiabá',st='cal',
  q='O modelo de inundação acerta os lugares que realmente alagaram?',
  simples='O modelo foi ajustado até reproduzir os bairros alagados nas cheias de 1974 e 1995 e comparado com as áreas de risco mapeadas em campo pelo SGB. Acerta bem os córregos; para o Rio Cuiabá, usa-se o cenário por cota.',
  tec='Nível da régua de Cuiabá (ANA 66260001, zero a 139,36 m) convertido em altitude e estendido pelo perfil do rio; ajuste de +2 m (Copernicus GLO-30) e +2,5 m (ANADEM) calibrado com Terceiro, Praeirinho e Porto; comparação com os 38 setores de risco do SGB. Em 01/10/2026 a camada de suscetibilidade foi reconstituída de forma independente (altura do terreno acima do rio ou córrego mais próximo em linha reta, rede OpenStreetMap, MDS Copernicus GLO-30) e, com o mesmo procedimento, estendida às sedes e distritos dos outros cinco municípios.',
  res='30 dos 38 setores de risco tocam a classe alta do modelo; manchas de 1974 dos dois modelos de terreno com correlação +0,97. Reconstituição independente da camada: 83% dos pixels na mesma classe, mesmas proporções de área (12,7%, 14,3% e 13,8% contra 12,4%, 15,2% e 14,1%) e correlação +0,89 por setor; a diferença vem da versão da rede de córregos do OpenStreetMap.',
  refazer='As tabelas de calibração, com cada ajuste testado, estão nos subitens Cheias e Carta SGB.',
  onde='<a href="#validacao">Cheias: calibração</a> · <a href="#refino">Carta SGB: validação</a>'),
 dict(n='Carta de suscetibilidade do SGB',s='base oficial, escala 1:25.000',st='ok',
  q='O mapa oficial de risco confirma o modelo do Atlas?',
  simples='Em boa parte. A carta do Serviço Geológico é a referência oficial; onde ela e o modelo divergem, vale a carta.',
  tec='Rasterização da carta a 10 m e cruzamento com o HAND e com a mancha da cheia de 1974 por setor.',
  res='Correlação +0,55 com o HAND; 82,3% da mancha urbana de 1974 está nas classes alta ou média da carta. Em Chapada dos Guimarães, cuja carta (2025) foi incorporada em 01/10/2026, a correlação entre a classe alta da carta e a do modelo é de +0,85 nos 35 setores urbanos.',
  refazer='Compare, no mapa, a camada "Carta de suscetibilidade SGB" com "Suscetibilidade a inundação".',
  onde='<a href="#refino">Carta SGB: validação</a>'),
 dict(n='Vegetação',s='NDVI, cobertura vegetal, vegetação nativa, vegetação por habitante',st='ok',
  q='Duas fontes diferentes enxergam a mesma vegetação?',
  simples='Sim. A vegetação medida pela imagem do satélite Sentinel-2 e a do mapa anual do MapBiomas, feitas de modo independente, apontam para os mesmos lugares.',
  tec='Correlação entre cobertura vegetal (NDVI ≥ 0,45, Sentinel-2) e vegetação nativa (MapBiomas coleção 9, 30 m) nos 1.719 setores urbanos dos 7 municípios. Em 01/10/2026 todos os setores foram reprocessados de forma independente e comparados com os valores anteriores da conurbação; as duas datas de imagem foram comparadas na faixa comum; e as grades de 10 m e de 40 m, nos mesmos setores.',
  res='Cobertura vegetal × vegetação nativa: +0,78. NDVI × cobertura vegetal: +0,95. Reprocessamento × valores anteriores: correlação +0,98, diferença média de 0,003 no NDVI. Imagens de 17/08 e 23/08 na faixa comum: diferença média de 0,002 no NDVI, correlação +0,99. Grade de 40 m contra a de 10 m: mesmo NDVI médio (diferença de 0,003) e cobertura vegetal 3 pontos percentuais menor (1,9 ponto nos setores com mais de 1 km²).',
  refazer='Alterne no mapa as camadas "Vegetação (NDVI)" e "Cobertura e uso da terra".',
  onde='<a href="#ambiente">Meio físico</a> · <a href="#formulas">Metodologia, item 3</a>'),
 dict(n='Temperatura de superfície e anomalia térmica',s='Landsat 9, 13/08/2026, e datas vizinhas nas bordas',st='ok',
  q='Os lugares mais verdes aparecem mais frescos, como se espera?',
  simples='Sim. Onde há mais vegetação, a temperatura da superfície é menor. Vale lembrar: é a temperatura do chão e dos telhados em um dia, não a do ar.',
  tec='Correlação NDVI × temperatura de superfície nos setores urbanos e conferência da média usada como referência da anomalia. Em 01/10/2026 todos os setores foram reprocessados e comparados com os valores anteriores; onde a imagem de 13/08 não alcança, as imagens de 12/08, 14/08 e 04/08 foram comparadas com ela na faixa comum.',
  res='Correlação −0,66. Média simples dos setores urbanos de Cuiabá e Várzea Grande: 39,1 °C, igual à usada na fórmula da anomalia. Reprocessamento × valores anteriores: correlação +0,99, diferença média de 0,1 °C. Diferença média para a imagem de 13/08 na faixa comum: −4,0 °C (12/08), +0,7 °C (14/08) e −2,0 °C (04/08), com desvio-padrão de 0,9 a 1,3 °C; o ajuste foi usado em 21 setores das bordas.',
  refazer='Compare no mapa as camadas de vegetação e de temperatura.',
  onde='<a href="#formulas">Metodologia, item 3</a>'),
 dict(n='Bacias, sub-bacias e microbacias',s='IBGE e modelo de terreno ANADEM',st='ok',
  q='As bacias cobrem toda a região, sem falhas nem sobreposição?',
  simples='Sim. As bacias oficiais do IBGE cobrem 99% da área da região (a diferença é de borda), e cada ponto do terreno pertence a uma só microbacia.',
  tec='Soma das áreas das bacias recortadas comparada com a área oficial da RMVRC; teste de sobreposição célula a célula nas microbacias.',
  res='31.945 km² de 32.283 km² (99%); 162 microbacias urbanas, nenhuma sobreposição.',
  refazer='Tabelas de bacias e microbacias no subitem Meio físico.',
  onde='<a href="#ambiente">Meio físico</a>'),
 dict(n='Solos e vulnerabilidade à erosão',s='método de Crepani et al. (2001)',st='res',
  q='O mapa de erosão pode ser refeito por outra pessoa?',
  simples='Pode: a fórmula e todas as notas estão publicadas. A ressalva é que duas escolhas foram da equipe e merecem revisão de especialista: as notas de cada tipo de rocha e o valor único adotado para o clima.',
  tec='V = (G + R + S + Vg + C) ÷ 5, com notas de 1 a 3 por tema; áreas por classe somadas por município.',
  res='Cálculo reprodutível. Notas da geologia atribuídas pela equipe a partir da tabela original; clima fixado em 2,0 para toda a região.',
  refazer='Tabelas de notas no item 6 da Metodologia.',
  onde='<a href="#ambiente">Meio físico</a> · <a href="#formulas">Metodologia, item 6</a>'),
 dict(n='Equipamentos e distâncias',s='saúde, escolas, parques e praças',st='res',
  q='As distâncias até o posto de saúde, a escola e a praça estão certas?',
  simples='A conta está certa, mas é uma distância em linha reta, não o caminho pelas ruas. Além disso, escolas e praças vêm de um mapa colaborativo, que pode estar incompleto.',
  tec='Fórmula de Haversine do centro do setor ao equipamento mais próximo; busca de duplicatas por categoria e coordenada; recálculo com todos os equipamentos da RMVRC.',
  res='1.222 equipamentos após retirar 11 duplicatas; 82 distâncias corrigidas na auditoria.',
  refazer='A lista de equipamentos, com a fonte de cada um, está em Dados abertos (aba Equipamentos).',
  onde='CNES/DATASUS · OpenStreetMap · <a href="#tabelas">Dados abertos</a>'),
 dict(n='Saúde ambiental',s='DRSAI, doenças respiratórias, dengue',st='ok',
  q='Os números de internações podem ser conferidos no DATASUS?',
  simples='Sim. A página Metodologia traz exatamente quais opções marcar no TabNet para obter as mesmas tabelas. Conferimos também que a soma dos grupos de doenças dá o total.',
  tec='Tabulação no TabNet com parâmetros publicados (linha, coluna, medida, períodos, seleções); soma dos cinco grupos de DRSAI comparada com o total; taxas recalculadas.',
  res='Soma dos grupos igual ao total em todos os municípios e anos. Os dados são por município, não por setor.',
  refazer='Siga o item 9.1 da Metodologia no TabNet do DATASUS.',
  onde='<a href="#saude">Saúde</a> · <a href="#formulas">Metodologia, item 9</a>'),
 dict(n='Prioridade territorial (IPT)',s='Laboratório de Governança',st='cal',
  q='A ordem de prioridade muda se os pesos mudarem?',
  simples='Em muitos territórios, muda. Por isso cada um traz a "robustez": em quantas de 300 combinações diferentes de pesos ele continua entre os mais prioritários.',
  tec='300 conjuntos de pesos aleatórios (Dirichlet, semente fixa 20261001); fração dos sorteios em que o setor fica entre os 20% de maior nota.',
  res='Robustez informada ao lado de cada índice; a maioria dos territórios é sensível aos pesos.',
  refazer='O sorteio usa semente fixa: repetindo o procedimento do item 11.6 da Metodologia, obtém-se o mesmo resultado.',
  onde='<a href="#lab">Governança</a> · <a href="#formulas">Metodologia, item 11</a>'),
]
PEND=[
 ('Renda média do responsável','A média do município é quase exata.','Média dos setores ponderada pelos domicílios ocupados.','Ponderar pelo número de responsáveis com rendimento de cada setor.','Pequeno: os dois pesos são muito parecidos, mas não idênticos.'),
 ('Renda mediana','A mediana do município é só indicativa.','Média ponderada das medianas dos setores.','A mediana de um município não se obtém das medianas dos setores; exigiria os microdados do Censo.','No setor, a mediana é a do IBGE; no agregado, use a renda média.'),
 ('Analfabetismo 15+','A média do município é uma boa aproximação.','Ponderado pelos moradores do setor.','Ponderar pela população de 15 anos ou mais.','Pequeno; maior onde há muitas crianças.'),
 ('Entorno urbano (arborização, pavimento, calçada, bueiro, iluminação, ônibus)','A média do município é uma boa aproximação.','Ponderado pelos moradores do setor.','Ponderar pelos moradores do universo da pesquisa de entorno (faces de quadra).','Pequeno nas áreas urbanas consolidadas.'),
 ('Cobertura vegetal e vegetação nativa','Só importa em setores com rio largo ou lagoa.','Ponderado pela área total do setor.','Ponderar pela área fora da água, que é o denominador do indicador.','Desprezível na maioria dos setores.'),
 ('Temperatura de superfície','Há duas médias, com usos diferentes.','Média ponderada pela área: 38,5 °C nos setores urbanos da conurbação.','A anomalia térmica usa a média simples dos setores: 39,1 °C.','A referência da anomalia é 39,1 °C em todo o Atlas; os dois critérios não se confundem.'),
 ('Cheias de 1974 e 1995 (ANADEM)','Duas tabelas diferem em 1 pessoa.','Cenários: 28.233 e 34.521 moradores; calibração: 28.232 e 34.520.','Mesmo arredondamento nas duas tabelas.','Diferença de 1 pessoa, por arredondamento.'),
]
E=_h.escape
cards=''.join(f"""<details class='dcard acard'><summary><b>{E(i['n'])}</b><span>{E(i['s'])}</span><span class='afs {i['st']}'>{ST[i['st']]}</span></summary>
<div class='ac-q'><span>Pergunta</span>{E(i['q'])}</div>
<div class='ac-a'><span>Em palavras simples</span>{E(i['simples'])}</div>
<dl><dt>Como foi aferido</dt><dd>{E(i['tec'])}</dd><dt>Resultado</dt><dd>{E(i['res'])}</dd><dt>Como refazer</dt><dd>{E(i['refazer'])}</dd><dt>Onde conferir</dt><dd>{i['onde']}</dd></dl></details>""" for i in IT)
prow=''.join(f"<tr><td class='l'><b>{E(a)}</b><br><small class='mu'>{E(b)}</small></td><td class='l'>{E(c)}</td><td class='l'>{E(d)}</td><td class='l'>{E(e)}</td></tr>" for a,b,c,d,e in PEND)
nok=sum(1 for i in IT if i['st']=='ok'); ncal=sum(1 for i in IT if i['st']=='cal'); nres=sum(1 for i in IT if i['st']=='res')
OUT=f'''<div class="sec-h" id="afericao" style="scroll-margin-top:calc(var(--tb) + 12px)"><span class="kick">Metodologia · dados abertos e auditáveis</span><h2>Aferição dos indicadores</h2><p>Como saber se os números do Atlas estão certos? Cada família de indicadores foi conferida de um jeito. Aqui está a pergunta feita, a resposta em palavras simples e, para quem quiser refazer, o procedimento técnico.</p></div>
<section class="block" id="afer-b">
  <div class="kpis vk">
    <div class="kpi"><div class="lab">Comparações com o IBGE</div><div class="val">46.560</div><div class="sub">1.940 setores × 24 indicadores do Censo, nenhuma divergência</div></div>
    <div class="kpi"><div class="lab">População</div><div class="val">1.047.730</div><div class="sub">igual à do IBGE (SIDRA 4714) nos 7 municípios</div></div>
    <div class="kpi"><div class="lab">Área dos setores</div><div class="val">0,28%</div><div class="sub">diferença mediana entre o mapa e a área oficial</div></div>
    <div class="kpi"><div class="lab">Famílias aferidas</div><div class="val">{len(IT)}</div><div class="sub">{nok} conferidas, {ncal} calibradas, {nres} com ressalva</div></div>
  </div>
  <div class="aferhow">
    <div><span class="afs ok">conferido</span><p>O valor foi comparado com a fonte oficial, ou com uma segunda fonte independente, e bateu.</p></div>
    <div><span class="afs cal">calibrado</span><p>É um modelo. Foi ajustado até reproduzir fatos observados, como os bairros alagados em cheias conhecidas.</p></div>
    <div><span class="afs res">com ressalva</span><p>A conta está certa e pode ser refeita, mas depende de uma escolha de método que é declarada.</p></div>
  </div>
  <h3 class="h3s">Aferição por família de indicadores</h3>
  <p class="note">Clique em uma linha para abrir a resposta simples e o detalhe técnico.</p>
  <div class="aferlist">{cards}</div>
  <h3 class="h3s">Pendências nas médias de município, bairro e microbacia</h3>
  <p class="note">Em palavras simples: os valores de cada <b>setor</b> reproduzem o Censo. Quando o Atlas junta vários setores para dar o valor de um município, bairro ou microbacia, algumas médias são aproximadas, porque o peso exato não está nos arquivos públicos. A tabela diz quais, e quanto isso importa.</p>
  <div class="tblwrap" style="max-height:none"><table class="dt afer"><thead><tr><th class="l">Indicador</th><th class="l">Como o Atlas agrega hoje</th><th class="l">O que seria exato</th><th class="l">Efeito</th></tr></thead><tbody>{prow}</tbody></table></div>
  <div class="split" style="margin-top:16px">
    <div>
      <h3>Como refazer a conferência</h3>
      <ol class="note">
        <li>Baixe os dados em <a href="#tabelas">Dados abertos</a> (CSV dos setores e GeoJSON).</li>
        <li>Abra os Agregados por Setores do Censo 2022 no site do IBGE; os endereços estão em <a href="#metodo">Fontes</a>.</li>
        <li>Escolha um setor e aplique a fórmula do indicador, que está no dicionário da <a href="#formulas">Metodologia</a>.</li>
        <li>Compare o resultado com a ficha do setor no mapa.</li>
      </ol>
    </div>
    <div>
      <h3>Limites declarados</h3>
      <ul class="note">
        <li>IVSA com menos componentes em 366 setores, quase todos rurais, por falta da pesquisa de entorno.</li>
        <li>Cheias do Rio Cuiabá só na conurbação Cuiabá–Várzea Grande. Carta do SGB só em Cuiabá, Várzea Grande e Chapada dos Guimarães: os outros quatro municípios não têm carta publicada. Suscetibilidade a inundação só em áreas urbanas (conurbação, sedes e distritos); 3 distritos sem córregos mapeados no OpenStreetMap ficam sem dado.</li>
        <li>Nos 246 setores que não cabem nos recortes de alta resolução, quase todos rurais, a vegetação usa pixels de 40 m e a temperatura, amostra de 120 m; a cobertura vegetal fica cerca de 2 pontos abaixo da que seria medida a 10 m.</li>
        <li>A suscetibilidade a inundação mede a altura acima do rio ou córrego mais próximo em linha reta, e não pelo caminho da água: é uma triagem, mais simples que o HAND completo.</li>
        <li>Distâncias em linha reta, só com equipamentos dentro da RMVRC.</li>
        <li>Em 209 setores o IBGE oculta células pequenas da pirâmide etária (sigilo).</li>
        <li>Cheias e microbacias usam modelo de terreno de 30 m: servem para planejamento, não para o lote.</li>
        <li>Moradores em APP e em manchas de inundação são população × fração da área: não localizam pessoas nem edificações.</li>
      </ul>
      <p class="note">A auditoria completa dos dados censitários, da geometria e dos cruzamentos foi feita em 01/10/2026. Os módulos acrescentados depois (saúde, ODS, vegetação por habitante e Laboratório) foram conferidos aritmeticamente na geração. Vegetação, temperatura e suscetibilidade a inundação foram reprocessadas e estendidas aos 7 municípios em 01/10/2026.</p>
    </div>
  </div>
</section>
'''
open('/home/claude/d/afer_sec.html','w').write(OUT)
