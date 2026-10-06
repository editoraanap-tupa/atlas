# Licenças, direitos de uso e atribuição das fontes + licença do Atlas (texto enviado pela Profa. Sandra em 01/10/2026)
H=open('/home/claude/d/atlas_rmvrc.html').read()
def rep(a,b,n=None):
    global H
    c=H.count(a); assert c>=1 and (n is None or c==n),(c,a[:90]); H=H.replace(a,b)
LIC=[
"O Atlas Socioambiental da Região Metropolitana do Vale do Rio Cuiabá integra dados provenientes de diferentes instituições públicas e plataformas de dados abertos. Cada conjunto de dados permanece submetido às condições de uso, licenciamento, atribuição e responsabilidade definidas por sua instituição de origem.",
"Os dados do <b>Instituto Brasileiro de Geografia e Estatística (IBGE)</b> utilizados no Atlas são provenientes do Censo Demográfico 2022, das Malhas Territoriais, do Banco de Dados de Informações Ambientais (BDiA) e de outros serviços geográficos oficiais, sendo a instituição, o produto, o ano e a fonte de acesso identificados nas referências correspondentes.",
"Os dados do <b>Projeto MapBiomas</b> são de uso público, aberto e gratuito mediante atribuição, disponibilizados sob licença Creative Commons Attribution 4.0 International (CC BY 4.0). Neste Atlas foi utilizada a Coleção 9 da Série Anual de Mapas de Cobertura e Uso da Terra do Brasil, referente ao ano de 2023.",
"Os dados do <b>OpenStreetMap</b> utilizados na representação da hidrografia e na localização de escolas, creches, universidades, centros comunitários e de assistência, praças, parques e unidades de conservação são disponibilizados sob a Open Data Commons Open Database License (ODbL). Atribuição: © OpenStreetMap contributors.",
"Os dados provenientes da <b>Agência Nacional de Águas e Saneamento Básico (ANA)</b>, incluindo informações do Sistema Nacional de Informações sobre Recursos Hídricos (SNIRH), HidroWeb e produtos disponibilizados no âmbito de sua política de dados abertos, foram utilizados com preservação da identificação da fonte e do respectivo produto.",
"As informações provenientes do <b>Ministério da Saúde</b>, incluindo DATASUS, SIH/SUS, SINAN e Cadastro Nacional de Estabelecimentos de Saúde (CNES), foram obtidas de sistemas e interfaces públicas oficiais. Os dados utilizados no Atlas são agregados ou disponibilizados em formato aberto e não incluem informações pessoais identificáveis.",
"Os dados <b>Landsat 8 e 9</b> utilizados no cálculo da temperatura de superfície são provenientes do U.S. Geological Survey (USGS). Os produtos Landsat distribuídos pelo USGS são de domínio público, sendo mantida a identificação da instituição e da missão como fonte.",
"Os dados <b>Sentinel-2</b> utilizados para análise da vegetação são provenientes do programa Copernicus da União Europeia e foram utilizados segundo o regime de acesso livre, pleno e aberto aplicável aos dados Sentinel. Aviso de atribuição: contém dados Copernicus Sentinel modificados (2026).",
"O produto <b>Copernicus DEM GLO-30</b> permanece sujeito às condições específicas de utilização definidas pelo programa Copernicus e pela European Space Agency (ESA), mantida sua identificação como fonte. Aviso de atribuição exigido pela licença: produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved.",
"As cartas de suscetibilidade e os setores de risco produzidos pelo <b>Serviço Geológico do Brasil (SGB/CPRM)</b> permanecem vinculados à autoria e às condições de utilização dos respectivos produtos disponibilizados no Repositório Institucional de Geociências – RIGeo. O Atlas mantém a indicação da instituição, título do produto, escala, ano e endereço de acesso.",
"As demais bases institucionais utilizadas, incluindo dados da Defesa Civil do Estado de Mato Grosso e do NOAA/NCEI, permanecem igualmente vinculadas às respectivas fontes e condições originais de utilização.",
"As transformações, recortes espaciais, integrações, cálculos, indicadores compostos, índices, classificações e representações desenvolvidos especificamente para este Atlas não alteram a titularidade ou a licença das bases originais. Recomenda-se que qualquer reutilização dos dados apresentados consulte e observe também as condições da fonte primária correspondente.",
]
ALIC=[
"© 2026 Ricardo Miranda dos Santos e Sandra Medina Benini — PPGAU/UNIVAG.",
"Salvo indicação em contrário, os conteúdos autorais, textos, análises, indicadores, gráficos e demais produtos originais deste Atlas são disponibilizados sob a licença <a href=\"https://creativecommons.org/licenses/by/4.0/deed.pt-br\" target=\"_blank\" rel=\"noopener\">Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)</a>.",
"As bases de dados, imagens de satélite, produtos cartográficos e demais conteúdos provenientes de terceiros permanecem submetidos às respectivas licenças, termos de uso e direitos de atribuição indicados na seção “Método e fontes”.",
]
SEC='''<section class="block fsec lic" id="mf-lic">
  <div class="fs-h"><span class="fs-n">4</span><div><h3>Licenças, direitos de uso e atribuição das fontes</h3><p>Condições de uso de cada base de dados e avisos de atribuição exigidos pelas fontes.</p></div></div>
  <div class="lic-t">'''+''.join('<p>'+t+'</p>' for t in LIC)+'''</div>
</section>
<section class="block fsec lic" id="mf-alic">
  <div class="fs-h"><span class="fs-n">5</span><div><h3>Licença do Atlas</h3><p>Como os conteúdos originais do Atlas podem ser reutilizados.</p></div></div>
  <div class="licbox">'''+''.join('<p>'+t+'</p>' for t in ALIC)+'''</div>
</section>
'''
i=H.find('<div class="page" data-page="metodo"'); j=H.find('<div class="pnav">',i); assert i>0 and j>i
H=H[:j]+SEC+H[j:]
rep('<a href="#mf-saude">Saúde e ODS</a></nav>','<a href="#mf-saude">Saúde e ODS</a><a href="#mf-lic">Licenças das fontes</a><a href="#mf-alic">Licença do Atlas</a></nav>',1)
CSS='''
.lic-t{columns:2 380px;column-gap:32px}
.lic-t p{margin:0 0 10px;font-size:13.5px;line-height:1.55;break-inside:avoid}
.licbox{border:1px solid var(--line);border-left:4px solid var(--gold,#ffc000);border-radius:10px;background:var(--panel);padding:12px 16px;max-width:92ch}
.licbox p{margin:0 0 8px;font-size:14px;line-height:1.55}
.licbox p:first-child{font-weight:700}
.licbox p:last-child{margin-bottom:0}
.cite + .lich{margin-top:16px}
'''
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSS+H[k:]
# rodapé
rep('<span>© 2026 PPGAU-UNIVAG · Elaboração: Prof. Dr. Ricardo Miranda dos Santos e Profa. Dra. Sandra Medina Benini · Pós-Doutorado 2025–2026</span>',
    '<span>© 2026 Ricardo Miranda dos Santos e Sandra Medina Benini — PPGAU/UNIVAG · Pós-Doutorado 2025–2026 · Conteúdo autoral sob licença <a href="https://creativecommons.org/licenses/by/4.0/deed.pt-br" target="_blank" rel="noopener">CC BY 4.0</a>; bases de terceiros seguem as licenças indicadas em <a href="#mf-lic">Método e fontes</a>.</span>',1)
rep('hidrografia, escolas e parques © colaboradores do OpenStreetMap; CNES/DATASUS; Copernicus GLO-30 (ESA); Sentinel-2 (Copernicus/ESA, via Earth Search); Landsat 9 (USGS, via Microsoft Planetary Computer).',
    'hidrografia, escolas e parques © OpenStreetMap contributors (ODbL); CNES/DATASUS; MapBiomas (CC BY 4.0); Copernicus GLO-30 (ESA); Sentinel-2 (Copernicus/ESA, via Earth Search); Landsat 8 e 9 (USGS, via Microsoft Planetary Computer).',1)
# página Sobre
m='(2025–2026).</div>'
assert H.count(m)==1
H=H.replace(m,m+'\n      <h3 class="lich" style="margin-top:16px">Licença</h3>\n      <div class="licbox">'+''.join('<p>'+t+'</p>' for t in ALIC)+'</div>')
# PDF da metodologia
rep("  h2('12. Referências metodológicas');",
    "  h2('12. Licenças, direitos de uso e atribuição das fontes');\n  document.querySelectorAll('#mf-lic .lic-t p').forEach(p=>para(p.textContent.replace(/\\s+/g,' ').trim(),{size:9.5,gap:4}));\n  para('Licença do Atlas',{bold:true,gap:3});\n  document.querySelectorAll('#mf-alic .licbox p').forEach(p=>para(p.textContent.replace(/\\s+/g,' ').trim(),{size:9.5,gap:3}));\n  h2('13. Referências metodológicas');",1)
# datas de acesso e fonte do MDS; nota de cobertura
rep('29–30 set. 2026','29 set.–1 out. 2026')
rep('"MDS Copernicus GLO-30", "ESA – Copernicus", "https://registry.opendata.aws/copernicus-dem/"','"MDS Copernicus GLO-30", "ESA – Copernicus, via AWS Open Data e Microsoft Planetary Computer", "https://registry.opendata.aws/copernicus-dem/ e https://planetarycomputer.microsoft.com/dataset/cop-dem-glo-30"',1)
rep("<li><b>Cobertura</b>: vegetação, temperatura, suscetibilidade a inundação, cheias do Rio Cuiabá, setores de risco do SGB e FCU existem apenas para Cuiabá e Várzea Grande. Nos demais municípios esses campos ficam sem dado e não entram no IVSA.</li>",
    "<li><b>Cobertura</b>: vegetação e temperatura existem para os 1.940 setores dos 7 municípios; suscetibilidade a inundação, para as áreas urbanas (conurbação e sedes e distritos dos demais); carta do SGB, para Cuiabá, Várzea Grande e Chapada dos Guimarães; cheias do Rio Cuiabá, setores de risco do SGB e FCU, apenas para Cuiabá e Várzea Grande. Onde não há dado, o campo fica vazio e não entra nos índices.</li>",1)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('lic ok',len(H))
