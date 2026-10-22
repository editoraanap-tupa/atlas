# Dados abertos do Atlas Socioambiental da RMVRC

Arquivos em UTF-8. Coordenadas geográficas em SIRGAS 2000 (compatível com WGS 84).

| Arquivo | Conteúdo | Fonte principal |
|---|---|---|
| `setores_rmvrc_indicadores.csv` | Indicadores dos 1.940 setores censitários. Separador `;`, decimal com vírgula. As colunas `sat_veg` e `sat_lst` informam a imagem e a grade usadas em cada setor. `ivsa` é o índice como a página calcula ao abrir (pesos padrão) e `ivsa_n`, quantos dos 7 componentes entraram (366 setores têm menos de 7). `w15` (pessoas de 15 anos ou mais), `went` (moradores do universo da pesquisa de entorno) e `wr` (responsáveis com rendimento) são os pesos usados nas médias de município, bairro e microbacia. `app_pct` segue as faixas da Lei 12.651/2012 em todos os setores (auditoria de 17/10/2026). | IBGE, Censo 2022; elaboração própria |
| `setores_rmvrc.geojson` | Os mesmos indicadores, com a geometria dos setores (contorno simplificado). | IBGE, malha de setores 2022 |
| `mun.geojson` | Limites dos sete municípios. | IBGE, malha municipal |
| `hidro.geojson` | Rios, córregos, canais, espelhos d'água e nascentes presumidas. Em polígonos, `ap` é a faixa de APP em metros e `ak` a categoria (`rio`, `lago`, `res` = reservatório, `peq` = menos de 1 ha). | OpenStreetMap (ODbL) |
| `bacias.geojson`, `subbacias.geojson` | Bacias e sub-bacias hidrográficas recortadas para a RMVRC. | IBGE, bacias ottocodificadas |
| `micro.geojson` | Microbacias urbanas. | elaboração própria, MDT ANADEM (ANA/UFRGS) |
| `sgb.geojson` | Setores de risco de Cuiabá (2014) e Várzea Grande (2018). | SGB/CPRM, RIGeo |
| `equipamentos.json` | Unidades de saúde, escolas, universidades, centros comunitários, parques, praças e unidades de conservação. | CNES/DATASUS; OpenStreetMap (ODbL) |
| `saude_municipios.json` | Internações (DRSAI, respiratórias, asma) e dengue por município e ano, 2023–2025. | DATASUS, SIH/SUS e SINAN |
| `serie_historica_municipios.csv` | Série histórica dos sete municípios nos Censos de 1991, 2000, 2010 e 2022: população (total e urbana), domicílios, água da rede, esgoto em rede geral ou pluvial, lixo coletado e alfabetização (15 anos ou mais), com as contagens e as porcentagens. Separador `,`, decimal com ponto. A coluna `tabelas_sidra` indica as tabelas de origem; diferenças de conceito entre os censos estão na página “Evolução dos municípios” do Atlas. | IBGE, Censos Demográficos (SIDRA) |
| `datasus_tabnet_bruto.json` | Tabelas do TabNet como foram obtidas. | DATASUS |
| `lentes_prioridade.json` | Indicadores de cada objetivo do Índice de Prioridade Territorial. | elaboração própria |

O IVSA e os índices de prioridade são calculados pela própria página ao abrir; o CSV traz o IVSA gravado na base. O dicionário completo de cada coluna, com fórmula e fonte, está na página Metodologia do Atlas (item “Dicionário de indicadores”) e em `docs/metodologia_fontes_atlas_rmvrc.pdf`.

Condições de uso de cada fonte: ver `LICENSE.md` na raiz do repositório.
