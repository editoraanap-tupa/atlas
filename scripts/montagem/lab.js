// ------- Laboratório de Governança Territorial -------
const LNR={};
const lensVal=(p,k)=> k==='fcu' ? (p.pop>=50 ? (p.fcu?1:0) : null) : p[k];
const lensName=k=> k==='fcu' ? 'Favela ou comunidade urbana' : (byK[k]?byK[k].n:k);
function lensZ(p,L){ return L.c.map(([k,s,lg])=>{ let x=lensVal(p,k); if(x==null) return null; if(k==='fcu') return x;
  if(lg){ if(x<=0) return s>0?0:1; x=Math.log(x); } const [lo,hi]=LNR[k+(lg?'_l':'')]; let z=Math.max(0,Math.min(1,(x-lo)/((hi-lo)||1))); return s<0?1-z:z; }); }
function computeLenses(){
  for(const L of LENS) for(const [k,s,lg] of L.c){ const id=k+(lg?'_l':''); if(k==='fcu'||LNR[id]) continue;
    let xs=F.filter(f=>f.properties.pop>=50).map(f=>lensVal(f.properties,k)).filter(v=>v!=null); if(lg) xs=xs.filter(v=>v>0).map(Math.log); xs.sort(d3.ascending); LNR[id]=[d3.quantile(xs,.02),d3.quantile(xs,.98)]; }
  for(const f of F){ const p=f.properties; p._lz={};
    for(const L of LENS){ const z=lensZ(p,L); p._lz[L.k]=z; let s=0,n=0; z.forEach(v=>{ if(v!=null){ s+=v; n++; } });
      p['ipt_'+L.k]=(p.pop>=50 && n>=Math.ceil(.6*L.c.length)) ? Math.round(1000*s/n)/10 : null; } }
  for(const L of LENS){ const k='ipt_'+L.k; sorted[k]=F.map(f=>f.properties[k]).filter(v=>v!=null).sort(d3.ascending); }
}

// robustez: 300 combinações de pesos aleatórios (Dirichlet(1), semente fixa)
const ROB={};
function robustez(L){
  if(ROB[L.k]) return ROB[L.k];
  let seed=20261001; const rnd=()=>{ seed|=0; seed=seed+0x6D2B79F5|0; let t=Math.imul(seed^seed>>>15,1|seed); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; };
  const fs=F.filter(f=>f.properties['ipt_'+L.k]!=null), D=300, cnt=new Map(fs.map(f=>[f.properties.id,0])), sc=new Float64Array(fs.length);
  for(let d=0; d<D; d++){ const w=L.c.map(()=>-Math.log(1-rnd()));
    fs.forEach((f,i)=>{ const z=f.properties._lz[L.k]; let s=0,ws=0; z.forEach((v,j)=>{ if(v!=null){ s+=w[j]*v; ws+=w[j]; } }); sc[i]=ws?s/ws:0; });
    const thr=d3.quantile(Array.from(sc).sort((a,b)=>a-b),.8); fs.forEach((f,i)=>{ if(sc[i]>=thr) cnt.set(f.properties.id,cnt.get(f.properties.id)+1); }); }
  const out={}; cnt.forEach((v,k)=>out[k]=v/D); return ROB[L.k]=out;
}
let LAB={lens:'geral',unit:'bairro',meta:'esgoto',scope:'rec',diag:null};
const labScope=()=>F.filter(f=>inSel(f.properties.mun)&&(st.area==='all'||f.properties.sit===st.area));
function groupKey(p,u){ return u==='setor'?p.id : u==='mun'?p.mun : u==='micro'?(p.micro||null) : ((p.bairro||p.dist||'')?(p.mun+'|'+(p.bairro||p.dist)):null); }
function groupName(key,u,fs){ const p=fs[0].properties; return u==='setor'?((p.bairro||p.dist||'Setor')+' · '+p.id.slice(-4)) : u==='mun'?key : u==='micro'?key : (p.bairro||(p.dist+' (distrito, sem bairro no IBGE)')); }
function territories(L,u){
  const R=robustez(L), k='ipt_'+L.k, G=new Map();
  for(const f of labScope()){ const p=f.properties; if(p[k]==null) continue; const g=groupKey(p,u); if(g==null) continue; (G.get(g)||G.set(g,[]).get(g)).push(f); }
  return [...G].map(([key,fs])=>{ const pop=d3.sum(fs,f=>f.properties.pop);
    const ipt=d3.sum(fs,f=>f.properties[k]*f.properties.pop)/pop, rob=d3.sum(fs,f=>(R[f.properties.id]||0)*f.properties.pop)/pop;
    const zc=L.c.map((c,j)=>{ let s=0,w=0; fs.forEach(f=>{ const v=f.properties._lz[L.k][j]; if(v!=null){ s+=v*f.properties.pop; w+=f.properties.pop; } }); return w?s/w:null; });
    const top=zc.map((z,j)=>[z,j]).filter(x=>x[0]!=null&&x[0]>=.6).sort((a,b)=>b[0]-a[0]).slice(0,3).map(x=>lensName(L.c[x[1]][0]));
    return {key,name:groupName(key,u,fs),mun:u==='mun'?'':(new Set(fs.map(f=>f.properties.mun)).size>1?'vários':fs[0].properties.mun),fs,pop,ipt,rob,top,n:fs.length}; }).sort((a,b)=>b.ipt-a.ipt);
}
function robTag(r){ return r>=.8?'<span class="rbt hi">robusta</span>':r>=.5?'<span class="rbt md">moderada</span>':'<span class="rbt lo">sensível aos pesos</span>'; }
function renderLab(){
  const box=document.getElementById('lab-lens'); if(!box) return;
  const L=LENS.find(x=>x.k===LAB.lens);
  box.innerHTML=LENS.map(x=>`<button class="lensb" data-l="${x.k}" aria-pressed="${x.k===LAB.lens}"><b>${x.n}</b><span>${x.c.length} indicadores</span></button>`).join('');
  document.getElementById('lab-info').innerHTML=`<div class="li-h"><div><h4>${L.n}</h4><p>${L.d}</p><div class="li-ods">${L.ods.slice().sort((a,b)=>a-b).map(odsBadge).join(' ')}</div></div><button class="btn" type="button" id="lab-map">Ver este índice no mapa</button></div>
    <div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th class="l">Indicador</th><th class="l">Sentido para a prioridade</th><th>Peso</th><th>Mediana dos setores</th></tr></thead><tbody>${L.c.map(([k,s,lg])=>`<tr><td class="l">${lensName(k)}${lg?' <small class="mu">(em log)</small>':''}</td><td class="l">${s>0?'quanto maior, maior a prioridade':'quanto menor, maior a prioridade'}</td><td class="num">1/${L.c.length}</td><td class="num">${k==='fcu'?'—':fv(k,d3.quantile(sorted[k]||[],.5))}</td></tr>`).join('')}</tbody></table></div>`;
  const T=territories(L,LAB.unit), totPop=d3.sum(T,t=>t.pop), top=T.filter(t=>t.rob>=.8);
  document.getElementById('lab-kpi').innerHTML=[
    ['Territórios analisados',ptBR(fmtN(T.length)),`${{bairro:'bairros',micro:'microbacias',setor:'setores',mun:'municípios'}[LAB.unit]} com valor no recorte`],
    ['Prioridade robusta',ptBR(fmtN(top.length)),'entre os 20% de maior prioridade em pelo menos 80% das combinações de pesos'],
    ['Moradores nesses territórios',ptBR(fmtN(d3.sum(top,t=>t.pop))),totPop?ptBR(fmt1(100*d3.sum(top,t=>t.pop)/totPop))+'% da população analisada':''],
    ['IPT mediano',T.length?ptBR(fmt1(d3.median(T,t=>t.ipt))):'—','0 = menor prioridade · 100 = maior']]
    .map(([a,b,c])=>`<div class="kpi"><div class="lab">${a}</div><div class="val">${b}</div><div class="sub">${c}</div></div>`).join('');
  const N=Math.min(25,T.length);
  document.getElementById('lab-rank').innerHTML=`<thead><tr><th>#</th><th class="l">Território</th>${LAB.unit==='mun'?'':'<th class="l">Município</th>'}<th>Moradores</th><th>IPT</th><th>Robustez</th><th class="l">Principais déficits</th><th></th></tr></thead><tbody>`+
    T.slice(0,N).map((t,i)=>`<tr><td class="num">${i+1}</td><td class="l"><b>${esc(t.name)}</b>${LAB.unit!=='setor'&&LAB.unit!=='mun'?` <small class="mu">${t.n} setor${t.n>1?'es':''}</small>`:''}</td>${LAB.unit==='mun'?'':`<td class="l">${t.mun}</td>`}<td class="num">${ptBR(fmtN(t.pop))}</td><td class="num"><span class="iptb" style="--v:${t.ipt}%">${ptBR(fmt1(t.ipt))}</span></td><td class="num">${ptBR(fmtN(100*t.rob))}% ${robTag(t.rob)}</td><td class="l">${t.top.join(' · ')||'<span class="mu">nenhum acima do limiar</span>'}</td><td><button class="lnk labd" data-i="${i}" type="button">Diagnóstico</button> <button class="lnk labm" data-i="${i}" type="button">Mapa</button></td></tr>`).join('')+'</tbody>';
  document.getElementById('lab-rnote').innerHTML=`Mostrando os ${N} primeiros de ${ptBR(fmtN(T.length))}. IPT do território = média dos setores ponderada pelos moradores. "Principais déficits" = indicadores do objetivo em que o território está na pior faixa (nota normalizada ≥ 0,6). Setores com menos de 50 moradores, ou com menos de 60% dos indicadores do objetivo, ficam sem valor.`;
  window.__labT=T;
  const dl=document.getElementById('lab-bairros'); if(dl&&!dl.children.length){ const B=[...new Set(F.filter(f=>f.properties.bairro).map(f=>f.properties.bairro+' · '+f.properties.mun))].sort((a,b)=>a.localeCompare(b,'pt')); dl.innerHTML=B.map(b=>`<option value="${esc(b)}">`).join(''); }
  renderDiag(); renderSim();
}
function diagOf(fs){
  const pop=d3.sum(fs,f=>f.properties.pop||0), sumP=k=>d3.sum(fs,f=>(f.properties.pop||0)*(f.properties[k]||0)/100);
  const ev=IND.filter(i=>i.pol!=='n'&&!i.k.startsWith('ipt_')&&!['ndvi','arv5','lst_anom','inund2'].includes(i.k)&&!/_pop$/.test(i.k)&&sorted[i.k]&&sorted[i.k].length).map(i=>{ const v=agg(fs,i); if(v==null) return null; const a=sorted[i.k], n=a.length, lo=d3.bisectLeft(a,v)/n, hi=d3.bisectRight(a,v)/n;
    const pior= i.pol==='r'? lo : 1-hi, melhor= i.pol==='r'? 1-hi : lo; return {i,v,pior,melhor}; }).filter(Boolean);
  return {pop,cri:sumP('criancas'),ido:sumP('idosos'),dom:d3.sum(fs,f=>f.properties.dppo||0),inund:d3.sum(fs,f=>f.properties.inund_pop||0),app:d3.sum(fs,f=>f.properties.app_pop||0),
    bad:ev.filter(e=>e.pior>=.6).sort((a,b)=>b.pior-a.pior), good:ev.filter(e=>e.melhor>=.8).sort((a,b)=>b.melhor-a.melhor)};
}
function renderDiag(){
  const el=document.getElementById('lab-diag'); if(!el) return;
  const D0=LAB.diag; if(!D0){ el.innerHTML='<div class="empty eempty">Nenhum território escolhido. Use o botão "Diagnóstico" na tabela ou digite um bairro.</div>'; return; }
  const d=diagOf(D0.fs), sev=pr=>pr>=.8?['crítico','#d73027','#fff']:['atenção','#fc8d59','#1d1d1d'];
  const ods=[...new Set(d.bad.flatMap(e=>IND_ODS[e.i.k]||[]))].sort((a,b)=>a-b);
  el.innerHTML=`<article class="diag"><header><div><span class="xk">Diagnóstico territorial</span><h4>${esc(D0.name)}</h4><span class="mu">${D0.mun||''} · ${D0.fs.length} setor${D0.fs.length>1?'es':''} censitário${D0.fs.length>1?'s':''}</span></div><button class="btn ghost" type="button" id="lab-dmap">Ver no mapa</button></header>
    <div class="dg-pop">${[['Moradores',d.pop],['Crianças 0–9',d.cri],['Idosos 60+',d.ido],['Domicílios',d.dom],['Em suscetibilidade alta a inundação',d.inund],['Em APP',d.app]].map(([a,b])=>`<div><b>${ptBR(fmtN(Math.round(b)))}</b><span>${a}</span></div>`).join('')}</div>
    <div class="dg-cols"><div><h5>Principais questões identificadas</h5>${d.bad.length?`<ul class="dg-l">${d.bad.slice(0,10).map(e=>{ const [t,bg,fg]=sev(e.pior); return `<li><span class="sevb" style="background:${bg};color:${fg}">${t}</span><span>${e.i.n}</span><b>${fv(e.i.k,e.v)}</b><em>pior que ${ptBR(fmtN(100*e.pior))}% dos setores · mediana RMVRC ${fv(e.i.k,d3.quantile(sorted[e.i.k],.5))}</em></li>`; }).join('')}</ul>`:'<p class="mu">Nenhum indicador pior que 60% dos setores da RMVRC.</p>'}</div>
      <div><h5>Situações adequadas</h5>${d.good.length?`<ul class="dg-l">${d.good.slice(0,6).map(e=>`<li><span class="sevb" style="background:#1a9850;color:#fff">adequado</span><span>${e.i.n}</span><b>${fv(e.i.k,e.v)}</b></li>`).join('')}</ul>`:'<p class="mu">Nenhum indicador entre os 20% melhores.</p>'}
      <h5 style="margin-top:12px">ODS relacionados</h5><div class="li-ods">${ods.map(odsBadge).join(' ')||'<span class="mu">—</span>'}</div></div></div>
    <p class="note">Crítico = valor pior que o de pelo menos 80% dos setores da RMVRC; atenção = pior que 60% a 80%; adequado = melhor que pelo menos 80%. Empates (por exemplo, muitos setores com 0%) não contam como pior. População de crianças e idosos estimada pelas porcentagens do Censo 2022 em cada setor.</p></article>`;
  document.getElementById('lab-dmap').onclick=()=>{ goPage('mapa',1); try{history.pushState(null,'','#mapa');}catch(_){} fitTo(D0.fs); st.sel=D0.fs[0].properties.id; renderDetail(); setTimeout(()=>document.querySelector('.mapcard').scrollIntoView({block:'start'}),60); };
}
function renderSim(){
  const el=document.getElementById('lab-sim'); if(!el) return;
  const k=LAB.meta, meta=k==='esgoto'?90:99, i=byK[k];
  const fs=(LAB.scope==='diag'&&LAB.diag)?LAB.diag.fs:labScope();
  const rows=fs.filter(f=>f.properties[k]!=null&&f.properties.dppo>0).map(f=>{ const p=f.properties, att=p[k]/100*p.dppo; return {p,dom:p.dppo,att,falta:p.dppo-att}; });
  const dom=d3.sum(rows,r=>r.dom), att=d3.sum(rows,r=>r.att), cur=dom?100*att/dom:0, alvo=meta/100*dom, gap=Math.max(0,alvo-att);
  const mor=gap*(d3.sum(rows,r=>r.p.pop)/(dom||1));
  const ord=rows.slice().sort((a,b)=>b.falta-a.falta); let acc=0, nset=0; for(const r of ord){ if(acc>=gap) break; acc+=r.falta; nset++; }
  const nome=(LAB.scope==='diag'&&LAB.diag)?LAB.diag.name:document.getElementById('munsel').selectedOptions[0].textContent;
  el.innerHTML=`<div class="simg"><div class="simk"><span class="xk">Situação atual · ${esc(nome)}</span><div class="simbar"><i style="width:${cur.toFixed(1)}%"></i><b style="left:${meta}%"></b></div><div class="simlg"><span><b>${ptBR(fmt1(cur))}%</b> dos domicílios com ${k==='esgoto'?'esgoto em rede':'água da rede geral'}</span><span>meta: <b>${meta}%</b> até 2033</span></div></div>
    <div class="dg-pop">${[['Domicílios no território',dom],['Domicílios atendidos',att],['Domicílios a atender para a meta',gap],['Moradores estimados nesses domicílios',mor],['Setores que bastam (maior déficit primeiro)',gap>0?nset:0]].map(([a,b])=>`<div><b>${ptBR(fmtN(Math.round(b)))}</b><span>${a}</span></div>`).join('')}</div></div>
    ${gap>0?`<div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th>#</th><th class="l">Setor</th><th class="l">Bairro</th><th class="l">Município</th><th>Domicílios</th><th>Atendidos hoje</th><th>Sem atendimento</th><th>Acumulado</th></tr></thead><tbody>${(()=>{ let a=0; return ord.slice(0,Math.min(15,nset)).map((r,j)=>{ a+=r.falta; return `<tr><td class="num">${j+1}</td><td class="l">${r.p.id}</td><td class="l">${esc(r.p.bairro||r.p.dist||'—')}</td><td class="l">${r.p.mun}</td><td class="num">${ptBR(fmtN(r.dom))}</td><td class="num">${ptBR(fmt1(r.p[k]))}%</td><td class="num">${ptBR(fmtN(Math.round(r.falta)))}</td><td class="num">${ptBR(fmt1(100*Math.min(1,a/gap)))}% da meta</td></tr>`; }).join(''); })()}</tbody></table></div><p class="note">Lista dos ${Math.min(15,nset)} primeiros dos ${nset} setores necessários. O Censo mede a ligação à rede, não o tratamento do esgoto; para a meta legal (coleta <i>e</i> tratamento), o valor do Atlas é um limite superior.</p>`:'<p class="note">O território já está acima da meta pela medida do Censo 2022.</p>'}`;
}
function labSetDiag(t){ LAB.diag={name:t.name,mun:t.mun,fs:t.fs}; renderDiag(); renderSim(); document.getElementById('lab-diag').scrollIntoView({behavior:'smooth',block:'start'}); }
document.addEventListener('click',e=>{
  const lb=e.target.closest('.lensb'); if(lb){ LAB.lens=lb.dataset.l; renderLab(); return; }
  if(e.target.id==='lab-map'){ const b=document.getElementById('i-ipt_'+LAB.lens); goPage('mapa',1); try{history.pushState(null,'','#mapa');}catch(_){} if(b) b.click(); setTimeout(()=>document.querySelector('.mapcard').scrollIntoView({block:'start'}),60); return; }
  const u=e.target.closest('#lab-unit button'); if(u){ LAB.unit=u.dataset.u; document.querySelectorAll('#lab-unit button').forEach(x=>x.setAttribute('aria-pressed',x===u)); renderLab(); return; }
  const m=e.target.closest('#lab-meta button'); if(m){ LAB.meta=m.dataset.m; document.querySelectorAll('#lab-meta button').forEach(x=>x.setAttribute('aria-pressed',x===m)); renderSim(); return; }
  const s=e.target.closest('#lab-scope button'); if(s){ LAB.scope=s.dataset.s; document.querySelectorAll('#lab-scope button').forEach(x=>x.setAttribute('aria-pressed',x===s)); renderSim(); return; }
  const d=e.target.closest('.labd'); if(d){ labSetDiag(window.__labT[+d.dataset.i]); return; }
  const mm=e.target.closest('.labm'); if(mm){ const t=window.__labT[+mm.dataset.i]; const b=document.getElementById('i-ipt_'+LAB.lens); goPage('mapa',1); try{history.pushState(null,'','#mapa');}catch(_){} if(b) b.click(); fitTo(t.fs); st.sel=t.fs[0].properties.id; renderDetail(); setTimeout(()=>document.querySelector('.mapcard').scrollIntoView({block:'start'}),60); return; }
});
document.getElementById('lab-q')?.addEventListener('change',e=>{ const val=e.target.value.trim(); if(!val) return; const [b,m]=val.split(' · '); const fs=F.filter(f=>f.properties.bairro&&f.properties.bairro.toLowerCase()===b.toLowerCase()&&(!m||f.properties.mun===m)); if(fs.length) labSetDiag({name:fs[0].properties.bairro,mun:m||fs[0].properties.mun,fs}); else say('Bairro não encontrado. Escolha um nome da lista.'); });
window.__labRefresh=()=>{ if(document.getElementById('lab-b')) renderLab(); };

// ------- PDFs do diagnóstico territorial -------
const pdfTxt=s=>String(s==null?'':s).replace(/<[^>]+>/g,'').replace(/−/g,'-').replace(/≥/g,'>=').replace(/≤/g,'<=').replace(/→/g,'->').replace(/[ -‏ ]/g,' ').replace(/[^\x00-\xff–—“”‘’•…€]/g,'');
function pdfFrame(pdf,title,sub){ const PW=pdf.internal.pageSize.getWidth(), M=34;
  pdf.setFont('helvetica','bold'); pdf.setFontSize(9); pdf.setTextColor(0,32,96); pdf.text('Atlas Socioambiental da RMVRC · PPGAU-UNIVAG',M,M);
  pdf.setFont('helvetica','normal'); pdf.setTextColor(86,96,122); pdf.text(pdfTxt(title),PW-M,M,{align:'right'});
  pdf.setDrawColor(255,192,0); pdf.setLineWidth(1.6); pdf.line(M,M+6,PW-M,M+6); return M+22; }
function pdfFoot(pdf,extra){ const PW=pdf.internal.pageSize.getWidth(), PH=pdf.internal.pageSize.getHeight(), M=34, n=pdf.internal.getNumberOfPages();
  for(let i=1;i<=n;i++){ pdf.setPage(i); pdf.setFont('helvetica','normal'); pdf.setFontSize(7.5); pdf.setTextColor(86,96,122);
    pdf.text(pdfTxt(`Elaboração: Prof. Dr. Ricardo Miranda dos Santos e Profa. Dra. Sandra Medina Benini · gerado em ${hoje()}${extra?' · '+extra:''}`),M,PH-18); pdf.text(`página ${i} de ${n}`,PW-M,PH-18,{align:'right'}); } }
function pdfTable(pdf,cols,rows,y0,title,sub){ // cols: [rótulo, alinhamento 'l'|'r', largura máx]; texto longo quebra em linhas
  const PW=pdf.internal.pageSize.getWidth(), PH=pdf.internal.pageSize.getHeight(), M=34, FS=7.6, LH=9.4, avail=PW-2*M;
  pdf.setFont('helvetica','bold'); pdf.setFontSize(FS); const mw=cols.map(c=>Math.max(...pdfTxt(c[0]).split(/\s+/).map(s=>pdf.getTextWidth(s)))+9);
  pdf.setFont('helvetica','normal'); let w=cols.map((c,k)=>Math.max(mw[k],Math.min(c[2]||160,Math.max(...rows.map(r=>pdf.getTextWidth(pdfTxt(r[k]))+9),0))));
  let tot=w.reduce((a,b)=>a+b,0); if(tot<avail){ const flex=cols.map(c=>c[3]?1:0), nf=flex.reduce((a,b)=>a+b,0); if(nf) w=w.map((x,k)=>x+(flex[k]?(avail-tot)/nf:0)); else w=w.map(x=>x*avail/tot); }
  else { const ex=w.map((x,k)=>x-mw[k]), te=ex.reduce((a,b)=>a+b,0), need=tot-avail; w=w.map((x,k)=>x-(te?ex[k]/te*need:0)); }
  let y=y0;
  const head=()=>{ pdf.setFont('helvetica','bold'); pdf.setFontSize(FS); pdf.setTextColor(15,29,58); const hl=cols.map((c,k)=>pdf.splitTextToSize(pdfTxt(c[0]),w[k]-6)); const hh=Math.max(...hl.map(l=>l.length))*LH+4;
    pdf.setFillColor(227,233,246); pdf.rect(M,y-2,avail,hh,'F'); let x=M; hl.forEach((l,k)=>{ const al=cols[k][1]!=='r'; pdf.text(l,al?x+3:x+w[k]-3,y+LH-2,{align:al?'left':'right'}); x+=w[k]; }); y+=hh+2; pdf.setFont('helvetica','normal'); };
  head();
  rows.forEach((r,j)=>{ pdf.setFontSize(FS); const ls=r.map((v,k)=>pdf.splitTextToSize(pdfTxt(v),w[k]-6)); const rh=Math.max(...ls.map(l=>l.length))*LH+3;
    if(y+rh>PH-34){ pdf.addPage(); y=pdfFrame(pdf,title,sub); head(); }
    if(j%2){ pdf.setFillColor(244,246,250); pdf.rect(M,y-1,avail,rh,'F'); }
    pdf.setTextColor(15,29,58); let x=M; ls.forEach((l,k)=>{ const al=cols[k][1]!=='r'; pdf.text(l,al?x+3:x+w[k]-3,y+LH-2,{align:al?'left':'right'}); x+=w[k]; }); y+=rh; });
  return y;
}
async function diagPDF(kind){
  const btns=document.querySelectorAll('#lab-pdfpop button'); btns.forEach(b=>b.disabled=true); say('Gerando PDF…',0);
  try{
    await window.__loadJsPDF(); const {jsPDF}=window.jspdf; const recorte=filtroTxt();
    if(kind==='sel'){
      const D0=LAB.diag; if(!D0){ say('Escolha um território antes.'); return; }
      const d=diagOf(D0.fs), pdf=new jsPDF({unit:'pt',format:'a4',compress:true}), PW=pdf.internal.pageSize.getWidth(), PH=pdf.internal.pageSize.getHeight(), M=34, T='Diagnóstico territorial';
      let y=pdfFrame(pdf,T);
      const need=h=>{ if(y+h>PH-34){ pdf.addPage(); y=pdfFrame(pdf,T); } };
      const h1=t=>{ need(30); y+=8; pdf.setFont('helvetica','bold'); pdf.setFontSize(10.5); pdf.setTextColor(0,32,96); pdf.text(pdfTxt(t),M,y); y+=12; };
      pdf.setFont('helvetica','bold'); pdf.setFontSize(18); pdf.setTextColor(15,29,58); const tl=pdf.splitTextToSize(pdfTxt(D0.name),PW-2*M); pdf.text(tl,M,y+8); y+=tl.length*20+2;
      pdf.setFont('helvetica','normal'); pdf.setFontSize(9.5); pdf.setTextColor(86,96,122); pdf.text(pdfTxt(`${D0.mun||''} · ${D0.fs.length} setor(es) censitário(s) · Censo 2022 e camadas do Atlas`),M,y+4); y+=16;
      h1('População afetada');
      const pp=[['Moradores',d.pop],['Crianças 0–9',d.cri],['Idosos 60+',d.ido],['Domicílios',d.dom],['Em suscetibilidade alta a inundação',d.inund],['Em APP',d.app]], bw=(PW-2*M-5*6)/6;
      pp.forEach(([a,b],k)=>{ const x=M+k*(bw+6); pdf.setDrawColor(217,223,235); pdf.setLineWidth(.8); pdf.roundedRect(x,y,bw,40,4,4,'S'); pdf.setFont('helvetica','bold'); pdf.setFontSize(13); pdf.setTextColor(15,29,58); pdf.text(ptBR(fmtN(Math.round(b))),x+6,y+16); pdf.setFont('helvetica','normal'); pdf.setFontSize(7.2); pdf.setTextColor(86,96,122); pdf.text(pdf.splitTextToSize(pdfTxt(a),bw-10),x+6,y+27); }); y+=50;
      h1(`Principais questões identificadas (${d.bad.length})`);
      if(d.bad.length) y=pdfTable(pdf,[['Classe','l',52],['Indicador','l',230,1],['Valor','r',70],['Pior que … dos setores','r',70],['Mediana RMVRC','r',80]],d.bad.map(e=>[e.pior>=.8?'CRÍTICO':'ATENÇÃO',e.i.n,fv(e.i.k,e.v),ptBR(fmtN(100*e.pior))+'%',fv(e.i.k,d3.quantile(sorted[e.i.k],.5))]),y,T)+4;
      else { pdf.setFont('helvetica','normal'); pdf.setFontSize(9); pdf.setTextColor(86,96,122); pdf.text('Nenhum indicador pior que 60% dos setores da RMVRC.',M,y+4); y+=14; }
      h1(`Situações adequadas (${d.good.length})`);
      if(d.good.length) y=pdfTable(pdf,[['Indicador','l',300,1],['Valor','r',80],['Melhor que … dos setores','r',90],['Mediana RMVRC','r',80]],d.good.map(e=>[e.i.n,fv(e.i.k,e.v),ptBR(fmtN(100*e.melhor))+'%',fv(e.i.k,d3.quantile(sorted[e.i.k],.5))]),y,T)+4;
      h1('Índice de Prioridade Territorial (IPT) por objetivo de política');
      const lr=LENS.map(L=>{ const k='ipt_'+L.k, fs=D0.fs.filter(f=>f.properties[k]!=null); if(!fs.length) return [L.n,'sem dado','—',L.c.map(c=>lensName(c[0])).join('; ')];
        const pop=d3.sum(fs,f=>f.properties.pop), R=robustez(L); return [L.n,ptBR(fmt1(d3.sum(fs,f=>f.properties[k]*f.properties.pop)/pop)),ptBR(fmtN(100*d3.sum(fs,f=>(R[f.properties.id]||0)*f.properties.pop)/pop))+'%',L.c.map(c=>lensName(c[0])).join('; ')]; });
      y=pdfTable(pdf,[['Objetivo','l',120],['IPT (0–100)','r',50],['Robustez','r',50],['Indicadores do objetivo','l',300,1]],lr,y,T)+4;
      const ods=[...new Set(d.bad.flatMap(e=>IND_ODS[e.i.k]||[]))].sort((a,b)=>a-b);
      h1('ODS relacionados às questões identificadas');
      pdf.setFont('helvetica','normal'); pdf.setFontSize(9); pdf.setTextColor(15,29,58); const ol=pdf.splitTextToSize(pdfTxt(ods.length?ods.map(n=>`ODS ${n} – ${ODS.find(o=>o.n===n).t}`).join('; ')+'.':'—'),PW-2*M); need(ol.length*11+6); pdf.text(ol,M,y); y+=ol.length*11+6;
      const nt=pdf.splitTextToSize(pdfTxt('Critérios: crítico = valor pior que o de pelo menos 80% dos setores da RMVRC; atenção = pior que 60% a 80%; adequado = melhor que pelo menos 80%; empates não contam como pior. Valor do território agregado pelas regras do Atlas (média ponderada por domicílios, moradores ou área, conforme o indicador). Crianças e idosos estimados pelas porcentagens do Censo 2022 em cada setor. IPT e robustez: ver Metodologia, item 11. Fontes: IBGE, Censo Demográfico 2022; SGB/CPRM; ANA/UFRGS (ANADEM); Copernicus Sentinel-2; USGS Landsat 9; MapBiomas; OpenStreetMap; CNES/DATASUS.'),PW-2*M);
      need(nt.length*9.5+10); pdf.setFontSize(7.8); pdf.setTextColor(86,96,122); pdf.text(nt,M,y+6);
      pdfFoot(pdf); await saveFile('diagnostico_'+D0.name.toLowerCase().normalize('NFD').replace(/[^a-z0-9]+/g,'_').slice(0,40)+'.pdf',pdf.output('blob'));
    } else {
      const G=new Map(); for(const f of labScope()){ const p=f.properties, nm=p.bairro||''; if(!nm) continue; const key=p.mun+'|'+nm; (G.get(key)||G.set(key,[]).get(key)).push(f); }
      const rows=[...G].map(([key,fs])=>{ const [mun,nm]=key.split('|'), d=diagOf(fs), cr=d.bad.filter(e=>e.pior>=.8), at=d.bad.filter(e=>e.pior<.8);
        return {mun,nm,r:[nm,mun,String(fs.length),ptBR(fmtN(d.pop)),ptBR(fmtN(Math.round(d.cri))),ptBR(fmtN(Math.round(d.ido))),ptBR(fmtN(d.dom)),String(cr.length),String(at.length),cr.map(e=>e.i.n).join('; ')||'—',[...new Set(d.bad.flatMap(e=>IND_ODS[e.i.k]||[]))].sort((a,b)=>a-b).join(', ')||'—']}; })
        .sort((a,b)=>a.mun.localeCompare(b.mun,'pt')||a.nm.localeCompare(b.nm,'pt'));
      const pdf=new jsPDF({unit:'pt',format:'a4',orientation:'landscape',compress:true}), T='Diagnóstico territorial · lista completa dos bairros · '+recorte;
      let y=pdfFrame(pdf,T); pdf.setFont('helvetica','bold'); pdf.setFontSize(14); pdf.setTextColor(15,29,58); pdf.text('Diagnóstico territorial: lista completa dos bairros',34,y+4); y+=18;
      pdf.setFont('helvetica','normal'); pdf.setFontSize(8.5); pdf.setTextColor(86,96,122); const it=pdf.splitTextToSize(pdfTxt(`${rows.length} bairros com nome na malha do IBGE · recorte: ${recorte} · ordem alfabética por município. Críticas = indicadores com valor pior que o de pelo menos 80% dos setores da RMVRC; atenção = pior que 60% a 80%. Setores sem nome de bairro no IBGE não entram nesta lista.`),pdf.internal.pageSize.getWidth()-68); pdf.text(it,34,y); y+=it.length*10+6;
      pdfTable(pdf,[['Bairro','l',130],['Município','l',90],['Setores','r',34],['Moradores','r',46],['Crianças 0–9','r',44],['Idosos 60+','r',40],['Domicílios','r',46],['Críticas','r',36],['Atenção','r',36],['Questões críticas','l',300,1],['ODS','l',60]],rows.map(x=>x.r),y,T);
      pdfFoot(pdf,rows.length+' bairros'); await saveFile('diagnostico_bairros_rmvrc.pdf',pdf.output('blob'));
    }
  }catch(e){ console.error(e); say('Não foi possível gerar o PDF.'); }
  finally{ btns.forEach(b=>b.disabled=false); syncPdfPop(); }
}
function syncPdfPop(){ const s=document.getElementById('lab-pdf-sel'); if(!s) return; const D0=LAB.diag; s.disabled=!D0; s.querySelector('span').textContent=D0?D0.name+(D0.mun?' · '+D0.mun:''):'escolha um território primeiro';
  const nb=new Set(labScope().filter(f=>f.properties.bairro).map(f=>f.properties.mun+'|'+f.properties.bairro)).size; document.querySelector('#lab-pdf-all span').textContent=ptBR(fmtN(nb))+' bairros do recorte selecionado no topo'; }
document.addEventListener('click',e=>{
  const pop=document.getElementById('lab-pdfpop'); if(!pop) return;
  if(e.target.closest('#lab-pdfbtn')){ pop.hidden=!pop.hidden; if(!pop.hidden) syncPdfPop(); return; }
  if(e.target.closest('#lab-pdf-x')){ pop.hidden=true; return; }
  const s=e.target.closest('#lab-pdf-sel'); if(s&&!s.disabled){ diagPDF('sel'); return; }
  if(e.target.closest('#lab-pdf-all')){ diagPDF('all'); return; }
  if(!pop.hidden&&!e.target.closest('#lab-pdfpop')) pop.hidden=true;
});

// ------- PDFs do simulador de metas -------
function simData(){ const k=LAB.meta, meta=k==='esgoto'?90:99; const fs=(LAB.scope==='diag'&&LAB.diag)?LAB.diag.fs:labScope();
  const rows=fs.filter(f=>f.properties[k]!=null&&f.properties.dppo>0).map(f=>{ const p=f.properties, att=p[k]/100*p.dppo; return {p,dom:p.dppo,att,falta:p.dppo-att}; });
  const dom=d3.sum(rows,r=>r.dom), att=d3.sum(rows,r=>r.att), gap=Math.max(0,meta/100*dom-att); const ord=rows.slice().sort((a,b)=>b.falta-a.falta); let acc=0,nset=0; for(const r of ord){ if(acc>=gap) break; acc+=r.falta; nset++; }
  const nome=(LAB.scope==='diag'&&LAB.diag)?LAB.diag.name:document.getElementById('munsel').selectedOptions[0].textContent;
  return {k,meta,rows,dom,att,gap,ord,nset,nome,lab:k==='esgoto'?'esgoto em rede':'água da rede geral'}; }
async function simPDF(kind){
  const btns=document.querySelectorAll('#sim-pdfpop button'); btns.forEach(b=>b.disabled=true); say('Gerando PDF…',0);
  try{ await window.__loadJsPDF(); const {jsPDF}=window.jspdf, S=simData(); const pdf=new jsPDF({unit:'pt',format:'a4',orientation:'landscape',compress:true}), PW=pdf.internal.pageSize.getWidth();
    const T=`Simulador de metas · ${S.lab} · meta ${S.meta}% · ${S.nome}`; let y=pdfFrame(pdf,T);
    pdf.setFont('helvetica','bold'); pdf.setFontSize(14); pdf.setTextColor(15,29,58); pdf.text(pdfTxt(`Simulador de metas de saneamento: ${S.lab} (meta de ${S.meta}% até 2033)`),34,y+4); y+=18;
    pdf.setFont('helvetica','normal'); pdf.setFontSize(9); pdf.setTextColor(15,29,58);
    const res=pdf.splitTextToSize(pdfTxt(`Território: ${S.nome} (${filtroTxt()}). Situação atual: ${ptBR(fmt1(S.dom?100*S.att/S.dom:0))}% dos ${ptBR(fmtN(S.dom))} domicílios com ${S.lab} (${ptBR(fmtN(Math.round(S.att)))} atendidos). Domicílios a atender para a meta: ${ptBR(fmtN(Math.round(S.gap)))}. Setores que bastam, do maior para o menor déficit: ${S.gap>0?ptBR(fmtN(S.nset)):0}.`),PW-68); pdf.text(res,34,y); y+=res.length*11+2;
    pdf.setFontSize(8); pdf.setTextColor(86,96,122); const nt=pdf.splitTextToSize(pdfTxt('Cálculo de distância até a meta, não previsão de efeitos. Domicílios atendidos = cobertura do setor x domicílios particulares permanentes ocupados (Censo 2022). O Censo mede a ligação à rede, não o tratamento do esgoto; para a meta legal (Lei nº 14.026/2020), a cobertura do Atlas é um limite superior.'),PW-68); pdf.text(nt,34,y); y+=nt.length*9.5+6;
    if(kind==='bairros'){
      const G=new Map(); for(const r of S.rows){ const p=r.p, key=p.mun+'|'+(p.bairro||(p.dist?p.dist+' (distrito, sem bairro no IBGE)':'(sem bairro)')); const g=G.get(key)||G.set(key,{dom:0,att:0,pop:0,n:0}).get(key); g.dom+=r.dom; g.att+=r.att; g.pop+=p.pop; g.n++; }
      const L=[...G].map(([key,g])=>{ const [mun,nm]=key.split('|'), falta=g.dom-g.att, gapb=Math.max(0,S.meta/100*g.dom-g.att); return {mun,nm,g,falta,gapb}; }).sort((a,b)=>b.falta-a.falta);
      let acc=0; const rows=L.map((x,i)=>{ acc+=x.falta; return [String(i+1),x.nm,x.mun,String(x.g.n),ptBR(fmtN(x.g.dom)),ptBR(fmt1(x.g.dom?100*x.g.att/x.g.dom:0))+'%',ptBR(fmtN(Math.round(x.falta))),ptBR(fmtN(Math.round(x.gapb))),ptBR(fmtN(Math.round(x.gapb*(x.g.pop/(x.g.dom||1))))),S.gap>0?ptBR(fmt1(100*Math.min(1,acc/S.gap)))+'%':'—']; });
      pdfTable(pdf,[['#','r',26],['Bairro','l',190,1],['Município','l',110],['Setores','r',40],['Domicílios','r',54],['Cobertura atual','r',56],['Domicílios sem atendimento','r',70],['Faltam para a meta no bairro','r',74],['Moradores estimados nesses domicílios','r',80],['Acumulado do déficit do território','r',78]],rows,y,T);
      pdfFoot(pdf,rows.length+' bairros, do maior para o menor número de domicílios sem atendimento'); await saveFile(`simulador_${S.k}_bairros.pdf`,pdf.output('blob'));
    } else {
      let acc=0; const rows=S.ord.slice(0,S.gap>0?S.nset:0).map((r,i)=>{ acc+=r.falta; return [String(i+1),r.p.id,r.p.bairro||r.p.dist||'—',r.p.mun,ptBR(fmtN(r.dom)),ptBR(fmt1(r.p[S.k]))+'%',ptBR(fmtN(Math.round(r.falta))),ptBR(fmt1(100*Math.min(1,acc/S.gap)))+'% da meta']; });
      if(!rows.length){ pdf.setFontSize(10); pdf.setTextColor(15,29,58); pdf.text('O território já está acima da meta pela medida do Censo 2022.',34,y+8); }
      else pdfTable(pdf,[['#','r',30],['Setor censitário','l',110],['Bairro','l',200,1],['Município','l',130],['Domicílios','r',60],['Atendidos hoje','r',64],['Sem atendimento','r',70],['Acumulado','r',84]],rows,y,T);
      pdfFoot(pdf,rows.length+' setores'); await saveFile(`simulador_${S.k}_setores.pdf`,pdf.output('blob'));
    }
  }catch(e){ console.error(e); say('Não foi possível gerar o PDF.'); }
  finally{ btns.forEach(b=>b.disabled=false); }
}
document.addEventListener('click',e=>{
  const pop=document.getElementById('sim-pdfpop'); if(!pop) return;
  if(e.target.closest('#sim-pdfbtn')){ pop.hidden=!pop.hidden; if(!pop.hidden){ const S=simData(); const nb=new Set(S.rows.map(r=>r.p.mun+'|'+(r.p.bairro||r.p.dist||''))).size; document.querySelector('#sim-pdf-bairros span').textContent=`${ptBR(fmtN(nb))} bairros · ${S.nome}`; document.querySelector('#sim-pdf-setores span').textContent=`${S.gap>0?ptBR(fmtN(S.nset)):0} setores · ${S.lab}, meta ${S.meta}%`; } return; }
  if(e.target.closest('#sim-pdf-x')){ pop.hidden=true; return; }
  if(e.target.closest('#sim-pdf-bairros')){ simPDF('bairros'); return; }
  if(e.target.closest('#sim-pdf-setores')){ simPDF('setores'); return; }
  if(!pop.hidden&&!e.target.closest('#sim-pdfpop')) pop.hidden=true;
});

// ------- PDFs do mapa de prioridades -------
const UNITN={bairro:'bairros',micro:'microbacias',setor:'setores',mun:'municípios'};
async function rankPDF(kind){
  const btns=document.querySelectorAll('#rk-pdfpop button'); btns.forEach(b=>b.disabled=true); say('Gerando PDF…',0);
  try{ await window.__loadJsPDF(); const {jsPDF}=window.jspdf, L=LENS.find(x=>x.k===LAB.lens), u=LAB.unit, pdf=new jsPDF({unit:'pt',format:'a4',orientation:'landscape',compress:true}), PW=pdf.internal.pageSize.getWidth();
    const intro=(t,txt)=>{ let y=pdfFrame(pdf,T); pdf.setFont('helvetica','bold'); pdf.setFontSize(14); pdf.setTextColor(15,29,58); pdf.text(pdfTxt(t),34,y+4); y+=18; pdf.setFont('helvetica','normal'); pdf.setFontSize(8.5); pdf.setTextColor(86,96,122); const it=pdf.splitTextToSize(pdfTxt(txt),PW-68); pdf.text(it,34,y); return y+it.length*10+6; };
    let T;
    if(kind==='lens'){
      const TT=territories(L,u); T=`Mapa de prioridades · ${L.n} · ${UNITN[u]} · ${filtroTxt()}`;
      const y=intro(`Prioridade territorial: ${L.n}`,`${TT.length} ${UNITN[u]} em ordem de prioridade · recorte: ${filtroTxt()}. Indicadores do objetivo (pesos iguais): ${L.c.map(c=>lensName(c[0])).join('; ')}. IPT de 0 (menor prioridade) a 100 (maior); no território, média dos setores ponderada pelos moradores. Robustez = % de 300 combinações aleatórias de pesos em que o território fica entre os 20% de maior prioridade (robusta >= 80%; moderada 50% a 80%; sensível aos pesos < 50%). Principais déficits = indicadores com nota normalizada média >= 0,6. Setores com menos de 50 moradores ou sem os dados do objetivo ficam fora.`);
      const cols=[['#','r',28],['Território','l',210,1],...(u==='mun'?[]:[['Município','l',110]]),...(u==='setor'||u==='mun'?[]:[['Setores','r',38]]),['Moradores','r',54],['IPT','r',36],['Robustez','r',46],['Classe de robustez','l',84],['Principais déficits','l',260,1]];
      const rows=TT.map((t,i)=>[String(i+1),t.name,...(u==='mun'?[]:[t.mun]),...(u==='setor'||u==='mun'?[]:[String(t.n)]),ptBR(fmtN(t.pop)),ptBR(fmt1(t.ipt)),ptBR(fmtN(100*t.rob))+'%',t.rob>=.8?'robusta':t.rob>=.5?'moderada':'sensível aos pesos',t.top.join('; ')||'—']);
      pdfTable(pdf,cols,rows,y,T); pdfFoot(pdf,`${rows.length} ${UNITN[u]}`); await saveFile(`prioridades_${L.k}_${u}.pdf`,pdf.output('blob'));
    } else {
      T=`Mapa de prioridades · quadro dos 9 objetivos · ${UNITN[u]} · ${filtroTxt()}`;
      const G=new Map(); for(const f of labScope()){ const g=groupKey(f.properties,u); if(g==null) continue; (G.get(g)||G.set(g,[]).get(g)).push(f); }
      const TT=[...G].map(([key,fs])=>{ const v=LENS.map(X=>{ const k='ipt_'+X.k, a=fs.filter(f=>f.properties[k]!=null); if(!a.length) return null; const pop=d3.sum(a,f=>f.properties.pop); return d3.sum(a,f=>f.properties[k]*f.properties.pop)/pop; });
        return {name:groupName(key,u,fs),mun:u==='mun'?'':fs[0].properties.mun,pop:d3.sum(fs,f=>f.properties.pop||0),v}; }).filter(t=>t.v.some(x=>x!=null));
      const li=LENS.findIndex(x=>x.k===L.k); TT.sort((a,b)=>(b.v[li]??-1)-(a.v[li]??-1));
      const y=intro('Prioridade territorial: quadro comparativo dos 9 objetivos',`${TT.length} ${UNITN[u]} · recorte: ${filtroTxt()} · ordenado pelo objetivo "${L.n}". Cada coluna é o IPT (0 a 100) do território naquele objetivo; "—" = sem dado suficiente (menos de 60% dos indicadores do objetivo). Os objetivos usam indicadores e escalas próprios: compare territórios dentro da mesma coluna, não colunas entre si.`);
      const cols=[['#','r',26],['Território','l',180,1],...(u==='mun'?[]:[['Município','l',96]]),['Moradores','r',50],...LENS.map(X=>[X.n,'r',62])];
      const rows=TT.map((t,i)=>[String(i+1),t.name,...(u==='mun'?[]:[t.mun]),ptBR(fmtN(t.pop)),...t.v.map(x=>x==null?'—':ptBR(fmt1(x)))]);
      pdfTable(pdf,cols,rows,y,T); pdfFoot(pdf,`${rows.length} ${UNITN[u]}`); await saveFile(`prioridades_9_objetivos_${u}.pdf`,pdf.output('blob'));
    }
  }catch(e){ console.error(e); say('Não foi possível gerar o PDF.'); }
  finally{ btns.forEach(b=>b.disabled=false); }
}
document.addEventListener('click',e=>{
  const pop=document.getElementById('rk-pdfpop'); if(!pop) return;
  if(e.target.closest('#rk-pdfbtn')){ pop.hidden=!pop.hidden; if(!pop.hidden){ const L=LENS.find(x=>x.k===LAB.lens), n=(window.__labT||[]).length; document.querySelector('#rk-pdf-lens span').textContent=`${L.n} · ${ptBR(fmtN(n))} ${UNITN[LAB.unit]}`; document.querySelector('#rk-pdf-all span').textContent=`${UNITN[LAB.unit]} do recorte selecionado no topo`; } return; }
  if(e.target.closest('#rk-pdf-x')){ pop.hidden=true; return; }
  if(e.target.closest('#rk-pdf-lens')){ rankPDF('lens'); return; }
  if(e.target.closest('#rk-pdf-all')){ rankPDF('all'); return; }
  if(!pop.hidden&&!e.target.closest('#rk-pdfpop')) pop.hidden=true;
});
