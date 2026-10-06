# legenda e norte saem de cima do mapa e vão para uma faixa abaixo dele; painéis laterais acompanham a altura
def _cut(tag_open, tag):
    global H
    a=H.find(tag_open); assert a>0, tag_open
    i=a; depth=0
    import re as _r4
    for m in _r4.finditer(r'<(/?)'+tag+r'\b[^>]*>',H[a:]):
        depth+= -1 if m.group(1) else 1
        if depth==0: b=a+m.end(); break
    frag=H[a:b]; H=H[:a]+H[b:]; return frag
_leg=_cut('<details class="legend" open>','details')
_t='<div class="mapfontes" id="mapfontes">'; assert H.count(_t)==1
assert H.count(_t)==1
H=H.replace(_t,'<div class="mapfoot" aria-label="Legenda do mapa">\n'+_leg+'\n</div>\n    '+_t)
CSSG="""
/* ---- legenda e norte abaixo do mapa ---- */
.mapcard{height:auto}
.mapwrap{flex:none;height:max(520px,calc(100vh - var(--tb) - 170px))}
.mapfoot{display:grid;grid-template-columns:minmax(0,1fr);border-top:1px solid var(--line);background:var(--panel)}
.mapfoot .legend{position:static;width:auto;max-height:none;overflow:visible;background:none;backdrop-filter:none;-webkit-backdrop-filter:none;border:0;border-radius:0;box-shadow:none;min-width:0}
.mapfoot .legend summary{pointer-events:none;padding:10px 16px 4px}
.mapfoot .legend summary::after{content:none}
.mapfoot .legend .lg-in{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(240px,1fr);gap:5px 26px;padding:0 16px 12px;align-items:start}
.mapfoot .legend .lg-in>*{grid-column:1;min-width:0}
.mapfoot .legend #hist{grid-column:2;grid-row:1/span 9;height:84px;align-self:center}
.mapfoot .legend .bins{display:flex;flex-wrap:wrap;gap:4px 18px}
.mapfoot .legend .bin{white-space:nowrap}
.mapfoot .legend #ramp{grid-column:1/-1;flex-wrap:wrap}
.mapfoot .legend .chl{display:flex;flex-wrap:wrap;gap:3px 16px;width:100%}
.mapfoot .legend .chl span{white-space:nowrap}
@media (min-width:821px){.side{height:var(--mh,var(--h))}}
@media (min-width:1181px){.detail{height:var(--mh,var(--h))}}
@media (max-width:820px){
  .mapwrap{height:72vh;min-height:420px}
  .mapfoot{grid-template-columns:minmax(0,1fr)}
  .mapfoot .legend .lg-in{grid-template-columns:minmax(0,1fr)}
  .mapfoot .legend #hist{grid-column:1;grid-row:auto;height:70px}
}
"""
_k=H.find('</style>',H.find('<title>')); H=H[:_k]+CSSG+H[_k:]
JSG="""<script>
(function(){ const mc=document.querySelector('.mapcard'), app=document.querySelector('.app'); if(!mc||!app||!window.ResizeObserver) return;
  const set=()=>{ const h=mc.offsetHeight; if(h>0) app.style.setProperty('--mh',h+'px'); };
  new ResizeObserver(set).observe(mc); set(); window.addEventListener('resize',set);
})();
</script>
"""
_k=H.rfind('</body>'); H=H[:_k]+JSG+H[_k:]
