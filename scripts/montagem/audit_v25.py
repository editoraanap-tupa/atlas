s=open('/home/claude/d/auditoria/auditoria_atlas_rmvrc_v10.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)
rep('<p class="lede">Varredura completa dos 1.940 setores censitários, das camadas espaciais e dos textos do Atlas, feita na versão de trabalho depois da cópia de segurança de 01/10/2026. Cada número foi refeito a partir das bases oficiais ou testado quanto à coerência interna.</p>',
    '<p class="lede">Varredura completa dos 1.940 setores censitários, das camadas espaciais e dos textos do Atlas. A primeira auditoria foi feita na versão 10; esta reauditoria repete todos os testes na versão 25, depois que as camadas de satélite e de inundação foram reprocessadas e estendidas aos 7 municípios. Cada número foi refeito a partir das bases oficiais ou testado quanto à coerência interna.</p>')
rep('Auditoria realizada em 01/10/2026 · Atlas: versão 10 (cópia de segurança) e versão 11 (com as correções desta auditoria) ·','Auditoria de 01/10/2026 (versões 10 e 11) · Reauditoria de 01/10/2026, à noite (versão 25) ·')
rep('<div class="big">Os dados censitários estão corretos e reproduzíveis. Os cruzamentos espaciais estão coerentes. Foram corrigidos 4 problemas e há 9 pontos de atenção de método.</div>',
    '<div class="big">Os dados censitários continuam corretos e reproduzíveis na versão 25. Vegetação e temperatura agora cobrem os 1.940 setores; a suscetibilidade a inundação, as áreas urbanas dos 7 municípios. Foram corrigidos 9 problemas e há 12 pontos de atenção de método.</div>')
rep('<p>A população de todos os municípios bate exatamente com o IBGE e os 24 indicadores do Censo foram recalculados do zero para os 1.940 setores sem nenhuma divergência. As camadas ambientais se comportam como esperado entre si (correlações com o sinal e a força previstos). Os problemas encontrados eram de atualização e de apresentação, não de cálculo, e já foram corrigidos no Atlas.</p>',
    '<p>A população de todos os municípios bate exatamente com o IBGE e os 24 indicadores do Censo foram recalculados do zero para os 1.940 setores sem nenhuma divergência, nas duas rodadas. As camadas ambientais se comportam como esperado entre si. Na reauditoria, vegetação, temperatura e inundação foram recalculadas de forma independente: os valores anteriores foram reproduzidos (correlação de +0,98 a +0,99), a descrição do modelo de inundação foi corrigida e a carta do SGB de Chapada dos Guimarães foi incorporada.</p>')
rep('<div class="s-ok"><b>14</b><span>verificações sem problema</span></div>','<div class="s-ok"><b>22</b><span>verificações sem problema</span></div>')
rep('<div class="s-fix"><b>4</b><span>problemas corrigidos</span></div>','<div class="s-fix"><b>9</b><span>problemas corrigidos</span></div>')
rep('<div class="s-warn"><b>9</b><span>pontos de atenção</span></div>','<div class="s-warn"><b>12</b><span>pontos de atenção</span></div>')
# seção 5
rep('<td class="num">+0,95</td><td class="num">1.585</td>','<td class="num">+0,95</td><td class="num">1.719</td>')
rep('<td class="num">−0,69</td><td class="num">1.585</td>','<td class="num">−0,66</td><td class="num">1.719</td>')
rep('<td class="num">+0,76</td><td class="num">1.585</td>','<td class="num">+0,78</td><td class="num">1.719</td>')
rep('<tr><td class="l">HAND × carta oficial do SGB</td><td class="num">+0,55</td><td class="num">1.628</td>','<tr><td class="l">Modelo de inundação × carta oficial do SGB</td><td class="num">+0,55</td><td class="num">1.663</td>')
rep('<td class="num">−0,03</td><td class="num">1.514</td><td class="l">sem relação: medem coisas diferentes (ver ponto de atenção 8)</td>','<td class="num">−0,04</td><td class="num">1.632</td><td class="l">sem relação: medem coisas diferentes (ver pontos de atenção)</td>')
rep('nos setores urbanos. Todos os pares se comportam como esperado:</p>','nos setores urbanos. Valores da versão 25, com os setores urbanos dos 7 municípios. Todos os pares se comportam como esperado:</p>')
NEW='''<section class="chk">
  <div class="hd"><span class="n">8</span><h2>Reprocessamento e extensão das camadas de satélite e de inundação</h2><span class="chip c-ok">Conferido</span></div>
  <p>Em 01/10/2026 a vegetação (Sentinel-2), a temperatura de superfície (Landsat) e a suscetibilidade a inundação foram recalculadas com rotinas novas, guardadas na cópia de segurança, e estendidas aos 7 municípios. O recálculo serviu também de teste independente dos valores que já existiam para Cuiabá e Várzea Grande.</p>
  <div class="tbl"><table><thead><tr><th class="l">Teste</th><th class="l">Resultado</th><th class="l">Leitura</th></tr></thead><tbody>
  <tr><td class="l">Área dos setores na grade de 10 m × área oficial</td><td class="l">razão mediana de 0,999 (P5–P95: 0,986–1,013)</td><td class="l">a contagem de pixels por centro reproduz a área do setor</td></tr>
  <tr><td class="l">NDVI e cobertura vegetal: recálculo × valores anteriores (1.613 setores)</td><td class="l">correlação +0,98 nos dois; diferença média de 0,003 no NDVI e de 0,1 ponto na cobertura</td><td class="l">valores anteriores reproduzidos; diferenças de borda de setor</td></tr>
  <tr><td class="l">Sentinel-2 de 17/08 × 23/08/2026 na faixa comum (2,2 milhões de pixels)</td><td class="l">NDVI médio 0,452 e 0,454; correlação +0,99</td><td class="l">as duas datas são equivalentes na estiagem</td></tr>
  <tr><td class="l">Grade de 40 m × grade de 10 m nos mesmos 1.751 setores</td><td class="l">NDVI médio igual (diferença de 0,003); cobertura vegetal 3,1 pontos menor a 40 m (1,9 nos setores com mais de 1 km²)</td><td class="l">limite declarado para os 246 setores calculados a 40 m</td></tr>
  <tr><td class="l">Temperatura: recálculo × valores anteriores (1.613 setores)</td><td class="l">correlação +0,99; diferença média absoluta de 0,1 °C; média urbana de Cuiabá e Várzea Grande 39,08 °C</td><td class="l">referência de 39,1 °C confirmada</td></tr>
  <tr><td class="l">Landsat de datas vizinhas × 13/08/2026 na faixa comum</td><td class="l">12/08: −4,0 °C (correlação +0,93); 14/08: +0,7 °C (+0,97); 04/08: −2,0 °C (+0,95); desvio-padrão de 0,9 a 1,3 °C</td><td class="l">ajuste por diferença média, usado em 21 setores das bordas</td></tr>
  <tr><td class="l">Modelo de inundação: reconstituição independente × camada original (conurbação)</td><td class="l">83% dos pixels na mesma classe; áreas de 12,7%, 14,3% e 13,8% contra 12,4%, 15,2% e 14,1%; correlação +0,89 por setor</td><td class="l">método identificado e reproduzido; diferença atribuída à versão da rede de córregos do OpenStreetMap</td></tr>
  <tr><td class="l">Modelo de inundação × carta do SGB em Chapada dos Guimarães (35 setores urbanos)</td><td class="l">correlação +0,85</td><td class="l">o modelo estendido concorda com a carta oficial onde ela existe</td></tr>
  </tbody></table></div>
  <div class="tbl"><table><thead><tr><th class="l">Cobertura na versão 25 (% dos setores com dado)</th><th>Vegetação</th><th>Temperatura</th><th>Inundação (modelo)</th><th>Carta do SGB</th></tr></thead><tbody>
  <tr><td class="l">Cuiabá</td><td class="num">100</td><td class="num">100</td><td class="num">99</td><td class="num">100</td></tr>
  <tr><td class="l">Várzea Grande</td><td class="num">100</td><td class="num">100</td><td class="num">100</td><td class="num">100</td></tr>
  <tr><td class="l">Acorizal</td><td class="num">100</td><td class="num">100</td><td class="num">42</td><td class="num">sem carta</td></tr>
  <tr><td class="l">Campo Verde</td><td class="num">100</td><td class="num">100</td><td class="num">64</td><td class="num">sem carta</td></tr>
  <tr><td class="l">Chapada dos Guimarães</td><td class="num">100</td><td class="num">100</td><td class="num">47</td><td class="num">100</td></tr>
  <tr><td class="l">Nossa Senhora do Livramento</td><td class="num">100</td><td class="num">100</td><td class="num">26</td><td class="num">sem carta</td></tr>
  <tr><td class="l">Santo Antônio de Leverger</td><td class="num">100</td><td class="num">100</td><td class="num">26</td><td class="num">sem carta</td></tr>
  </tbody></table></div>
  <p class="meta">O modelo de inundação é calculado só para setores urbanos (127 dos 130 dos cinco municípios novos); por isso a porcentagem é menor onde há muitos setores rurais. Antes da versão 25, vegetação, temperatura e inundação existiam só para Cuiabá e Várzea Grande.</p>
</section>

'''
i=s.index('<section class="chk">\n  <div class="hd"><span class="n">8</span><h2>Correções feitas nesta auditoria</h2>')
s=s[:i]+NEW+s[i:]
rep('<span class="n">8</span><h2>Correções feitas nesta auditoria</h2>','<span class="n">9</span><h2>Correções feitas nas duas auditorias</h2>')
rep('<span class="n">9</span><h2>Pontos de atenção</h2>','<span class="n">10</span><h2>Pontos de atenção</h2>')
# novas correções: acrescenta linhas ao fim da tabela da seção 9
i=s.index('<span class="n">9</span><h2>Correções feitas nas duas auditorias</h2>'); j=s.index('</tbody>',i)
ROWS='''  <tr><td class="l"><b>Reauditoria (versão 25).</b> A metodologia descrevia o modelo de inundação como HAND pelo caminho do escoamento, com rede de drenagem derivada do terreno. A reconstituição mostrou que a camada mede a altura acima do rio ou córrego mais próximo em linha reta, com a rede do OpenStreetMap.</td><td class="l">Descrição, fórmula e dicionário corrigidos; o método passou a ser chamado de forma simplificada do HAND e o limite foi declarado.</td></tr>
  <tr><td class="l">Hora da imagem Landsat informada como “10h45 local”. A passagem foi às 13h45 UTC, isto é, 9h45 no horário de Mato Grosso (10h45 é o horário de Brasília).</td><td class="l">Corrigido em todos os textos para 9h45 (horário de Mato Grosso).</td></tr>
  <tr><td class="l">Vegetação, temperatura e inundação existiam só para Cuiabá e Várzea Grande; 295 setores dos outros municípios e 17 setores rurais de Cuiabá ficavam sem dado.</td><td class="l">Vegetação e temperatura calculadas para os 1.940 setores; inundação, para 127 dos 130 setores urbanos dos cinco municípios novos.</td></tr>
  <tr><td class="l">A carta de suscetibilidade do SGB de Chapada dos Guimarães (2025) não estava no Atlas.</td><td class="l">Incorporada a partir do RIGeo (doc/25797.2, arquivos vetoriais na versão 2, de julho de 2026): mapa e indicador nos 75 setores do município.</td></tr>
  <tr><td class="l">O Atlas não informava as licenças das bases nem a licença do próprio conteúdo; o rodapé citava só o Landsat 9.</td><td class="l">Incluídas a seção “Licenças, direitos de uso e atribuição das fontes”, com os avisos exigidos pelo Copernicus e pelo OpenStreetMap, e a licença CC BY 4.0 do Atlas.</td></tr>
'''
s=s[:j]+ROWS+s[j:]
# pontos de atenção
a=s.index('    <article class="hi"><h4>Camadas de satélite e modelo só em Cuiabá e Várzea Grande</h4>'); b=s.index('    <article><h4>Distâncias em linha reta e efeito de borda</h4>')
ATT='''    <article class="hi"><h4>Modelo de inundação: método simplificado e rede de córregos incompleta</h4>
      <p>O modelo mede a altura do terreno acima do rio ou córrego mais próximo em linha reta, e não pelo caminho que a água percorre, como no HAND original. Depende da rede do OpenStreetMap: onde um córrego não está mapeado, o modelo não o enxerga, e em terreno plano aparecem manchas de contorno reto. Três distritos sem nenhum córrego mapeado ficaram sem dado.</p>
      <p class="rec"><b>Recomendação:</b> manter como triagem, sempre abaixo da carta do SGB onde ela existe; avaliar, com especialista em hidrologia, a troca pelo HAND por caminho de escoamento sobre o MDT ANADEM.</p></article>
    <article class="hi"><h4>Camada de inundação da conurbação não é reproduzida pixel a pixel</h4>
      <p>A rotina original da camada de Cuiabá e Várzea Grande não foi guardada. A reconstituição independente chega a 83% de concordância de pixels e correlação de +0,89 por setor; a diferença vem da versão da rede de córregos do OpenStreetMap. A camada original foi mantida porque é a que foi validada com os setores de risco do SGB.</p>
      <p class="rec"><b>Recomendação:</b> decidir se a conurbação deve ser recalculada com a rotina nova, refazendo depois as tabelas de validação, para que os 7 municípios usem exatamente o mesmo procedimento.</p></article>
    <article><h4>Setores rurais com resolução menor</h4>
      <p>Nos 246 setores que não cabem nos recortes de alta resolução, quase todos rurais, a vegetação usa pixels de 40 m e a temperatura uma amostra de 120 m. O NDVI médio não muda; a cobertura vegetal fica cerca de 2 pontos percentuais abaixo da que seria medida a 10 m. A ficha e o CSV informam a imagem e a grade de cada setor.</p></article>
    <article><h4>Temperatura de 21 setores vem de datas vizinhas</h4>
      <p>A imagem Landsat de 13/08/2026 não cobre o extremo oeste de Livramento, parte de Acorizal e o extremo leste de Campo Verde e de Leverger. Nesses setores a temperatura vem de imagens de 12/08, 14/08 ou 04/08, ajustadas pela diferença média na faixa comum, com incerteza de cerca de 1 °C.</p></article>
'''
s=s[:a]+ATT+s[b:]
rep('<p>Método da auditoria: recálculo independente em Python a partir dos arquivos originais do IBGE (Agregados por Setores Censitários, malha de setores), consulta à API SIDRA do IBGE (tabela 4714) para população e área oficiais, testes de coerência interna em todos os setores, réplica do IVSA, recálculo das distâncias e correlações entre bases independentes. A cópia de segurança da versão auditada (01/10/2026) está guardada separadamente, com o HTML, o PDF de metodologia, os dados em CSV e GeoJSON e os scripts.</p>',
    '<p>Método da auditoria: recálculo independente em Python a partir dos arquivos originais do IBGE (Agregados por Setores Censitários, malha de setores), consulta à API SIDRA do IBGE (tabela 4714) para população e área oficiais, testes de coerência interna em todos os setores, réplica do IVSA, recálculo das distâncias e correlações entre bases independentes. Na reauditoria, vegetação e temperatura foram recalculadas a partir das imagens Sentinel-2 e Landsat originais, e o modelo de inundação, a partir do Copernicus GLO-30 e da rede do OpenStreetMap. As cópias de segurança das versões auditadas (01/10/2026) estão guardadas separadamente, com o HTML, o PDF de metodologia, os dados em CSV e GeoJSON e os scripts.</p>')
open('/home/claude/d/auditoria/auditoria_atlas_rmvrc.html','w').write(s); print('auditoria ok',len(s), s.count('<article'))
