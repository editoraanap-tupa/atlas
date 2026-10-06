# Dados abertos do Atlas Socioambiental da RMVRC

Arquivos em UTF-8. Coordenadas geográficas em SIRGAS 2000 (compatível com WGS 84).

| Arquivo | Conteúdo | Fonte principal |
|---|---|---|
| `setores_rmvrc_indicadores.csv` | Indicadores dos 1.940 setores censitários. Separador `;`, decimal com vírgula. As colunas `sat_veg` e `sat_lst` informam a imagem e a grade usadas em cada setor. | IBGE, Censo 2022; elaboração própria |
| `setores_rmvrc.geojson` | Os mesmos indicadores, com a geometria dos setores (contorno simplificado). | IBGE, malha de setores 2022 |
| `mun.geojson` | Limites dos sete municípios. | IBGE, malha municipal |
| `hidro.geojson` | Rios, córregos, canais, espelhos d'água e nascentes presumidas. Em polígonos, `ap` é a faixa de APP em metros e `ak` a categoria (`rio`, `lago`, `res` = reservatório, `peq` = menos de 1 ha). | OpenStreetMap (ODbL) |
| `bacias.geojson`, `subbacias.geojson` | Bacias e sub-bacias hidrográficas recortadas para a RMVRC. | IBGE, bacias ottocodificadas |
| `micro.geojson` | Microbacias urbanas. | elaboração própria, MDT ANADEM (ANA/UFRGS) |
| `sgb.geojson` | Setores de risco de Cuiabá (2014) e Várzea Grande (2018). | SGB/CPRM, RIGeo |
| `equipamentos.json` | Unidades de saúde, escolas, universidades, centros comunitários, parques, praças e unidades de conservação. | CNES/DATASUS; OpenStreetMap (ODbL) |
| `saude_municipios.json` | Internações (DRSAI, respiratórias, asma) e dengue por município e ano, 2023–2025. | DATASUS, SIH/SUS e SINAN |
| `datasus_tabnet_bruto.json` | Tabelas do TabNet como foram obtidas. | DATASUS |
| `lentes_prioridade.json` | Indicadores de cada objetivo do Índice de Prioridade Territorial. | elaboração própria |

O IVSA e os índices de prioridade são calculados pela própria página ao abrir; o CSV traz o IVSA gravado na base. O dicionário completo de cada coluna, com fórmula e fonte, está na página Metodologia do Atlas (item “Dicionário de indicadores”) e em `docs/metodologia_fontes_atlas_rmvrc.pdf`.

Condições de uso de cada fonte: ver `LICENSE.md` na raiz do repositório.
