# página "Método e fontes": Fontes dos dados e Tratamento dos dados em blocos separados (executado em site.py)
import re as _rf
i=H.find('<div class="page" data-page="metodo"'); j=H.find('<div class="pnav">',i); P=H[i:j]
m=_rf.search(r'<article>\s*<h2>Fontes dos dados</h2>\s*(<ul class="refs">.*?</ul>)\s*<h2 style="margin-top:14px">Tratamento dos dados</h2>\s*(<ul>.*?</ul>)\s*(<p>.*?</p>)\s*</article>\s*</section>',P,flags=_rf.S)
assert m, 'bloco fontes'
refs,trat,extr=m.group(1),m.group(2),m.group(3)
cards_start=P.find('<section class="notes">')
cards=P[cards_start:m.start()]+'</section>'
for a,b in [('<h2>Validação da mancha de inundação</h2>','<h2 id="mf-valid">Validação da mancha de inundação</h2>'),('<h2>Como as novas camadas foram feitas</h2>','<h2 id="mf-camadas">Como as novas camadas foram feitas</h2>'),('<h2>Saúde ambiental e ODS</h2>','<h2 id="mf-saude">Saúde ambiental e ODS</h2>')]:
    assert a in cards,a; cards=cards.replace(a,b)
NEW=f'''<nav class="mfnav" aria-label="Nesta página"><span>Nesta página</span><a href="#mf-fontes">Fontes dos dados</a><a href="#mf-trat">Tratamento dos dados</a><a href="#mf-camadas">Camadas</a><a href="#mf-valid">Validação</a><a href="#mf-saude">Saúde e ODS</a></nav>
<section class="block fsec" id="mf-fontes">
  <div class="fs-h"><span class="fs-n">1</span><div><h3>Fontes dos dados</h3><p>Todas as bases são públicas e oficiais ou, quando indicado, colaborativas de licença aberta. Referência completa de cada uma:</p></div></div>
  {refs.replace('<ul class="refs">','<ul class="refs fcols">')}
</section>
<section class="block fsec" id="mf-trat">
  <div class="fs-h"><span class="fs-n">2</span><div><h3>Tratamento dos dados</h3><p>Como as bases foram recortadas, combinadas e preparadas antes do cálculo dos indicadores.</p></div></div>
  {trat.replace('<ul>','<ul class="trat fcols">',1)}
  {extr.replace('<p>','<p class="note">',1)}
</section>
<div class="fs-h fs-out"><span class="fs-n">3</span><div><h3>Camadas, validação e saúde</h3><p>Como foram produzidas as camadas ambientais, como a mancha de inundação foi validada e de onde vêm os dados de saúde e ODS.</p></div></div>
{cards}'''
NEW=_rf.sub(r'<article>(\s*<h2 id="mf-camadas">)',r'<article class="mf-wide">\1',NEW,count=1)
assert 'mf-wide' in NEW
NEW=NEW.replace('<section class="notes">','<section class="notes mfcards">',1)
P2=P[:cards_start]+NEW+P[m.end():]
P2=P2.replace('com o dicionário de indicadores e os pesos do IVSA em uso.','com fontes, tratamento, fórmulas e o dicionário de indicadores.')
H=H[:i]+P2+H[j:]
CSSF="""
.mfnav{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin:0 0 14px}
.mfnav span{font:700 11px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-right:4px}
.mfnav a{font:600 13px var(--f-body);color:var(--accent);text-decoration:none;border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:4px 12px}
.mfnav a:hover{border-color:var(--gold,#ffc000)}
.fsec{margin-bottom:16px;scroll-margin-top:calc(var(--tb) + 12px)}
.fs-h{display:flex;gap:12px;align-items:flex-start;margin-bottom:12px}
.fs-h h3{margin:0;font:800 19px/1.2 var(--f-display);color:var(--fg);text-transform:none;letter-spacing:0}
.fs-h p{margin:3px 0 0;color:var(--muted);font-size:14px;max-width:80ch}
.fs-n{flex:none;width:30px;height:30px;border-radius:8px;background:var(--accent);color:var(--panel);display:grid;place-items:center;font:800 15px var(--f-display)}
.fs-out{margin:22px 0 2px}
.fcols{columns:2 380px;column-gap:32px;margin:0;padding-left:18px}
.fcols li{break-inside:avoid;margin:0 0 8px;font-size:13.5px;line-height:1.5}
.notes h2{scroll-margin-top:calc(var(--tb) + 12px)}
.notes.mfcards{grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-flow:dense}
.notes.mfcards .mf-wide{grid-column:1/-1}
.notes.mfcards .mf-wide ul{columns:2 380px;column-gap:32px}
.notes.mfcards .mf-wide li{break-inside:avoid}
@media (max-width:760px){.notes.mfcards{grid-template-columns:minmax(0,1fr)}}
"""
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSSF+H[k:]
_o1="  fontes.querySelectorAll('li').forEach(li=>para(li.textContent.replace(/\\s+/g,' ').trim(),{bullet:true,indent:6}));\n  fontes.querySelectorAll('p').forEach(p=>para(p.textContent.trim()));"
assert H.count(_o1)==1, 'pdf trat'
H=H.replace(_o1,"  document.querySelectorAll('#mf-trat ul.trat li').forEach(li=>para(li.textContent.replace(/\\s+/g,' ').trim(),{bullet:true,indent:6}));\n  document.querySelectorAll('#mf-trat p.note').forEach(p=>para(p.textContent.trim()));")
H=H.replace('<span>Versão de 30/09/2026</span>','<span>Versão de 01/10/2026</span>')
