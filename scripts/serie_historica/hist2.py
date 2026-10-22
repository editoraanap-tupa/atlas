# Série histórica: cartão "Evolução do município" no mapa, logo abaixo do mapa e acima da ficha do setor
H=open('/home/claude/d/atlas_rmvrc.html').read()
CARD='''<section class="convite" id="convite" aria-labelledby="cv-t"><div class="cv-txt"><span class="kick">Série histórica · IBGE · Censos 1991, 2000, 2010 e 2022</span><h2 id="cv-t">Três décadas de transformação no Vale do Rio Cuiabá</h2><p>Quanto a região cresceu e quanto melhoraram as condições de vida desde 1991? Percorra os quatro últimos Censos município por município e veja como mudaram o acesso à água, ao esgoto, à coleta de lixo e à escrita.</p><ol class="cv-line" aria-label="Censos da série"><li>1991</li><li>2000</li><li>2010</li><li>2022</li></ol></div>
<nav class="cv-go" aria-label="Explorar a série histórica"><a href="#historico"><b>Linha do tempo</b><span>População, domicílios, água, esgoto, lixo e alfabetização em quatro censos</span><i aria-hidden="true">→</i></a><a href="#hs-ind"><b>Compare os municípios</b><span>Os sete municípios lado a lado, censo a censo</span><i aria-hidden="true">→</i></a><a href="#metodo-hist"><b>Como os números foram calculados</b><span>Fórmulas, mudanças entre os censos e tabelas originais do IBGE</span><i aria-hidden="true">→</i></a></nav></section>
'''
k=H.find('<section class="eixos" id="ficha"'); assert k>0 and H.count('<section class="eixos" id="ficha"')==1
H=H[:k]+CARD+H[k:]
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('hist2 ok',len(H))
# referência da série histórica na página Fontes e no PDF de metodologia
REF_L='Série histórica municipal (Censos 1991, 2000, 2010 e 2022)'
REF_T='IBGE – INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. Sistema IBGE de Recuperação Automática (SIDRA): Censo Demográfico, tabelas 179, 180, 182, 202 e 204 (1991); 202, 204, 1442, 1444 e 1447 (2000); 202, 1379, 3154 e 3218 (2010); 6804, 6805, 6892, 9542 e 9923 (2022). Rio de Janeiro: IBGE. Disponível em: https://sidra.ibge.gov.br. Acesso em: 17 out. 2026.'
k=H.find('<ul class="refs fcols"><li><b>Internações hospitalares'); assert k>0
k=H.find('<li>',k)
H=H[:k]+f'<li><b>{REF_L}:</b> {REF_T}</li>'+H[k:]
import json as _j
assert H.count('const FONTES_REF = [')==1
H=H.replace('const FONTES_REF = [','const FONTES_REF = ['+_j.dumps([REF_L,REF_T],ensure_ascii=False)+', ',1)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('hist2 refs ok')
# ---- Grade Estatística: referência nas Fontes e no PDF; seção nova na Metodologia e no PDF (série histórica + grade)
H=open('/home/claude/d/atlas_rmvrc.html').read()
# Metodologia (página): nova seção 12, Referências passa a 13

def _build_met():
    import re as _re
    D='/home/claude/d/'
    g=open(D+'moved_grade.html').read(); h=open(D+'moved_hist.html').read(); t=open(D+'moved_tab.html').read()
    def uls(x): return _re.findall(r'<ul class="note">(.*?)</ul>',x,_re.S)
    hu=uls(h); gu=uls(g)
    hu0=hu[0].replace('(valor no censo ÷ valor no censo anterior)<sup>1 ÷ anos entre os censos</sup> − 1','(valor no censo ÷ valor no censo anterior) elevado a (1 ÷ anos entre os censos), menos 1')
    lis=_re.findall(r'<li>.*?</li>',gu[0],_re.S)
    P50='<p><b>Domicílios em quadrículas de cerca de 50 m (2022).</b> A partir das coordenadas dos endereços do Censo 2022 (CNEFE, IBGE), contam-se os domicílios particulares (espécie 1) em quadrículas de cerca de 50 m × 50 m (0,000467° de longitude × 50 m de latitude, na mesma grade de imagem do mapa). Entram só os endereços com coordenada própria, modificada (apartamentos no mesmo número) ou estimada pela face de quadra (níveis 1 a 4); ficam fora os localizados pela localidade ou pelo centro do setor (níveis 5 e 6). O CNEFE não separa domicílios ocupados de vagos ou de uso ocasional, por isso o total (455 mil) é maior que o de domicílios ocupados do censo. Vale só para 2022, porque os endereços de 2010 não têm coordenadas para a maioria dos domicílios.</p>'; PIN='<p><b>Moradores em suscetibilidade a inundação e em APP (estimativa).</b> Em cada célula inteiramente dentro da área com modelo de inundação (conurbação e 17 sedes e distritos), 64 pontos regularmente espaçados dão a fração da célula em suscetibilidade alta (f alta) e em APP (f APP, faixas da camada de APP e raio de 50 m das nascentes presumidas). Moradores estimados = soma, em todas as células, de moradores da célula × f. Supõe ocupação uniforme dentro da célula.</p>'
    lis=[('<li>'+P50[3:-4]+'</li>') if 'Domicílios em 2022' in l else ('<li>'+PIN[3:-4]+'</li>') if 'Inundação e APP' in l else l for l in lis]
    t=t.replace('<h3 style="margin-top:16px">Tabelas do IBGE usadas</h3>','')
    return ('<h3 style="margin-top:18px" id="metodo-hist">12. Série histórica dos Censos (1991–2022)</h3>\n'+'<p><b>Série histórica municipal.</b> População, domicílios particulares permanentes (ocupados), água da rede geral, esgoto em rede geral ou pluvial, lixo coletado e alfabetização das pessoas de 15 anos ou mais, nos Censos de 1991, 2000, 2010 e 2022, por município, a partir das tabelas do SIDRA (lista das tabelas em 12.3). Indicador (%) = domicílios (ou pessoas) com a característica ÷ total × 100; para a RMVRC, soma das contagens dos sete municípios. Taxa média de crescimento ao ano = (valor final ÷ valor inicial) elevado a (1 ÷ número de anos), menos 1.</p>'+'\n'
      +'<h4>12.1 Indicadores e fórmulas da série histórica</h4><ul>'+hu0+'</ul>\n'
      +'<h4>12.2 O que muda de um censo para outro</h4><ul>'+hu[1]+'</ul>\n'
      +'<h4>12.3 Tabelas do IBGE usadas</h4>'+t+'\n')
MET=_build_met()
k=H.find('<h3 style="margin-top:18px">12. Referências</h3>'); assert k>0
H=H[:k]+MET+H[k:].replace('<h3 style="margin-top:18px">12. Referências</h3>','<h3 style="margin-top:18px">13. Referências</h3>',1)
# PDF de metodologia: nova seção 10; renumera as seguintes
for a,b in [("h2('13. Referências metodológicas')","h2('14. Referências metodológicas')"),("h2('12. Licenças, direitos de uso e atribuição das fontes')","h2('13. Licenças, direitos de uso e atribuição das fontes')"),("h2('11. Limitações')","h2('12. Limitações')"),("h2('10. Aferição dos indicadores')","h2('11. Aferição dos indicadores')")]:
    assert H.count(a)==1,a; H=H.replace(a,b)
PDFS="""h2('10. Série histórica dos Censos (1991–2022)');
  document.querySelectorAll('#metodo-hist-pdf p, #metodo-hist-pdf h4, #metodo-hist-pdf li, #metodo-hist-pdf tr').forEach(p=>{ const tx=(p.tagName==='TR'?[...p.children].map(c=>c.textContent.trim()).join(' · '):p.textContent).replace(/\\s+/g,' ').trim(); if(!tx) return; if(p.tagName==='H4') para(tx,{size:10,bold:true,gap:3}); else if(p.tagName==='LI') para(tx,{size:9.5,gap:3,bullet:true,indent:10}); else para(tx,{size:9.5,gap:4}); });
  h2('11. Aferição dos indicadores')"""
H=H.replace("h2('11. Aferição dos indicadores')",PDFS,1)
# o PDF lê o texto da seção da Metodologia: marca o bloco
H=H.replace(MET,'<div id="metodo-hist-pdf">'+MET+'</div>',1)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('hist2 grade/metodo ok')
# PDF de metodologia: Helvetica (WinAnsi) não tem símbolos gregos e matemáticos; troca por equivalentes legíveis
H=open('/home/claude/d/atlas_rmvrc.html').read()
old="const para=(t,{size=10,bold=false,indent=0,gap=4,color,bullet}={})=>{\n"
assert H.count(old)==1
H=H.replace(old,old+"    t=String(t).replace(/Σ\\s*/g,'soma ').replace(/∩/g,' interseção ').replace(/Δ/g,'d').replace(/φ/g,'lat').replace(/λ/g,'lon').replace(/√/g,'raiz').replace(/ⱼ/g,'j').replace(/ᵢ/g,'i').replace(/₁/g,'1').replace(/₂/g,'2').replace(/′/g,\"'\").replace(/≈/g,'~').replace(/±/g,'+/-').replace(/  +/g,' ');\n",1)
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('pdf glyphs ok')
