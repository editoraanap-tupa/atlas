# ================= referências das bases de dados (HTML e PDF de metodologia) =================
import json as _j, html as _h
H=open('/home/claude/d/atlas_rmvrc.html').read()
REFS=[
 ('Internações hospitalares (DRSAI e respiratórias)','BRASIL. Ministério da Saúde. DATASUS. Sistema de Informações Hospitalares do SUS (SIH/SUS): morbidade hospitalar do SUS por local de residência – Mato Grosso. Brasília: Ministério da Saúde, 2026. Disponível em: http://tabnet.datasus.gov.br. Acesso em: 1 out. 2026.'),
 ('Dengue','BRASIL. Ministério da Saúde. Secretaria de Vigilância em Saúde e Ambiente. Sistema de Informação de Agravos de Notificação (SINAN): dengue – notificações registradas, Mato Grosso. Brasília: Ministério da Saúde, 2026. Disponível em: http://tabnet.datasus.gov.br. Acesso em: 1 out. 2026.'),
 ('Setores censitários e indicadores','IBGE – INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. Censo Demográfico 2022: Agregados por Setores Censitários (Básico; Demografia; Cor ou raça; Alfabetização; Características do domicílio 2; Características urbanísticas do entorno dos domicílios; Rendimento do responsável). Rio de Janeiro: IBGE, 2024–2026. Disponível em: https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/. Acesso em: 30 set. 2026.'),
 ('Malha de setores censitários','IBGE. Malha de Setores Censitários do Censo Demográfico 2022 com atributos – Mato Grosso (MT_setores_CD2022). Rio de Janeiro: IBGE, 2024.'),
 ('Limites municipais','IBGE. Malha Municipal (API de Malhas Geográficas, v3). Disponível em: https://servicodados.ibge.gov.br/api/docs/malhas. Acesso em: 30 set. 2026.'),
 ('Região metropolitana','MATO GROSSO. Lei Complementar nº 359, de 27 de maio de 2009; Lei Complementar nº 577, de 19 de maio de 2016; Lei Complementar nº 796, de 26 de junho de 2024 (Região Metropolitana do Vale do Rio Cuiabá).'),
 ('Solos, geologia e geomorfologia','IBGE. Banco de Dados de Informações Ambientais (BDiA): Bases Contínuas de Pedologia, Geologia e Geomorfologia do Brasil, escala 1:250.000. Disponível em: https://geoservicos.ibge.gov.br/geoserver/BDIA/wfs. Acesso em: 30 set. 2026.'),
 ('Bacias hidrográficas','IBGE. Bacias Hidrográficas do Brasil – ottocodificação, níveis 3 a 6 (BHB250). Disponível em: https://geoservicos.ibge.gov.br/geoserver/CREN/wfs. Acesso em: 30 set. 2026.'),
 ('Cobertura e uso da terra','PROJETO MAPBIOMAS. Coleção 9 da Série Anual de Mapas de Cobertura e Uso da Terra do Brasil, ano 2023 (30 m). Disponível em: https://brasil.mapbiomas.org. Acesso em: 30 set. 2026.'),
 ('Suscetibilidade a inundação (oficial)','SERVIÇO GEOLÓGICO DO BRASIL (SGB/CPRM). Carta de suscetibilidade a movimentos gravitacionais de massa e inundação: município de Cuiabá, MT. Escala 1:25.000. Brasília: SGB, 2022; e Carta de suscetibilidade … município de Várzea Grande, MT. Disponível em: https://rigeo.sgb.gov.br. Acesso em: 30 set. 2026.'),
 ('Setores de risco','SERVIÇO GEOLÓGICO DO BRASIL (SGB/CPRM). Setorização de áreas de alto e muito alto risco a movimentos de massa, enchentes e inundações: Cuiabá (2014) e Várzea Grande (2018). Disponível em: https://rigeo.sgb.gov.br.'),
 ('Modelo digital de terreno','ANA – AGÊNCIA NACIONAL DE ÁGUAS E SANEAMENTO BÁSICO; UFRGS. ANADEM v1: Modelo Digital de Terreno para a América do Sul (30 m), 2024. Disponível em: https://metadados.snirh.gov.br. Acesso em: 30 set. 2026.'),
 ('Modelo digital de superfície','EUROPEAN SPACE AGENCY. Copernicus DEM GLO-30 (30 m). 2021.'),
 ('Cotas e régua fluviométrica','ANA. Estação fluviométrica Cuiabá, código 66260001 (HidroWeb/Telemetria). MATO GROSSO. Secretaria de Estado de Defesa Civil (SUDEC-MT): cotas de alerta, emergência e calamidade e cheias de 1974 e 1995.'),
 ('Vegetação (NDVI)','EUROPEAN SPACE AGENCY. Copernicus Sentinel-2 MSI Nível 2A, imagem de 23/08/2026 (via Earth Search/Element 84).'),
 ('Temperatura de superfície','U.S. GEOLOGICAL SURVEY. Landsat 9 OLI/TIRS Collection 2 Level-2 (ST_B10), imagem de 13/08/2026 (via Microsoft Planetary Computer).'),
 ('Estabelecimentos de saúde','BRASIL. Ministério da Saúde. Cadastro Nacional de Estabelecimentos de Saúde (CNES) – API de Dados Abertos. Disponível em: https://apidadosabertos.saude.gov.br. Acesso em: 30 set. 2026.'),
 ('Hidrografia, escolas e praças','OPENSTREETMAP CONTRIBUTORS. OpenStreetMap (licença ODbL), extração via Overpass API em 29–30 set. 2026. Disponível em: https://www.openstreetmap.org.'),
 ('APP','BRASIL. Lei nº 12.651, de 25 de maio de 2012 (Código Florestal), art. 4º; Lei nº 14.285, de 29 de dezembro de 2021.'),
 ('Declinação magnética','NOAA/NCEI; BGS. World Magnetic Model WMM-2025.'),
]
i=H.index('const FORM = ')
H=H[:i]+'const FONTES_REF = '+_j.dumps(REFS,ensure_ascii=False)+';\n'+H[i:]
old="  h2('1. Fontes de dados e tratamento');"
assert H.count(old)==1
H=H.replace(old,"  h2('1. Fontes dos dados');\n  para('Todas as bases utilizadas são públicas e oficiais (ou colaborativas de licença aberta, quando indicado). Referências completas:',{size:9.5,gap:4});\n  FONTES_REF.forEach(([t,r])=>para(`${t}: ${r}`,{bullet:true,indent:6,size:9,gap:2}));\n  y-=4;\n  h2('2. Tratamento dos dados');")
for a,b in [("h2('2. Como as camadas ambientais foram produzidas');","h2('3. Como as camadas ambientais foram produzidas');"),("h2('3. Índice de Vulnerabilidade Socioambiental (IVSA)');","h2('4. Índice de Vulnerabilidade Socioambiental (IVSA)');"),("h2('4. Dicionário de indicadores');","h2('5. Dicionário de indicadores (fórmula e fonte de cada indicador)');"),("h2('5. Validação da mancha de inundação');","h2('6. Validação da mancha de inundação');"),("h2('6. Limitações e próximos passos');","h2('7. Limitações');")]:
    assert H.count(a)==1,a; H=H.replace(a,b)
# HTML: lista de referências no artigo "Fontes e tratamento"
refs_html=''.join(f"<li><b>{_h.escape(t)}:</b> {_h.escape(r)}</li>" for t,r in REFS)
old2='<h2>Fontes e tratamento</h2>'
assert H.count(old2)==1
H=H.replace(old2,'<h2>Fontes dos dados</h2>\n    <ul class="refs">'+refs_html+'</ul>\n    <h2 style="margin-top:14px">Tratamento dos dados</h2>')
H=H.replace('.dgrid{margin-top:8px}','.dgrid{margin-top:8px}\n.refs li{margin-bottom:5px;font-size:13px}',1)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('fontes ok')

# ================= referências: base cartográfica (onde foi obtida) + metodologia =================
H=open('/home/claude/d/atlas_rmvrc.html').read()
BASE=[
 ('Morbidade hospitalar do SUS por local de residência (MT)','Ministério da Saúde – DATASUS, SIH/SUS (TabNet)','http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/nrmt.def (Internações por ano de atendimento; Lista de Morbidade CID-10 e Capítulo X; arquivos jan/2022–jul/2026; consulta em 01/10/2026)'),
 ('Dengue – casos prováveis por município de residência (MT)','Ministério da Saúde – SVSA, SINAN (TabNet)','http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinannet/cnv/denguebmt.def (ano do 1º sintoma, 2023–2025; consulta em 01/10/2026)'),
 ('Censo 2022 – Agregados por Setores Censitários','IBGE','https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/ (Básico, Demografia, Cor ou raça, Alfabetização, Características do domicílio 2); .../Agregados_por_Setores_Censitarios_Rendimento_do_Responsavel/; .../Agregados_por_Setores_Censitarios_Caracteristicas_urbanisticas_do_entorno_dos_domicilios/'),
 ('Malha de setores censitários 2022 (MT)','IBGE','https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/malha_com_atributos/setores/shp/UF/MT/MT_setores_CD2022.zip'),
 ('Limites municipais','IBGE – API de Malhas Geográficas v3','https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{código do município}?formato=application/vnd.geo+json&qualidade=maxima'),
 ('Pedologia, geologia e geomorfologia 1:250.000','IBGE – BDiA (serviço WFS)','https://geoservicos.ibge.gov.br/geoserver/BDIA/wfs (camadas BDIA:pedo_area, BDIA:geol_area, BDIA:geom_area)'),
 ('Bacias hidrográficas ottocodificadas','IBGE (serviço WFS)','https://geoservicos.ibge.gov.br/geoserver/CREN/wfs (camadas CREN:bacias_nivel_3 a CREN:bacias_nivel_6)'),
 ('Cobertura e uso da terra 2023 (coleção 9)','MapBiomas','https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_9/lclu/coverage/brasil_coverage_2023.tif'),
 ('Carta de suscetibilidade – Cuiabá (1:25.000)','SGB/CPRM – Repositório Institucional de Geociências (RIGeo)','https://rigeo.sgb.gov.br/handle/doc/22635 (arquivo sig_cuiaba_mt_suscet.zip)'),
 ('Carta de suscetibilidade – Várzea Grande (1:25.000)','SGB/CPRM – RIGeo','https://rigeo.sgb.gov.br/handle/doc/25663 (arquivo sig_varzea_grande_mt_suscet.zip)'),
 ('Setorização de áreas de risco','SGB/CPRM – RIGeo','https://rigeo.sgb.gov.br (doc/19365 – Cuiabá, 2014; doc/20780 – Várzea Grande, 2018)'),
 ('MDT ANADEM v1 (30 m)','ANA/UFRGS – SNIRH','https://metadados.snirh.gov.br/files/anadem_v1_tiles/ (tiles anadem_v1_21L.tif e anadem_v1_21K.tif); documentação: https://hge-iph.github.io/anadem/'),
 ('MDS Copernicus GLO-30','ESA – Copernicus','https://registry.opendata.aws/copernicus-dem/'),
 ('Estação fluviométrica Cuiabá (66260001)','ANA – HidroWeb / serviço de telemetria','https://www.snirh.gov.br/hidroweb/ ; https://telemetriaws1.ana.gov.br/ServiceANA.asmx'),
 ('Cotas de alerta, emergência e calamidade; cheias históricas','Defesa Civil de Mato Grosso (SUDEC-MT)','Boletins e registros oficiais da SUDEC-MT'),
 ('Imagem Sentinel-2 L2A (23/08/2026)','ESA – Copernicus, via Earth Search (Element 84)','https://earth-search.aws.element84.com/v1 (coleção sentinel-2-l2a)'),
 ('Imagem Landsat 9 C2 L2 (13/08/2026)','USGS, via Microsoft Planetary Computer','https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2'),
 ('Estabelecimentos de saúde','Ministério da Saúde – CNES, API de Dados Abertos','https://apidadosabertos.saude.gov.br/cnes/estabelecimentos'),
 ('Hidrografia, escolas, praças e parques','OpenStreetMap (licença ODbL), via Overpass API','https://overpass-api.de/api/interpreter'),
 ('Leis complementares da RMVRC','Governo de Mato Grosso – Legislação SEFAZ-MT','https://app1.sefaz.mt.gov.br/sistema/legislacao/'),
 ('Declinação magnética','NOAA/NCEI – World Magnetic Model 2025','https://www.ncei.noaa.gov/products/world-magnetic-model'),
]
METR=[
 'BRASIL. Lei nº 14.026, de 15 de julho de 2020. Atualiza o marco legal do saneamento básico. <i>Diário Oficial da União</i>, Brasília, 16 jul. 2020.',
 'BRASIL. Fundação Nacional de Saúde. <i>Impactos na saúde e no Sistema Único de Saúde decorrentes de agravos relacionados a um saneamento ambiental inadequado</i>. Brasília: Funasa, 2010. (Estudos e Pesquisas, 3).',
 'IPEA – INSTITUTO DE PESQUISA ECONÔMICA APLICADA. <i>Agenda 2030: ODS – metas nacionais dos Objetivos de Desenvolvimento Sustentável</i>. Brasília: Ipea, 2018.',
 'ONU – ORGANIZAÇÃO DAS NAÇÕES UNIDAS. <i>Transformando nosso mundo: a Agenda 2030 para o Desenvolvimento Sustentável</i>. Nova York: ONU, 2015.',
 'BARNES, R.; LEHMAN, C.; MULLA, D. Priority-flood: an optimal depression-filling and watershed-labeling algorithm for digital elevation models. <i>Computers &amp; Geosciences</i>, v. 62, p. 117–127, 2014.',
 'BRASIL. Lei nº 12.651, de 25 de maio de 2012. Dispõe sobre a proteção da vegetação nativa. <i>Diário Oficial da União</i>, Brasília, 28 maio 2012.',
 'CREPANI, E.; MEDEIROS, J. S.; HERNANDEZ FILHO, P.; FLORENZANO, T. G.; DUARTE, V.; BARBOSA, C. C. F. <i>Sensoriamento remoto e geoprocessamento aplicados ao zoneamento ecológico-econômico e ao ordenamento territorial</i>. São José dos Campos: INPE, 2001. (INPE-8454-RPQ/722).',
 'IBGE. <i>Censo Demográfico 2022: Agregados por Setores Censitários – dicionário de dados</i>. Rio de Janeiro: IBGE, 2026.',
 'IBGE. <i>Manual técnico de geomorfologia</i>. 2. ed. Rio de Janeiro: IBGE, 2009.',
 'IBGE. <i>Manual técnico de pedologia</i>. 3. ed. Rio de Janeiro: IBGE, 2015.',
 'LAIPELT, L. et al. ANADEM: a digital terrain model for South America. <i>Remote Sensing</i>, v. 16, n. 13, 2321, 2024.',
 'NOBRE, A. D. et al. Height Above the Nearest Drainage – a hydrologically relevant new terrain model. <i>Journal of Hydrology</i>, v. 404, n. 1–2, p. 13–29, 2011.',
 'PFAFSTETTER, O. <i>Classificação de bacias hidrográficas: metodologia de codificação</i>. Rio de Janeiro: DNOS, 1989.',
 'RENNÓ, C. D. et al. HAND, a new terrain descriptor using SRTM-DEM: mapping terra-firme rainforest environments in Amazonia. <i>Remote Sensing of Environment</i>, v. 112, n. 9, p. 3469–3481, 2008.',
 'ROUSE, J. W.; HAAS, R. H.; SCHELL, J. A.; DEERING, D. W. Monitoring vegetation systems in the Great Plains with ERTS. In: EARTH RESOURCES TECHNOLOGY SATELLITE-1 SYMPOSIUM, 3., 1973, Washington. <i>Proceedings</i>. Washington: NASA, 1974. v. 1, p. 309–317.',
 'SANTOS, H. G. et al. <i>Sistema Brasileiro de Classificação de Solos</i>. 5. ed. Brasília: Embrapa, 2018.',
 'SINNOTT, R. W. Virtues of the Haversine. <i>Sky and Telescope</i>, v. 68, n. 2, p. 159, 1984.',
 'SOUZA, C. M. et al. Reconstructing three decades of land use and land cover changes in Brazilian biomes with Landsat archive and Earth Engine. <i>Remote Sensing</i>, v. 12, n. 17, 2735, 2020.',
 'TRICART, J. <i>Ecodinâmica</i>. Rio de Janeiro: IBGE/SUPREN, 1977.',
 'U.S. GEOLOGICAL SURVEY. <i>Landsat 8-9 Collection 2 Level 2 Science Product Guide</i>. Sioux Falls: USGS EROS Center, 2023.',
]
a=H.index('<h3 style="margin-top:18px">Referências do método</h3>'); b=H.index('</ul>',a)+len('</ul>')
base_html=''.join(f"<li><b>{_h.escape(n)}</b> — {_h.escape(o)}. Obtido em: <span class='url'>{_h.escape(u)}</span>. Acesso em: 29–30 set. 2026.</li>" for n,o,u in BASE)
import re as _re2
METR.sort(key=lambda s:_re2.sub('<[^>]+>','',s).upper())
met_html=''.join(f"<li>{r}</li>" for r in METR)
H=H[:a]+f'''<h3 style="margin-top:18px">9. Referências</h3>
  <h4 class="dax" style="margin-top:8px">Base cartográfica e dados — onde foram obtidos</h4>
  <ul class="refs">{base_html}</ul>
  <h4 class="dax">Referências metodológicas</h4>
  <ul class="refs">{met_html}</ul>'''+H[b:]
H=H.replace('.refs li{margin-bottom:5px;font-size:13px}','.refs li{margin-bottom:5px;font-size:13px}\n.refs .url{font-family:var(--f-mono);font-size:11.5px;word-break:break-all}',1)
# PDF: fontes com local de obtenção + referências metodológicas
import re as _re
i=H.index('const FONTES_REF = ')
H=H[:i]+'const FONTES_BASE = '+_j.dumps(BASE,ensure_ascii=False)+';\nconst REF_MET = '+_j.dumps([_re.sub('<[^>]+>','',r).replace('&amp;','&') for r in METR],ensure_ascii=False)+';\n'+H[i:]
old="  FONTES_REF.forEach(([t,r])=>para(`${t}: ${r}`,{bullet:true,indent:6,size:9,gap:2}));\n  y-=4;"
assert H.count(old)==1
H=H.replace(old,old+"\n  para('Onde cada base foi obtida (repositório e endereço):',{size:10,bold:true,gap:3});\n  FONTES_BASE.forEach(([n,o,u])=>para(`${n} — ${o}. Obtido em: ${u}. Acesso em: 29–30 set. 2026.`,{bullet:true,indent:6,size:8.5,gap:2}));\n  y-=4;")
old2="  newPage();\n  return buildPDF(pages"
assert H.count(old2)==1
H=H.replace(old2,"  h2('8. Referências metodológicas');\n  REF_MET.forEach(r=>para(r,{bullet:true,indent:6,size:9,gap:2}));\n"+old2)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('refs ok')
