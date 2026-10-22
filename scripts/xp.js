// ------- Explorar, Desigualdade e validação, Subsídios a políticas -------
(function(){
const XK=IND.filter(i=>!['pop','dens'].includes(i.k)).map(i=>i.k);
const XMUN=MUN.features.map(m=>m.properties.nome);
const TERR=[['urb','Áreas urbanas da RMVRC'],['cvg','Conurbação Cuiabá–Várzea Grande'],['all','RMVRC – todos os setores']].concat(XMUN.map(m=>['m:'+m,m+' (área urbana)']));
const terrF=t=>t==='all'?F:t==='urb'?F.filter(f=>f.properties.sit==='Urbana'):t==='cvg'?F.filter(f=>f.properties.sit==='Urbana'&&['Cuiabá','Várzea Grande'].includes(f.properties.mun)):F.filter(f=>f.properties.sit==='Urbana'&&f.properties.mun===t.slice(2));
const optI=(sel,v)=>{ if(!sel) return; sel.innerHTML=IND.filter(i=>XK.includes(i.k)).map(i=>`<option value="${i.k}"${i.k===v?' selected':''}>${esc(i.n)}${i.u&&i.u!=='%'?' ('+esc(i.u)+')':''}</option>`).join(''); };
const optT=(sel,v)=>{ if(!sel) return; sel.innerHTML=TERR.map(([k,l])=>`<option value="${k}"${k===v?' selected':''}>${esc(l)}</option>`).join(''); };
const val=(f,k)=>{ const v=f.properties[k]; return v==null||isNaN(v)?null:v; };
const xFmt=(k,v)=>fv(k,v);
// recorte do enquadramento: ignora setores muito grandes ao enquadrar áreas urbanas
function fitFeats(fs){ if(fs.length<15) return fs; const a=fs.map(f=>f.properties.area).sort(d3.ascending); const lim=Math.max(3,d3.quantile(a,.92)); const s=fs.filter(f=>f.properties.area<=lim); return s.length>=5?s:fs; }
const BAS={};
function baseMap(id,fs,opt={}){
  const svg=d3.select('#'+id); const node=svg.node(); const W=Math.max(300,node.parentNode.clientWidth||700), H=Math.round(Math.min(560,Math.max(320,W*.72)));
  svg.attr('viewBox',`0 0 ${W} ${H}`).attr('height',H); svg.selectAll('*').remove();
  const proj=d3.geoMercator().fitExtent([[8,8],[W-8,H-8]],{type:'FeatureCollection',features:fitFeats(opt.fit||fs)}); const path=d3.geoPath(proj);
  const g=svg.append('g');
  g.append('g').selectAll('path').data(MUN.features).join('path').attr('d',path).attr('fill','var(--panel-2)').attr('stroke','none');
  const ps=g.append('g').selectAll('path').data(fs).join('path').attr('d',path).attr('stroke','var(--panel)').attr('stroke-width',.25).attr('vector-effect','non-scaling-stroke');
  g.append('path').attr('d',path({type:'FeatureCollection',features:HIDRO.features.filter(f=>f.properties.t==='r')})).attr('fill','none').attr('stroke','var(--water-line,#5aa0d0)').attr('stroke-width',.9).attr('vector-effect','non-scaling-stroke').attr('pointer-events','none');
  g.append('g').selectAll('path').data(MUN.features).join('path').attr('d',path).attr('fill','none').attr('stroke','var(--fg)').attr('stroke-opacity',.55).attr('stroke-width',.9).attr('vector-effect','non-scaling-stroke').attr('pointer-events','none');
  const hl=g.append('g').attr('pointer-events','none');
  const z=d3.zoom().scaleExtent([1,40]).translateExtent([[-W,-H],[2*W,2*H]]).on('zoom',e=>{ g.attr('transform',e.transform); if(opt.onZoom&&e.sourceEvent) opt.onZoom(e.transform); });
  svg.call(z).on('dblclick.zoom',null);
  const m={svg,g,ps,proj,path,z,hl,W,H}; BAS[id]=m; return m;
}
function tip(ev,html){ const t=hTipEl(); t.innerHTML=html; t.hidden=false; const tw=t.offsetWidth, th=t.offsetHeight; let px=ev.clientX+14; if(px+tw>innerWidth-8) px=ev.clientX-tw-14; t.style.left=px+'px'; t.style.top=Math.max(8,Math.min(ev.clientY-th/2,innerHeight-th-8))+'px'; }
const nmB=p=>p.bairro||p.dist||p.mun;
function spear(a,b){ const n=a.length; if(n<8) return null; const r=x=>{ const o=x.map((v,i)=>[v,i]).sort((p,q)=>p[0]-q[0]); const rk=new Array(n); let i=0; while(i<n){ let j=i; while(j+1<n&&o[j+1][0]===o[i][0]) j++; for(let k=i;k<=j;k++) rk[o[k][1]]=(i+j)/2; i=j+1; } return rk; }; const ra=r(a), rb=r(b); const ma=d3.mean(ra), mb=d3.mean(rb); let s=0,sa=0,sb=0; for(let i=0;i<n;i++){ s+=(ra[i]-ma)*(rb[i]-mb); sa+=(ra[i]-ma)**2; sb+=(rb[i]-mb)**2; } return sa&&sb?s/Math.sqrt(sa*sb):null; }
function rng(seed){ return function(){ seed|=0; seed=seed+0x6D2B79F5|0; let t=Math.imul(seed^seed>>>15,1|seed); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
const pctF=v=>v==null?'—':ptBR(fmt1(v))+'%';
const nF=v=>v==null?'—':ptBR(fmtN(v));
function csvOut(name,fs,keys){ const cols=[['id','Setor'],['mun','Município'],['sit','Situação'],['bairro','Bairro'],['dist','Distrito'],['pop','Moradores']].concat(keys.map(k=>[k,byK[k].n+(byK[k].u?' ('+byK[k].u+')':'')])); save(name,toCSV(cols,fs.map(f=>f.properties))); }
// ===================== 1. bivariado =====================
const BIV=[['#e8e8e8','#e4acac','#c85a5a'],['#b0d5df','#ad9ea5','#985356'],['#64acbe','#627f8c','#574249']];
let XS={x:'ivsa',y:'inund',t:'cvg',sel:null};
function terc(k){ const v=F.map(f=>val(f,k)).filter(v=>v!=null).sort(d3.ascending); return [d3.quantile(v,1/3),d3.quantile(v,2/3)]; }
const cl3=(v,t)=>v==null?-1:v<=t[0]?0:v<=t[1]?1:2;
function renderBiv(){
  const fs=terrF(XS.t), tx=terc(XS.x), ty=terc(XS.y), ix=byK[XS.x], iy=byK[XS.y];
  const m=baseMap('xp-map',fs);
  const col=f=>{ const a=cl3(val(f,XS.x),tx), b=cl3(val(f,XS.y),ty); return a<0||b<0?'var(--nodata,#cdd3de)':BIV[b][a]; };
  m.ps.attr('fill',col).style('cursor','pointer')
    .on('pointermove',(ev,f)=>{ const p=f.properties; tip(ev,`<div class="hst-t">${esc(nmB(p))} · ${esc(p.mun)}</div><div class="hst-r"><b>${xFmt(XS.x,val(f,XS.x))}</b><span>${esc(ix.n)}</span></div><div class="hst-r"><b>${xFmt(XS.y,val(f,XS.y))}</b><span>${esc(iy.n)}</span></div><div class="hst-n">${nF(p.pop)} moradores · setor ${p.id}</div>`); })
    .on('pointerleave',()=>hTipHide());
  XS.m=m;
  // legenda 3x3
  const L=document.getElementById('xp-leg'); const lab=['baixo','médio','alto'];
  let h=`<div class="bivl"><div class="bivy">${esc(iy.n)} →</div><div class="bivg">`;
  for(let r=2;r>=0;r--) for(let c=0;c<3;c++) h+=`<i style="background:${BIV[r][c]}" title="${esc(ix.n)}: ${lab[c]} · ${esc(iy.n)}: ${lab[r]}"></i>`;
  h+=`</div><div class="bivx">${esc(ix.n)} →</div></div><p class="note">Terços da RMVRC — ${esc(ix.n)}: até ${xFmt(XS.x,tx[0])}, até ${xFmt(XS.x,tx[1])}, acima. ${esc(iy.n)}: até ${xFmt(XS.y,ty[0])}, até ${xFmt(XS.y,ty[1])}, acima.</p>`;
  L.innerHTML=h;
  // resumo por célula
  const cnt=Array.from({length:3},()=>[0,0,0]); let tot=0;
  for(const f of fs){ const a=cl3(val(f,XS.x),tx), b=cl3(val(f,XS.y),ty); if(a<0||b<0) continue; cnt[b][a]+=f.properties.pop; tot+=f.properties.pop; }
  const pv=fs.filter(f=>val(f,XS.x)!=null&&val(f,XS.y)!=null&&f.properties.pop>=50); const rho=spear(pv.map(f=>val(f,XS.x)),pv.map(f=>val(f,XS.y)));
  const hh=fs.filter(f=>cl3(val(f,XS.x),tx)===2&&cl3(val(f,XS.y),ty)===2); const bb=d3.rollups(hh,v=>d3.sum(v,f=>f.properties.pop),f=>nmB(f.properties)+' ('+f.properties.mun+')').sort((a,b)=>b[1]-a[1]).slice(0,6);
  document.getElementById('xp-sum').innerHTML=`<div class="xpk"><b>${tot?pctF(100*cnt[2][2]/tot):'—'}</b><span>dos moradores com os dois dados vivem em setores com <b>${esc(ix.n.toLowerCase())}</b> e <b>${esc(iy.n.toLowerCase())}</b> no terço alto (${nF(cnt[2][2])} pessoas).</span></div>
   <div class="xpk"><b>${rho==null?'—':ptBR(d3.format('+.2f')(rho))}</b><span>correlação de Spearman entre os dois indicadores nos ${nF(pv.length)} setores com 50 ou mais moradores deste território.</span></div>
   ${bb.length?`<p class="note"><b>Onde se concentram os setores alto–alto:</b> ${bb.map(([n,v])=>esc(n)+' – '+nF(v)).join('; ')}.</p>`:''}`;
  renderScatter(fs);
}
// ===================== 2. dispersão ligada =====================
function renderScatter(fs){
  const svg=d3.select('#xp-sc'), W=Math.max(300,svg.node().parentNode.clientWidth||600), H=380, M={l:56,r:14,t:28,b:42};
  svg.attr('viewBox',`0 0 ${W} ${H}`).attr('height',H); svg.selectAll('*').remove();
  const pts=fs.filter(f=>val(f,XS.x)!=null&&val(f,XS.y)!=null&&f.properties.pop>=50);
  const lx=['renda','renda_med','d_ubs','d_saude','d_esc','d_parque','verde_hab'].includes(XS.x), ly=['renda','renda_med','d_ubs','d_saude','d_esc','d_parque','verde_hab'].includes(XS.y);
  const ex=d3.extent(pts,f=>val(f,XS.x)), ey=d3.extent(pts,f=>val(f,XS.y));
  const X=(lx?d3.scaleLog().domain([Math.max(1,ex[0]||1),ex[1]||10]):d3.scaleLinear().domain(ex)).nice().range([M.l,W-M.r]);
  const Y=(ly?d3.scaleLog().domain([Math.max(1,ey[0]||1),ey[1]||10]):d3.scaleLinear().domain(ey)).nice().range([H-M.b,M.t]);
  const xv=f=>X(Math.max(lx?1:-Infinity,val(f,XS.x))), yv=f=>Y(Math.max(ly?1:-Infinity,val(f,XS.y)));
  svg.append('g').attr('transform',`translate(0,${H-M.b})`).call(d3.axisBottom(X).ticks(6,lx?'~s':undefined).tickFormat(v=>ptBR(d3.format(lx?'~s':',~r')(v)))).attr('class','xpax');
  svg.append('g').attr('transform',`translate(${M.l},0)`).call(d3.axisLeft(Y).ticks(6).tickFormat(v=>ptBR(d3.format(ly?'~s':',~r')(v)))).attr('class','xpax');
  svg.append('text').attr('x',W-M.r).attr('y',H-6).attr('text-anchor','end').attr('class','xpaxt').text(byK[XS.x].n+(lx?' (escala log)':''));
  svg.append('text').attr('x',M.l).attr('y',M.t-12).attr('class','xpaxt').text(byK[XS.y].n+(ly?' (escala log)':''));
  const dots=svg.append('g').selectAll('circle').data(pts).join('circle').attr('cx',xv).attr('cy',yv).attr('r',2.6).attr('fill','var(--accent)').attr('fill-opacity',.45);
  const out=document.getElementById('xp-brush'); XS.sel=null;
  const summary=sel=>{ if(!sel||!sel.length){ out.innerHTML='<p class="note">Nenhum setor selecionado. Arraste sobre o gráfico.</p>'; XS.m.ps.attr('fill-opacity',1); return; }
    const ids=new Set(sel.map(f=>f.properties.id)); XS.m.ps.attr('fill-opacity',f=>ids.has(f.properties.id)?1:.15);
    const pop=d3.sum(sel,f=>f.properties.pop), dom=d3.sum(sel,f=>f.properties.dppo||0);
    const bb=d3.rollups(sel,v=>d3.sum(v,f=>f.properties.pop),f=>nmB(f.properties)+' ('+f.properties.mun+')').sort((a,b)=>b[1]-a[1]).slice(0,8);
    out.innerHTML=`<div class="xpk"><b>${nF(sel.length)}</b><span>setores · ${nF(pop)} moradores · ${nF(dom)} domicílios</span></div><div class="xpk"><b>${xFmt(XS.x,agg(sel,byK[XS.x]))}</b><span>${esc(byK[XS.x].n)} (média da seleção)</span></div><div class="xpk"><b>${xFmt(XS.y,agg(sel,byK[XS.y]))}</b><span>${esc(byK[XS.y].n)} (média da seleção)</span></div><p class="note"><b>Principais bairros:</b> ${bb.map(([n,v])=>esc(n)+' – '+nF(v)).join('; ')}.</p>`; };
  const br=d3.brush().extent([[M.l,M.t],[W-M.r,H-M.b]]).on('brush end',ev=>{ const s=ev.selection; if(!s){ XS.sel=null; dots.attr('fill-opacity',.45).attr('fill','var(--accent)'); summary(null); return; }
    const [[x0,y0],[x1,y1]]=s; const sel=pts.filter(f=>{ const x=xv(f),y=yv(f); return x>=x0&&x<=x1&&y>=y0&&y<=y1; }); XS.sel=sel; const ids=new Set(sel.map(f=>f.properties.id));
    dots.attr('fill',f=>ids.has(f.properties.id)?'var(--bad-fg,#c0392b)':'var(--accent)').attr('fill-opacity',f=>ids.has(f.properties.id)?.9:.2); summary(sel); });
  svg.append('g').attr('class','xpbr').call(br); summary(null);
}
// ===================== 3. consulta =====================
let QC=[{k:'esgoto',op:'<',v:50},{k:'renda',op:'<',v:2000}], QT='cvg', QR=[];
function medianOf(k){ return d3.median(F.map(f=>val(f,k)).filter(v=>v!=null)); }
function renderConds(){
  const el=document.getElementById('xp-conds');
  el.innerHTML=QC.map((c,j)=>`<div class="xpcond" data-j="${j}"><select data-f="k">${IND.filter(i=>XK.includes(i.k)).map(i=>`<option value="${i.k}"${i.k===c.k?' selected':''}>${esc(i.n)}</option>`).join('')}</select><select data-f="op"><option value="<"${c.op==='<'?' selected':''}>menor que</option><option value=">"${c.op==='>'?' selected':''}>maior que</option></select><input data-f="v" type="number" step="any" value="${c.v}"><span class="u">${esc(byK[c.k].u||'')}</span><button type="button" data-del="${j}" aria-label="Remover condição">×</button></div>`).join('');
}
function runQuery(){
  const fs=terrF(QT); QR=fs.filter(f=>QC.every(c=>{ const v=val(f,c.k); return v!=null&&(c.op==='<'?v<c.v:v>c.v); }));
  const ids=new Set(QR.map(f=>f.properties.id)); const m=baseMap('xp-qmap',fs);
  m.ps.attr('fill',f=>ids.has(f.properties.id)?'var(--bad-fg,#c0392b)':'var(--panel-2)').attr('stroke',f=>ids.has(f.properties.id)?'var(--panel)':'var(--line)')
    .on('pointermove',(ev,f)=>{ const p=f.properties; tip(ev,`<div class="hst-t">${esc(nmB(p))} · ${esc(p.mun)}</div>`+QC.map(c=>`<div class="hst-r"><b>${xFmt(c.k,val(f,c.k))}</b><span>${esc(byK[c.k].n)}</span></div>`).join('')+`<div class="hst-n">${ids.has(p.id)?'atende a todas as condições':'não atende'}</div>`); }).on('pointerleave',()=>hTipHide());
  const pop=d3.sum(QR,f=>f.properties.pop), dom=d3.sum(QR,f=>f.properties.dppo||0), tp=d3.sum(fs,f=>f.properties.pop);
  const bb=d3.rollups(QR,v=>[v.length,d3.sum(v,f=>f.properties.pop)],f=>nmB(f.properties)+' ('+f.properties.mun+')').sort((a,b)=>b[1][1]-a[1][1]).slice(0,12);
  document.getElementById('xp-qres').innerHTML=`<div class="xpk"><b>${nF(QR.length)}</b><span>setores atendem às ${QC.length} condições</span></div><div class="xpk"><b>${nF(pop)}</b><span>moradores (${pctF(tp?100*pop/tp:null)} do território) · ${nF(dom)} domicílios</span></div>${bb.length?`<div class="tblwrap" style="max-height:none"><table class="dt xpt"><thead><tr><th class="l">Bairro / distrito</th><th>Setores</th><th>Moradores</th></tr></thead><tbody>${bb.map(([n,[s,p]])=>`<tr><td class="l">${esc(n)}</td><td>${s}</td><td>${nF(p)}</td></tr>`).join('')}</tbody></table></div>`:''}`;
}
// ===================== 4. lado a lado =====================
let CP={a:'ivsa',b:'verde',t:'cvg'};
function qBreaks(k){ const v=F.map(f=>val(f,k)).filter(v=>v!=null).sort(d3.ascending); return [.2,.4,.6,.8].map(q=>d3.quantile(v,q)); }
function rampOf(k){ const i=byK[k]; return i.pol==='b'?d3.interpolateBlues:i.pol==='r'?d3.interpolateReds:d3.interpolatePurples; }
function renderCmp(){
  const fs=terrF(CP.t); const ms=[];
  const sync=t=>{ for(const m of ms){ m.g.attr('transform',t); m.svg.property('__zoom',t); } };
  for(const [side,k] of [['1',CP.a],['2',CP.b]]){
    const b=qBreaks(k), ramp=rampOf(k), cols=[.15,.35,.55,.75,.92].map(ramp);
    const m=baseMap('xp-cm'+side,fs,{onZoom:sync}); ms.push(m);
    const ci=v=>v==null?null:cols[d3.bisectRight(b,v)];
    m.ps.attr('fill',f=>ci(val(f,k))||'var(--nodata,#cdd3de)')
      .on('pointermove',(ev,f)=>{ const p=f.properties; tip(ev,`<div class="hst-t">${esc(nmB(p))} · ${esc(p.mun)}</div><div class="hst-r"><b>${xFmt(CP.a,val(f,CP.a))}</b><span>${esc(byK[CP.a].n)}</span></div><div class="hst-r"><b>${xFmt(CP.b,val(f,CP.b))}</b><span>${esc(byK[CP.b].n)}</span></div>`); for(const mm of ms) mm.hl.selectAll('*').remove(); for(const mm of ms) mm.hl.append('path').attr('d',mm.path(f)).attr('fill','none').attr('stroke','var(--fg)').attr('stroke-width',2).attr('vector-effect','non-scaling-stroke'); })
      .on('pointerleave',()=>{ hTipHide(); for(const mm of ms) mm.hl.selectAll('*').remove(); });
    document.getElementById('xp-c'+side+'t').innerHTML=`<b>${esc(byK[k].n)}</b>`;
    document.getElementById('xp-cl'+side).innerHTML=cols.map((c,j)=>`<span><i style="background:${c}"></i>${j===0?'até '+xFmt(k,b[0]):j===4?'mais de '+xFmt(k,b[3]):xFmt(k,b[j-1])+' a '+xFmt(k,b[j])}</span>`).join('')+'<span><i style="background:var(--nodata,#cdd3de)"></i>sem dado</span>';
  }
}
// ===================== Desigualdade: LISA =====================
let DS={k:'ivsa',t:'cvg'};
function knn(fs,k){ const c=fs.map(f=>d3.geoCentroid(f)); const lat0=d3.mean(c,x=>x[1])*Math.PI/180, cx=Math.cos(lat0); const n=c.length, nb=new Array(n);
  for(let i=0;i<n;i++){ const d=[]; for(let j=0;j<n;j++){ if(j===i) continue; const dx=(c[i][0]-c[j][0])*cx, dy=c[i][1]-c[j][1]; d.push([dx*dx+dy*dy,j]); } d.sort((a,b)=>a[0]-b[0]); nb[i]=d.slice(0,k).map(x=>x[1]); } return nb; }
function renderLisa(){
  const all=terrF(DS.t).filter(f=>val(f,DS.k)!=null&&f.properties.pop>=50); const n=all.length; const sum=document.getElementById('ds-sum');
  if(n<30){ baseMap('ds-map',terrF(DS.t)).ps.attr('fill','var(--panel-2)'); sum.innerHTML='<p class="note">Poucos setores com dado neste território para a análise (mínimo de 30).</p>'; return; }
  const x=all.map(f=>val(f,DS.k)), mu=d3.mean(x), sd=d3.deviation(x)||1, z=x.map(v=>(v-mu)/sd), K=6, nb=knn(all,K);
  const lag=nb.map(js=>d3.mean(js,j=>z[j])); const m2=d3.sum(z,v=>v*v)/n; const I=d3.sum(z.map((v,i)=>v*lag[i]))/(n*m2);
  const R=rng(20261022), P=999; let ge=0;
  for(let p=0;p<P;p++){ const zz=d3.shuffle(z.slice(),0,n,R); let s=0; for(let i=0;i<n;i++){ let l=0; for(const j of nb[i]) l+=zz[j]; s+=zz[i]*l/K; } if(s/(n*m2)>=I) ge++; }
  const pG=(ge+1)/(P+1);
  const cls=new Array(n);
  for(let i=0;i<n;i++){ const Ii=z[i]*lag[i]; let c=0; const others=z.filter((_,j)=>j!==i);
    for(let p=0;p<199;p++){ let l=0; for(let q=0;q<K;q++) l+=others[Math.floor(R()*others.length)]; if(Ii>=0 ? z[i]*l/K>=Ii : z[i]*l/K<=Ii) c++; }
    const pi=(c+1)/200; cls[i]=pi<0.05?(z[i]>0&&lag[i]>0?'HH':z[i]<0&&lag[i]<0?'LL':z[i]>0?'HL':'LH'):'NS'; }
  const COL={HH:'#d7191c',LL:'#2c7bb6',HL:'#fdae61',LH:'#abd9e9',NS:'var(--xp-ns)'}, LAB={HH:'alto-alto',LL:'baixo-baixo',HL:'alto-baixo',LH:'baixo-alto',NS:'não significativo'};
  const byId=new Map(all.map((f,i)=>[f.properties.id,cls[i]]));
  const m=baseMap('ds-map',terrF(DS.t)); m.ps.attr('fill',f=>COL[byId.get(f.properties.id)]||'var(--nodata,#cdd3de)')
    .on('pointermove',(ev,f)=>{ const p=f.properties; tip(ev,`<div class="hst-t">${esc(nmB(p))} · ${esc(p.mun)}</div><div class="hst-r"><b>${xFmt(DS.k,val(f,DS.k))}</b><span>${esc(byK[DS.k].n)}</span></div><div class="hst-n">${LAB[byId.get(p.id)]||'sem dado ou menos de 50 moradores'}</div>`); }).on('pointerleave',()=>hTipHide());
  const cnt=k=>all.filter((_,i)=>cls[i]===k); const hh=cnt('HH'), ll=cnt('LL');
  const top=d3.rollups(hh,v=>d3.sum(v,f=>f.properties.pop),f=>nmB(f.properties)+' ('+f.properties.mun+')').sort((a,b)=>b[1]-a[1]).slice(0,8);
  const hi=byK[DS.k].pol==='b'?'baixo-baixo':'alto-alto';
  sum.innerHTML=`<div class="xpk"><b>${ptBR(d3.format('+.3f')(I))}</b><span>Moran global (p = ${ptBR(d3.format('.3f')(pG))}, ${P} permutações; ${nF(n)} setores). ${I>0.3?'Forte':I>0.1?'Moderada':'Fraca'} tendência de setores vizinhos terem valores parecidos.</span></div>
  <div class="lisal">${['HH','LL','HL','LH','NS'].map(k=>`<span><i style="background:${COL[k]}"></i>${LAB[k]} · ${nF(cnt(k).length)} setores · ${nF(d3.sum(cnt(k),f=>f.properties.pop))} mor.</span>`).join('')}</div>
  <p class="note">${byK[DS.k].pol==='n'?'':`Para este indicador, a situação desfavorável corresponde aos agrupamentos <b>${hi}</b>. `}${top.length?`<b>Maiores bolsões alto-alto:</b> ${top.map(([a,b])=>esc(a)+' – '+nF(b)).join('; ')}.`:''}</p>`;
}
// ===================== Desigualdade de renda =====================
function giniW(v,w){ const o=v.map((x,i)=>[x,w[i]]).filter(a=>a[0]!=null&&a[1]>0).sort((a,b)=>a[0]-b[0]); const W=d3.sum(o,a=>a[1]), M=d3.sum(o,a=>a[0]*a[1])/W; let cum=0,cumx=0,B=0; for(const [x,w] of o){ const prev=cumx; cum+=w; cumx+=x*w; B+=w*(prev+cumx)/2; } return 1-2*B/(W*M*W)*1+0; }
function gini2(v,w){ const o=v.map((x,i)=>[x,w[i]]).filter(a=>a[0]!=null&&a[1]>0).sort((a,b)=>a[0]-b[0]); const W=d3.sum(o,a=>a[1]), T=d3.sum(o,a=>a[0]*a[1]); let cw=0,cx=0,area=0; for(const [x,w] of o){ const nw=cw+w, nx=cx+x*w; area+=(nw-cw)/W*((cx+nx)/T)/2; cw=nw; cx=nx; } return 1-2*area; }
function theil(rows){ const W=d3.sum(rows,r=>r.w), M=d3.sum(rows,r=>r.w*r.y)/W; return d3.sum(rows,r=>r.w/W*(r.y/M)*Math.log(r.y/M)); }
function renderIneq(){
  const rowsOf=fs=>fs.filter(f=>val(f,'renda')>0&&(f.properties.wr||f.properties.dppo)>0).map(f=>({y:f.properties.renda,w:f.properties.wr||f.properties.dppo,m:f.properties.mun}));
  const all=rowsOf(F); const T=theil(all), W=d3.sum(all,r=>r.w), M=d3.sum(all,r=>r.w*r.y)/W;
  let between=0, within=0; const lines=[];
  for(const mn of XMUN){ const r=rowsOf(F.filter(f=>f.properties.mun===mn)); if(!r.length) continue; const w=d3.sum(r,x=>x.w), m=d3.sum(r,x=>x.w*x.y)/w, s=w*m/(W*M); const t=theil(r); between+=s*Math.log(m/M); within+=s*t;
    lines.push([mn,r.length,m,gini2(r.map(x=>x.y),r.map(x=>x.w)),t,d3.quantile(r.map(x=>x.y).sort(d3.ascending),.9)/d3.quantile(r.map(x=>x.y).sort(d3.ascending),.1)]); }
  lines.sort((a,b)=>b[3]-a[3]);
  const g=gini2(all.map(r=>r.y),all.map(r=>r.w)), ys=all.map(r=>r.y).sort(d3.ascending);
  document.getElementById('ds-gini').innerHTML=`<thead><tr><th class="l">Município</th><th>Setores</th><th>Renda média</th><th>Gini</th><th>Theil T</th><th>Razão P90/P10</th></tr></thead><tbody>${lines.map(l=>`<tr><td class="l">${esc(l[0])}</td><td>${nF(l[1])}</td><td>${fv('renda',l[2])}</td><td>${ptBR(d3.format('.3f')(l[3]))}</td><td>${ptBR(d3.format('.3f')(l[4]))}</td><td>${ptBR(d3.format('.1f')(l[5]))}</td></tr>`).join('')}<tr class="tot"><td class="l">RMVRC</td><td>${all.length}</td><td>${fv('renda',M)}</td><td>${ptBR(d3.format('.3f')(g))}</td><td>${ptBR(d3.format('.3f')(T))}</td><td>${ptBR(d3.format('.1f')(d3.quantile(ys,.9)/d3.quantile(ys,.1)))}</td></tr></tbody>`;
  document.getElementById('ds-theil').innerHTML=`<b>Decomposição do Theil da RMVRC (${ptBR(d3.format('.3f')(T))}):</b> ${ptBR(fmt1(100*within/T))}% da desigualdade de renda entre setores está <b>dentro</b> dos municípios e ${ptBR(fmt1(100*between/T))}% <b>entre</b> eles. A desigualdade é, portanto, sobretudo intramunicipal: está entre bairros da mesma cidade. P90/P10 = razão entre a renda média do setor no percentil 90 e no percentil 10.`;
}
const GK=['esgoto','agua','lixo','analf','pav','arvore','bueiro','calcada','verde','lst','inund','app_pct','d_ubs','d_saude','d_parque','ivsa'];
let GT='urb';
function renderGrad(){
  const fs=terrF(GT).filter(f=>val(f,'renda')>0&&f.properties.pop>0).sort((a,b)=>val(a,'renda')-val(b,'renda'));
  const tot=d3.sum(fs,f=>f.properties.pop); let acc=0; const q1=[],q5=[];
  for(const f of fs){ const mid=acc+f.properties.pop/2; if(mid<=tot*.2) q1.push(f); else if(mid>=tot*.8) q5.push(f); acc+=f.properties.pop; }
  const rows=GK.filter(k=>byK[k]).map(k=>{ const a=agg(q1,byK[k]), b=agg(q5,byK[k]); const i=byK[k]; let gap=''; if(a!=null&&b!=null){ const worse=i.pol==='b'?a<b:i.pol==='r'?a>b:null; gap=(i.u==='%'?ptBR(d3.format('+.1f')(b-a))+' p.p.':b&&a?ptBR(d3.format('.2f')(a/b))+'×':''); return [i.n,fv(k,a),fv(k,b),gap,worse==null?'':worse?'<span class="dsw">mais pobres em pior situação</span>':'<span class="dsb">mais pobres em situação igual ou melhor</span>']; } return [i.n,fv(k,a),fv(k,b),'','']; });
  document.getElementById('ds-grad').innerHTML=`<thead><tr><th class="l">Indicador</th><th>20% mais pobres</th><th>20% mais ricos</th><th>Diferença (ricos − pobres) ou razão (pobres ÷ ricos)</th><th class="l">Leitura</th></tr></thead><tbody>${rows.map(r=>`<tr><td class="l">${esc(r[0])}</td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td class="l">${r[4]}</td></tr>`).join('')}</tbody><caption class="note" style="caption-side:bottom;text-align:left">Renda média dos dois grupos: ${fv('renda',agg(q1,byK.renda))} e ${fv('renda',agg(q5,byK.renda))}. ${nF(d3.sum(q1,f=>f.properties.pop))} e ${nF(d3.sum(q5,f=>f.properties.pop))} moradores.</caption>`;
}
// ===================== Validação do IVSA =====================
function renderVal(){
  const ps=F.map(f=>f.properties).filter(p=>p.ivsa!=null);
  const cv=ps.filter(p=>['Cuiabá','Várzea Grande'].includes(p.mun)&&p.sit==='Urbana');
  const fc=cv.filter(p=>p.fcu), nf=cv.filter(p=>!p.fcu);
  let auc=0; for(const a of fc) for(const b of nf) auc+=a.ivsa>b.ivsa?1:a.ivsa===b.ivsa?.5:0; auc/=fc.length*nf.length||1;
  const ext=[['negros','Pretos e pardos (%)',1],['criancas','Crianças de 0 a 9 anos (%)',1],['mor','Moradores por domicílio',1],['inund','Suscetibilidade alta a inundação',1]];
  const sp=(U,k)=>{ const q=U.filter(p=>p[k]!=null&&p.pop>=50); return [spear(q.map(p=>p.ivsa),q.map(p=>p[k])),q.length]; };
  const cvu=cv.filter(p=>p.pop>=50);
  const rr=ext.map(([k,n,e])=>{ const A=sp(ps,k), B=sp(cv,k); return [n,e,A[0],A[1],B[0],B[1]]; });
  const ok=(r,e)=>r==null?'—':(Math.sign(r)===e&&Math.abs(r)>=.1)?'<span class="dsb">sim</span>':Math.abs(r)<.1?'fraca':'<span class="dsw">não</span>';
  const f2=v=>v==null?'—':ptBR(d3.format('+.2f')(v));
  const bad=rr.filter(r=>r[2]!=null&&Math.sign(r[2])!==r[1]&&Math.abs(r[2])>=.1).map(r=>r[0].toLowerCase());
  document.getElementById('ds-conv').innerHTML=`<div class="xpk"><b>${ptBR(d3.format('.2f')(auc))}</b><span>AUC: probabilidade de um setor de favela ou comunidade urbana (IBGE) ter IVSA maior que um setor comum, nas áreas urbanas da conurbação (${nF(fc.length)} e ${nF(nf.length)} setores). 0,5 = acaso; 1 = separação perfeita; acima de 0,7 costuma ser considerado discriminação aceitável. Média do IVSA: ${ptBR(fmt1(d3.mean(fc,p=>p.ivsa)))} nas favelas e comunidades urbanas e ${ptBR(fmt1(d3.mean(nf,p=>p.ivsa)))} nos demais.</span></div>
  <div class="tblwrap" style="max-height:none"><table class="dt xpt"><thead><tr><th class="l">Variável fora do índice</th><th>Sinal esperado</th><th>RMVRC</th><th>Confere?</th><th>Conurbação urbana</th><th>Confere?</th></tr></thead><tbody>${rr.map(r=>`<tr><td class="l">${r[0]}</td><td>${r[1]>0?'+':'−'}</td><td>${f2(r[2])}</td><td>${ok(r[2],r[1])}</td><td>${f2(r[4])}</td><td>${ok(r[4],r[1])}</td></tr>`).join('')}</tbody></table></div>
  <p class="note">Correlação de Spearman nos setores com 50 ou mais moradores (${nF(ps.filter(p=>p.pop>=50).length)} na RMVRC; ${nF(cvu.length)} na conurbação urbana). Essas variáveis não entram no cálculo do IVSA.</p>`;
  // robustez: 300 conjuntos de pesos de Dirichlet(1) sobre os 7 componentes
  const CC=WC.filter(c=>W0[c.k]>0), C=CC.map(c=>c.k), w0=CC.map(c=>W0[c.k]);
  const base=F.filter(f=>f.properties.pop>=50&&f.properties._ic);
  const Z=base.map(f=>C.map(k=>{ const v=f.properties._ic[k]; return v==null?null:v/100; }));
  const score=w=>Z.map(zs=>{ let s=0,sw=0,tw=d3.sum(w); zs.forEach((z,j)=>{ if(z!=null){ s+=w[j]*z; sw+=w[j]; } }); return sw>=.6*tw?s/sw:null; });
  const s0=score(w0); const q80=d3.quantile(s0.filter(v=>v!=null).sort(d3.ascending),.8);
  const top0=s0.map(v=>v!=null&&v>=q80); const R=rng(20261001), hits=new Array(base.length).fill(0), N=300;
  const gam=()=>-Math.log(1-R());
  for(let t=0;t<N;t++){ const w=C.map(gam); const s=score(w); const q=d3.quantile(s.filter(v=>v!=null).sort(d3.ascending),.8); s.forEach((v,i)=>{ if(v!=null&&v>=q) hits[i]++; }); }
  const ntop=top0.filter(Boolean).length, rob=top0.filter((t,i)=>t&&hits[i]>=.8*N).length, mod=top0.filter((t,i)=>t&&hits[i]>=.5*N&&hits[i]<.8*N).length;
  const loo=C.map((k,j)=>{ const w=w0.map((x,i)=>i===j?0:x); const s=score(w); const idx=s0.map((v,i)=>v!=null&&s[i]!=null?i:-1).filter(i=>i>=0); return [byK[k].n,spear(idx.map(i=>s0[i]),idx.map(i=>s[i]))]; });
  document.getElementById('ds-rob').innerHTML=`<div class="xpk"><b>${pctF(100*rob/ntop)}</b><span>dos ${nF(ntop)} setores entre os 20% mais vulneráveis continuam nesse grupo em pelo menos 80% de ${N} sorteios de pesos (Dirichlet α = 1, semente fixa); ${pctF(100*mod/ntop)} em 50% a 80%.</span></div>
  <div class="tblwrap" style="max-height:none"><table class="dt xpt"><thead><tr><th class="l">Componente retirado</th><th>Spearman com o IVSA completo</th></tr></thead><tbody>${loo.map(r=>`<tr><td class="l">${esc(r[0])}</td><td>${ptBR(d3.format('.3f')(r[1]))}</td></tr>`).join('')}</tbody></table></div>
  <p class="note">${rob/ntop>=.7?'A maior parte do grupo mais vulnerável se mantém com qualquer combinação de pesos.':'Com pesos sorteados, a composição exata do grupo dos 20% mais vulneráveis muda bastante: '+pctF(100*(rob+mod)/ntop)+' dos setores permanecem nele em pelo menos metade dos sorteios. Use o IVSA como gradiente (mais ou menos vulnerável) e não como fronteira rígida; os setores que se mantêm em 80% dos sorteios são o núcleo mais seguro para priorização.'} Na tabela, correlação acima de 0,95 indica que retirar o componente quase não muda a ordem dos setores; a menor correlação aponta o componente que mais pesa no resultado.</p>`;
}
// ===================== Confiabilidade =====================
function conf(p){ const why=[]; let s=100;
  if(p.pop<50){ s-=40; why.push('menos de 50 moradores'); } else if(p.pop<200){ s-=15; why.push('menos de 200 moradores'); }
  if(p._icf){ s-=15; why.push('IVSA com '+p._icn+' componentes'); }
  if(p.pav==null&&p.sit==='Urbana'){ s-=10; why.push('sem pesquisa de entorno'); }
  if(p.vr===40){ s-=10; why.push('vegetação em pixels de 40 m'); }
  if(p.lr||p.ld){ s-=10; why.push('temperatura de imagem vizinha ou amostra de 120 m'); }
  if(p.inund==null&&p.sit==='Urbana'){ s-=10; why.push('sem modelo de inundação'); }
  s=Math.max(0,s); return {s,c:s>=80?'alta':s>=60?'média':'baixa',why}; }
window.__xConf=conf;
function renderConf(){
  const COL={alta:'#4c9a6a',média:'#e0b24a',baixa:'#c0392b'}; const m=baseMap('ds-cmap',F.filter(f=>f.properties.sit==='Urbana'),{fit:terrF('cvg')});
  m.ps.attr('fill',f=>COL[conf(f.properties).c]).on('pointermove',(ev,f)=>{ const p=f.properties, r=conf(p); tip(ev,`<div class="hst-t">${esc(nmB(p))} · ${esc(p.mun)}</div><div class="hst-r"><b>${r.s}</b><span>confiabilidade ${r.c}</span></div><div class="hst-n">${r.why.length?esc(r.why.join('; ')):'sem limitação conhecida'}</div>`); }).on('pointerleave',()=>hTipHide());
  const rows=XMUN.map(mn=>{ const fs=F.filter(f=>f.properties.mun===mn); const c={alta:0,média:0,baixa:0}; for(const f of fs) c[conf(f.properties).c]+=f.properties.pop; const t=d3.sum(fs,f=>f.properties.pop); return [mn,c.alta/t,c.média/t,c.baixa/t]; });
  document.getElementById('ds-csum').innerHTML=`<div class="lisal">${Object.entries(COL).map(([k,c])=>`<span><i style="background:${c}"></i>${k} (${k==='alta'?'80 a 100':k==='média'?'60 a 79':'abaixo de 60'})</span>`).join('')}</div><div class="tblwrap" style="max-height:none"><table class="dt xpt"><thead><tr><th class="l">Município</th><th>Alta</th><th>Média</th><th>Baixa</th></tr></thead><tbody>${rows.map(r=>`<tr><td class="l">${esc(r[0])}</td>${r.slice(1).map(v=>`<td>${pctF(100*v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div><p class="note">Porcentagem dos moradores de cada município (todos os setores) por classe de confiabilidade. Mapa: setores urbanos.</p>`;
}
// ===================== Subsídios a políticas =====================
const DK=['esgoto','esg_prec','agua','lixo','sem_banh','renda','analf','pav','calcada','bueiro','luz','onibus','arvore','verde','lst','inund','app_pct','sgb_alta','a1974','eros_alta','d_ubs','d_saude','d_esc','d_parque','ivsa'];
const URBK=['pav','calcada','bueiro','luz','onibus','arvore','lst','inund','verde'];
const KB={
 san:{n:'Saneamento básico',ks:['esgoto','esg_prec','agua','lixo','sem_banh'],acoes:['Priorizar a expansão da rede coletora e as ligações intradomiciliares nos setores com menor cobertura, começando pelos de maior número de domicílios sem atendimento.','Programas de ligação à rede para famílias de baixa renda (tarifa social e apoio à instalação).','Substituir fossas rudimentares e lançamentos em vala ou curso d’água por soluções adequadas (rede ou sistema individual com tratamento) onde a rede não chegar no curto prazo.','Garantir abastecimento regular de água pela rede e cobertura universal da coleta de resíduos.'],inst:['Lei nº 11.445/2007 e Lei nº 14.026/2020 (marco do saneamento): metas de 99% de água e 90% de esgoto até 31/12/2033.','Plano Municipal de Saneamento Básico (PMSB), revisto no máximo a cada 10 anos.','Lei nº 12.305/2010 (Política Nacional de Resíduos Sólidos).'],mon:'Domicílios ligados à rede de esgoto e de água (Censo, SNIS/SINISA); internações por DRSAI (DATASUS).',org:'Prefeitura, prestador do serviço de saneamento, agência reguladora, titular do serviço.'},
 dren:{n:'Drenagem, inundações e APP',ks:['inund','sgb_alta','a1974','app_pct','bueiro','eros_alta'],acoes:['Delimitar em campo as áreas de risco e as APPs urbanas; não autorizar novas ocupações nas faixas de suscetibilidade alta.','Obras de microdrenagem (bueiros, galerias) e soluções baseadas na natureza (parques lineares, áreas de retenção) nas microbacias com mais moradores expostos.','Sistemas de alerta e planos de contingência para os bairros abaixo das cotas de cheia do Rio Cuiabá.','Recuperar a vegetação das APPs e controlar a erosão em encostas e cabeceiras.'],inst:['Lei nº 12.608/2012 (Política Nacional de Proteção e Defesa Civil): mapeamento de áreas de risco e planos de contingência.','Lei nº 12.651/2012 (Código Florestal), art. 4º, e Lei nº 14.285/2021 (APP em área urbana consolidada).','Plano Diretor (Lei nº 10.257/2001 – Estatuto da Cidade): zoneamento das áreas de risco e de proteção.','Cartas de suscetibilidade do Serviço Geológico do Brasil como base do planejamento.'],mon:'Moradores em suscetibilidade alta e em APP (Atlas); ocorrências de alagamento (Defesa Civil); área de APP recuperada.',org:'Prefeitura (obras, meio ambiente, planejamento), Defesa Civil municipal e estadual, órgão ambiental.'},
 hab:{n:'Habitação, regularização e entorno urbano',ks:['pav','calcada','luz','sem_banh','renda'],acoes:['Urbanização integrada de assentamentos precários: pavimentação, calçadas, iluminação, drenagem e equipamentos.','Regularização fundiária urbana (REURB-S) dos núcleos informais consolidados fora de áreas de risco.','Demarcar Zonas Especiais de Interesse Social (ZEIS) no Plano Diretor.'],inst:['Lei nº 13.465/2017 (Regularização Fundiária Urbana – REURB).','Lei nº 10.257/2001 (Estatuto da Cidade): ZEIS, IPTU progressivo, outorga onerosa.','Plano Local de Habitação de Interesse Social.'],mon:'Moradores em faces com pavimentação, calçada e iluminação (Censo); títulos de REURB emitidos.',org:'Prefeitura (habitação, obras, regularização fundiária), cartório de registro de imóveis.'},
 verde:{n:'Áreas verdes e calor urbano',ks:['arvore','verde','lst','d_parque'],acoes:['Plano de arborização urbana priorizando os setores mais quentes e com menos vegetação.','Implantar praças e parques de bairro onde a distância a áreas verdes é maior.','Exigir permeabilidade e arborização em novos loteamentos e em reformas de vias.'],inst:['Lei nº 14.904/2024 (diretrizes para planos de adaptação à mudança do clima).','Plano Diretor e legislação de parcelamento do solo (taxa de permeabilidade, áreas verdes).','Plano Municipal de Arborização Urbana.'],mon:'Cobertura vegetal e temperatura de superfície por setor (Sentinel-2 e Landsat, anualmente na estiagem).',org:'Prefeitura (meio ambiente, obras, planejamento).'},
 mob:{n:'Mobilidade e acessibilidade',ks:['onibus','calcada','pav','d_esc'],acoes:['Ampliar a cobertura do transporte coletivo e de pontos de parada nos bairros sem atendimento.','Programa de calçadas acessíveis nas rotas para escolas e unidades de saúde.'],inst:['Lei nº 12.587/2012 (Política Nacional de Mobilidade Urbana) e Plano de Mobilidade Urbana.','Lei nº 13.146/2015 (Estatuto da Pessoa com Deficiência): acessibilidade.'],mon:'Moradores em faces com ponto de ônibus e calçada (Censo); tempo de deslocamento (pesquisa origem-destino).',org:'Prefeitura (mobilidade, obras), operadoras de transporte, órgão metropolitano.'},
 saude:{n:'Saúde e serviços sociais',ks:['d_ubs','d_saude'],acoes:['Rever a territorialização da Atenção Primária para cobrir os setores mais distantes de USF/UBS.','Estratégias de saúde itinerante ou unidades de apoio nas áreas rurais e periurbanas.','Vigilância de DRSAI e de dengue integrada às ações de saneamento.'],inst:['Política Nacional de Atenção Básica (Portaria GM/MS nº 2.436/2017).','Plano Municipal de Saúde.'],mon:'Distância à USF/UBS (Atlas); cobertura da Atenção Primária; internações por condições sensíveis à atenção primária.',org:'Secretaria Municipal de Saúde, Secretaria de Estado de Saúde.'},
 soc:{n:'Renda, educação e vulnerabilidade social',ks:['renda','analf','ivsa','d_esc'],acoes:['Educação de jovens e adultos (EJA) e alfabetização nos setores com maior analfabetismo.','Busca ativa para o Cadastro Único e programas de transferência de renda nos setores de menor renda.','Integrar as ações setoriais nos territórios de IVSA muito alto (abordagem territorial integrada).'],inst:['Plano Municipal de Educação (Lei nº 13.005/2014 – Plano Nacional de Educação).','Sistema Único de Assistência Social (Lei nº 8.742/1993 – LOAS) e CRAS de referência.'],mon:'Analfabetismo e renda (Censo); famílias no Cadastro Único; IVSA (Atlas).',org:'Secretarias de assistência social e de educação.'}
};
function posRel(k,v,urbOnly){ const i=byK[k]; if(v==null) return null; let tot=0,bet=0; // parcela dos moradores da RMVRC em setores em situação melhor (empates contam metade)
  for(const f of F){ const p=f.properties, x=p[k]; if(x==null||!(p.pop>=50)||(urbOnly&&p.sit!=='Urbana')) continue; tot+=p.pop; if(i.pol==='b'?x>v:x<v) bet+=p.pop; else if(x===v) bet+=p.pop/2; } return tot?bet/tot:null; }
function situ(k,v,r,pr){ const i=byK[k]; if(pr==null||r==null) return ''; const worse=i.pol==='b'?v<r:v>r, gap=i.u==='%'?Math.abs(v-r)>1:Math.abs(v-r)>.05*Math.abs(r);
  if(worse&&gap&&pr>=.8) return 'critico'; if(worse&&gap&&pr>=.6) return 'atencao'; if(!worse&&pr<=.2) return 'bom'; return 'medio'; }
function renderPol(){
  const mn=document.getElementById('pp-m').value, b=document.getElementById('pp-b2').value;
  let fs=F.filter(f=>f.properties.mun===mn); if(b) fs=fs.filter(f=>nmB(f.properties)===b);
  const name=b?`${b} (${mn})`:mn; const pop=d3.sum(fs,f=>f.properties.pop), dom=d3.sum(fs,f=>f.properties.dppo||0);
  const urb=fs.filter(f=>f.properties.sit==='Urbana');
  const diag=DK.filter(k=>byK[k]).map(k=>{ const u=URBK.includes(k)&&urb.length>0; const v=agg(u?urb:fs,byK[k]); if(v==null) return null; const r=agg(u?F.filter(f=>f.properties.sit==='Urbana'):F,byK[k]); const pr=byK[k].pol==='n'?null:posRel(k,v,u); return {k,v,r,pr,st:situ(k,v,r,pr)}; }).filter(Boolean);
  const crit=diag.filter(d=>d.st==='critico'), att=diag.filter(d=>d.st==='atencao');
  const dom2=Object.entries(KB).map(([id,kb])=>({id,kb,hits:[...crit,...att].filter(d=>kb.ks.includes(d.k))})).filter(x=>x.hits.length).sort((a,b)=>d3.sum(b.hits,d=>d.st==='critico'?2:1)-d3.sum(a.hits,d=>d.st==='critico'?2:1));
  const ev=fs.filter(f=>val(f,'esgoto')!=null), av=fs.filter(f=>val(f,'agua')!=null);
  const semEsg=d3.sum(ev,f=>f.properties.dppo*(1-f.properties.esgoto/100)), lig90=Math.max(0,.9*d3.sum(ev,f=>f.properties.dppo)-d3.sum(ev,f=>f.properties.dppo*f.properties.esgoto/100)), lig99=Math.max(0,.99*d3.sum(av,f=>f.properties.dppo)-d3.sum(av,f=>f.properties.dppo*f.properties.agua/100));
  const far=d3.sum(fs.filter(f=>val(f,'d_ubs')>1000),f=>f.properties.pop);
  const lens=IND.filter(i=>i.k.startsWith('ipt_')&&i.k!=='ipt_geral').map(i=>[i,agg(fs,i)]).filter(x=>x[1]!=null).sort((a,b)=>b[1]-a[1]);
  const L=lens[0]&&lens[0][0];
  const topS=L?fs.filter(f=>val(f,L.k)!=null&&f.properties.pop>=50).sort((a,b)=>val(b,L.k)-val(a,L.k)).slice(0,10):[];
  const SL={critico:['crítico','pdc'],atencao:['atenção','pda'],medio:['intermediário','pdm'],bom:['favorável','pdb'],'':['descritivo','pdm']};
  const bar=d=>d.pr==null?'':`<span class="ppbar"><i style="width:${(100*d.pr).toFixed(0)}%"></i></span>`;
  document.getElementById('pp-out').innerHTML=`
  <div class="pph"><div><span class="kick">Ficha de subsídios · ${esc(name)}</span><h3>${esc(name)}</h3><p>${nF(fs.length)} setores · ${nF(pop)} moradores · ${nF(dom)} domicílios ocupados (Censo 2022)</p></div>
  <div class="ppk"><div><b>${nF(crit.length)}</b><span>indicadores em situação crítica</span></div><div><b>${nF(att.length)}</b><span>em atenção</span></div><div><b>${nF(agg(fs,byK.inund_pop)||0)}</b><span>moradores em suscetibilidade alta a inundação (estim.)</span></div><div><b>${nF(agg(fs,byK.app_pop)||0)}</b><span>moradores em APP (estim.)</span></div></div></div>
  <h4 class="xh4">1. Diagnóstico em relação à RMVRC</h4>
  <p class="note">Posição relativa = parcela dos moradores da RMVRC (setores com 50 ou mais moradores) que vivem em setores em situação melhor que a deste território. <b>Crítico</b>: pior que a média da RMVRC (diferença acima de 1 ponto percentual, ou de 5% nos demais indicadores) e posição de 80% ou mais; <b>atenção</b>: idem, com posição de 60% a 79%; <b>favorável</b>: não pior que a média e posição de até 20%; <b>intermediário</b>: os demais. Indicadores do entorno, vegetação, calor e inundação comparam só setores urbanos (do território e da RMVRC).</p>
  <div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th class="l">Indicador</th><th>${esc(b||mn)}</th><th>RMVRC</th><th class="l">Posição relativa (barra = moradores em situação melhor)</th><th class="l">Situação</th></tr></thead><tbody>${diag.sort((a,b)=>(b.pr??-1)-(a.pr??-1)).map(d=>`<tr><td class="l">${esc(byK[d.k].n)}</td><td>${fv(d.k,d.v)}</td><td>${fv(d.k,d.r)}</td><td class="l">${bar(d)}</td><td class="l"><span class="pps ${SL[d.st][1]}">${SL[d.st][0]}</span></td></tr>`).join('')}</tbody></table></div>
  <h4 class="xh4">2. Dimensionamento</h4>
  <ul class="note ppul"><li><b>${nF(semEsg)}</b> domicílios sem esgoto ligado à rede; para a meta de 90% (Lei nº 14.026/2020), ligar ao menos <b>${nF(lig90)}</b> domicílios.</li><li>Para a meta de 99% de abastecimento de água: <b>${nF(lig99)}</b> domicílios a atender.</li><li><b>${nF(far)}</b> moradores (${pctF(pop?100*far/pop:null)}) vivem a mais de 1 km, em linha reta, de uma USF/UBS.</li><li>IVSA médio: <b>${fv('ivsa',agg(fs,byK.ivsa))}</b> (RMVRC: ${fv('ivsa',agg(F,byK.ivsa))}).</li></ul>
  <h4 class="xh4">3. Ações e instrumentos recomendados</h4>
  ${dom2.length?dom2.map(({kb,hits})=>`<div class="ppd"><div class="ppdh"><b>${esc(kb.n)}</b><span>${hits.map(d=>`<span class="pps ${SL[d.st][1]}">${esc(byK[d.k].n)}: ${fv(d.k,d.v)}</span>`).join(' ')}</span></div><div class="split"><div><b class="pplab">Ações</b><ul>${kb.acoes.map(a=>`<li>${a}</li>`).join('')}</ul></div><div><b class="pplab">Instrumentos e referências legais</b><ul>${kb.inst.map(a=>`<li>${a}</li>`).join('')}</ul><b class="pplab">Monitoramento</b><p>${kb.mon}</p><b class="pplab">Responsáveis</b><p>${kb.org}</p></div></div></div>`).join(''):'<p class="note">Nenhum indicador em situação crítica ou de atenção neste território.</p>'}
  <h4 class="xh4">4. Setores prioritários${L?' · lente '+esc(L.n.toLowerCase()):''}</h4>
  ${topS.length?`<p class="note">A lente do Índice de Prioridade Territorial com maior média neste território é <b>${esc(L.n)}</b> (${fv(L.k,lens[0][1])}). Os dez setores com maior nota nessa lente:</p><div class="tblwrap" style="max-height:none"><table class="dt xpt"><thead><tr><th class="l">Setor</th><th class="l">Bairro / distrito</th><th>Moradores</th><th>IPT</th><th>IVSA</th></tr></thead><tbody>${topS.map(f=>`<tr><td class="l">${f.properties.id}</td><td class="l">${esc(nmB(f.properties))}</td><td>${nF(f.properties.pop)}</td><td>${fv(L.k,val(f,L.k))}</td><td>${fv('ivsa',val(f,'ivsa'))}</td></tr>`).join('')}</tbody></table></div>`:'<p class="note">Sem setores com IPT neste território.</p>'}
  <h4 class="xh4">5. Como usar esta ficha nos planos</h4>
  <ul class="note ppul"><li><b>Plano Diretor</b> (Estatuto da Cidade, Lei nº 10.257/2001, revisto ao menos a cada 10 anos): use o diagnóstico e os setores prioritários para delimitar ZEIS, áreas de risco, áreas de proteção e de qualificação urbana.</li><li><b>Plano Municipal de Saneamento Básico</b> (Lei nº 11.445/2007): use os domicílios a ligar como linha de base e as metas de 2033 como horizonte.</li><li><b>Plano de Desenvolvimento Urbano Integrado da RMVRC</b> (Estatuto da Metrópole, Lei nº 13.089/2015): compare o território com os demais municípios gerando a ficha de cada um.</li><li><b>Planos de contingência e de adaptação climática</b> (Leis nº 12.608/2012 e 14.904/2024): use os moradores em suscetibilidade alta, em APP e nas manchas de cheia.</li><li><b>Pesquisas</b>: os setores prioritários e os agrupamentos espaciais (página Desigualdade) indicam onde aprofundar o diagnóstico em campo.</li></ul>
  <p class="note"><b>Limites:</b> o diagnóstico é relativo à RMVRC e baseado no Censo 2022 e nas camadas do Atlas; não substitui levantamento de campo, cadastros municipais nem a participação dos moradores. Fontes: IBGE (Censo 2022), CNES/DATASUS, SGB, ANA, Copernicus, USGS, MapBiomas, OpenStreetMap; ver página Fontes.</p>`;
}
function fillPolB(){ const mn=document.getElementById('pp-m').value; const bs=[...new Set(F.filter(f=>f.properties.mun===mn).map(f=>nmB(f.properties)))].sort((a,b)=>a.localeCompare(b,'pt'));
  document.getElementById('pp-b2').innerHTML='<option value="">Todo o município</option>'+bs.map(b=>`<option>${esc(b)}</option>`).join(''); }
// ===================== ligação dos controles =====================
let done={};
const LASTW={};
function renderExplore(force){ try{
  if(!done.x){ optI(document.getElementById('xp-x'),XS.x); optI(document.getElementById('xp-y'),XS.y); optT(document.getElementById('xp-t'),XS.t); optT(document.getElementById('xp-qt'),QT); optI(document.getElementById('xp-c1'),CP.a); optI(document.getElementById('xp-c2'),CP.b); optT(document.getElementById('xp-ct'),CP.t);
    optI(document.getElementById('ds-k'),DS.k); optT(document.getElementById('ds-t'),DS.t); optT(document.getElementById('ds-gt'),GT);
    document.getElementById('pp-m').innerHTML=XMUN.map(m=>`<option>${esc(m)}</option>`).join(''); fillPolB(); done.x=1; }
  const pg=id=>{ const e=document.querySelector(`[data-page="${id}"]`); return e&&!e.hidden; };
  const w=Math.round((document.querySelector('main,body').clientWidth||0)/40);
  const due=id=>{ if(!pg(id)) return false; if(!force&&LASTW[id]===w) return false; LASTW[id]=w; return true; };
  if(due('explorar')){ renderBiv(); renderConds(); runQuery(); renderCmp(); }
  if(due('desig')){ renderLisa(); renderIneq(); renderGrad(); renderVal(); }
  if(due('politicas')) renderPol();
 }catch(e){ console.error(e); } }
window.renderExplore=renderExplore; window.__xp={renderBiv,renderLisa,renderVal,renderPol,conf,knn};
const on=(id,ev,fn)=>document.getElementById(id)?.addEventListener(ev,fn);
on('xp-x','change',e=>{ XS.x=e.target.value; renderBiv(); }); on('xp-y','change',e=>{ XS.y=e.target.value; renderBiv(); }); on('xp-t','change',e=>{ XS.t=e.target.value; renderBiv(); });
on('xp-swap','click',()=>{ [XS.x,XS.y]=[XS.y,XS.x]; document.getElementById('xp-x').value=XS.x; document.getElementById('xp-y').value=XS.y; renderBiv(); });
on('xp-csv1','click',()=>{ if(XS.sel&&XS.sel.length) csvOut('setores_selecionados_dispersao.csv',XS.sel,[XS.x,XS.y,'ivsa']); else say('Selecione setores no gráfico de dispersão primeiro.'); });
on('xp-conds','change',e=>{ const row=e.target.closest('.xpcond'); if(!row) return; const j=+row.dataset.j, f=e.target.dataset.f; if(f==='k'){ QC[j].k=e.target.value; QC[j].v=+d3.format('.3~f')(medianOf(QC[j].k)); renderConds(); } else if(f==='op') QC[j].op=e.target.value; else QC[j].v=+e.target.value; runQuery(); });
on('xp-conds','click',e=>{ const b=e.target.closest('[data-del]'); if(!b) return; QC.splice(+b.dataset.del,1); renderConds(); runQuery(); });
on('xp-add','click',()=>{ if(QC.length>=5) return; QC.push({k:'inund',op:'>',v:+d3.format('.3~f')(medianOf('inund'))}); renderConds(); runQuery(); });
on('xp-qt','change',e=>{ QT=e.target.value; runQuery(); });
on('xp-csv2','click',()=>{ if(QR.length) csvOut('setores_consulta.csv',QR,[...new Set(QC.map(c=>c.k).concat(['ivsa']))]); else say('Nenhum setor atende às condições.'); });
on('xp-c1','change',e=>{ CP.a=e.target.value; renderCmp(); }); on('xp-c2','change',e=>{ CP.b=e.target.value; renderCmp(); }); on('xp-ct','change',e=>{ CP.t=e.target.value; renderCmp(); });
on('ds-k','change',e=>{ DS.k=e.target.value; renderLisa(); }); on('ds-t','change',e=>{ DS.t=e.target.value; renderLisa(); }); on('ds-gt','change',e=>{ GT=e.target.value; renderGrad(); });
on('pp-m','change',()=>{ fillPolB(); renderPol(); }); on('pp-b2','change',renderPol);
document.querySelector('#xp-biv .xpzoom')?.addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b||!XS.m) return; const z=+b.dataset.z; if(z===0) XS.m.svg.transition().call(XS.m.z.transform,d3.zoomIdentity); else XS.m.svg.transition().call(XS.m.z.scaleBy,z>0?1.6:1/1.6); });
window.addEventListener('hashchange',()=>setTimeout(renderExplore,140));
let rz=0; window.addEventListener('resize',()=>{ clearTimeout(rz); rz=setTimeout(renderExplore,300); });
window.__xpDirty=()=>{ for(const k in LASTW) delete LASTW[k]; if(document.querySelector('[data-page="explorar"]:not([hidden]),[data-page="desig"]:not([hidden]),[data-page="politicas"]:not([hidden])')) renderExplore(true); };
})();
