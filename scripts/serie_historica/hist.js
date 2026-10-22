// ------- Série histórica municipal (IBGE, Censos 1991, 2000, 2010 e 2022) -------
const HK=[
  {k:'pop',n:'População residente',s:'habitantes',t:'n'},
  {k:'dom',n:'Domicílios',s:'particulares permanentes ocupados',t:'n'},
  {k:'agua',n:'Água da rede geral',s:'% dos domicílios',t:'p',num:'agua',den:'dom'},
  {k:'esg',n:'Esgoto em rede',s:'% dos domicílios · rede geral ou pluvial',t:'p',num:'esg',den:'dom'},
  {k:'lixo',n:'Lixo coletado',s:'% dos domicílios',t:'p',num:'lixo',den:'dom'},
  {k:'alf',n:'Alfabetização',s:'% das pessoas de 15 anos ou mais',t:'p',num:'alf',den:'p15'}
];
const HKT=[...HK.slice(0,2),{k:'urb',n:'Urbanização',s:'% da população',t:'p',num:'popu',den:'pop'},...HK.slice(2)];
const HMUN=Object.keys(HIST.mun), HY=HIST.anos;
let HSEL='Cuiabá', HIND='esg';
function hRec(name){
  if(HIST.mun[name]) return HIST.mun[name];
  const ms=name==='RMVRC'?HMUN:['Cuiabá','Várzea Grande'], o={};
  for(const f of ['pop','popu','dom','agua','esg','lixo','p15','alf']) o[f]=HY.map((_,i)=>d3.sum(ms,m=>HIST.mun[m][f][i]));
  o.esg91_rede=d3.sum(ms,m=>HIST.mun[m].esg91_rede); o.esg22_fossa=d3.sum(ms,m=>HIST.mun[m].esg22_fossa);
  return o;
}
function hBadge(d,r){ const a=hVal(r,d,0), b=hVal(r,d,3); if(d.t==='n'){ const x=b/a; return x>=1.95?'×'+ptBR(fmt1(x)):(b>=a?'+':'−')+ptBR(fmt1(Math.abs(100*(x-1))))+'%'; } const q=b-a; return (q>=0?'+':'−')+ptBR(fmt1(Math.abs(q)))+' p.p.'; }
function hVal(r,d,i){ return d.t==='n'?r[d.k][i]:100*r[d.num][i]/r[d.den][i]; }
const hFmt=(d,v)=>d.t==='n'?ptBR(fmtN(Math.round(v))):ptBR(fmt1(v))+'%';
const hShort=n=>({'Nossa Senhora do Livramento':'N. S. do Livramento','Santo Antônio de Leverger':'S. A. de Leverger','Chapada dos Guimarães':'Chapada dos Guimarães','Cuiabá + Várzea Grande':'Cuiabá + VG'})[n]||n;
function hDelta(d,r){ const a=hVal(r,d,0), b=hVal(r,d,3);
  if(d.t==='n'){ const x=b/a; return x>=1.95?`${ptBR(fmt1(x))} vezes o valor de 1991`:`${b>=a?'+':'−'}${ptBR(fmt1(Math.abs(100*(b/a-1))))}% desde 1991`; }
  const p=b-a; return `${p>=0?'+':'−'}${ptBR(fmt1(Math.abs(p)))} p.p. desde 1991`; }
const HMETA={agua:[99,'meta 2033: 99%'],esg:[90,'meta 2033: 90%']}; // Lei 14.026/2020 (Marco Legal do Saneamento), art. 11-B
const hTaxa=(a,b,n)=>100*(Math.pow(b/a,1/n)-1);
let hTip=null;
function hTipEl(){ if(hTip) return hTip; hTip=document.createElement('div'); hTip.className='hstip'; hTip.hidden=true; document.body.appendChild(hTip); return hTip; }
function hTipShow(ev,el,d,name,i){
  const t=hTipEl(); t.replaceChildren(); const r=hRec(name), a=HY[i];
  const add=(cls,txt)=>{ const e=document.createElement('div'); e.className=cls; e.textContent=txt; t.appendChild(e); return e; };
  const row=(val,lab,key,strong)=>{ const e=document.createElement('div'); e.className='hst-r'+(strong?' hst-s':''); const k=document.createElement('i'); k.className='hst-k '+key; const v=document.createElement('b'); v.textContent=val; const l=document.createElement('span'); l.textContent=lab; e.append(k,v,l); t.appendChild(e); };
  add('hst-t',`${d.n} · ${a}`);
  row(hFmt(d,hVal(r,d,i)),name==='RMVRC'?'RMVRC':hShort(name),'k-sel',true);
  if(d.t==='n'){
    if(i>0){ const p=hVal(r,d,i-1), v=hVal(r,d,i); add('hst-n',`${HY[i-1]} → ${a}: ${v>=p?'+':'−'}${ptBR(fmt1(Math.abs(100*(v/p-1))))}% (${ptBR(fmt1(hTaxa(p,v,a-HY[i-1])))}% ao ano)`); }
    if(d.k==='pop'){ const u=100*r.popu[i]/r.pop[i]; add('hst-n',`População urbana: ${ptBR(fmt1(u))}%`); }
    if(d.k==='dom'){ add('hst-n',`Moradores por domicílio: ${ptBR(fmt1(r.pop[i]/r.dom[i]))}`); }
  } else {
    if(d.k==='esg'&&i===3){ add('hst-n',`Com fossa ligada à rede (conceito de 2022): ${hFmt(d,100*r.esg22_fossa/r.dom[3])}`); }
    if(name!=='RMVRC') row(hFmt(d,hVal(hRec('RMVRC'),d,i)),'RMVRC','k-rm',false);
    const oth=HMUN.filter(o=>o!==name).map(o=>[o,hVal(HIST.mun[o],d,i)]).sort((p,q)=>q[1]-p[1]);
    add('hst-h','Outros municípios');
    for(const [o,v] of oth) row(hFmt(d,v),hShort(o),'k-oth',false);
  }
  t.hidden=false;
  const bx=el.getBoundingClientRect(), tw=t.offsetWidth, th=t.offsetHeight;
  let px=(ev&&ev.clientX!=null?ev.clientX:bx.left+bx.width*(i+0.5)/4)+14; if(px+tw>window.innerWidth-8) px=Math.max(8,px-tw-28);
  let py=(ev&&ev.clientY!=null?ev.clientY:bx.top+20)-th/2; py=Math.max(8,Math.min(py,window.innerHeight-th-8));
  t.style.left=px+'px'; t.style.top=py+'px';
}
function hTipHide(){ if(hTip) hTip.hidden=true; }
// gráfico de linha com os anos na escala do tempo
function hChart(svgEl,d,name,mini){
  const wide=!mini&&svgEl.dataset.wide, W=mini?Math.round(Math.max(130,Math.min(420,(svgEl.clientWidth||150)))):wide?Math.round(Math.max(320,svgEl.clientWidth||560)):Math.round(Math.max(280,Math.min(340,(svgEl.clientWidth||320)))), H=mini?64:wide?Math.round(Math.min(300,Math.max(210,W*0.46))):200, m=mini?{l:6,r:6,t:7,b:7}:{l:8,r:14,t:24,b:28};
  const s=d3.select(svgEl); s.selectAll('*').remove(); s.attr('viewBox',`0 0 ${W} ${H}`).attr('preserveAspectRatio','xMidYMid meet');
  const r=hRec(name), x=d3.scaleLinear().domain([1991,2022]).range([m.l+(mini?2:(d.t==='p'?40:30)),W-m.r-(mini?2:26)]);
  const vs=HY.map((_,i)=>hVal(r,d,i));
  const y=d3.scaleLinear().domain(d.t==='p'?[0,100]:[0,d3.max(vs)*1.15]).range([H-m.b,m.t]);
  const line=d3.line().x((v,i)=>x(HY[i])).y(v=>y(v));
  const halo=sel=>sel.style('paint-order','stroke').style('stroke','var(--panel-2)').style('stroke-width',3).style('stroke-linejoin','round');
  if(mini){
    (d.t==='p'?[0,50,100]:[0]).forEach(t=>s.append('line').attr('x1',0).attr('x2',W).attr('y1',y(t)).attr('y2',y(t)).style('stroke','var(--line)').style('stroke-width',1).style('opacity',t===0?1:.6));
    if(d.t==='p'&&name!=='RMVRC') s.append('path').attr('d',line(HY.map((_,i)=>hVal(hRec('RMVRC'),d,i)))).style('fill','none').style('stroke','var(--muted)').style('stroke-width',1.2).style('stroke-dasharray','3 2.5');
    if(d.t==='n') s.append('path').attr('d',d3.area().x((v,i)=>x(HY[i])).y0(y(0)).y1(v=>y(v))(vs)).style('fill','var(--accent)').style('opacity',.08);
    s.append('path').attr('d',line(vs)).style('fill','none').style('stroke','var(--accent)').style('stroke-width',2.2).style('stroke-linejoin','round');
    const dts=vs.map((v,i)=>s.append('circle').attr('cx',x(HY[i])).attr('cy',y(v)).attr('r',3).style('fill','var(--accent)').style('stroke','var(--panel-2)').style('stroke-width',1.2));
    const ring=s.append('circle').attr('r',5).style('fill','none').style('stroke','var(--accent)').style('stroke-width',1.3).style('opacity',0).style('pointer-events','none');
    s.append('rect').attr('width',W).attr('height',H).style('fill','transparent')
      .on('pointermove',ev=>{ const [px]=d3.pointer(ev,svgEl); let bi=0,bd=1e9; HY.forEach((a,i)=>{ const dd=Math.abs(x(a)-px); if(dd<bd){bd=dd;bi=i;} }); ring.attr('cx',x(HY[bi])).attr('cy',y(vs[bi])).style('opacity',1); hTipShow(ev,svgEl,d,name,bi); })
      .on('pointerleave',()=>{ ring.style('opacity',0); hTipHide(); });
    return;
  }
  const g=s.append('g');
  (d.t==='p'?[0,25,50,75,100]:y.ticks(4)).forEach(t=>{ const major=d.t==='n'?t===0:(t%50===0);
    g.append('line').attr('x1',m.l).attr('x2',W-m.r).attr('y1',y(t)).attr('y2',y(t)).style('stroke','var(--line)').style('stroke-width',1).style('opacity',major?1:.55);
    if(d.t==='p'&&t%50===0) g.append('text').attr('x',m.l).attr('y',y(t)-3).text(t+'%').style('fill','var(--muted)').style('font-size','10px'); });
  HY.forEach(a=>g.append('text').attr('x',x(a)).attr('y',H-9).attr('text-anchor','middle').text(a).style('fill','var(--muted)').style('font-size','10.5px'));
  if(HMETA[d.k]){ const [mv,ml]=HMETA[d.k];
    g.append('line').attr('x1',x(1991)).attr('x2',W-m.r).attr('y1',y(mv)).attr('y2',y(mv)).style('stroke','var(--good-fg)').style('stroke-width',1.2).style('opacity',.75);
    g.append('text').attr('x',W-m.r).attr('y',y(mv)-4).attr('text-anchor','end').text(ml).style('fill','var(--good-fg)').style('font-size','10px').style('font-weight',700).call(halo); }
  if(d.t==='p'){
    for(const o of HMUN) if(o!==name) s.append('path').attr('d',line(HY.map((_,i)=>hVal(HIST.mun[o],d,i)))).style('fill','none').style('stroke','var(--muted)').style('stroke-opacity',.3).style('stroke-width',1);
    if(name!=='RMVRC') s.append('path').attr('d',line(HY.map((_,i)=>hVal(hRec('RMVRC'),d,i)))).style('fill','none').style('stroke','var(--muted)').style('stroke-width',1.4).style('stroke-dasharray','4 3');
  } else {
    // área sob a linha e taxa média anual de crescimento em cada intervalo
    s.append('path').attr('d',d3.area().x((v,i)=>x(HY[i])).y0(y(0)).y1(v=>y(v))(vs)).style('fill','var(--accent)').style('opacity',.07);
    for(let i=1;i<4;i++){ const tx=hTaxa(vs[i-1],vs[i],HY[i]-HY[i-1]), xm=(x(HY[i-1])+x(HY[i]))/2, ym=(y(vs[i-1])+y(vs[i]))/2;
      s.append('text').attr('x',xm).attr('y',ym+16).attr('text-anchor','middle').text(`${tx>=0?'+':'−'}${ptBR(fmt1(Math.abs(tx)))}% a.a.`).style('fill','var(--muted)').style('font-size','10px').call(halo); }
  }
  s.append('path').attr('d',line(vs)).style('fill','none').style('stroke','var(--accent)').style('stroke-width',2.6).style('stroke-linejoin','round');
  const dots=vs.map((v,i)=>s.append('circle').attr('cx',x(HY[i])).attr('cy',y(v)).attr('r',3.6).style('fill','var(--accent)').style('stroke','var(--panel-2)').style('stroke-width',1.5));
  // rótulos só no início e no fim; os valores intermediários ficam no destaque ao passar o mouse e na tabela
  [0,3].forEach(i=>{ const v=vs[i]; let dy=-9;
    if(d.k==='esg'&&i===3){ const vf=100*r.esg22_fossa/r.dom[3]; if(vf-v>0.4&&vf-v<14) dy=17; }
    if(y(v)+dy<m.t-2) dy=17;
    if(dy>0&&y(v)+dy>H-m.b-3) dy=-9;
    if(HMETA[d.k]){ const ym=y(HMETA[d.k][0]); if(Math.abs(y(v)+dy-4-ym)<10) dy=dy<0?17:-9; if(i===3&&Math.abs(y(v)+dy-4-ym)<12) dy=17; }
    s.append('text').attr('x',x(HY[i])).attr('y',y(v)+dy).attr('text-anchor','middle').text(hFmt(d,v)).style('fill','var(--fg)').style('font-size','11px').style('font-weight',700).call(halo); });
  if(d.k==='esg'){ const v=100*r.esg22_fossa/r.dom[3]; if(v-vs[3]>0.4){
    s.append('circle').attr('cx',x(2022)).attr('cy',y(v)).attr('r',3.6).style('fill','var(--panel-2)').style('stroke','var(--accent)').style('stroke-width',1.6);
    s.append('text').attr('x',x(2022)).attr('y',Math.min(y(v)-8,y(vs[3])-22)).attr('text-anchor','middle').text(hFmt(d,v)).style('fill','var(--muted)').style('font-size','10px').style('font-weight',700).call(halo); } }
  // camada de destaque: linha vertical que encaixa no censo mais próximo + quadro com os valores
  const hair=s.append('line').attr('y1',m.t-6).attr('y2',H-m.b).style('stroke','var(--fg)').style('stroke-width',1).style('opacity',0).style('pointer-events','none');
  const ring=s.append('circle').attr('r',6.5).style('fill','none').style('stroke','var(--accent)').style('stroke-width',1.5).style('opacity',0).style('pointer-events','none');
  let cur=-1;
  const show=(i,ev)=>{ cur=i; hair.attr('x1',x(HY[i])).attr('x2',x(HY[i])).style('opacity',.35); ring.attr('cx',x(HY[i])).attr('cy',y(vs[i])).style('opacity',1); hTipShow(ev,svgEl,d,name,i); };
  const hide=()=>{ cur=-1; hair.style('opacity',0); ring.style('opacity',0); hTipHide(); };
  s.append('rect').attr('x',m.l).attr('y',0).attr('width',W-m.l-m.r).attr('height',H-m.b+8).style('fill','transparent').style('cursor','crosshair')
    .on('pointermove',ev=>{ const [px]=d3.pointer(ev,svgEl); let bi=0,bd=1e9; HY.forEach((a,i)=>{ const dd=Math.abs(x(a)-px); if(dd<bd){bd=dd;bi=i;} }); show(bi,ev); })
    .on('pointerleave',hide);
  s.attr('tabindex',0).on('focus',()=>show(3,null)).on('blur',hide)
    .on('keydown',ev=>{ if(ev.key==='ArrowLeft'||ev.key==='ArrowRight'){ ev.preventDefault(); show(Math.max(0,Math.min(3,(cur<0?3:cur)+(ev.key==='ArrowLeft'?-1:1))),null); } if(ev.key==='Escape') hide(); });
}
function hLeg(d,lab){
  if(d.t==='n') return `<div class="hscl"><span><i class="hsl-sel"></i>${lab}</span><span class="hscl-n">a.a. = crescimento médio ao ano entre dois censos</span></div>`;
  const it=[`<span><i class="hsl-sel"></i>${lab}</span>`];
  if(HSEL!=='RMVRC') it.push('<span><i class="hsl-rm"></i>RMVRC (sete municípios juntos)</span>');
  it.push('<span><i class="hsl-oth"></i>outros municípios</span>');
  if(HMETA[d.k]) it.push(`<span><i class="hsl-meta"></i>meta 2033</span>`);
  if(d.k==='esg') it.push('<span><i class="hsl-new"></i>com fossa ligada à rede</span>');
  return `<div class="hscl">${it.join('')}</div>`;
}
function renderHist(){
  const box=document.getElementById('hs-mun'); if(!box) return;
  const opts=[...HMUN.slice().sort((a,b)=>HIST.mun[b].pop[3]-HIST.mun[a].pop[3]),'RMVRC'];
  box.innerHTML=opts.map(n=>`<button data-m="${n}" aria-pressed="${n===HSEL}">${hShort(n)}</button>`).join('');
  const r=hRec(HSEL), lab=HSEL==='RMVRC'?'RMVRC (sete municípios)':HSEL;
    document.getElementById('hs-ch-t').textContent='Evolução em quatro censos · '+lab;
  const K=[HK[0],HK[1],HK[3],HK[5]];
  document.getElementById('hs-kpi').innerHTML=K.map(d=>`<div class="kpi"><div class="lab">${d.n}${d.t==='p'?'':''}</div><div class="val">${hFmt(d,hVal(r,d,3))}</div><div class="sub">${d.t==='p'?d.s.replace('% ','')+' · ':''}Censo 2022</div><div class="sub"><b>${hDelta(d,r)}</b></div></div>`).join('');
  const gr=document.getElementById('hs-grid');
  gr.innerHTML=HK.map(d=>`<figure class="hsc"><figcaption><div><b>${d.n}</b><span>${d.s}</span></div><em class="hsc-d">${hBadge(d,r)}<small>1991 → 2022</small></em></figcaption><svg role="img" aria-label="${d.n}, ${lab}, 1991 a 2022" data-k="${d.k}"></svg>${hLeg(d,lab)}</figure>`).join('');
  gr.querySelectorAll('svg').forEach(el=>hChart(el,HK.find(d=>d.k===el.dataset.k),HSEL,false));
  // tabela comparativa
  document.getElementById('hs-ind').innerHTML=HKT.map(d=>`<button data-k="${d.k}" aria-pressed="${d.k===HIND}">${d.n}</button>`).join('');
  const d=HKT.find(x=>x.k===HIND), rows=HMUN.slice().sort((a,b)=>HIST.mun[b].pop[3]-HIST.mun[a].pop[3]);
  const cell=(rr,i)=>`<td class="num">${hFmt(d,hVal(rr,d,i))}</td>`;
  const dlt=rr=>{ const a=hVal(rr,d,0), b=hVal(rr,d,3); return d.t==='n'?`${b>=a?'+':'−'}${ptBR(fmt1(Math.abs(100*(b/a-1))))}%`:`${b>=a?'+':'−'}${ptBR(fmt1(Math.abs(b-a)))} p.p.`; };
  let h=`<thead><tr><th class="l">Município</th>${HY.map(a=>`<th>${a}</th>`).join('')}<th>1991 → 2022</th></tr></thead><tbody>`;
  for(const n of rows){ const rr=HIST.mun[n]; h+=`<tr${n===HSEL?' class="hsrow"':''}><td class="l">${n}</td>${HY.map((_,i)=>cell(rr,i)).join('')}<td class="num"><b>${dlt(rr)}</b></td></tr>`; }
  const rm=hRec('RMVRC'); h+=`<tr class="tot"><td class="l">RMVRC</td>${HY.map((_,i)=>cell(rm,i)).join('')}<td class="num"><b>${dlt(rm)}</b></td></tr></tbody>`;
  document.getElementById('hs-tab').innerHTML=h;
  document.getElementById('hs-tnote').textContent=`${d.n}: ${d.s}. ${d.t==='n'?'A última coluna mostra a variação percentual entre 1991 e 2022.':'A última coluna mostra a diferença em pontos percentuais (p.p.) entre 1991 e 2022.'}${d.k==='esg'?' Em 2022, só rede geral ou pluvial; com a fossa ligada à rede (conceito atual do IBGE), a RMVRC chega a '+ptBR(fmt1(100*rm.esg22_fossa/rm.dom[3]))+'%.':''}`;
  // notas com números
  const pc=(a,b)=>ptBR(fmt1(100*a/b))+'%', C=HIST.mun['Cuiabá'], V=HIST.mun['Várzea Grande'];
  document.getElementById('hs-e91c').textContent=pc(C.esg91_rede,C.dom[0])+' (e não '+pc(C.esg[0],C.dom[0])+')';
  document.getElementById('hs-e91v').textContent=pc(V.esg91_rede,V.dom[0])+' (e não '+pc(V.esg[0],V.dom[0])+')';
  document.getElementById('hs-e22c').textContent=pc(C.esg22_fossa,C.dom[3]); document.getElementById('hs-e22cs').textContent=pc(C.esg[3],C.dom[3]);
  const L={pop:'População',dom:'Domicílios',agua:'Água',esg:'Esgoto',lixo:'Lixo',alf:'Alfabetização'};
  document.getElementById('hs-src').innerHTML=`<thead><tr><th class="l">Indicador</th>${HY.map(a=>`<th>${a}</th>`).join('')}</tr></thead><tbody>`+
    Object.keys(L).map(k=>`<tr><td class="l">${L[k]}</td>${HY.map(a=>{ const t=HIST.tab[k][a]; return `<td class="num"><a href="https://sidra.ibge.gov.br/tabela/${t}" target="_blank" rel="noopener">tabela ${t}</a></td>`; }).join('')}</tr>`).join('')+'</tbody>';
  const cs=HIST.consulta.split('-'); document.getElementById('hs-cons').textContent=`${cs[2]}/${cs[1]}/${cs[0]}`;
}
function histCSV(){
  const head=['municipio','ano','populacao','populacao_urbana','domicilios','dom_agua_rede','dom_esgoto_rede_ou_pluvial','dom_lixo_coletado','pessoas_15mais','alfabetizadas_15mais','agua_rede_pct','esgoto_rede_pct','lixo_coletado_pct','alfabetizacao_pct','tabelas_sidra'];
  const L=[head.join(',')];
  for(const n of [...HMUN,'RMVRC']){ const r=hRec(n); HY.forEach((a,i)=>{ const p=(x,y)=>(100*x/y).toFixed(1);
    const tb=n==='RMVRC'?'soma dos municípios':[...new Set(Object.values(HIST.tab).map(t=>t[a]))].sort((x,y)=>x-y).join(' ');
    L.push([`"${n}"`,a,r.pop[i],r.popu[i],r.dom[i],r.agua[i],r.esg[i],r.lixo[i],r.p15[i],r.alf[i],p(r.agua[i],r.dom[i]),p(r.esg[i],r.dom[i]),p(r.lixo[i],r.dom[i]),p(r.alf[i],r.p15[i]),`"${tb}"`].join(',')); }); }
  const blob=new Blob(['﻿'+L.join('\n')],{type:'text/csv'});
  if(typeof saveFile==='function') saveFile('serie_historica_rmvrc_1991_2022.csv',blob);
  else { const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='serie_historica_rmvrc_1991_2022.csv'; document.body.appendChild(a); a.click(); setTimeout(()=>a.remove(),1000); }
}
// cartão no mapa: evolução do município (ou da região) escolhido no filtro
let MHK='esg';
const MHCH=[['all','RMVRC'],['conurb','Cuiabá + VG'],['Cuiabá','Cuiabá'],['Várzea Grande','Várzea Grande'],['Campo Verde','Campo Verde'],['Chapada dos Guimarães','Chapada'],['Santo Antônio de Leverger','S. A. de Leverger'],['Nossa Senhora do Livramento','N. S. do Livramento'],['Acorizal','Acorizal']];
function mhName(){ const v=document.getElementById('munsel').value; return v==='all'?'RMVRC':v==='conurb'?'Cuiabá + Várzea Grande':v; }
function mhCount(el){ // números do destaque sobem de 0 até o valor (uma vez, quando o cartão aparece)
  const red=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  el.querySelectorAll('[data-to]').forEach(n=>{ const to=+n.dataset.to, dec=+(n.dataset.dec||0), pre=n.dataset.pre||'', suf=n.dataset.suf||'';
    const f=v=>pre+(dec?ptBR(v.toFixed(dec)):ptBR(fmtN(Math.round(v))))+suf;
    if(red){ n.textContent=f(to); return; } const t0=performance.now(), D=900;
    const step=t=>{ const k=Math.min(1,(t-t0)/D), e=1-Math.pow(1-k,3); n.textContent=f(to*e); if(k<1) requestAnimationFrame(step); }; requestAnimationFrame(step); });
}
function mhStory(name,r){ // frase-resumo gerada a partir dos números
  const P=HK[0], pa=hVal(r,P,0), pb=hVal(r,P,3), lab=name==='RMVRC'?'a RMVRC':name==='Cuiabá + Várzea Grande'?'Cuiabá e Várzea Grande':name;
  const ks=['agua','esg','lixo','alf'].map(k=>HK.find(d=>d.k===k)), gain=ks.map(d=>[d,hVal(r,d,3)-hVal(r,d,0)]).sort((x,y)=>y[1]-x[1])[0];
  const low=ks.filter(d=>d.k!=='alf').map(d=>[d,hVal(r,d,3)]).sort((x,y)=>x[1]-y[1])[0];
  const pop=pb>=pa?`ganhou ${ptBR(fmtN(Math.round(pb-pa)))} moradores (${hBadge(P,r)})`:`perdeu ${ptBR(fmtN(Math.round(pa-pb)))} moradores (${hBadge(P,r)})`;
  const nm={agua:'a água da rede',esg:'o esgoto em rede',lixo:'a coleta de lixo',alf:'a alfabetização'};
  return `Em 31 anos, ${lab} ${pop}. O maior avanço foi ${nm[gain[0].k]}, que subiu ${ptBR(fmt1(gain[1]))} pontos percentuais; o que mais falta é ${nm[low[0].k]}, que chega a ${ptBR(fmt1(low[1]))}% dos domicílios em 2022.`;
}
function renderMunHist(){
  const sec=document.getElementById('munhist'); if(!sec) return;
  const v=document.getElementById('munsel').value, name=mhName(), r=hRec(name);
  document.getElementById('mh-n').textContent=name==='RMVRC'?'Evolução da RMVRC':name==='Cuiabá + Várzea Grande'?'Evolução de Cuiabá e Várzea Grande':'Evolução de '+name;
  document.getElementById('mh-chips').innerHTML=MHCH.map(([k,l])=>`<button type="button" data-m="${k}" aria-pressed="${k===v}">${l}</button>`).join('');
  // destaque: quatro números grandes e a frase-resumo
  const P=HK[0], D=HK[1], E=HK.find(d=>d.k==='esg'), L=HK.find(d=>d.k==='lixo'), A=HK.find(d=>d.k==='alf'), W=HK.find(d=>d.k==='agua');
  const big=(lab,to,opt,sub)=>`<div class="mhb"><span class="mhb-l">${lab}</span><b data-to="${to}" ${opt}>0</b><span class="mhb-s">${sub}</span></div>`;
  const dp=hVal(r,P,3)-hVal(r,P,0);
  document.getElementById('mh-hero').innerHTML=`<p class="mhstory">${mhStory(name,r)}</p><div class="mhbig">`+
    big('Moradores a mais desde 1991',Math.abs(dp),`data-pre="${dp>=0?'+':'−'}"`,`${hFmt(P,hVal(r,P,0))} → ${hFmt(P,hVal(r,P,3))}`)+
    big('Água da rede em 2022',hVal(r,W,3).toFixed(1),'data-dec="1" data-suf="%"',`era ${hFmt(W,hVal(r,W,0))} em 1991 · meta: 99%`)+
    big('Esgoto em rede em 2022',hVal(r,E,3).toFixed(1),'data-dec="1" data-suf="%"',`era ${hFmt(E,hVal(r,E,0))} em 1991 · meta: 90%`)+
    big('Lixo coletado em 2022',hVal(r,L,3).toFixed(1),'data-dec="1" data-suf="%"',`era ${hFmt(L,hVal(r,L,0))} em 1991`)+`</div>`;
  if(window.__mhAnim!==name){ window.__mhAnim=name; mhCount(document.getElementById('mh-hero')); } else document.querySelectorAll('#mh-hero [data-to]').forEach(n=>{ const to=+n.dataset.to, dec=+(n.dataset.dec||0); n.textContent=(n.dataset.pre||'')+(dec?ptBR(to.toFixed(dec)):ptBR(fmtN(Math.round(to))))+(n.dataset.suf||''); });
  // seletores (indicadores) e gráfico em destaque
  const g=document.getElementById('mh-grid');
  g.innerHTML=HK.map(d=>`<button type="button" class="mhc" data-k="${d.k}" aria-pressed="${d.k===MHK}"><span class="mhc-t"><span>${d.n}</span><b>${hBadge(d,r)}</b></span><svg data-k="${d.k}" aria-hidden="true"></svg><span class="mhc-v"><span>1991 <b>${hFmt(d,hVal(r,d,0))}</b></span><span>2022 <b>${hFmt(d,hVal(r,d,3))}</b></span></span></button>`).join('');
  g.querySelectorAll('svg').forEach(el=>hChart(el,HK.find(d=>d.k===el.dataset.k),name,true));
  mhFeat(name);
  document.getElementById('mh-leg').innerHTML=`<span><i class="hsl-sel"></i>${name==='RMVRC'?'RMVRC (sete municípios juntos)':name}</span>`+(name!=='RMVRC'?'<span><i class="hsl-rm"></i>RMVRC</span><span><i class="hsl-oth"></i>outros municípios</span>':'')+'<span><i class="hsl-meta"></i>meta de 2033</span><span>clique num quadro para ver o indicador em destaque · passe o mouse para ver cada censo</span>';
  document.getElementById('mh-note').textContent='Fontes: IBGE, Censos 1991, 2000, 2010 e 2022 (SIDRA, consulta em 17/10/2026); IBGE, Grade Estatística de 2010 (publicada em 2016) e de 2022 (publicada em 12/06/2025). Município inteiro, áreas urbana e rural. Esgoto: rede geral ou pluvial, como nos censos anteriores; o mapa por setor usa o conceito de 2022, que inclui a fossa ligada à rede. Metas de 2033: Lei 14.026/2020.';
  const go=document.getElementById('mh-go'); go.onclick=()=>{ HSEL=name==='Cuiabá + Várzea Grande'?'Cuiabá':name; renderHist(); };
}
function mhFeat(name,anim){
  const d=HK.find(x=>x.k===MHK), r=hRec(name||mhName()), box=document.getElementById('mh-feat'); if(!box) return;
  box.classList.remove('mhin'); if(anim){ void box.offsetWidth; box.classList.add('mhin'); }
  document.getElementById('mh-ft').innerHTML=`<b>${d.n}</b><span>${d.s}</span>`;
  document.getElementById('mh-fv').innerHTML=HY.map((a,i)=>`<span><small>${a}</small><b>${hFmt(d,hVal(r,d,i))}</b></span>`).join('')+`<span class="mhfd"><small>1991 → 2022</small><b>${hBadge(d,r)}</b></span>`;
  hChart(document.getElementById('mh-fsvg'),d,name||mhName(),false);
}
document.getElementById('mh-grid')?.addEventListener('click',e=>{ const b=e.target.closest('.mhc'); if(!b) return; MHK=b.dataset.k; document.querySelectorAll('#mh-grid .mhc').forEach(x=>x.setAttribute('aria-pressed',x===b)); mhFeat(null,true); });
document.getElementById('mh-chips')?.addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; const s=document.getElementById('munsel'); s.value=b.dataset.m; s.dispatchEvent(new Event('change')); });
document.getElementById('hs-mun')?.addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; HSEL=b.dataset.m; renderHist(); });
document.getElementById('hs-ind')?.addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; HIND=b.dataset.k; renderHist(); });
document.getElementById('hs-csv')?.addEventListener('click',histCSV);
document.getElementById('munsel')?.addEventListener('change',renderMunHist);
window.__hist={HIST,hRec,hVal,HK,renderHist,renderMunHist};
let hRz=0; window.addEventListener('resize',()=>{ clearTimeout(hRz); hRz=setTimeout(()=>{ renderMunHist(); const pg=document.querySelector('[data-page="historico"]'); if(pg&&!pg.hidden) renderHist(); },200); });
window.addEventListener('hashchange',()=>setTimeout(renderMunHist,80));
