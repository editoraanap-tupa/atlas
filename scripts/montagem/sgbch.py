# Carta do SGB de Chapada dos Guimarães (RIGeo doc/25797.2) — textos e fontes
H=open('/home/claude/d/atlas_rmvrc.html').read()
def rep(a,b,n=None):
    global H
    c=H.count(a); assert c>=1 and (n is None or c==n),(c,a[:90]); H=H.replace(a,b)
rep("<small>oficial · 1:25.000 · Cuiabá e VG</small>","<small>oficial · Cuiabá, VG e Chapada</small>",1)
CH=" PINHO, D.; FERNANDES, R. L. G. Carta de suscetibilidade a movimentos gravitacionais de massa e inundação: município de Chapada dos Guimarães - MT. [S. l.]: Serviço Geológico do Brasil, dez. 2025. Escala 1:250.000. Arquivos vetoriais, versão 2 (jul. 2026). Disponível em: https://rigeo.sgb.gov.br/handle/doc/25797.2. Acesso em: 1 out. 2026."
rep("município de Várzea Grande, MT. Disponível em: https://rigeo.sgb.gov.br. Acesso em: 30 set. 2026.","município de Várzea Grande, MT. Disponível em: https://rigeo.sgb.gov.br. Acesso em: 30 set. 2026."+CH,2)
rep('"https://rigeo.sgb.gov.br/handle/doc/25663 (arquivo sig_varzea_grande_mt_suscet.zip)"]','"https://rigeo.sgb.gov.br/handle/doc/25663 (arquivo sig_varzea_grande_mt_suscet.zip)"], ["Carta de suscetibilidade – Chapada dos Guimarães (2025; vetores, versão 2)", "SGB/CPRM – RIGeo", "https://rigeo.sgb.gov.br/handle/doc/25797.2 (arquivo sig_chapada_dos_guimaraes_mt_suscet.zip, camada Inundacao_A)"]',1)
rep("<span class='url'>https://rigeo.sgb.gov.br/handle/doc/25663 (arquivo sig_varzea_grande_mt_suscet.zip)</span>. Acesso em: 29 set.–1 out. 2026.</li>","<span class='url'>https://rigeo.sgb.gov.br/handle/doc/25663 (arquivo sig_varzea_grande_mt_suscet.zip)</span>. Acesso em: 29 set.–1 out. 2026.</li><li><b>Carta de suscetibilidade – Chapada dos Guimarães (2025; vetores, versão 2)</b> — SGB/CPRM – RIGeo. Obtido em: <span class='url'>https://rigeo.sgb.gov.br/handle/doc/25797.2 (arquivo sig_chapada_dos_guimaraes_mt_suscet.zip, camada Inundacao_A)</span>. Acesso em: 29 set.–1 out. 2026.</li>",1)
rep("— Cuiabá (2021, publicada em 2022) e Várzea Grande;","— Cuiabá (2021, publicada em 2022), Várzea Grande e Chapada dos Guimarães (2025; vetores na versão 2, de jul. 2026);",1)
rep("Serviço Geológico do Brasil (SGB/CPRM) – Cuiabá (2021) e Várzea Grande","Serviço Geológico do Brasil (SGB/CPRM) – Cuiabá (2021), Várzea Grande e Chapada dos Guimarães (2025)",2)
rep("Existe apenas para Cuiabá e Várzea Grande.</dd>","Existe para Cuiabá, Várzea Grande e Chapada dos Guimarães; os outros quatro municípios não têm carta publicada.</dd>")
rep("Serviço Geológico do Brasil (1:25.000; Cuiabá e Várzea Grande, 2021).'","Serviço Geológico do Brasil (Cuiabá, Várzea Grande e Chapada dos Guimarães).'",1)
rep("Cartas de Suscetibilidade SGB/CPRM 1:25.000 (Cuiabá 2021; Várzea Grande)","Cartas de Suscetibilidade SGB/CPRM (Cuiabá 2021; Várzea Grande; Chapada dos Guimarães 2025)",1)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('sgbch ok',len(H))
