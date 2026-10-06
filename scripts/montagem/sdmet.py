# metodologia detalhada (HTML + PDF) e fontes para Saúde ambiental e ODS — executado em ods.py
import html as _hh
MUNCOD='510010 Acorizal; 510267 Campo Verde; 510300 Chapada dos Guimarães; 510340 Cuiabá; 510610 Nossa Senhora do Livramento; 510780 Santo Antônio de Leverger; 510840 Várzea Grande'
DRS=[('Feco-oral','Cólera (A00); Febres tifoide e paratifoide (A01); Shiguelose (A03); Amebíase (A06); Diarreia e gastroenterite de origem infecciosa presumível (A09); Outras doenças infecciosas intestinais (A02, A04, A05, A07, A08)'),
 ('Transmitidas por inseto vetor','Dengue clássico (A90); Febre hemorrágica da dengue (A91); Febre amarela (A95); Leishmanioses visceral, cutânea, cutâneo-mucosa e não especificada (B55); Malária, todas as formas (B50–B54); Tripanossomíase/doença de Chagas (B56–B57); Filariose (B74)'),
 ('Transmitidas pelo contato com a água','Leptospirose icterohemorrágica, outras formas e não especificada (A27); Esquistossomose (B65)'),
 ('Relacionadas com a higiene','Tracoma (A71); Conjuntivite e outros transtornos da conjuntiva (H10–H11); Micoses (B35–B49)'),
 ('Geo-helmintos e teníases','Ancilostomíase (B76); Outras helmintíases (B68–B71, B75, B77–B83)')]
FML=[('Taxa anual de internação','T(a) = I(a) ÷ P × 10.000','I(a) = internações de moradores do município no ano de atendimento a; P = população residente do Censo 2022 (mesmo denominador para os três anos)'),
 ('Taxa média 2023–2025','T̄ = [(I2023 + I2024 + I2025) ÷ 3] ÷ P × 10.000','média aritmética das contagens anuais'),
 ('Incidência de dengue','D(a) = C(a) ÷ P × 100.000','C(a) = casos prováveis (todas as notificações, exceto descartadas) com primeiro sintoma no ano a, por município de residência'),
 ('Participação das DRSAI','%DRSAI = I_DRSAI ÷ I_total × 100','I_total = todas as internações de moradores no SUS, qualquer causa'),
 ('Variação 2023 → 2025','Δ% = (T2025 − T2023) ÷ T2023 × 100','sem valor quando T2023 = 0'),
 ('RMVRC','I_RMVRC = Σ I(município); P_RMVRC = Σ P(município)','a taxa da região é a razão das somas, não a média das taxas')]
def tbl(head,rows):
    return '<div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr>'+''.join(f'<th class="l">{h}</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td class="l">{_hh.escape(c)}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
HT=f'''<h3 style="margin-top:18px">9. Saúde ambiental (DATASUS)</h3>
<p><b>Objetivo.</b> Medir o peso, na saúde dos moradores, das doenças ligadas ao saneamento inadequado, das doenças respiratórias e da dengue, por município e por ano (2023, 2024 e 2025), para leitura junto aos indicadores de saneamento e ambiente do Atlas (ODS 3, metas 3.3 e 3.9).</p>
<p><b>9.1 Extração dos dados.</b> As tabulações foram feitas no TabNet do DATASUS em 01/10/2026:</p>
<ul>
<li><b>Internações</b>: SIH/SUS, "Morbidade Hospitalar do SUS – por local de residência – Mato Grosso" (sih/cnv/nrmt.def). Linha = Município (ou Lista Morb CID-10, para os grupos de doenças); Coluna = Ano atendimento; Medida = Internações (AIH aprovadas). Períodos de processamento = jan/2022 a jul/2026, para incluir internações de 2023–2025 processadas com atraso. Seleções: municípios {MUNCOD}; itens da Lista de Morbidade CID-10 descritos abaixo. Recortes mensais: Linha = Ano/mês atendimento.</li>
<li><b>Dengue</b>: SINAN, "Dengue – notificações registradas – Mato Grosso" (sinannet/cnv/denguebmt.def). Linha = Município de residência; Coluna = Ano do 1º sintoma; Medida = Casos prováveis; arquivos 2022 a 2025.</li>
<li><b>População</b>: Censo Demográfico 2022 (IBGE), soma dos setores censitários de cada município (igual à tabela SIDRA 4714).</li>
</ul>
<p><b>9.2 Fórmulas.</b></p>
{tbl(['Indicador','Fórmula','Variáveis'],FML)}
<p style="margin-top:10px"><b>9.3 Doenças Relacionadas ao Saneamento Ambiental Inadequado (DRSAI).</b> Classificação da Funasa (BRASIL, 2010), aplicada aos itens da Lista de Morbidade CID-10 do SIH. Entre parênteses, os códigos da CID-10 de cada item. A hepatite A fica de fora porque a lista do SIH a agrega às demais hepatites virais.</p>
{tbl(['Categoria','Itens da Lista de Morbidade (CID-10)'],DRS)}
<p style="margin-top:10px"><b>9.4 Doenças respiratórias.</b> Capítulo X da CID-10 (J00–J99). O recorte "pneumonia, asma e DPOC" soma pneumonia (J12–J18), asma (J45–J46) e bronquite, enfisema e outras doenças pulmonares obstrutivas crônicas (J40–J44).</p>
<p><b>9.5 Comparação entre anos.</b> Os três anos usam o mesmo denominador (Censo 2022). Por isso a variação reflete a mudança no número de casos, não na população. O total de internações no SUS de cada município é mostrado como referência: se uma taxa cresce no mesmo ritmo do total, o aumento pode refletir mais oferta de leitos ou de registro, e não mais doença. A sazonalidade é a soma mensal das internações dos sete municípios em cada ano.</p>
<p><b>9.6 Limitações.</b> (a) Os dados públicos só identificam o município de residência, sem bairro ou setor; o cruzamento com os setores exige os microdados do SIH com CEP (SES-MT ou Lei de Acesso à Informação). (b) Só entram internações no SUS. (c) Municípios pequenos internam menos por terem menos leitos e encaminharem pacientes, então taxa baixa não é sinônimo de menos doença. (d) Com contagens pequenas, uma epidemia altera muito a taxa. (e) Com sete municípios não se faz inferência estatística; a leitura é descritiva.</p>
<h3 style="margin-top:18px">10. Relação dos indicadores com os ODS</h3>
<p><b>10.1 Associação indicador → ODS.</b> Cada indicador foi associado ao Objetivo de Desenvolvimento Sustentável e à meta que ajuda a monitorar, conforme a Agenda 2030 (ONU, 2015) e as metas nacionais adaptadas pelo IPEA (2018). Um indicador pode servir a mais de um ODS (por exemplo, coleta de lixo: ODS 1, meta 1.4, e ODS 11, meta 11.6). As associações estão na página ODS e no dicionário dos indicadores.</p>
<p><b>10.2 Valor municipal.</b> Usa as mesmas regras de agregação do Atlas, aplicadas aos setores urbanos de cada município: média ponderada pelos domicílios nos indicadores de domicílio, pela população nos de pessoas, pela área nos de cobertura, e soma nos de moradores. Vegetação por habitante = soma da área vegetada ÷ soma da população. Indicadores de saúde: taxa média 2023–2025 do item 9.</p>
<p><b>10.3 Cor do painel.</b> Os sete municípios são ordenados em cada indicador (posição r = 0 para o menor valor). Calcula-se q = r ÷ (n − 1), invertido quando "maior é melhor", e a classe = ⌊(1 − q) × 5⌋ (0 = pior, 4 = melhor). A cor compara os municípios entre si; não indica cumprimento de meta.</p>
<p><b>10.4 Metas numéricas.</b> Só o saneamento tem meta legal com valor: 99% da população com água potável e 90% com coleta e tratamento de esgoto até 31/12/2033 (Lei nº 14.026/2020, art. 11-B). O Censo informa a ligação à rede de esgoto, não o tratamento; o indicador do Atlas é, portanto, um limite superior para a meta.</p>
'''
i=H.find('<h3 style="margin-top:18px">9. Referências</h3>'); assert i>0
H=H[:i]+HT+'<h3 style="margin-top:18px">11. Referências</h3>'+H[i+len('<h3 style="margin-top:18px">9. Referências</h3>'):]
# artigo na página Fontes
ART='''<article>
    <h2>Saúde ambiental e ODS</h2>
    <p><b>Internações:</b> Ministério da Saúde, DATASUS, SIH/SUS, Morbidade Hospitalar por local de residência (MT), via TabNet; anos de atendimento 2023, 2024 e 2025.</p>
    <p><b>Dengue:</b> Ministério da Saúde, SVSA, SINAN, casos prováveis por município de residência e ano do primeiro sintoma, via TabNet.</p>
    <p><b>Denominador:</b> população do Censo 2022 (IBGE).</p>
    <p><b>ODS:</b> Agenda 2030 (ONU, 2015); metas nacionais (IPEA, 2018); metas de saneamento da Lei nº 14.026/2020.</p>
    <p>Tratamento: contagens anuais e mensais por município, taxas por 10 mil (internações) e por 100 mil habitantes (dengue), classificação DRSAI da Funasa (2010) e associação de cada indicador aos ODS. Fórmulas completas nos itens 9 e 10 da página Metodologia.</p>
  </article>
'''
k=H.find('<h2>Fontes dos dados</h2>'); k=H.rfind('<article>',0,k); assert k>0
H=H[:k]+ART+H[k:]
# PDF de metodologia: novas seções 9 e 10, limitações e referências renumeradas
def pdfs(s): return (_r.sub(r'^9\.(\d)',r'7.\1',_r.sub(r'^10\.(\d)',r'8.\1',s)).replace('→','->').replace('≥','>=').replace('−','-').replace('⌊','').replace('⌋','').replace('Σ ','soma de ').replace('T̄','Tm').replace('Δ%','Var%').replace('“','"').replace('”','"').replace("'","\\'"))
import re as _r
def strip(s): return _r.sub(r'<[^>]+>','',s)
js=["  h2('7. Saúde ambiental (DATASUS)');"]
js.append("  para('"+pdfs("Objetivo: medir o peso das doenças ligadas ao saneamento inadequado (DRSAI), das doenças respiratórias e da dengue nos moradores dos sete municípios, por ano (2023, 2024 e 2025), para leitura junto aos indicadores de saneamento e ambiente (ODS 3, metas 3.3 e 3.9).")+"',{gap:4});")
js.append("  para('Extração (TabNet/DATASUS, consulta em 01/10/2026):',{bold:true,size:10,gap:2});")
for li in _r.findall(r'<li>(.*?)</li>',HT.split('9.2 Fórmulas')[0],flags=_r.S): js.append("  para('"+pdfs(strip(li))+"',{bullet:true,indent:6,size:9.5,gap:1});")
js.append("  para('Fórmulas:',{bold:true,size:10,gap:2});")
for a,b,c in FML: js.append("  para('"+pdfs(f'{a}: {b}. {c}.')+"',{bullet:true,indent:6,size:9.5,gap:1});")
js.append("  para('"+pdfs("Classificação DRSAI (Funasa, 2010), itens da Lista de Morbidade CID-10 do SIH. Hepatite A excluída por estar agregada às demais hepatites virais:")+"',{bold:true,size:10,gap:2});")
for a,b in DRS: js.append("  para('"+pdfs(f'{a}: {b}.')+"',{bullet:true,indent:6,size:9.5,gap:1});")
for tag in ['9.4','9.5','9.6']:
    m=_r.search(r'<p[^>]*><b>'+_r.escape(tag)+r'.*?</p>',HT,flags=_r.S); js.append("  para('"+pdfs(strip(m.group(0)))+"',{gap:3});")
js.append("  h2('8. Relação dos indicadores com os ODS');")
for tag in ['10.1','10.2','10.3','10.4']:
    m=_r.search(r'<p[^>]*><b>'+_r.escape(tag)+r'.*?</p>',HT,flags=_r.S); js.append("  para('"+pdfs(strip(m.group(0)))+"',{gap:3});")
js.append("  ODS.forEach(o=>para(`ODS ${o.n} – ${o.t}: metas ${o.metas.map(m=>m.split(' ')[0]).join(', ')}. Indicadores: ${o.ks.filter(k=>byK[k]).map(k=>byK[k].n).join('; ')}${o.sd?'; '+o.sd.map(k=>SD_IND[k].n).join('; '):''}.`,{bullet:true,indent:6,size:9,gap:1}));")
old="  h2('7. Limitações');"; assert H.count(old)==1
H=H.replace(old,'\n'.join(js)+"\n  h2('9. Limitações');")
old="  h2('8. Referências metodológicas');"; assert H.count(old)==1
H=H.replace(old,"  h2('10. Referências metodológicas');")
