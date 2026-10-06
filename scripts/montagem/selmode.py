# ficha do setor e indicadores por tema só aparecem com um setor selecionado; sem seleção o mapa ocupa a largura
_o="function renderDetail(){\n  const el=document.getElementById('detail'); if(!st.sel) return;"
assert H.count(_o)==1
H=H.replace(_o,"""function syncSel(){ const app=document.querySelector('.app'), on=!!st.sel, was=app.classList.contains('has-sel'); app.classList.toggle('has-sel',on); const fx=document.getElementById('ficha'); if(fx) fx.hidden=!on;
  if(on!==was) requestAnimationFrame(()=>window.dispatchEvent(new Event('resize'))); }
function clearSel(){ st.sel=null; paths.classed('sel',false); const bm=document.getElementById('detail'); if(bm) bm.innerHTML=''; syncSel(); }
function renderDetail(){
  syncSel();
  const el=document.getElementById('detail'); if(!st.sel) return;""")
# abre sem setor selecionado
_a=H.find("// abre com o setor urbano de maior IVSA selecionado"); _b=H.find("render();",_a); assert 0<_a<_b
H=H[:_a]+"// abre sem setor selecionado: a ficha só aparece depois de um clique\n"+H[_b:]
# ficha: botão de fechar; comparativo municipal vai para a faixa abaixo do mapa
_o='<div class="phead"><h2>Ficha do setor</h2></div>'; assert H.count(_o)==1
H=H.replace(_o,'<div class="phead"><h2>Ficha do setor</h2><button type="button" class="fxbtn" id="fx-close" title="Fechar a ficha e ampliar o mapa">Fechar ×</button></div>')
_o='\n    <h2 class="cmp-h">Comparativo municipal</h2>\n    <table class="cmp" id="cmp"></table>'; assert H.count(_o)==1
H=H.replace(_o,'')
_i=H.find('<div class="mapfoot"'); _j=H.find('<div class="mapfontes"',_i); _k=H.rfind('</div>',_i,_j); assert _i>0 and _k>_i
H=H[:_k]+'<aside class="mf-cmp" aria-label="Comparativo municipal"><h3>Comparativo municipal</h3><table class="cmp" id="cmp"></table></aside>\n'+H[_k:]
_o='<div class="def" id="t-def"></div>'; assert H.count(_o)==1
H=H.replace(_o,_o+'<div class="selhint">Clique em um setor do mapa para abrir a ficha do setor e os indicadores por tema.</div>')
_o="document.getElementById('ex-met').addEventListener('click',"; assert H.count(_o)==1
H=H.replace(_o,"document.getElementById('fx-close').addEventListener('click',clearSel);\ndocument.addEventListener('keydown',e=>{ if(e.key==='Escape'&&st.sel&&!document.querySelector('.hlpop:not([hidden]),.pdfpop:not([hidden])')) clearSel(); });\n"+_o)
CSSS="""
/* ---- ficha só com setor selecionado ---- */
.app{grid-template-columns:272px minmax(0,1fr)}
.app.has-sel{grid-template-columns:272px minmax(0,1fr) 384px}
.app:not(.has-sel)>.detail{display:none}
@media (max-width:1180px){.app,.app.has-sel{grid-template-columns:260px minmax(0,1fr)}}
@media (max-width:820px){.app,.app.has-sel{grid-template-columns:minmax(0,1fr)}}
.detail .phead{display:flex;align-items:center;justify-content:space-between;gap:8px}
.fxbtn{border:1px solid var(--line);background:var(--panel);color:var(--accent);font:700 12px var(--f-body);padding:4px 10px;border-radius:999px;cursor:pointer;white-space:nowrap}
.fxbtn:hover{border-color:var(--gold,#ffc000)}
.selhint{margin-top:4px;font-size:12.5px;color:var(--accent);font-weight:600}
.app.has-sel .selhint{display:none}
.mapfoot{grid-template-columns:minmax(0,1fr) minmax(300px,380px)}
.mf-cmp{border-left:1px solid var(--line);background:var(--panel-2);padding:10px 14px 12px;min-width:0;overflow-x:auto}
.mf-cmp h3{margin:0;font:700 11px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.mf-cmp .cmp{margin-top:4px;font-size:12.5px}
.app.has-sel .mapfoot .legend .lg-in{grid-template-columns:minmax(0,1fr)}
.app.has-sel .mapfoot .legend #hist{grid-column:1;grid-row:auto;height:70px}
@media (max-width:820px){.mapfoot{grid-template-columns:minmax(0,1fr)}.mf-cmp{border-left:0;border-top:1px solid var(--line)}}
"""
_k=H.find('</style>',H.find('<title>')); H=H[:_k]+CSSS+H[_k:]
H=H.replace('a ficha abre ao lado e os indicadores por tema logo abaixo do mapa,','a ficha abre ao lado e os indicadores por tema aparecem logo abaixo do mapa,')

# rótulos do mapa: escala por transform (evita o halo gigante em zoom alto, quando a fonte fica menor que 1 unidade)
import re as _rs
_n=0
def _fx(m):
    global _n; _n+=1
    return ".attr('font-size',%s).attr('stroke-width',%s).attr('transform',f=>{const q=proj([f.properties.lx,f.properties.ly]); return `translate(${q[0]},${q[1]}) scale(${1/k}) translate(${-q[0]},${-q[1]})`;})"%(m.group(1),m.group(2))
H=_rs.sub(r"\.attr\('font-size',([\d.]+)/k\)\.attr\('stroke-width',([\d.]+)/k\)",_fx,H)
assert _n==3,_n
_o="el.attr('display',null).attr('font-size',fsz/k).attr('stroke-width',3/k).attr('transform',`translate(${d.x},${d.y}) rotate(${d.a})`);"
assert H.count(_o)==1
H=H.replace(_o,"el.attr('display',null).attr('font-size',fsz).attr('stroke-width',3).attr('transform',`translate(${d.x},${d.y}) rotate(${d.a}) scale(${1/k})`);")
