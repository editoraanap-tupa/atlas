# tema claro/escuro com botão, barra adaptável e ajustes para tablet e celular (executado no fim de site.py)
# --- tema salvo aplicado antes da pintura
_k=H.find('</style>',H.find('<title>'))+len('</style>')
H=H[:_k]+"\n<script>try{var __t=localStorage.getItem('atlas-rmvrc-tema');if(__t==='dark'||__t==='light')document.documentElement.setAttribute('data-theme',__t);}catch(e){}</script>"+H[_k:]
# --- barra: filtros agrupados, botão de tema, botão de filtros (celular)
_a=H.find('<select id="munsel"'); _b=H.find('<nav aria-label="Páginas">'); assert 0<_a<_b
H=H[:_a]+'<button type="button" class="filtbtn" id="filt-btn" aria-expanded="false" aria-controls="filt">Filtros</button>\n    <div class="filt" id="filt">'+H[_a:_b].rstrip()+'</div>\n    '+H[_b:]
_c=H.find('</nav>',H.find('<nav aria-label="Páginas">'))+len('</nav>')
H=H[:_c]+'\n    <button type="button" class="thbtn" id="theme-btn" aria-label="Alternar entre tema claro e escuro" title="Alternar entre tema claro e escuro"><svg viewBox="0 0 24 24" aria-hidden="true" class="ic-sun"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.6M12 18.9v2.6M2.5 12h2.6M18.9 12h2.6M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M18.7 5.3l-1.8 1.8M7.1 16.9l-1.8 1.8"/></svg><svg viewBox="0 0 24 24" aria-hidden="true" class="ic-moon"><path d="M20 14.5A8.2 8.2 0 0 1 9.5 4a8.2 8.2 0 1 0 10.5 10.5z"/></svg><span></span></button>'+H[_c:]
# --- seletor de indicador e botão "mover mapa" (celular)
_o='<div class="mhtools">'; assert H.count(_o)==1
H=H.replace(_o,'<select id="indsel" class="munsel indsel" aria-label="Indicador do mapa"></select>\n      '+_o)
_o='<div class="zoombtns">'; assert H.count(_o)==1
H=H.replace(_o,'<button type="button" class="maplock" id="maplock" aria-pressed="false">Mover mapa</button>\n      '+_o)
_o='<div class="phead">\n      <div class="ptabs"'; assert H.count(_o)==1, H.count(_o)
H=H.replace(_o,'<button type="button" class="sidetog" id="sidetog" aria-expanded="false">Camadas e lista de indicadores</button>\n    '+_o)
# zoom por toque só com o mapa destravado (no celular a página rola normalmente sobre o mapa)
_o='svg.call(zoom);'; assert H.count(_o)==1
H=H.replace(_o,"zoom.filter(e=>(!e.ctrlKey||e.type==='wheel')&&!e.button&&!(window.__mapLock&&/^touch/.test(e.type)));\nsvg.call(zoom);")
CSST="""
/* ---- tema, barra adaptável, tablet e celular ---- */
.filt{display:contents}
.filtbtn,.sidetog,.maplock,.indsel{display:none}
.thbtn{flex:none;display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--panel);color:var(--fg);font:600 12.5px var(--f-body);padding:6px 10px;border-radius:999px;cursor:pointer}
.thbtn:hover{border-color:var(--gold,#ffc000)}
.thbtn svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.thbtn .ic-moon{display:none}
:root[data-theme="dark"] .thbtn .ic-sun{display:none}
:root[data-theme="dark"] .thbtn .ic-moon{display:block}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .thbtn .ic-sun{display:none}:root:not([data-theme="light"]) .thbtn .ic-moon{display:block}}
:root{--ipt:#fdbb84;--halo:#ffffff}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ipt:#8a4a14;--halo:#0d1830}}
:root[data-theme="dark"]{--ipt:#8a4a14;--halo:#0d1830}
.iptb{background:linear-gradient(90deg,var(--ipt) var(--v),transparent var(--v))}
html{scroll-padding-top:calc(var(--tb) + 10px)}
@media (max-width:1180px){
  .mapfoot .legend .lg-in{grid-template-columns:minmax(0,1fr)}
  .mapfoot .legend #hist{grid-column:1;grid-row:auto;height:70px}
  .xsubg{grid-template-columns:repeat(2,minmax(0,1fr))}
  .dt{font-size:13px}
}
@media (max-width:1024px){
  .mapfoot{grid-template-columns:minmax(0,1fr)}
  .mf-cmp{border-left:0;border-top:1px solid var(--line)}
  .kpis.vk{grid-template-columns:repeat(2,minmax(0,1fr))}
  .odsg{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:820px){
  .bar{position:sticky;top:env(safe-area-inset-top,0px)}
  .bar .wrap{flex-wrap:wrap;gap:6px 8px;padding-block:7px}
  .bar nav{order:1;flex:1 1 0;min-width:0;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;margin-left:0}
  .bar nav::-webkit-scrollbar{display:none}
  .bar nav a{white-space:nowrap;flex:none}
  .thbtn{order:2;padding:6px 8px}.thbtn span{display:none}
  .filtbtn{order:3;display:inline-flex;align-items:center;border:1px solid var(--line);background:var(--panel);color:var(--fg);font:600 12.5px var(--f-body);padding:6px 10px;border-radius:999px;cursor:pointer}
  .filtbtn[aria-expanded="true"]{background:var(--accent);border-color:var(--accent);color:var(--panel)}
  .filt{order:4;display:none;flex:1 1 100%;flex-wrap:wrap;gap:8px;align-items:center;padding-top:4px}
  .bar.open .filt{display:flex}
  .filt .munsel{flex:1 1 180px}.filt .search{flex:1 1 160px}.filt .search input{width:100%}
  .sidetog{display:flex;width:100%;justify-content:space-between;align-items:center;border:0;background:none;color:var(--fg);font:700 14px var(--f-display);padding:12px 2px;cursor:pointer}
  .sidetog::after{content:"▾";color:var(--muted)}
  .side.mopen .sidetog::after{content:"▴"}
  .side:not(.mopen)>:not(.sidetog){display:none!important}
  .side{padding-bottom:4px}
  .indsel{display:block;width:100%;margin-top:8px}
  .maphead>div:first-child{flex:1 1 100%}
  .mhtools{flex-wrap:wrap;gap:6px}
  .mapwrap{height:62vh;min-height:360px}
  .maplock{position:absolute;left:50%;top:10px;transform:translateX(-50%);z-index:4;border:1px solid var(--line);background:var(--panel);color:var(--fg);font:700 12.5px var(--f-body);padding:7px 14px;border-radius:999px;box-shadow:var(--shadow)}
  .maplock[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--panel)}
  body.touch .maplock{display:block}
  #map.locked{touch-action:pan-y}
  .sec-h{margin-top:30px}
  .sec-h h2{font-size:clamp(1.35rem,6vw,1.9rem)}
  .block{padding:14px 14px}
  .subnav{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin-right:-16px;padding-right:16px}
  .subnav::-webkit-scrollbar{display:none}
  .subnav a,.subnav span{flex:none;white-space:nowrap}
  .crumb .ppdf{margin-left:0}
  .odsg{grid-template-columns:minmax(0,1fr)}
  .lenses{grid-template-columns:repeat(2,minmax(0,1fr))}
  .pdfwrap{margin-left:0}
  .pdfpop{right:auto;left:0}
  .dcard dl{grid-template-columns:minmax(0,1fr)}
  .pnav{grid-template-columns:minmax(0,1fr)}
  .hlp{width:26px;height:26px}
  .seg button{padding:8px 11px}
}
@media (max-width:480px){
  .kpis.vk{grid-template-columns:minmax(0,1fr)}
  .dg-pop{grid-template-columns:repeat(2,minmax(0,1fr))}
  .edts{grid-template-columns:minmax(0,1fr)}
  .edts .edt:first-child{grid-column:auto}
}
"""
_k=H.find('</style>',H.find('<title>')); H=H[:_k]+CSST+H[_k:]
JST=r"""<script>
(function(){
  const root=document.documentElement, bar=document.querySelector('.bar');
  // tema
  const tb=document.getElementById('theme-btn'), mq=matchMedia('(prefers-color-scheme: dark)');
  const cur=()=>root.getAttribute('data-theme')||(mq.matches?'dark':'light');
  const lab=()=>{ const d=cur()==='dark'; tb.querySelector('span').textContent=d?'Escuro':'Claro'; tb.title=d?'Tema escuro ativo. Clique para o tema claro.':'Tema claro ativo. Clique para o tema escuro.'; tb.setAttribute('aria-pressed',d); };
  tb.addEventListener('click',()=>{ const n=cur()==='dark'?'light':'dark'; root.setAttribute('data-theme',n); try{localStorage.setItem('atlas-rmvrc-tema',n);}catch(e){} lab(); window.dispatchEvent(new Event('resize')); });
  mq.addEventListener&&mq.addEventListener('change',lab);
  new MutationObserver(lab).observe(root,{attributes:true,attributeFilter:['data-theme']}); lab();
  // altura real da barra fixa -> posição dos painéis e das âncoras
  const setTb=()=>{ const h=Math.round(bar.getBoundingClientRect().height); if(h>0) root.style.setProperty('--tb',h+'px'); };
  if(window.ResizeObserver) new ResizeObserver(setTb).observe(bar); window.addEventListener('resize',setTb); setTb();
  // filtros no celular
  const fb=document.getElementById('filt-btn');
  fb.addEventListener('click',()=>{ const o=bar.classList.toggle('open'); fb.setAttribute('aria-expanded',o); });
  // painel lateral recolhível no celular
  const st=document.getElementById('sidetog'), side=document.querySelector('.side');
  st.addEventListener('click',()=>{ const o=side.classList.toggle('mopen'); st.setAttribute('aria-expanded',o); });
  // seletor de indicador (celular)
  const sel=document.getElementById('indsel'), menu=document.getElementById('menu');
  const fill=()=>{ sel.innerHTML=[...menu.querySelectorAll('.axis')].map(ax=>`<optgroup label="${ax.querySelector('h3').textContent}">`+[...ax.querySelectorAll('.ind')].map(b=>`<option value="${b.dataset.k}">${b.textContent}</option>`).join('')+'</optgroup>').join(''); sync(); };
  const sync=()=>{ const b=menu.querySelector('.ind[aria-pressed="true"]'); if(b) sel.value=b.dataset.k; };
  sel.addEventListener('change',()=>{ const b=document.getElementById('i-'+sel.value); if(b) b.click(); });
  new MutationObserver(sync).observe(document.getElementById('t-ind'),{childList:true,characterData:true,subtree:true}); fill();
  // gestos do mapa em telas de toque
  const map=document.getElementById('map'), lk=document.getElementById('maplock'), touch=matchMedia('(pointer: coarse)').matches;
  if(touch){ document.body.classList.add('touch'); window.__mapLock=true; map.classList.add('locked');
    lk.addEventListener('click',()=>{ window.__mapLock=!window.__mapLock; map.classList.toggle('locked',window.__mapLock); lk.setAttribute('aria-pressed',!window.__mapLock); lk.textContent=window.__mapLock?'Mover mapa':'Travar mapa'; }); }
})();
</script>
"""
_k=H.rfind('</body>'); H=H[:_k]+JST+H[_k:]
# rótulos do mapa: halo acompanha o tema
# --- mapa do bairro (canvas da ficha) acompanha o tema; relatórios em PDF continuam claros
_a=H.find('function drawBairroMap'); _b=H.find('\nfunction ',_a+10); _s=H[_a:_b]
def _r(a,b,n=1):
    global _s
    assert _s.count(a)>=1,a; _s=_s.replace(a,b,n)
_r("{pad=.12, lw=2, labels=true, font=13}={}","{pad=.12, lw=2, labels=true, font=13, dark=false}={}")
_r("ctx.fillStyle='#f1f4fa'; ctx.fillRect(0,0,W2,H2);","ctx.fillStyle=dark?'#12203d':'#f1f4fa'; ctx.fillRect(0,0,W2,H2);")
_r("ctx.lineWidth=Math.max(.8,lw/2); ctx.strokeStyle='#ffffff';","ctx.lineWidth=Math.max(.8,lw/2); ctx.strokeStyle=dark?'#0d1830':'#ffffff';")
_r("ctx.fillStyle='#e2e7e2'; ctx.fill(); ctx.stroke();","ctx.fillStyle=dark?'#26355a':'#e2e7e2'; ctx.fill(); ctx.stroke();")
_r("ctx.strokeStyle='#2f7fc1';","ctx.strokeStyle=dark?'#6fb3e8':'#2f7fc1';")
_r("tr(f.geometry); ctx.strokeStyle='#ffffff'; ctx.lineWidth=lw*3.2; ctx.stroke(); ctx.strokeStyle='#0f1d3a';","tr(f.geometry); ctx.strokeStyle=dark?'#0d1830':'#ffffff'; ctx.lineWidth=lw*3.2; ctx.stroke(); ctx.strokeStyle=dark?'#ffffff':'#0f1d3a';")
_r("ctx.fillStyle='rgba(255,255,255,.85)'; ctx.fillRect(m-6, H2-m-fs2-16, bw+24, fs2+26);\n  ctx.fillStyle='#0f1d3a';","ctx.fillStyle=dark?'rgba(13,24,48,.88)':'rgba(255,255,255,.85)'; ctx.fillRect(m-6, H2-m-fs2-16, bw+24, fs2+26);\n  ctx.fillStyle=dark?'#e8edf7':'#0f1d3a';")
_r("ctx.strokeStyle='#c8d0ca'; ctx.lineWidth=2; ctx.strokeRect(1,1,W2-2,H2-2);","ctx.strokeStyle=dark?'#233253':'#c8d0ca'; ctx.lineWidth=2; ctx.strokeRect(1,1,W2-2,H2-2);")
H=H[:_a]+_s+H[_b:]
_o="drawBairroMap(cv,f,{lw:2,font:15})"; assert H.count(_o)==1
H=H.replace(_o,"drawBairroMap(cv,f,{lw:2,font:15,dark:(document.documentElement.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))==='dark'})")
_o='border:2.5px solid #14221f;display:inline-block"></i>setor selecionado'; assert H.count(_o)==1
H=H.replace(_o,'border:2.5px solid var(--fg);display:inline-block"></i>setor selecionado')
_o='<i style="width:12px;height:10px;background:#e2e7e2;display:inline-block"></i>outros bairros'; assert H.count(_o)==1
H=H.replace(_o,'<i style="width:12px;height:10px;background:var(--nodata);display:inline-block"></i>outros bairros')
H=H.replace(' (IVSA) com pesos ajustáveis',' (IVSA)')
# --- menu em lista no celular
_o='<nav aria-label="Páginas">'; assert H.count(_o)==1
H=H.replace(_o,'<button type="button" class="navbtn" id="nav-btn" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg><span>Menu</span></button>\n    '+_o)
CSST2="""
.navbtn{display:none}
.note a,.afer a,.acard a,.fcols a,.notes article a,.about a,.ac-a a{color:var(--accent);text-underline-offset:2px}
.refs li,.fcols li,.notes li,.note,.dcard dd,.about p{overflow-wrap:anywhere}
#lab-rank{min-width:760px}
@media (max-width:1180px){
  .app.has-sel>.side{position:static}
  #detail{columns:2 320px;column-gap:14px}
  #detail>.sname,#detail>.meta{column-span:all}
  #detail .card{break-inside:avoid;margin-top:0;margin-bottom:12px}
}
@media (max-width:820px){
  .navbtn{order:1;flex:1 1 0;min-width:0;display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);background:var(--panel);color:var(--fg);font:700 13.5px var(--f-display);padding:7px 12px;border-radius:999px;cursor:pointer}
  .navbtn svg{width:17px;height:17px;flex:none;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round}
  .navbtn span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .navbtn[aria-expanded="true"]{border-color:var(--gold,#ffc000)}
  .bar nav{order:5;display:none;flex:1 1 100%;overflow:visible}
  .bar.navopen nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;padding:4px 0 6px}
  .bar nav a{border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-size:14px;background:var(--panel)}
  .bar .wrap>.hlp{display:none}
  .dcard summary{display:grid;grid-template-columns:auto minmax(0,1fr);gap:2px 8px;align-items:baseline}
  .dcard summary>span,.dcard summary>.odsw{grid-column:2;margin-left:0;justify-self:start}
}
"""
_k=H.find('</style>',H.find('<title>')); H=H[:_k]+CSST2+H[_k:]
JST2=r"""<script>
(function(){ const bar=document.querySelector('.bar'), nb=document.getElementById('nav-btn'), lab=nb.querySelector('span');
  const sync=()=>{ const a=bar.querySelector('nav a[aria-current="page"]'); lab.textContent=a?('Menu · '+a.textContent):'Menu'; };
  nb.addEventListener('click',()=>{ const o=bar.classList.toggle('navopen'); nb.setAttribute('aria-expanded',o); });
  bar.querySelector('nav').addEventListener('click',e=>{ if(e.target.closest('a')){ bar.classList.remove('navopen'); nb.setAttribute('aria-expanded','false'); } });
  new MutationObserver(sync).observe(bar.querySelector('nav'),{attributes:true,subtree:true,attributeFilter:['aria-current']}); sync();
})();
</script>
"""
_k=H.rfind('</body>'); H=H[:_k]+JST2+H[_k:]
