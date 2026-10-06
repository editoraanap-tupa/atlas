# painel de indicadores por eixo abaixo do mapa (executado dentro de site.py)
a=H.find('  // eixos\n  for(const ax of'); b=H.find('  el.innerHTML=h; afterDetail(p);',a)
assert a>0 and b>a
H=H[:a]+"  h+=`<button class=\"btn ghost eix-go\" type=\"button\" onclick=\"document.getElementById('ficha').scrollIntoView({behavior:'smooth',block:'start'})\">Ver todos os indicadores por tema ↓</button>`;\n"+H[b:]
rep('  el.innerHTML=h; afterDetail(p);','  el.innerHTML=h; afterDetail(p); renderEixos(p);')
JSE=r"""
// ------- painel de indicadores por tema -------
const ECOL=['#d73027','#fc8d59','#e8c547','#91cf60','#1a9850']; // índice = classe da condição (0 pior … 4 melhor)
const MUNC={'Nossa Senhora do Livramento':'N. Sra. Livr.','Santo Antônio de Leverger':'Sto. Ant. Lev.','Chapada dos Guimarães':'Chapada','Várzea Grande':'Várzea Gde.'};
const _mm={};
function munMed(k,mun){ const key=k+'|'+mun; if(!(key in _mm)){ const xs=F.filter(f=>f.properties.mun===mun&&f.properties.sit==='Urbana').map(f=>f.properties[k]).filter(v=>v!=null); _mm[key]=xs.length?d3.median(xs):null; } return _mm[key]; }
function rmMed(k){ const a=sorted[k]; return a&&a.length?d3.quantile(a,.5):null; }
function ecls(c){ return c==null?null:Math.min(4,Math.floor(c*5)); }
function ecol(i,v){ const c=v==null?null:cond(i,v); return c==null?'var(--accent)':ECOL[ecls(c)]; }
function eflag(i,v){ const c=v==null?null:cond(i,v); return c==null?'':c<=.2?'<span class="flag bad">20% piores</span>':c>=.8?'<span class="flag good">20% melhores</span>':''; }
function frase(i,v){
  const a=sorted[i.k]; if(v==null||!a||!a.length||i.pol==='n') return '';
  const n=a.length, lo=d3.bisectLeft(a,v)/n, hi=d3.bisectRight(a,v)/n, eq=hi-lo;
  const pior = i.pol==='r'? lo : 1-hi, melhor = i.pol==='r'? 1-hi : lo;
  if(eq>=.5) return `Igual a ${Math.round(eq*100)}% dos setores`;
  if(pior>=.5) return `<b>Pior</b> que ${Math.round(pior*100)}% dos setores`;
  if(melhor>=.5) return `<b>Melhor</b> que ${Math.round(melhor*100)}% dos setores`;
  return 'Na faixa intermediária';
}
function strip(i,v){
  const c=v==null?null:cond(i,v);
  let s='<svg class="strip" viewBox="0 0 200 26" role="img" aria-label="Posição entre os setores">';
  for(let j=0;j<5;j++) s+=`<rect x="${j*40+(j?1:0)}" y="8" width="${j?39:40}" height="9" rx="${j===0||j===4?4:0}" fill="${ECOL[4-j]}" opacity="${c==null?.25:.9}"/>`;
  if(c!=null){ const x=Math.max(3,Math.min(197,(1-c)*200)); s+=`<path d="M${x-6} 0 h12 l-6 7z" fill="var(--fg)"/><line x1="${x}" x2="${x}" y1="6" y2="20" stroke="var(--fg)" stroke-width="2"/>`; }
  s+='<text x="0" y="26" font-size="7.5" fill="var(--muted)">melhor</text><text x="200" y="26" text-anchor="end" font-size="7.5" fill="var(--muted)">pior</text></svg>';
  return s;
}
const ECLS=['muito pior','pior','intermediário','melhor','muito melhor'];
function gauge(i,v){
  const c=v==null?null:cond(i,v), cx=70, cy=66, r=52, sw=15;
  let s=`<svg class="gauge2" viewBox="0 0 140 84" role="img" aria-label="${c==null?'sem dado':'Classe: '+ECLS[ecls(c)]}">`;
  for(let j=0;j<5;j++){ const a0=Math.PI*(1+j/5)+(j?0.018:0), a1=Math.PI*(1+(j+1)/5)-(j<4?0.018:0);
    s+=`<path d="M${(cx+r*Math.cos(a0)).toFixed(2)} ${(cy+r*Math.sin(a0)).toFixed(2)} A${r} ${r} 0 0 1 ${(cx+r*Math.cos(a1)).toFixed(2)} ${(cy+r*Math.sin(a1)).toFixed(2)}" fill="none" stroke="${ECOL[4-j]}" stroke-width="${sw}" opacity="${c==null?.25:(c!=null&&4-j===ecls(c)?1:.55)}"/>`; }
  if(c!=null){ const a=Math.PI*(1+Math.max(.02,Math.min(.98,1-c))), L=r-4;
    s+=`<line x1="${cx}" y1="${cy}" x2="${(cx+L*Math.cos(a)).toFixed(2)}" y2="${(cy+L*Math.sin(a)).toFixed(2)}" stroke="var(--fg)" stroke-width="3.2" stroke-linecap="round"/><circle cx="${cx}" cy="${cy}" r="6" fill="var(--fg)"/><circle cx="${cx}" cy="${cy}" r="2.4" fill="var(--panel)"/>`; }
  s+=`<text x="${cx-r}" y="${cy+16}" text-anchor="middle" font-size="10" fill="var(--muted)">melhor</text><text x="${cx+r}" y="${cy+16}" text-anchor="middle" font-size="10" fill="var(--muted)">pior</text></svg>`;
  return s;
}
function cpill(i,v){ const c=v==null?null:cond(i,v); if(c==null) return '<span class="cpill nd">sem dado</span>'; const k=ecls(c); return `<span class="cpill" style="background:${ECOL[k]};color:${k===0||k===4?'#fff':'#1d1d1d'}">${ECLS[k]}</span>`; }
function riskTile(k,kp,p){
  const i=byK[k], v=p[k]; if(!i) return '';
  const mor = kp&&p[kp]!=null ? `<div class="et-sub"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="5" r="3"/><path d="M2 15c0-3.5 2.7-5.5 6-5.5s6 2 6 5.5z"/></svg>≈ ${fv(kp,p[kp])} moradores</div>` : '';
  const med=rmMed(k);
  return `<div class="etile rt"><div class="et-n">${i.n}</div>
    <div class="rt-g">${gauge(i,v)}<div class="rt-v"><div class="et-v">${fv(k,v)}</div>${cpill(i,v)}</div></div>
    ${mor}<div class="rt-f"><div class="et-f">${v==null?'sem dado':frase(i,v)}</div><div class="et-m">${med===0?'Na maioria dos setores: '+fv(k,0):'Mediana RMVRC: '+fv(k,med)}</div></div></div>`;
}
function donut(k,p){
  const i=byK[k]; if(!i) return ''; const v=p[k]; const r=30, C=2*Math.PI*r, f=v==null?0:Math.max(0,Math.min(100,v))/100;
  const col=ecol(i,v);
  return `<div class="edon"><svg viewBox="0 0 80 80" role="img" aria-label="${i.n}: ${fv(k,v)}"><circle cx="40" cy="40" r="${r}" fill="none" stroke="var(--line)" stroke-width="10"/>${v==null?'':`<circle cx="40" cy="40" r="${r}" fill="none" stroke="${col}" stroke-width="10" stroke-dasharray="${(C*f).toFixed(1)} ${C.toFixed(1)}" transform="rotate(-90 40 40)" stroke-linecap="${f>0&&f<1?'round':'butt'}"/>`}<text x="40" y="45" text-anchor="middle" font-size="15" font-weight="800" fill="var(--fg)" font-family="var(--f-display)">${v==null?'—':Math.round(v)+'%'}</text></svg>
  <div class="ed-n">${i.n}</div>${eflag(i,v)}<div class="et-m">RMVRC: ${fv(k,rmMed(k))}</div></div>`;
}
function trio(k,p){
  const i=byK[k]; if(!i) return ''; const v=p[k], vm=munMed(k,p.mun), vr=rmMed(k);
  const vals=[v,vm,vr], mx=d3.max(vals.filter(x=>x!=null))||1, Hh=96, bw=42, gap=22, pad=14, W0=3*bw+2*gap+2*pad;
  const labs=['Setor',MUNC[p.mun]||p.mun,'RMVRC'];
  let s=`<svg class="trio" viewBox="0 0 ${W0} ${Hh+34}" role="img" aria-label="${i.n}: setor ${fv(k,v)}, ${p.mun} ${fv(k,vm)}, RMVRC ${fv(k,vr)}">`;
  vals.forEach((x,j)=>{ const X=pad+j*(bw+gap); const h=x==null?0:Math.max(2,(Hh-16)*x/mx); const y=Hh-h;
    s+=`<rect x="${X}" y="${y}" width="${bw}" height="${h}" rx="4" fill="${j===0?ecol(i,v):'var(--trio-ref)'}"/>`;
    s+=`<text x="${X+bw/2}" y="${y-4}" text-anchor="middle" font-size="11" font-weight="${j===0?800:600}" fill="var(--fg)">${fv(k,x)}</text>`;
    s+=`<text x="${X+bw/2}" y="${Hh+13}" text-anchor="middle" font-size="10.5" fill="var(--muted)" font-weight="${j===0?700:400}">${labs[j]}</text>`; });
  s+=`<line x1="${pad-4}" x2="${W0-pad+4}" y1="${Hh}" y2="${Hh}" stroke="var(--line)"/></svg>`;
  return `<div class="etrio"><div class="et-n">${i.n}${eflag(i,v)}</div>${s}<div class="et-f">${v==null?'sem dado':frase(i,v)}</div></div>`;
}
function waffle(k,p){
  const i=byK[k]; const v=p[k]; if(v==null) return `<div class="etile"><div class="et-n">${i.n}</div><div class="et-f">sem dado</div></div>`;
  const n=Math.round(v), col=ecol(i,v); let s='<svg class="waf" viewBox="0 0 100 100" role="img" aria-label="'+n+' em cada 100">';
  for(let j=0;j<100;j++){ const x=(j%10)*10+5, y=Math.floor(j/10)*10+5; s+=`<circle cx="${x}" cy="${y}" r="3.6" fill="${j<n?col:'var(--line)'}"/>`; }
  s+='</svg>';
  return `<div class="ewaf">${s}<div><div class="et-n">${i.n}${eflag(i,v)}</div><div class="et-v">${n} <small>em cada 100</small></div><div class="et-f">pessoas com 15 anos ou mais não sabem ler e escrever. Mediana RMVRC: ${fv(k,rmMed(k))}</div><div class="et-f">${frase(i,v)}</div></div></div>`;
}
function demTile(k,p){ const i=byK[k]; if(!i) return ''; return `<div class="edt"><div class="et-n">${i.n}</div><div class="et-v">${fv(k,p[k])}</div><div class="et-m">${MUNC[p.mun]||p.mun}: ${fv(k,munMed(k,p.mun))} · RMVRC: ${fv(k,rmMed(k))}</div></div>`; }
function ehead(ax,sub){ return `<div class="ep-h"><span class="dot" style="background:${AX[ax].cor}"></span><h3>${AX[ax].nome}</h3><span>${sub}</span></div>`; }
function renderEixos(p){
  const el=document.getElementById('eixos'); if(!el) return;
  document.getElementById('eixo-nome').textContent=' · '+(p.bairro||p.dist||'Setor')+' ('+p.mun+')';
  let h='';
  h+=`<div class="ep s6">${ehead('amb','')}<div class="barkey" aria-label="Como ler as barras"><b class="bk-t">Como ler as barras</b>
      <div class="bk-i"><span class="bk-s"><span class="track"><i style="width:62%;background:#e31a1c"></i></span></span><span><b>Barra colorida</b> = valor deste setor. Quanto mais comprida, maior o valor.</span></div>
      <div class="bk-i"><span class="bk-s"><span class="track"><b style="left:38%"></b></span></span><span><b>Marcador de referência</b> (linha vertical) = mediana da RMVRC, o valor central da distribuição: metade dos setores tem menos, metade tem mais. Se a barra ultrapassa o marcador, o setor está acima da mediana. Quando a mediana é zero, o marcador fica na origem da escala.</span></div>
      <div class="bk-i"><span class="bk-s"><span class="track"></span></span><span><b>Faixa de fundo</b> = escala do indicador: de 0 a 100% nas porcentagens; nos demais, de zero até os valores mais altos da região.</span></div>
      <div class="bk-i"><span class="bk-s"><span class="track"><i style="width:50%;background:#fee08b"></i><i style="left:50%;width:50%;background:#bd0026"></i></span></span><span><b>Cor</b> = posição entre os setores: amarelo, situação melhor; vermelho, pior. As etiquetas "20% piores" e "20% melhores" marcam os extremos.</span></div>
    </div><div class="ebul">${IND.filter(i=>i.ax==='amb'&&!['ndvi','arv5'].includes(i.k)).map(i=>bulletRow(i,p)).join('')}</div>${typeof satNote==='function'&&satNote(p)?`<p class="satnote">${satNote(p)}</p>`:''}</div>`;
  h+=`<div class="ep s3">${ehead('san','% dos domicílios')}<div class="edons">${['agua','agua_enc','esgoto','esg_prec','lixo','sem_banh'].map(k=>donut(k,p)).join('')}</div></div>`;
  h+=`<div class="ep s3">${ehead('ent','% dos domicílios com o item na face de quadra')}<div class="edons">${['arvore','pav','calcada','bueiro','luz','onibus'].map(k=>donut(k,p)).join('')}</div></div>`;
  h+=`<div class="ep s3">${ehead('ace','distância em linha reta · setor × mediana do município × RMVRC')}<div class="etrios g2">${['d_ubs','d_saude','d_esc','d_parque'].map(k=>trio(k,p)).join('')}</div></div>`;
  h+=`<div class="ep s3 eren">${ehead('ren','setor × mediana do município × RMVRC')}${trio('renda',p)}${waffle('analf',p)}</div>`;
  h+=`<div class="ep s6">${ehead('dem','')}<div class="edem"><div class="edts">${['pop','dens','criancas','idosos','negros','indig','mor'].map(k=>demTile(k,p)).join('')}</div><div class="epyr"><div class="esub" style="margin-top:0">Pirâmide etária (% dos moradores)</div>${pyramidSVG(p)}</div></div></div>`;
  el.innerHTML=h;
}
"""
rep('// ------- IVSA com pesos ajustáveis -------',JSE+'\n// ------- IVSA com pesos ajustáveis -------')
CSSE="""
:root{--trio-ref:#b9c3d6}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--trio-ref:#4a5878}}
:root[data-theme="dark"]{--trio-ref:#4a5878}
.eix-go{margin-top:12px;width:100%}
.eixos{margin-top:16px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px 20px;box-shadow:var(--shadow);scroll-margin-top:calc(var(--tb) + 12px)}
.eh-n{font:600 .62em var(--f-body);color:var(--muted);letter-spacing:0}
.ekey{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:center;font-size:12.5px;color:var(--muted);margin:-4px 0 14px}
.ekey span{display:inline-flex;align-items:center;gap:5px}.ekey i{width:14px;height:10px;border-radius:2px;display:inline-block}
.ekey em{font-style:normal;opacity:.85}
.egrid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px}
.eempty{grid-column:1/-1;padding:22px;border:1.5px dashed var(--line);border-radius:12px;text-align:center}
.ep{background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:12px 14px 14px;min-width:0}
.ep.s6{grid-column:span 6}.ep.s4{grid-column:span 4}.ep.s3{grid-column:span 3}.ep.s2{grid-column:span 2}
@media (max-width:1100px){.ep.s4,.ep.s2{grid-column:span 3}}
@media (max-width:820px){.ep.s4,.ep.s3,.ep.s2{grid-column:span 6}}
.ep-h{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.ep-h .dot{width:10px;height:10px;border-radius:50%}
.ep-h h3{margin:0;font:800 15px var(--f-display);color:var(--fg)}
.ep-h span:last-child{font-size:12.5px;color:var(--muted)}
.esub{font:700 11px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:10px 0 6px}
.etiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}
.etile.rt{display:flex;flex-direction:column;gap:4px}
.rt .et-n{min-height:2.6em}
.rt-g{display:flex;flex-direction:column;align-items:center;gap:2px}
.gauge2{width:min(160px,100%);height:auto;flex:none}
.rt-v{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:4px 8px;min-width:0;margin-top:-4px}
.rt-v .et-v{margin:0}
.cpill{font:700 11px var(--f-body);padding:2px 8px;border-radius:999px;white-space:nowrap}
.cpill.nd{background:var(--line);color:var(--muted)}
.et-sub{display:flex;align-items:center;justify-content:center;gap:5px}
.et-sub svg{width:13px;height:13px;fill:var(--muted)}
.rt-f{margin-top:auto;padding-top:6px;border-top:1px solid var(--line)}
.etile,.etrio,.edon,.edt,.ewaf{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 12px;min-width:0}
.et-n{font:600 13px/1.3 var(--f-body);color:var(--fg)}
.et-v{font:800 22px/1.15 var(--f-display);color:var(--fg);margin-top:4px;font-variant-numeric:tabular-nums}
.et-v small{font:600 12px var(--f-body);color:var(--muted)}
.et-sub{font-size:12.5px;color:var(--muted)}
.et-f{font-size:12.5px;color:var(--fg);margin-top:2px;line-height:1.4}
.et-m{font-size:11.5px;color:var(--muted);margin-top:2px}
.strip{width:100%;height:auto;display:block;margin-top:6px}
.edons{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
@media (max-width:480px){.edons{grid-template-columns:repeat(2,minmax(0,1fr))}}
.edon{text-align:center;display:flex;flex-direction:column;align-items:center;gap:2px}
.edon svg{width:84px;height:84px}
.ed-n{font:600 12.5px/1.25 var(--f-body);color:var(--fg)}
.etrios{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
.etrios.one{grid-template-columns:minmax(0,1fr)}

.trio{width:100%;max-width:300px;height:auto;display:block;margin:8px auto 2px;font-family:var(--f-body)}
.ewaf{display:flex;gap:12px;align-items:flex-start;margin-top:10px}
.ewaf .waf{width:96px;height:96px;flex:none}
.edem{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:14px;align-items:start}
@media (max-width:900px){.edem{grid-template-columns:minmax(0,1fr)}}
.edts{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
.epyr{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 12px;min-width:0;overflow-x:auto}
"""
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSSE+H[k:]

CSS3="""
.satnote{margin:10px 0 0;font-size:12.5px;line-height:1.45;color:var(--muted);border-left:3px solid var(--line);padding-left:10px}
.barkey{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 24px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:2px 0 12px;font-size:13px;line-height:1.45}
.barkey .bk-t{grid-column:1/-1;font:700 11px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.bk-i{display:grid;grid-template-columns:64px minmax(0,1fr);gap:10px;align-items:start}
.bk-s{padding-top:6px}
.bk-s .track{display:block;position:relative;height:8px;border-radius:4px;background:var(--line)}
.bk-s .track i{position:absolute;left:0;top:0;bottom:0;border-radius:4px}
.bk-s .track b{position:absolute;top:-4px;bottom:-4px;width:2px;background:var(--fg)}
@media (max-width:820px){.barkey{grid-template-columns:minmax(0,1fr)}}
.ebul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2px 28px}
@media (max-width:1100px){.ebul{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.ebul{grid-template-columns:minmax(0,1fr)}}
.ebul .bullet{padding:5px 0}
.ep.s3{display:flex;flex-direction:column}
.etrios.g2{grid-template-columns:repeat(2,minmax(0,1fr));flex:1}
@media (max-width:520px){.etrios.g2{grid-template-columns:minmax(0,1fr)}}
.etrio{display:flex;flex-direction:column}
.etrio .trio{margin-top:auto}
.eren{gap:10px}
.eren>.etrio{flex:1}
.eren>.etrio .trio{max-width:300px;margin:auto}
.eren .ewaf{margin-top:0}
.ewaf .waf{width:110px;height:110px}
.edem{grid-template-columns:minmax(0,1fr) 400px;align-items:stretch}
.edts{grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:1fr}
.edts .edt:first-child{grid-column:span 2}
.edts .edt:first-child .et-v{font-size:30px}
.edt{display:flex;flex-direction:column;justify-content:center}
.edt .et-v{font-size:26px}
@media (max-width:1100px){.edts{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){.edem{grid-template-columns:minmax(0,1fr)}}
"""
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSS3+H[k:]
