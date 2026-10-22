# Pós-processamento do módulo Explorar/Desigualdade/Políticas (executado no fim de assemble.py, depois de audit_fix.py)
import re as _re, json as _j
H=open('/home/claude/d/atlas_rmvrc.html').read()
def _rep(a,b,n=1):
    global H
    assert H.count(a)==n,(H.count(a),a[:80]); H=H.replace(a,b)

# 1. pesos alterados -> refaz as análises visíveis
_rep("recomputeIVSA(); render(); }, 120);","recomputeIVSA(); render(); if(window.__xpDirty) window.__xpDirty(); }, 120);")

# 3. Metodologia: seções 13 e 14; Referências passa a 15
MET13='''<div id="metodo-xp-pdf"><h3 style="margin-top:18px" id="metodo-xp">13. Análise espacial, desigualdade e validação</h3>
<p>A página <a href="#desig">Desigualdade</a> calcula tudo no navegador, a partir dos mesmos setores e indicadores do mapa. As agregações por território usam a mesma ponderação do Atlas (por domicílios, moradores ou área, conforme o indicador). Sorteios usam semente fixa, de modo que os resultados se repetem.</p>
<h4>13.1 Autocorrelação espacial (Moran global e LISA)</h4><ul>
<li><b>Vizinhança:</b> os 6 setores mais próximos pelo centroide (distância plana com correção do cosseno da latitude), pesos padronizados por linha (w<sub>ij</sub> = 1/6). Entram os setores com 50 ou mais moradores e com o dado.</li>
<li><b>Moran global:</b> I = Σ<sub>i</sub> z<sub>i</sub> · L<sub>i</sub> ÷ Σ<sub>i</sub> z<sub>i</sub>², em que z<sub>i</sub> é o valor padronizado do setor e L<sub>i</sub> a média de z nos 6 vizinhos (Moran, 1950). Pseudo-valor p = (número de permutações com I maior ou igual ao observado + 1) ÷ (999 + 1).</li>
<li><b>LISA:</b> I<sub>i</sub> = z<sub>i</sub> · L<sub>i</sub> (Anselin, 1995), com pseudo-valor p por 199 permutações condicionais (o valor do setor fica fixo e os vizinhos são sorteados entre os demais). Setores com p &lt; 0,05 são classificados como alto-alto, baixo-baixo, alto-baixo ou baixo-alto conforme os sinais de z<sub>i</sub> e L<sub>i</sub>. Não há correção para comparações múltiplas: os agrupamentos indicam onde verificar, não provam um padrão.</li></ul>
<h4>13.2 Desigualdade de renda entre setores</h4><ul>
<li><b>Variável e peso:</b> renda média dos responsáveis com rendimento no setor (IBGE, Censo 2022), ponderada pelo número de responsáveis com rendimento (ou pelos domicílios, na falta desse dado).</li>
<li><b>Gini:</b> 1 − 2 × área sob a curva de Lorenz ponderada (regra dos trapézios), com os setores em ordem crescente de renda (Gini, 1912).</li>
<li><b>Theil T:</b> T = Σ<sub>i</sub> s<sub>i</sub> (y<sub>i</sub>/μ) ln(y<sub>i</sub>/μ), com s<sub>i</sub> = peso do setor ÷ peso total (Theil, 1967). Decomposição: T = Σ<sub>m</sub> S<sub>m</sub> T<sub>m</sub> (dentro dos municípios) + Σ<sub>m</sub> S<sub>m</sub> ln(μ<sub>m</sub>/μ) (entre municípios), em que S<sub>m</sub> é a parcela do município na renda total.</li>
<li><b>Razão P90/P10:</b> percentil 90 ÷ percentil 10 das rendas médias dos setores.</li>
<li><b>Limite:</b> por usar médias de setor, os índices medem a desigualdade entre lugares e subestimam a desigualdade entre pessoas (falácia ecológica).</li></ul>
<h4>13.3 Gradiente social dos serviços</h4><ul>
<li>Setores em ordem crescente de renda média; a população acumulada define cinco grupos com o mesmo número de moradores (cada setor vai para o grupo em que cai o ponto médio da sua população). O Atlas compara o primeiro grupo (20% de moradores nos setores de menor renda) com o último (20% de maior renda), com a agregação ponderada de cada indicador.</li>
<li>Diferença em pontos percentuais para indicadores em %; razão (mais pobres ÷ mais ricos) para os demais.</li></ul>
<h4>13.4 Validação do IVSA</h4><ul>
<li><b>Validade convergente:</b> área sob a curva ROC (AUC), estimada pela estatística de Mann-Whitney: proporção de pares (setor de favela ou comunidade urbana do IBGE, setor comum) em que o primeiro tem IVSA maior, contando empates como meio (Hanley; McNeil, 1982). Universo: setores urbanos de Cuiabá e Várzea Grande com IVSA. AUC = 0,5 indica acaso; 1, separação perfeita. Complementa: correlação de Spearman do IVSA com variáveis que não entram no índice (cor ou raça, crianças de 0 a 9 anos, moradores por domicílio e suscetibilidade alta a inundação).</li>
<li><b>Robustez aos pesos:</b> 300 conjuntos de pesos sorteados de uma distribuição de Dirichlet com α = 1 (pesos uniformes no simplex) sobre os componentes do IVSA com peso padrão, mantendo a normalização e a regra dos 60% de peso disponível. Mede-se a proporção dos setores do quintil mais vulnerável (com os pesos padrão) que permanecem nesse quintil em pelo menos 80% dos sorteios (OECD; JRC, 2008; Saltelli et al., 2008).</li>
<li><b>Sensibilidade a cada componente:</b> recalcula-se o índice sem cada componente e mede-se a correlação de Spearman com o índice completo.</li></ul>
<h3 style="margin-top:18px" id="metodo-pol">14. Subsídios a políticas públicas</h3>
<ul>
<li><b>Posição relativa:</b> para cada indicador com sentido definido (maior é melhor ou maior é pior), calcula-se a parcela dos moradores da RMVRC (setores com 50 ou mais moradores) que vivem em setores em situação melhor que o valor agregado do território, contando os empates pela metade. <b>Crítico:</b> território pior que a média da RMVRC, com diferença acima de 1 ponto percentual (indicadores em %) ou de 5% (demais), e posição de 80% ou mais; <b>atenção:</b> mesma condição, com posição de 60% a 79%; <b>favorável:</b> não pior que a média e posição de até 20%; <b>intermediário:</b> os demais. A exigência de diferença em relação à média evita classificar como crítico um valor igual ao da região em indicadores com muitos setores em zero. Indicadores do entorno, vegetação, calor e inundação comparam só os setores urbanos, do território e da RMVRC (valor de referência e distribuição).</li>
<li><b>Dimensionamento:</b> domicílios a ligar = máx(0; meta × domicílios ocupados − domicílios atendidos), com as metas de 99% de água e 90% de esgoto até 2033 (Lei nº 14.026/2020, que alterou a Lei nº 11.445/2007); moradores a mais de 1 km em linha reta de uma USF/UBS (CNES).</li>
<li><b>Ações e instrumentos:</b> cada indicador em situação crítica ou de atenção aciona um eixo (saneamento; drenagem e risco; habitação e entorno; áreas verdes e calor; mobilidade; saúde; renda, educação e assistência), com ações típicas, a legislação federal de referência, os indicadores de monitoramento e os órgãos responsáveis. As ações são orientações gerais, a detalhar nos planos municipais.</li>
<li><b>Setores prioritários:</b> os dez setores com 50 ou mais moradores de maior nota na lente do Índice de Prioridade Territorial com maior média no território.</li>
<li><b>Limites:</b> o diagnóstico é relativo à RMVRC, usa o Censo 2022 e as camadas do Atlas e não substitui levantamento de campo, cadastros municipais nem a participação social.</li></ul></div>
'''
_rep('<h3 style="margin-top:18px">13. Referências</h3>',MET13+'<h3 style="margin-top:18px">15. Referências</h3>')

# 4. Referências (lista HTML e PDF), em ordem alfabética
NEWR=['ANSELIN, L. Local indicators of spatial association – LISA. <i>Geographical Analysis</i>, v. 27, n. 2, p. 93–115, 1995.',
'BRASIL. Lei nº 8.742, de 7 de dezembro de 1993. Dispõe sobre a organização da Assistência Social. <i>Diário Oficial da União</i>, Brasília, 8 dez. 1993.',
'BRASIL. Lei nº 10.257, de 10 de julho de 2001. Estatuto da Cidade. <i>Diário Oficial da União</i>, Brasília, 11 jul. 2001.',
'BRASIL. Lei nº 11.445, de 5 de janeiro de 2007. Estabelece as diretrizes nacionais para o saneamento básico. <i>Diário Oficial da União</i>, Brasília, 8 jan. 2007.',
'BRASIL. Lei nº 12.305, de 2 de agosto de 2010. Institui a Política Nacional de Resíduos Sólidos. <i>Diário Oficial da União</i>, Brasília, 3 ago. 2010.',
'BRASIL. Lei nº 12.587, de 3 de janeiro de 2012. Institui as diretrizes da Política Nacional de Mobilidade Urbana. <i>Diário Oficial da União</i>, Brasília, 4 jan. 2012.',
'BRASIL. Lei nº 12.608, de 10 de abril de 2012. Institui a Política Nacional de Proteção e Defesa Civil. <i>Diário Oficial da União</i>, Brasília, 11 abr. 2012.',
'BRASIL. Lei nº 13.005, de 25 de junho de 2014. Aprova o Plano Nacional de Educação. <i>Diário Oficial da União</i>, Brasília, 26 jun. 2014.',
'BRASIL. Lei nº 13.089, de 12 de janeiro de 2015. Institui o Estatuto da Metrópole. <i>Diário Oficial da União</i>, Brasília, 13 jan. 2015.',
'BRASIL. Lei nº 13.146, de 6 de julho de 2015. Institui a Lei Brasileira de Inclusão da Pessoa com Deficiência. <i>Diário Oficial da União</i>, Brasília, 7 jul. 2015.',
'BRASIL. Lei nº 13.465, de 11 de julho de 2017. Dispõe sobre a regularização fundiária rural e urbana. <i>Diário Oficial da União</i>, Brasília, 12 jul. 2017.',
'BRASIL. Lei nº 14.285, de 29 de dezembro de 2021. Altera a Lei nº 12.651/2012 quanto às áreas de preservação permanente no entorno de cursos d’água em áreas urbanas consolidadas. <i>Diário Oficial da União</i>, Brasília, 30 dez. 2021.',
'BRASIL. Lei nº 14.904, de 27 de junho de 2024. Estabelece diretrizes para a elaboração de planos de adaptação à mudança do clima. <i>Diário Oficial da União</i>, Brasília, 28 jun. 2024.',
'BRASIL. Ministério da Saúde. Portaria nº 2.436, de 21 de setembro de 2017. Aprova a Política Nacional de Atenção Básica. <i>Diário Oficial da União</i>, Brasília, 22 set. 2017.',
'GINI, C. <i>Variabilità e mutabilità</i>: contributo allo studio delle distribuzioni e delle relazioni statistiche. Bologna: Tipografia di Paolo Cuppini, 1912.',
'HANLEY, J. A.; McNEIL, B. J. The meaning and use of the area under a receiver operating characteristic (ROC) curve. <i>Radiology</i>, v. 143, n. 1, p. 29–36, 1982.',
'MORAN, P. A. P. Notes on continuous stochastic phenomena. <i>Biometrika</i>, v. 37, n. 1/2, p. 17–23, 1950.',
'OECD; JRC. <i>Handbook on constructing composite indicators</i>: methodology and user guide. Paris: OECD Publishing, 2008.',
'SALTELLI, A. et al. <i>Global sensitivity analysis</i>: the primer. Chichester: John Wiley &amp; Sons, 2008.',
'THEIL, H. <i>Economics and information theory</i>. Amsterdam: North-Holland, 1967.']
k=H.find('<h4 class="dax">Referências metodológicas</h4>'); assert k>0
a=H.find('<ul class="refs">',k); b=H.find('</ul>',a)
items=_re.findall(r'<li>(.*?)</li>',H[a:b],_re.S)
low=lambda t:_re.sub('<[^>]+>','',t).replace('&amp;','&')
have={low(t)[:60] for t in items}
add=[r for r in NEWR if low(r)[:60] not in have and not any(low(r)[:40]==low(t)[:40] for t in items)]
import unicodedata as _u
_key=lambda t:_u.normalize('NFD',low(t)).encode('ascii','ignore').decode().upper()
allr=sorted(items+add,key=_key)
H=H[:a]+'<ul class="refs">'+''.join(f'<li>{t}</li>' for t in allr)+H[b:]
i=H.index('const REF_MET = '); j=H.index(';\n',i)
rm=_j.loads(H[i+len('const REF_MET = '):j])
rm=sorted(rm+[low(r) for r in add],key=_key)
H=H[:i]+'const REF_MET = '+_j.dumps(rm,ensure_ascii=False)+H[j:]
print('refs +',len(add))

# 5. PDF da metodologia: nova seção 14; referências passa a 15
_rep("h2('14. Referências metodológicas');","""h2('14. Análise espacial, desigualdade, validação e subsídios a políticas');
  document.querySelectorAll('#metodo-xp-pdf h3, #metodo-xp-pdf p, #metodo-xp-pdf h4, #metodo-xp-pdf li').forEach(p=>{ let tx=p.textContent.replace(/\\s+/g,' ').trim(); if(!tx) return; if(p.tagName[0]==='H') tx=tx.replace(/^1[34](\\.\\d)?\\.?\\s+/,''); if(p.tagName==='H3') para(tx,{size:10.5,bold:true,gap:4}); else if(p.tagName==='H4') para(tx,{size:10,bold:true,gap:3}); else if(p.tagName==='LI') para(tx,{size:9.5,gap:3,bullet:true,indent:10}); else para(tx,{size:9.5,gap:4}); });
  y-=4;
  h2('15. Referências metodológicas');""")

_rep(".replace(/±/g,'+/-').replace(/  +/g,' ');",".replace(/±/g,'+/-').replace(/μ/g,'mu').replace(/α/g,'alfa').replace(/≥/g,'>=').replace(/≤/g,'<=').replace(/−/g,'-').replace(/  +/g,' ');")
# 6. "Fontes" e sumário da Metodologia: item novo no índice da página, se houver lista de seções
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('xp_post ok')
