// ------- ODS e saúde ambiental -------
const ODS=[
 {n:1, c:'#E5243B', t:'Erradicação da pobreza', metas:['1.2 Reduzir a pobreza em todas as dimensões','1.4 Acesso a serviços básicos'], ks:['renda','agua','esgoto','lixo']},
 {n:3, c:'#4C9F38', t:'Saúde e bem-estar', metas:['3.3 Combater doenças transmitidas pela água e por vetores','3.8 Acesso a serviços de saúde','3.9 Reduzir doenças por contaminação da água, do ar e do solo'], ks:['d_ubs','d_saude'], sd:['drsai_tx','resp_tx','deng_tx']},
 {n:4, c:'#C5192D', t:'Educação de qualidade', metas:['4.6 Alfabetização de jovens e adultos','4.a Instalações educacionais acessíveis'], ks:['analf','d_esc']},
 {n:6, c:'#26BDE2', t:'Água potável e saneamento', metas:['6.1 Água potável segura para todos','6.2 Saneamento e higiene adequados','6.3 Reduzir esgoto sem tratamento'], ks:['agua','agua_enc','esgoto','esg_prec','sem_banh']},
 {n:10, c:'#DD1367', t:'Redução das desigualdades', metas:['10.2 Inclusão social, econômica e política de todos'], ks:['ivsa','negros','renda']},
 {n:11, c:'#FD9D24', t:'Cidades e comunidades sustentáveis', metas:['11.1 Moradia adequada e urbanização de favelas','11.2 Transporte público acessível','11.5 Reduzir pessoas afetadas por desastres, inclusive os ligados à água','11.6 Gestão de resíduos','11.7 Espaços públicos e verdes seguros e acessíveis'], ks:['pav','calcada','bueiro','luz','onibus','lixo','arvore','d_parque','verde_hab','inund_pop','sgb_alta_pop']},
 {n:13, c:'#3F7E44', t:'Ação contra a mudança global do clima', metas:['13.1 Resiliência e adaptação a riscos climáticos e desastres naturais'], ks:['inund','sgb_alta','a1974','alerta','lst','lst_anom']},
 {n:15, c:'#56C02B', t:'Vida terrestre', metas:['15.1 Conservação dos ecossistemas terrestres e de água doce','15.3 Combater a degradação do solo'], ks:['veg_nat','verde','app_pct','erosao','eros_alta']}
];
const SD_IND={drsai_tx:{n:'Internações por DRSAI',u:'por 10 mil hab./ano',pol:'r',f:v=>ptBR(fmt1(v))},resp_tx:{n:'Internações respiratórias',u:'por 10 mil hab./ano',pol:'r',f:v=>ptBR(fmt1(v))},asma_tx:{n:'Pneumonia, asma e DPOC',u:'por 10 mil hab./ano',pol:'r',f:v=>ptBR(fmt1(v))},deng_tx:{n:'Dengue (casos prováveis)',u:'por 100 mil hab./ano',pol:'r',f:v=>ptBR(fmtN(v))}};
const odsTxt=n=>[6,11,15].includes(n)?'#10202a':'#fff';
function odsBadge(n){ const o=ODS.find(x=>x.n===n); return `<span class="odsb" style="background:${o.c};color:${odsTxt(n)}" title="ODS ${n} · ${o.t}">ODS ${n}</span>`; }
const IND_ODS={}; ODS.forEach(o=>o.ks.forEach(k=>{ (IND_ODS[k]=IND_ODS[k]||[]).push(o.n); }));
function munVal(k,mun){ const fs=F.filter(f=>f.properties.sit==='Urbana'&&(mun==='RMVRC'||f.properties.mun===mun)); const i=byK[k]; if(!i) return null; if(i.w!=='vhab'&&!fs.some(f=>f.properties[k]!=null)) return null; if(i.w==='vhab'&&!fs.some(f=>f.properties.verde!=null)) return null; return agg(fs,i); }
function sdVal(k,mun){ if(mun==='RMVRC') return SAUDE.tot[k]; const m=SAUDE.mun.find(x=>x.mun===mun); return m?m[k]:null; }
function renderODS(){
  const el=document.getElementById('ods-cards'); if(!el) return;
  el.innerHTML=ODS.map(o=>{
    const rows=o.ks.filter(k=>byK[k]).map(k=>{ const i=byK[k]; return `<li><button class="odsi" data-k="${k}" title="Ver no mapa">${i.n}</button><span class="num">${fv(k,munVal(k,'RMVRC'))}</span></li>`; }).join('')
      + (o.sd||[]).map(k=>`<li><span class="odsi nd">${SD_IND[k].n}</span><span class="num">${SD_IND[k].f(SAUDE.tot[k])} <small>${SD_IND[k].u}</small></span></li>`).join('');
    return `<article class="odsc"><header style="--oc:${o.c}"><b style="background:${o.c};color:${odsTxt(o.n)}">${o.n}</b><div><span class="xk">ODS ${o.n}</span><h4>${o.t}</h4></div></header>
      <div class="odsm">${o.metas.map(m=>`<span>${m}</span>`).join('')}</div>
      <ul class="odsl">${rows}</ul><div class="odsf">valor da área urbana da RMVRC · clique no nome para ver no mapa</div></article>`; }).join('');
  el.addEventListener('click',e=>{ const b=e.target.closest('button.odsi'); if(!b) return; const mb=document.getElementById('i-'+b.dataset.k); if(mb){ goPage('mapa'); mb.click(); try{history.pushState(null,'','#mapa');}catch(_){} setTimeout(()=>document.querySelector('.mapcard').scrollIntoView({block:'start'}),60); } });
  // painel por município
  const MS=['RMVRC',...MUNS], ab={'Nossa Senhora do Livramento':'N. S. do<br>Livramento','Santo Antônio de Leverger':'S. A. de<br>Leverger','Chapada dos Guimarães':'Chapada dos<br>Guimarães','Várzea Grande':'Várzea<br>Grande','Campo Verde':'Campo<br>Verde'};
  const LIN=[[6,'agua',99],[6,'esgoto',90],[6,'esg_prec'],[1,'renda'],[4,'analf'],[10,'ivsa'],[11,'pav'],[11,'bueiro'],[11,'lixo'],[11,'verde_hab'],[11,'d_parque'],[11,'inund_pop'],[13,'lst'],[15,'veg_nat'],[15,'eros_alta'],[3,'d_ubs'],[3,'sd:drsai_tx'],[3,'sd:resp_tx'],[3,'sd:deng_tx']];
  let h=`<thead><tr><th class="l">ODS</th><th class="l">Indicador</th><th>Meta</th>${MS.map(m=>`<th>${ab[m]||m}</th>`).join('')}</tr></thead><tbody>`;
  for(const [n,k,meta] of LIN){
    const sd=k.startsWith('sd:'), kk=sd?k.slice(3):k, def=sd?SD_IND[kk]:byK[kk]; if(!def) continue;
    const vals=MS.map(m=>sd?sdVal(kk,m):munVal(kk,m));
    const mv=vals.slice(1).map((v,j)=>[v,j]).filter(x=>x[0]!=null);
    const srt=mv.slice().sort((a,b)=>a[0]-b[0]); const cls={};
    srt.forEach((x,r)=>{ let q=srt.length>1?r/(srt.length-1):.5; if(def.pol==='b') q=1-q; cls[x[1]]=Math.min(4,Math.floor((1-q)*4.999)); });
    const sum=kk==='inund_pop';
    h+=`<tr><td class="l">${odsBadge(n)}</td><td class="l">${def.n}${sd?` <small class="mu">${def.u}</small>`:''}</td><td class="num">${meta?meta+'%':'—'}</td>`+
      vals.map((v,j)=>{ const txt=v==null?'—':(sd?def.f(v):fv(kk,v)); if(j===0) return `<td class="num rm">${txt}</td>`;
        const c=cls[j-1]; const bg=c==null?'var(--panel-2)':ECOL[c]; const fg=c==null?'var(--muted)':(c===0||c===4?'#fff':'#1d1d1d');
        return `<td class="num oc" style="background:${bg};color:${fg}">${txt}</td>`; }).join('')+'</tr>';
  }
  document.getElementById('ods-tab').innerHTML=h+'</tbody>';
  odsBadges();
}
function odsBadges(){
  document.querySelectorAll('.dcard[data-k]').forEach(d=>{ const ns=IND_ODS[d.dataset.k]; if(!ns) return; const s=d.querySelector('summary'); if(s.querySelector('.odsb')) return; s.insertAdjacentHTML('beforeend','<span class="odsw">'+ns.map(odsBadge).join(' ')+'</span>'); });
}
const SDK={drsai:{n:'Internações por DRSAI',f:1e4,u:'por 10 mil hab.',d:1},resp:{n:'Internações respiratórias',f:1e4,u:'por 10 mil hab.',d:1},asma:{n:'Pneumonia, asma e DPOC',f:1e4,u:'por 10 mil hab.',d:1},deng:{n:'Dengue, casos prováveis',f:1e5,u:'por 100 mil hab.',d:0},all:{n:'Todas as internações no SUS',f:1e4,u:'por 10 mil hab.',d:0}};
const SDA={drsai:'anos_drsai',resp:'anos_resp',asma:'anos_asma',deng:'anos_deng',all:'anos_all'};
const sdFmt=(k,v)=>v==null?'—':(SDK[k].d?ptBR(fmt1(v)):ptBR(fmtN(v)));
const sdPct=v=>(v>0?'+':v<0?'−':'')+ptBR(fmtN(Math.abs(v)))+'%';
function sdCount(k,m,p){ const a=m?m[SDA[k]]:SAUDE.tot.anos[k]; return p==='m'?d3.mean(a):a[p]; }
function sdRate(k,m,p){ const pop=m?m.pop:SAUDE.tot.pop; return sdCount(k,m,p)/pop*SDK[k].f; }
let SDP='m', SDI='drsai';
function renderSaude(){
  const k=document.getElementById('sd-kpi'); if(!k) return;
  const per=SDP==='m'?'média 2023–2025':String(2023+SDP);
  k.innerHTML=['drsai','resp','asma','deng'].map(c=>{ const v=sdCount(c,null,SDP), r=sdRate(c,null,SDP), r0=sdRate(c,null,0), r2=sdRate(c,null,2), dv=100*(r2-r0)/r0;
    return `<div class="kpi"><div class="lab">${SDK[c].n}</div><div class="val">${ptBR(fmtN(v))}${SDP==='m'?'/ano':''}</div><div class="sub">${sdFmt(c,r)} ${SDK[c].u} · ${per}</div><div class="sub">2023 → 2025: <b>${sdPct(dv)}</b></div></div>`; }).join('');
  document.getElementById('sd-tab-t').textContent=SDP==='m'?'Taxas por município (média anual 2023–2025)':`Taxas por município em ${2023+SDP}`;
  const cols=['drsai','resp','asma','deng'];
  const mx=Object.fromEntries(cols.map(c=>[c,d3.max(SAUDE.mun,m=>sdRate(c,m,SDP))]));
  const bar=(c,v)=>`<span class="sdb"><i style="width:${(100*v/(mx[c]||1)).toFixed(1)}%"></i></span>`;
  let h=`<thead><tr><th class="l">Município</th><th>População<br><small>Censo 2022</small></th><th>DRSAI<br><small>/10 mil</small></th><th>Respiratórias<br><small>/10 mil</small></th><th>Pneum., asma, DPOC<br><small>/10 mil</small></th><th>Dengue<br><small>/100 mil</small></th><th>DRSAI no total<br><small>de internações</small></th><th>Esgoto na rede<br><small>todo o município</small></th><th>Água da rede<br><small>todo o município</small></th></tr></thead><tbody>`;
  for(const m of SAUDE.mun.slice().sort((a,b)=>b.pop-a.pop)) h+=`<tr><td class="l">${m.mun}</td><td class="num">${ptBR(fmtN(m.pop))}</td>${cols.map(c=>{const r=sdRate(c,m,SDP); return `<td class="num">${sdFmt(c,r)}${bar(c,r)}</td>`;}).join('')}<td class="num">${ptBR(fmt1(100*sdCount('drsai',m,SDP)/sdCount('all',m,SDP)))}%</td><td class="num">${ptBR(fmt1(m.esgoto))}%</td><td class="num">${ptBR(fmt1(m.agua))}%</td></tr>`;
  h+=`<tr class="tot"><td class="l">RMVRC</td><td class="num">${ptBR(fmtN(SAUDE.tot.pop))}</td>${cols.map(c=>`<td class="num">${sdFmt(c,sdRate(c,null,SDP))}</td>`).join('')}<td class="num">${ptBR(fmt1(100*sdCount('drsai',null,SDP)/sdCount('all',null,SDP)))}%</td><td></td><td></td></tr></tbody>`;
  document.getElementById('sd-tab').innerHTML=h;
  renderSdYears();
  // grupos por ano
  const G=SAUDE.grupos.map(g=>g[0]).sort((a,b)=>d3.sum(SAUDE.gy[b])-d3.sum(SAUDE.gy[a]));
  const tot=[0,1,2].map(j=>d3.sum(G,g=>SAUDE.gy[g][j]));
  document.getElementById('sd-grp').innerHTML=`<thead><tr><th class="l">Forma de transmissão</th><th>2023</th><th>2024</th><th>2025</th><th>Total</th></tr></thead><tbody>`+
    G.map(g=>{ const d=SAUDE.grupos.find(x=>x[0]===g)[1], a=SAUDE.gy[g]; return `<tr><td class="l"><b>${g}</b><br><small class="mu">${d}</small></td>${a.map(v=>`<td class="num">${ptBR(fmtN(v))}</td>`).join('')}<td class="num"><b>${ptBR(fmtN(d3.sum(a)))}</b> <small class="mu">(${ptBR(fmt1(100*d3.sum(a)/d3.sum(tot)))}%)</small></td></tr>`; }).join('')+
    `<tr class="tot"><td class="l">Total DRSAI</td>${tot.map(v=>`<td class="num">${ptBR(fmtN(v))}</td>`).join('')}<td class="num">${ptBR(fmtN(d3.sum(tot)))}</td></tr></tbody>`;
  let d=`<thead><tr><th class="l">Município</th>${SAUDE.anos.map(a=>`<th>${a}</th>`).join('')}</tr></thead><tbody>`;
  for(const m of SAUDE.mun.slice().sort((a,b)=>b.pop-a.pop)){ const mxa=Math.max(...m.anos_deng); d+=`<tr><td class="l">${m.mun}</td>${m.anos_deng.map(v=>`<td class="num${v===mxa&&v>0?' pk':''}">${ptBR(fmtN(v))}</td>`).join('')}</tr>`; }
  document.getElementById('sd-deng').innerHTML=d+'</tbody>';
  const ML=['J','F','M','A','M','J','J','A','S','O','N','D'], MN=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];
  function lchart(id,obj){ const s=d3.select('#'+id); s.selectAll('*').remove(); const W0=360,H0=170,l=34,r=10,t=12,b=22;
    const ys=['2023','2024','2025'], mxv=d3.max(ys,y=>d3.max(obj[y]));
    const x=d3.scalePoint().domain(d3.range(12)).range([l+6,W0-r-6]), y=d3.scaleLinear().domain([0,mxv*1.1]).nice(4).range([H0-b,t]);
    y.ticks(4).forEach(v=>{ s.append('line').attr('x1',l).attr('x2',W0-r).attr('y1',y(v)).attr('y2',y(v)).attr('stroke','var(--line)'); s.append('text').attr('x',l-5).attr('y',y(v)+3).attr('text-anchor','end').attr('font-size',9).attr('fill','var(--muted)').text(ptBR(fmtN(v))); });
    ML.forEach((m,j)=>s.append('text').attr('x',x(j)).attr('y',H0-7).attr('text-anchor','middle').attr('font-size',9.5).attr('fill','var(--muted)').text(m));
    ys.forEach((yy,q)=>{ const c=`var(--y${q+1})`;
      s.append('path').attr('d',d3.line().x((v,j)=>x(j)).y(v=>y(v))(obj[yy])).attr('fill','none').attr('stroke',c).attr('stroke-width',2);
      obj[yy].forEach((v,j)=>s.append('circle').attr('cx',x(j)).attr('cy',y(v)).attr('r',3).attr('fill',c).attr('stroke','var(--panel)').attr('stroke-width',1.2).append('title').text(`${MN[j]} de ${yy}: ${ptBR(fmtN(v))} internações`)); });
  }
  lchart('sd-m1',SAUDE.mes_ano_resp); lchart('sd-m2',SAUDE.mes_ano_drsai);
}
function renderSdYears(){
  const svg=d3.select('#sd-yc'); if(svg.empty()) return; svg.selectAll('*').remove();
  const K=SDI, MS=SAUDE.mun.slice().sort((a,b)=>b.pop-a.pop), rows=[...MS.map(m=>[m.mun,m]),['RMVRC',null]];
  const ab={'Nossa Senhora do Livramento':'Livramento','Santo Antônio de Leverger':'Leverger','Chapada dos Guimarães':'Chapada','Várzea Grande':'V. Grande','Campo Verde':'C. Verde'};
  const W0=640,H0=260,l=44,r=8,t=18,b=34; svg.attr('viewBox',`0 0 ${W0} ${H0}`);
  const vals=rows.map(([n,m])=>[0,1,2].map(p=>sdRate(K,m,p))); const mxv=d3.max(vals.flat());
  const x0=d3.scaleBand().domain(rows.map(r=>r[0])).range([l,W0-r]).paddingInner(.22).paddingOuter(.06), x1=d3.scaleBand().domain([0,1,2]).range([0,x0.bandwidth()]).padding(.08), y=d3.scaleLinear().domain([0,mxv*1.12]).nice(4).range([H0-b,t]);
  y.ticks(4).forEach(v=>{ svg.append('line').attr('x1',l).attr('x2',W0-r).attr('y1',y(v)).attr('y2',y(v)).attr('stroke','var(--line)'); svg.append('text').attr('x',l-6).attr('y',y(v)+3).attr('text-anchor','end').attr('font-size',10).attr('fill','var(--muted)').text(sdFmt(K,v)); });
  rows.forEach(([n,m],i)=>{ const g=svg.append('g').attr('transform',`translate(${x0(n)},0)`);
    if(n==='RMVRC') svg.append('rect').attr('x',x0(n)-4).attr('y',t-6).attr('width',x0.bandwidth()+8).attr('height',H0-b-t+6).attr('fill','var(--panel-2)').lower();
    vals[i].forEach((v,p)=>{ const rr=g.append('rect').attr('x',x1(p)).attr('y',y(v)).attr('width',x1.bandwidth()).attr('height',Math.max(0,y(0)-y(v))).attr('rx',2).attr('fill',`var(--y${p+1})`); rr.append('title').text(`${n} · ${2023+p}: ${sdFmt(K,v)} ${SDK[K].u} (${ptBR(fmtN(sdCount(K,m,p)))} ${K==='deng'?'casos':'internações'})`); });
    svg.append('text').attr('x',x0(n)+x0.bandwidth()/2).attr('y',H0-b+14).attr('text-anchor','middle').attr('font-size',10.5).attr('font-weight',n==='RMVRC'?700:400).attr('fill','var(--fg)').text(ab[n]||n); });
  svg.append('line').attr('x1',l).attr('x2',W0-r).attr('y1',y(0)).attr('y2',y(0)).attr('stroke','var(--muted)');
  document.getElementById('sd-unit').textContent=SDK[K].n+' · '+SDK[K].u+' (população do Censo 2022)';
  let h=`<thead><tr><th class="l">Município</th><th>2023</th><th>2024</th><th>2025</th><th>Variação<br><small>2023 → 2025</small></th></tr></thead><tbody>`;
  rows.forEach(([n,m],i)=>{ const v=vals[i], dv=v[0]?100*(v[2]-v[0])/v[0]:null; const c=dv==null?'':dv>10?'up':dv<-10?'down':'';
    h+=`<tr${n==='RMVRC'?' class="tot"':''}><td class="l">${n}</td>${v.map((x,p)=>`<td class="num">${sdFmt(K,x)}<br><small class="mu">${ptBR(fmtN(sdCount(K,m,p)))}</small></td>`).join('')}<td class="num vr ${c}">${dv==null?'—':sdPct(dv)}</td></tr>`; });
  document.getElementById('sd-yt').innerHTML=h+'</tbody>';
  const N={drsai:'Em 2023–2025 as DRSAI somaram '+ptBR(fmtN(d3.sum(SAUDE.tot.anos.drsai)))+' internações. O aumento de 2024 vem principalmente da dengue (grupo "inseto vetor"); em 2025 cresceram as diarreias (grupo feco-oral).',
   resp:'Na RMVRC, as internações respiratórias cresceram 54% de 2023 para 2025, bem mais que o total de internações no SUS (+22%, aba "Todas as internações"). O crescimento, portanto, não se explica só pelo aumento do volume de atendimento.',
   asma:'Pneumonia, asma e DPOC respondem por cerca de dois terços das internações respiratórias e seguem a mesma tendência.',
   deng:'Contagem de casos prováveis notificados no SINAN, não de internações. 2024 foi o ano de maior número de casos em Cuiabá, Campo Verde, Chapada dos Guimarães e Nossa Senhora do Livramento; em Várzea Grande e Santo Antônio de Leverger o pico foi em 2025, e em Acorizal, em 2023.',
   all:'Total de internações no SUS de moradores de cada município, de qualquer causa. É a referência para ler as outras abas: se uma taxa cresce no mesmo ritmo do total, o aumento pode refletir mais oferta de leitos ou de registro, e não mais doença.'};
  document.getElementById('sd-ynote').innerHTML='Abaixo de cada taxa, o número absoluto do ano. '+N[K];
}
document.getElementById('sd-per')?.addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; SDP=b.dataset.p==='m'?'m':+b.dataset.p; document.querySelectorAll('#sd-per button').forEach(x=>x.setAttribute('aria-pressed',x===b)); renderSaude(); });
document.getElementById('sd-ind')?.addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b) return; SDI=b.dataset.k; document.querySelectorAll('#sd-ind button').forEach(x=>x.setAttribute('aria-pressed',x===b)); renderSdYears(); });
renderODS(); renderSaude();
