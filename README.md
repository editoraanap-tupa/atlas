# Atlas Socioambiental da Região Metropolitana do Vale do Rio Cuiabá (RMVRC)

Atlas digital interativo com indicadores socioambientais dos **1.940 setores censitários** dos sete municípios do núcleo da RMVRC (Cuiabá, Várzea Grande, Acorizal, Campo Verde, Chapada dos Guimarães, Nossa Senhora do Livramento e Santo Antônio de Leverger), em Mato Grosso.

**Acesse o Atlas:** https://editoraanap-tupa.github.io/atlas/

## O que o Atlas reúne

- Indicadores do Censo Demográfico 2022 (IBGE) por setor censitário: população, saneamento, renda, alfabetização e entorno dos domicílios.
- Índice de Vulnerabilidade Socioambiental (IVSA) e Índice de Prioridade Territorial (Laboratório de Governança Territorial).
- Vegetação (Sentinel-2), temperatura de superfície (Landsat 8 e 9), suscetibilidade a inundação, cenários de cheia do Rio Cuiabá, carta de suscetibilidade do SGB, solos, erosão e cobertura da terra (MapBiomas).
- Demarcação de Áreas de Preservação Permanente e de nascentes pela Lei 12.651/2012, art. 4º.
- Saúde ambiental (DATASUS, 2023–2025) e relação dos indicadores com os Objetivos de Desenvolvimento Sustentável.
- Metodologia com fórmulas, fontes, aferição de cada indicador e relatório de auditoria.

## Elaboração

- **Prof. Dr. Ricardo Miranda dos Santos** — pesquisador de Pós-Doutorado, PPGAU-UNIVAG (2025–2026)
- **Profa. Dra. Sandra Medina Benini** — supervisora da pesquisa, docente do PPGAU-UNIVAG

Resultado da pesquisa de Pós-Doutorado *“Indicadores ambientais como ferramenta para a sustentabilidade urbana: estudo de caso na Região Metropolitana do Vale do Rio Cuiabá (RMVRC)”*, desenvolvida no Programa de Pós-Graduação em Arquitetura e Urbanismo do Centro Universitário de Várzea Grande (PPGAU-UNIVAG).

## Como citar

> SANTOS, Ricardo Miranda dos; BENINI, Sandra Medina. **Atlas Socioambiental da Região Metropolitana do Vale do Rio Cuiabá (RMVRC)**. Várzea Grande: PPGAU-UNIVAG, 2026. Atlas digital interativo.

## Conteúdo do repositório

| Pasta ou arquivo | O que é |
|---|---|
| `index.html` | A página do Atlas (textos, estilos e rotinas). Abre em qualquer navegador; precisa de internet para as bibliotecas de mapa e de PDF. |
| `atlas-dados-1.js`, `atlas-dados-2.js` | Dados embutidos que a página carrega: setores e hidrografia (parte 1); equipamentos, municípios, imagens das camadas, bacias e microbacias (parte 2). Devem ficar na mesma pasta do `index.html`. |
| `docs/` | Metodologia e fontes (PDF), relatório de auditoria dos dados (PDF) e um exemplo de relatório de bairro. |
| `dados/` | Dados abertos: indicadores por setor (CSV e GeoJSON), municípios, hidrografia, bacias, microbacias, equipamentos e saúde. Ver `dados/LEIAME.md`. |
| `scripts/` | Rotinas em Python e JavaScript usadas para calcular os indicadores, montar a página e auditar os dados. |

## Verificação e reprodução

Todos os indicadores podem ser conferidos: a página **Metodologia** do Atlas traz a fórmula e a fonte de cada um, e a página **Aferição** descreve como cada família de indicadores foi testada. O relatório `docs/auditoria_atlas_rmvrc_v25.pdf` registra o recálculo independente dos 24 indicadores censitários para os 1.940 setores, sem divergência.

As imagens de satélite e os modelos de terreno originais não estão no repositório por causa do tamanho; `scripts/satelite_inundacao/` documenta de onde foram obtidos e como foram processados.

## Limites

O Atlas é um instrumento de planejamento e de pesquisa. As estimativas de moradores em áreas de risco supõem ocupação uniforme dentro do setor; a suscetibilidade a inundação e a demarcação de APP são triagens sobre modelo de terreno de 30 m e hidrografia do OpenStreetMap, e não substituem levantamento de campo, a carta oficial do Serviço Geológico do Brasil, o mapeamento da Defesa Civil nem o Cadastro Ambiental Rural. Os limites de cada camada estão declarados na Metodologia.

## Licença

© 2026 Ricardo Miranda dos Santos e Sandra Medina Benini — PPGAU/UNIVAG.

Salvo indicação em contrário, os conteúdos autorais, textos, análises, indicadores, gráficos e demais produtos originais deste Atlas são disponibilizados sob a licença [Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt-br).

As bases de dados, imagens de satélite, produtos cartográficos e demais conteúdos provenientes de terceiros permanecem submetidos às respectivas licenças, termos de uso e direitos de atribuição — ver [`LICENSE.md`](LICENSE.md) e a seção “Licenças, direitos de uso e atribuição das fontes” do Atlas.
