# legenda dinâmica: tudo o que estiver ligado em "Sobrepor" e em "Equipamentos" aparece na legenda do mapa
_o='<div class="hidleg" id="hidleg">'; assert H.count(_o)==1
H=H.replace(_o,'<div class="ovleg" id="ovleg" aria-label="Camadas sobrepostas e equipamentos ligados"></div>\n      '+_o)
CSSO="""
#hidleg,#appleg,#sgbleg,#fculeg{display:none!important}
.ovleg{display:flex;flex-direction:column;gap:6px;font-size:12.5px;color:var(--fg)}
.ovleg .og{display:flex;flex-wrap:wrap;gap:4px 16px;align-items:center}
.ovleg .ot{flex:0 0 100%;font:700 10.5px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.ovleg .oi{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.ovleg .oi svg{flex:none;display:block}
.mapfoot .legend #ovleg{grid-column:1/-1}
.ovleg .oi svg path,#eqboxes svg path{stroke:var(--fg);stroke-opacity:.55;stroke-width:.7}
.ramp .bar{position:static;z-index:auto;min-height:0;height:12px;display:block;background-color:transparent;backdrop-filter:none;-webkit-backdrop-filter:none;border:1px solid var(--line);top:auto}
"""
_k=H.find('</style>',H.find('<title>')); H=H[:_k]+CSSO+H[_k:]
JSO=r"""<script>
(function(){
  const el=document.getElementById('ovleg'); if(!el) return;
  const on=id=>{ const e=document.getElementById(id); return !!(e&&e.checked); };
  const ln=(col,w,dash,op)=>`<svg width="26" height="12"><line x1="1" y1="6" x2="25" y2="6" stroke="${col}" stroke-width="${w}"${dash?` stroke-dasharray="${dash}"`:''}${op?` stroke-opacity="${op}"`:''} stroke-linecap="round"/></svg>`;
  const bx=(fill,stroke,extra)=>`<svg width="20" height="13"><rect x="1" y="1" width="18" height="11" rx="2" fill="${fill}"${stroke?` stroke="${stroke}" stroke-width="1.5"`:''}/>${extra||''}</svg>`;
  const tx=(col,it)=>`<svg width="26" height="13"><text x="13" y="11" text-anchor="middle" font-size="11" font-weight="700" ${it?'font-style="italic"':''} fill="${col}">Abc</text></svg>`;
  const it=(sw,t)=>`<span class="oi">${sw}${t}</span>`;
  function draw(){
    const L=[];
    if(on('hid-on')) L.push(it(ln('var(--water-line)',3),'Rio'), it(ln('var(--water-line)',1),'Córrego / canal'), it(bx('var(--water)'),"Espelho d'água"));
    if(on('nmr-on')) L.push(it(tx('var(--water-text)',1),'Nomes de rios e ribeirões'));
    if(on('nmc-on')) L.push(it(tx('var(--water-text)',1),'Nomes de córregos e canais'));
    if(on('app-on')) L.push(it(bx('rgba(0,150,90,.8)'),'APP (faixa marginal e nascentes)'));
    if(on('bac-on')) L.push(it(ln('#b10026',3),'Bacia hidrográfica'));
    if(on('sbac-on')) L.push(it(ln('#e31a1c',1.6,'6 3'),'Sub-bacia'));
    if(on('mbac-on')) L.push(it(bx('rgba(106,27,154,.10)','#6a1b9a'),'Microbacia urbana'));
    if(on('utm-on')) L.push(it(ln('var(--fg)',1,null,.45),'Grade UTM (SIRGAS 2000, fuso 21 S)'));
    if(on('mun-on')) L.push(it(ln('var(--fg)',2,'6 4'),'Divisa municipal'));
    if(on('sgb-on')) L.push(it(bx('rgba(214,51,42,.35)','#9b2415'),'Área de risco mapeada (SGB/CPRM)'));
    if(on('fcu-on')) L.push(it(bx('var(--fcu)','var(--fcu-line)','<rect x="1" y="1" width="18" height="11" fill="url(#hatchF)"/>'),'Favela ou comunidade urbana (IBGE)'));
    const E=[]; document.querySelectorAll('#eqboxes label').forEach(lb=>{ const inp=lb.querySelector('input'); if(!inp||!inp.checked) return; const sv=lb.querySelector('svg'), c=lb.querySelector('.c'); let nm=''; lb.childNodes.forEach(n=>{ if(n.nodeType===3) nm+=n.textContent; }); E.push(it(sv?sv.outerHTML:'',nm.trim()+(c?' ('+c.textContent+')':''))); });
    el.innerHTML=(L.length?`<div class="og"><span class="ot">Camadas sobrepostas</span>${L.join('')}</div>`:'')+(E.length?`<div class="og"><span class="ot">Equipamentos</span>${E.join('')}</div>`:'');
    el.hidden=!(L.length||E.length);
  }
  const pane=document.getElementById('pane-cam');
  pane.addEventListener('change',()=>setTimeout(draw,0)); pane.addEventListener('click',()=>setTimeout(draw,30));
  draw(); setTimeout(draw,600);
})();
</script>
"""
_k=H.rfind('</body>'); H=H[:_k]+JSO+H[_k:]
# mesma regra no mapa em PDF/PNG: nomes de rios e córregos também entram na legenda
_o="  if(on('app-on')){ ctx.globalAlpha=OPA.app/100; sw('rgba(0,150,90,.85)',y);"; assert H.count(_o)==1
H=H.replace(_o,"  if(on('nmr-on')||on('nmc-on')){ ctx.fillStyle='#1c5f96'; ctx.font='italic 700 19px Arial'; ctx.fillText('Abc', cx, y); ctx.font='21px Arial'; ctx.fillStyle='#0f1d3a'; ctx.fillText('Nomes de '+[on('nmr-on')?'rios':'',on('nmc-on')?'córregos':''].filter(Boolean).join(' e '), cx+48, y); y+=32; }\n"+_o)
