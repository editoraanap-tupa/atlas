# Correções da auditoria de dados de 17/10/2026 (executado no fim de assemble.py)
import json, re
H=open('/home/claude/d/atlas_rmvrc.html').read()
def rep(a,b,n=1):
    global H
    c=H.count(a); assert c==n,(c,a[:100]); H=H.replace(a,b)
dec=json.JSONDecoder()
# 1. pesos exatos nas médias agregadas
for k in ['analf']: rep(f"s de 15 anos ou mais que não sabem ler e escrever.',w:'pop'}}",f"s de 15 anos ou mais que não sabem ler e escrever.',w:'w15'}}")
for t in ["radores em face de quadra com ao menos uma árvore.',w:'pop'}","Moradores em face de quadra com 5 ou mais árvores.',w:'pop'}","d:'Moradores em face com via pavimentada.',w:'pop'}","d:'Moradores em face com iluminação pública.',w:'pop'}","d:'Moradores em face com calçada.',w:'pop'}","d:'Moradores em face com bueiro ou boca de lobo.',w:'pop'}","d:'Moradores em face com ponto de ônibus ou van.',w:'pop'}"]:
    rep(t,t.replace("w:'pop'}","w:'went'}"))
rep("mensal dos responsáveis com rendimento (V06004).',w:'dppo'}","mensal dos responsáveis com rendimento (V06004).',w:'wr'}")
rep("    const w = i.w==='dppo'?p.dppo:p.pop; num+=v*w; den+=w; }","    const w = i.w==='dppo'?p.dppo:i.w==='pop'?p.pop:(p[i.w]||0); if(!w) continue; num+=v*w; den+=w; }")
# 2. IVSA: quantos componentes entraram (aviso na ficha e coluna no CSV)
rep("      p._ic[c.k]=100*z; if(WT[c.k]>0){ s+=WT[c.k]*z; sw+=WT[c.k]; } }\n    p.ivsa = sw >= .6*tot ? Math.round(1000*s/sw)/10 : null;",
    "      p._ic[c.k]=100*z; if(WT[c.k]>0){ s+=WT[c.k]*z; sw+=WT[c.k]; } }\n    p.ivsa = sw >= .6*tot ? Math.round(1000*s/sw)/10 : null;\n    { const ws=WC.filter(c=>WT[c.k]>0); const nu=ws.filter(c=>p._ic[c.k]!=null).length; p._icn = p.ivsa==null ? null : nu+' de '+ws.length; p._icf = p.ivsa!=null && nu<ws.length ? ws.filter(c=>p._ic[c.k]==null).map(c=>c.k) : null; }")
rep("      : `<div class=\"bullet\"><span>${lab}</span><span class=\"v\">${Math.round(v)}</span><span class=\"track\"><i style=\"width:${v}%;background:${d3.interpolateYlOrRd(.1+.85*v/100)}\"></i></span></div>`; }); }\n  h+='</div>';",
    "      : `<div class=\"bullet\"><span>${lab}</span><span class=\"v\">${Math.round(v)}</span><span class=\"track\"><i style=\"width:${v}%;background:${d3.interpolateYlOrRd(.1+.85*v/100)}\"></i></span></div>`; });\n    if(p._icf){ const NM={arvore:'arborização da rua',pav:'pavimentação',analf:'alfabetização',esgoto:'esgoto',lixo:'coleta de lixo',agua:'abastecimento de água',renda:'renda'}; const L=p._icf.map(k=>NM[k]||k), ent=p._icf.every(k=>k==='arvore'||k==='pav');\n      h+=`<p class=\"ivwarn\"><b>Atenção:</b> índice calculado com ${p._icn} componentes. Ficaram de fora ${L.join(' e ')}, ${ent?'porque o IBGE não fez a pesquisa do entorno neste setor. Sem esses itens, o índice tende a ficar mais baixo':'porque o IBGE não divulgou esses dados para o setor (sigilo ou ausência)'}: compare com cautela.</p>`; } }\n  h+='</div>';")
rep("['sat_veg','Vegetação: imagem e grade']","['_icn','IVSA: componentes usados'],['sat_veg','Vegetação: imagem e grade']")
k=H.find('</style>',H.find('<title>')); H=H[:k]+'\n.ivwarn{margin:10px 0 2px;padding:8px 10px;border-left:3px solid var(--ochre);background:var(--panel-2);border-radius:6px;font-size:12.5px;line-height:1.45;color:var(--fg)}\n'+H[k:]
# 3. equipamentos: retira pontos que não são unidades de conservação (SNUC) ou ficam fora da RMVRC
pref='const EQUIP = '; i=H.index(pref); EQ,j=dec.raw_decode(H[i+len(pref):])
FORA={'Centro Histórico do Porto','Centro Histórico de Cuiabá','Zona de Restrição Máxima','Área de Preservação Permanente Córrego do Barbado','Planície Alagável da Bacia do Alto Paraguai',''}
n0=len(EQ); EQ=[e for e in EQ if not (e['c']=='uc' and e['n'] in FORA)]; NRM=n0-len(EQ); assert NRM==6,NRM
H=H[:i+len(pref)]+json.dumps(EQ,ensure_ascii=False,separators=(',',':'))+H[i+len(pref)+j:]
NEQ=f'{len(EQ):,}'.replace(',','.')
rep('1.222 equipamentos após retirar 11 duplicatas;',f'{NEQ} equipamentos após retirar 11 duplicatas e, na auditoria de 17/10/2026, 6 pontos marcados como unidade de conservação que não são unidades do SNUC (centros históricos, zoneamento, APP e uma área fora da RMVRC);',2)
# 4. saúde: saneamento do município inteiro pelo SIDRA (Censo 2022), sem o viés dos setores com sigilo
HS=json.load(open('/home/claude/d/serie/hist.json'))['mun']
pref='const SAUDE='; i=H.index(pref); S,j=dec.raw_decode(H[i+len(pref):])
pc=lambda a,b: round(100*a/b,1)
for m in S['mun']:
    r=HS[m['mun']]; m['esgoto']=pc(r['esg22_fossa'],r['dom'][3]); m['agua']=pc(r['agua'][3],r['dom'][3]); m['lixo']=pc(r['lixo'][3],r['dom'][3])
T={k:sum(HS[m][k][3] if k!='esg22_fossa' else HS[m][k] for m in HS) for k in ['esg22_fossa','agua','lixo']}; D3=sum(HS[m]['dom'][3] for m in HS)
S['tot']['esgoto']=pc(T['esg22_fossa'],D3); S['tot']['agua']=pc(T['agua'],D3); S['tot']['lixo']=pc(T['lixo'],D3)
H=H[:i+len(pref)]+json.dumps(S,ensure_ascii=False)+H[i+len(pref)+j:]
open('/home/claude/aud/saude_saneamento.json','w').write(json.dumps({m['mun']:[m['esgoto'],m['agua'],m['lixo']] for m in S['mun']},ensure_ascii=False))
rep('Esgoto na rede<br><small>todo o município</small></th><th>Água da rede<br><small>todo o município</small></th>','Esgoto na rede<br><small>município · Censo 2022</small></th><th>Água da rede<br><small>município · Censo 2022</small></th>')
rep('sdCount(\'all\',null,SDP)))}%</td><td></td><td></td></tr></tbody>`;','sdCount(\'all\',null,SDP)))}%</td><td class="num">${ptBR(fmt1(SAUDE.tot.esgoto))}%</td><td class="num">${ptBR(fmt1(SAUDE.tot.agua))}%</td></tr></tbody>`;')
# 5. cheias: mesmo arredondamento nas duas tabelas (soma exata dos setores, arredondada uma vez)
rep("<td class='num'>28.232</td><td class='num'>34.520</td>","<td class='num'>28.233</td><td class='num'>34.521</td>")
# 6. versão
rep('<span>Versão de 01/10/2026</span>','<span>Versão de 17/10/2026 · dados auditados em 17/10/2026</span>')
# 7. datas de publicação e textos harmonizados
rep('do Serviço Geológico do Brasil (1:25.000, validada em campo em 2021) para Cuiabá e Várzea Grande,','do Serviço Geológico do Brasil (1:25.000) para Cuiabá (publicada em fev. 2022) e Várzea Grande (set. 2025),')
rep('1:25.000 — Cuiabá (2021, publicada em 2022), Várzea Grande e Chapada dos Guimarães (2025; vetores na versão 2, de jul. 2026);','1:25.000 — Cuiabá (CPRM, fev. 2022) e Várzea Grande (SGB, set. 2025); Chapada dos Guimarães (SGB, dez. 2025; o registro do RIGeo informa escala 1:250.000; vetores na versão 2, de 15/07/2026);')
rep('Serviço Geológico do Brasil (SGB/CPRM) – Cuiabá (2021), Várzea Grande e Chapada dos Guimarães (2025)','Serviço Geológico do Brasil (SGB/CPRM) – Cuiabá (fev. 2022), Várzea Grande (set. 2025) e Chapada dos Guimarães (dez. 2025)',2)
rep('município de Cuiabá, MT. Escala 1:25.000. Brasília: SGB, 2022; e Carta de suscetibilidade … município de Várzea Grande, MT. Disponível','município de Cuiabá, MT. Escala 1:25.000. Mato Grosso: CPRM, fev. 2022; e Carta de suscetibilidade … município de Várzea Grande, MT. [S. l.]: SGB, set. 2025. Disponível',2)
rep('Rendimento do responsável). Rio de Janeiro: IBGE, 2024–2026. Disponível','Rendimento do responsável). Rio de Janeiro: IBGE: Demografia, Cor ou raça e Alfabetização publicadas em 12/11/2024; Características do domicílio 2 e Entorno, em 17/04/2025; Rendimento do responsável, em 08/05/2026; Básico republicada em 20/05/2026 (conteúdo idêntico ao usado). Disponível',2)
rep('Malha de Setores Censitários do Censo Demográfico 2022 com atributos – Mato Grosso (MT_setores_CD2022). Rio de Janeiro: IBGE, 2024.','Malha de Setores Censitários do Censo Demográfico 2022 com atributos – Mato Grosso (MT_setores_CD2022). Rio de Janeiro: IBGE, arquivo de 13/11/2024.',2)
rep('“Rendimento do responsável” (publicação de 2026)','“Rendimento do responsável” (publicação de 08/05/2026)',2)
rep('(fórmula de Haversine, R = 6.371 km)','(fórmula de Haversine, R = 6.371,0088 km)')
rep('Diferença média para a imagem de 13/08 na faixa comum: −4,0 °C (12/08), +0,7 °C (14/08) e −2,0 °C (04/08), com desvio-padrão de 0,9 a 1,3 °C;','Na faixa comum, as imagens vizinhas ficaram 4,0 °C mais frias (12/08), 0,7 °C mais quentes (14/08) e 2,0 °C mais frias (04/08) que a de 13/08, com desvio-padrão de 0,9 a 1,3 °C; por isso a correção soma +4,0, −0,7 e +2,0 °C, como na Metodologia;')
rep('Classes: robusta (≥ 80%), moderada (50% a 80%), sensível aos pesos (< 50%).</p>','Classes: robusta (≥ 80%), moderada (50% a 80%), sensível aos pesos (&lt; 50%).</p>')
# 8. APP: método novo
rep('O indicador “Área em APP” segue a regra do item anterior, mais simples (30 m em torno de todo corpo d’água), e só nos setores urbanos.','O indicador “Área em APP” usa as mesmas faixas desta camada, nos 1.940 setores (recalculado na auditoria de 17/10/2026; antes usava 30 m em torno de todo corpo d’água e só os setores urbanos).')
rep('<li>Desenham-se as faixas do Código Florestal (Lei 12.651/2012, art. 4º) sobre a hidrografia: 100 m no Rio Cuiabá, 50 m no Coxipó, 30 m nos demais rios e córregos e em lagoas, 50 m de raio nas nascentes.</li><li>Convertem-se setor e faixas para uma grade fina (5 m).</li>',
    '<li>Usam-se as faixas da camada de APP do Atlas (Lei 12.651/2012, art. 4º): nos cursos d’água, 30, 50, 100 ou 200 m conforme a largura (100 m no Rio Cuiabá e 50 m no Coxipó), medidos a partir da margem; em lagos e lagoas naturais com 1 ha ou mais, 30 m em área urbana e 50 m (até 20 ha) ou 100 m em área rural; 50 m de raio nas nascentes. Reservatórios e espelhos d’água com menos de 1 ha não geram faixa.</li><li>Convertem-se setor, água e faixas para uma grade de 5 m (setores com menos de 3 km²), 10 m (até 40 km²), 20 m (até 400 km²) ou 30 m (maiores).</li>')
rep('IVSA com menos componentes em 366 setores, quase todos rurais, por falta da pesquisa de entorno.','IVSA com menos componentes em 366 setores: em 178 (141 rurais) falta a pesquisa de entorno do IBGE (arborização e pavimentação); em 188, quase todos urbanos, falta um dado que o IBGE não divulgou por sigilo (em 158, a alfabetização). A ficha do setor avisa quando isso acontece e o CSV traz a coluna “IVSA: componentes usados”.')
def repall(a,b,nmin=1):
    global H
    c=H.count(a); assert c>=nmin,(c,a[:100]); H=H.replace(a,b)
# contagens conferidas nos arquivos de processamento (ndvi_out.json e lst_out.json)
repall('1.694 setores); nos outros 246, pixels de 40 m','1.751 setores); nos outros 189, pixels de 40 m')
repall('Nos 246 setores que não cabem','Nos 189 setores que não cabem')
repall('de 40 m nos 246 setores que não cabem','de 40 m nos 189 setores que não cabem')
repall('21 setores','19 setores',5)
repall('Diferença média para a imagem de 13/08 na faixa comum: -4,0 °C (12/08), +0,7 °C (14/08) e -2,0 °C (04/08), com desvio-padrão de 0,9 a 1,3 °C;','Na faixa comum, as imagens vizinhas ficaram 4,0 °C mais frias (12/08), 0,7 °C mais quentes (14/08) e 2,0 °C mais frias (04/08) que a de 13/08, com desvio-padrão de 0,9 a 1,3 °C; por isso a correção soma +4,0, -0,7 e +2,0 °C;')
# 9. registro da auditoria no cartão do Censo
rep('46.560 comparações, nenhuma divergência acima de 0,05 ponto percentual;','46.560 comparações, nenhuma divergência acima de 0,05 ponto percentual; na auditoria de 17/10/2026, as sete tabelas do IBGE usadas foram comparadas com as versões vigentes no FTP (inclusive a tabela Básico republicada em 20/05/2026) e são idênticas nos 1.940 setores;',2)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('audit_fix ok', NEQ)
