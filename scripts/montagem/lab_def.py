# definição das lentes do Índice de Prioridade Territorial (IPT)
# (chave, nome, sentido: +1 = maior valor => maior prioridade; -1 = menor valor => maior prioridade, log)
LENS=[
 ('geral','Prioridade geral','Visão de conjunto: vulnerabilidade social somada a risco hídrico, calor, falta de vegetação e acesso à saúde.',[11,1,3,10,13],
   [('ivsa',1,0),('inund',1,0),('verde',-1,0),('lst',1,0),('d_ubs',1,1)]),
 ('san','Saneamento','Onde faltam rede de esgoto, água, coleta de lixo e banheiro.',[6,3,11],
   [('esgoto',-1,0),('esg_prec',1,0),('agua',-1,0),('lixo',-1,0),('sem_banh',1,0)]),
 ('verde','Infraestrutura verde','Onde há menos vegetação e árvores, mais calor e parques mais distantes.',[11,13,15],
   [('verde',-1,0),('verde_hab',-1,1),('arvore',-1,0),('lst',1,0),('d_parque',1,1)]),
 ('saude','Saúde','Onde o acesso a serviços de saúde é pior e há mais população sensível (crianças e idosos) com saneamento deficiente.',[3,6],
   [('d_ubs',1,1),('d_saude',1,1),('esgoto',-1,0),('agua',-1,0),('idosos',1,0),('criancas',1,0)]),
 ('hab','Habitação','Precariedade habitacional: favelas e comunidades urbanas, adensamento, banheiro, pavimentação e renda.',[11,1],
   [('fcu',1,0),('mor',1,0),('sem_banh',1,0),('pav',-1,0),('renda',-1,1)]),
 ('dren','Drenagem','Onde faltam bueiros e pavimentação e há suscetibilidade a inundação e ocupação de APP.',[6,11,13],
   [('bueiro',-1,0),('pav',-1,0),('inund',1,0),('a1974',1,0),('app_pct',1,0)]),
 ('mob','Mobilidade','Onde faltam ponto de ônibus, calçada e pavimentação, e escolas e saúde estão longe.',[11],
   [('onibus',-1,0),('calcada',-1,0),('pav',-1,0),('d_esc',1,1),('d_saude',1,1)]),
 ('desig','Redução de desigualdades','Concentração de baixa renda, analfabetismo, população preta e parda e favelas.',[10,1,4],
   [('renda',-1,1),('analf',1,0),('negros',1,0),('fcu',1,0)]),
 ('clima','Adaptação climática','Exposição a calor, inundação, suscetibilidade da carta do SGB e erosão, com pouca vegetação.',[13,11,15],
   [('lst',1,0),('inund',1,0),('sgb_alta',1,0),('erosao',1,0),('verde',-1,0)])
]
