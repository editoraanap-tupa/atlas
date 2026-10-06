// ------- relatório do setor/bairro (v2): mesmo desenho da página — cartões por tema, leitura em texto e notas -------
const RC={bg:'#f2f4f8',card:'#ffffff',line:'#d9dfeb',fg:'#0f1d3a',mu:'#56607a',navy:'#002060',gold:'#ffc000',ochre:'#9a6f00',track:'#dfe4ee',ref:'#b9c3d6',soft:'#f6f8fc',badb:'#fbe3df',badf:'#9b2415',goodb:'#dff1e6',goodf:'#1d6b3a'};
const FD='Montserrat, "Segoe UI", Arial, sans-serif', FB='"Source Sans 3", "Segoe UI", Arial, sans-serif', FM='"JetBrains Mono", Consolas, monospace';
function rRR(c,x,y,w,h,r){ r=Math.max(0,Math.min(r,w/2,h/2)); c.beginPath(); c.moveTo(x+r,y); c.arcTo(x+w,y,x+w,y+h,r); c.arcTo(x+w,y+h,x,y+h,r); c.arcTo(x,y+h,x,y,r); c.arcTo(x,y,x+w,y,r); c.closePath(); }
function rCard(c,x,y,w,h,fill){ rRR(c,x,y,w,h,18); c.fillStyle=fill||RC.card; c.fill(); c.strokeStyle=RC.line; c.lineWidth=2; c.stroke(); }
function rHead(c,ax,title,sub,x,y,maxW){
  c.textAlign='left'; c.fillStyle=ax&&AX[ax]?AX[ax].cor:RC.gold; c.beginPath(); c.arc(x+9,y-10,8,0,2*Math.PI); c.fill();
  c.fillStyle=RC.fg; c.font='800 29px '+FD; c.fillText(title,x+28,y); const tw=c.measureText(title).width;
  if(sub){ c.fillStyle=RC.mu; c.font='19px '+FB; let s=sub; while(c.measureText(s).width>maxW-tw-60&&s.length>8) s=s.slice(0,-2); c.fillText(s+(s!==sub?'…':''),x+28+tw+16,y); } }
function rFlag(c,cd,x,y){ if(cd==null||(cd>.2&&cd<.8)) return 0; const bad=cd<=.2, t=bad?'20% piores':'20% melhores'; c.font='700 15px '+FB; const w=c.measureText(t).width+18; rRR(c,x,y-17,w,23,6); c.fillStyle=bad?RC.badb:RC.goodb; c.fill(); c.fillStyle=bad?RC.badf:RC.goodf; const ta=c.textAlign; c.textAlign='left'; c.fillText(t,x+9,y); c.textAlign=ta; return w; }
const rCol=(i,v)=>{ const cd=v==null?null:cond(i,v); return cd==null?RC.navy:ECOL[ecls(cd)]; };
const rTxt=s=>String(s).replace(/<[^>]+>/g,'');
function rWrap(c,t,x,y,maxW,lh,maxL){ const L=wrapText(c,t,maxW), M=maxL?L.slice(0,maxL):L; M.forEach((s,j)=>c.fillText(s,x,y+j*lh)); return M.length*lh; }
// texto corrido com trechos em negrito: segs=[[texto,negrito],…]; devolve a altura usada
function rRich(c,segs,x,y,maxW,lh,size,dry){ let cx=x, cy=y; c.textAlign='left';
  for(const [t,b] of segs){ c.font=(b?'700 ':'')+size+'px '+FB; const sp=c.measureText(' ').width;
    for(const w of String(t).split(/(\s+)/)){ if(!w) continue; if(/^\s+$/.test(w)){ if(cx>x) cx+=sp; continue; } const ww=c.measureText(w).width; if(cx+ww>x+maxW&&cx>x){ cx=x; cy+=lh; } if(!dry) c.fillText(w,cx,cy); cx+=ww; } }
  return cy-y+lh; }
function rBullet(c,i,p,x,y,w){ const v=p[i.k], cd=v==null?null:cond(i,v), val=v==null?'sem dado':fv(i.k,v);
  c.font='700 19px '+FM; const vw=c.measureText(val).width, fw=(cd!=null&&(cd<=.2||cd>=.8))?108:0;
  let fs=20; c.font=fs+'px '+FB; while(fs>12&&c.measureText(i.n).width>w-vw-fw-18){ fs--; c.font=fs+'px '+FB; }
  c.textAlign='left'; c.fillStyle=RC.fg; c.fillText(i.n,x,y); const nw=c.measureText(i.n).width; if(fw) rFlag(c,cd,x+nw+8,y);
  c.textAlign='right'; c.font='700 19px '+FM; c.fillStyle=v==null?RC.mu:RC.fg; c.fillText(val,x+w,y); c.textAlign='left';
  const ty=y+12, th=10; rRR(c,x,ty,w,th,5); c.fillStyle=RC.track; c.fill();
  if(v!=null){ const a=sorted[i.k], med=d3.quantile(a,.5), lo=i.u==='%'?0:(['lst','lst_anom','ndvi'].includes(i.k)?d3.quantile(a,.02):0), hi=i.u==='%'?100:d3.quantile(a,.98), pos=q=>Math.max(0,Math.min(1,(q-lo)/((hi-lo)||1)));
    const bw=w*pos(v); if(bw>1){ rRR(c,x,ty,Math.max(bw,10),th,5); c.fillStyle=cd==null?RC.navy:d3.interpolateYlOrRd(.12+.83*(1-cd)); c.fill(); }
    c.fillStyle=RC.fg; c.fillRect(x+w*pos(med)-1.5,ty-5,3,th+10); } }
function rDonut(c,k,p,cx,cy,cellW){ const i=byK[k], v=p[k], r=44; c.lineWidth=15; c.strokeStyle=RC.track; c.beginPath(); c.arc(cx,cy,r,0,2*Math.PI); c.stroke();
  if(v!=null){ const f=Math.max(0,Math.min(100,v))/100; if(f>0){ c.strokeStyle=rCol(i,v); c.lineCap=f<1?'round':'butt'; c.beginPath(); c.arc(cx,cy,r,-Math.PI/2,-Math.PI/2+2*Math.PI*f); c.stroke(); c.lineCap='butt'; } }
  c.textAlign='center'; c.fillStyle=RC.fg; c.font='800 25px '+FD; c.fillText(v==null?'—':Math.round(v)+'%',cx,cy+9);
  c.font='700 18px '+FB; const L=wrapText(c,i.n,cellW-16).slice(0,2); L.forEach((s,j)=>c.fillText(s,cx,cy+r+36+j*22)); let yy=cy+r+36+L.length*22;
  const cd=v==null?null:cond(i,v); if(cd!=null&&(cd<=.2||cd>=.8)){ c.font='700 15px '+FB; const t=cd<=.2?'20% piores':'20% melhores', w=c.measureText(t).width+18; rFlag(c,cd,cx-w/2,yy+2); yy+=27; }
  c.textAlign='center'; c.fillStyle=RC.mu; c.font='17px '+FB; c.fillText('RMVRC: '+fv(k,rmMed(k)),cx,yy+4); c.textAlign='left'; }
function rTrio(c,k,p,x,y,w,h){ const i=byK[k], v=p[k], vm=munMed(k,p.mun), vr=rmMed(k), vals=[v,vm,vr], mx=d3.max(vals.filter(q=>q!=null))||1;
  rRR(c,x,y,w,h,12); c.fillStyle=RC.card; c.fill(); c.strokeStyle=RC.line; c.lineWidth=1.5; c.stroke();
  c.textAlign='left'; c.fillStyle=RC.fg; let fs=20; c.font='700 '+fs+'px '+FB; const cd=v==null?null:cond(i,v), fw=(cd!=null&&(cd<=.2||cd>=.8))?112:0; while(fs>13&&c.measureText(i.n).width>w-28-fw){ fs--; c.font='700 '+fs+'px '+FB; }
  c.fillText(i.n,x+14,y+30); const nw=c.measureText(i.n).width; if(fw) rFlag(c,cd,x+14+nw+8,y+30);
  const by=y+h-74, bh=h-74-78, bw=Math.min(96,(w-60)/3-18), gap=(w-3*bw)/4, labs=['Setor',MUNC[p.mun]||p.mun,'RMVRC'];
  vals.forEach((q,j)=>{ const X=x+gap+j*(bw+gap), hh=q==null?0:Math.max(4,bh*q/mx); if(hh>0){ rRR(c,X,by-hh,bw,hh,6); c.fillStyle=j===0?rCol(i,v):RC.ref; c.fill(); }
    c.textAlign='center'; c.fillStyle=RC.fg; c.font=(j===0?'800 ':'600 ')+'19px '+FB; c.fillText(fv(k,q),X+bw/2,by-hh-8); c.fillStyle=RC.mu; c.font=(j===0?'700 ':'')+'17px '+FB; c.fillText(labs[j],X+bw/2,by+24); });
  c.strokeStyle=RC.line; c.lineWidth=2; c.beginPath(); c.moveTo(x+gap-12,by); c.lineTo(x+w-gap+12,by); c.stroke();
  c.textAlign='left'; c.fillStyle=RC.mu; c.font='17px '+FB; c.fillText(v==null?'sem dado':rTxt(frase(i,v)),x+14,y+h-18); }
function rWaffle(c,k,p,x,y,sz){ const i=byK[k], v=p[k], n=v==null?0:Math.round(v), col=rCol(i,v), s=sz/10; for(let j=0;j<100;j++){ c.fillStyle=j<n?col:RC.track; c.beginPath(); c.arc(x+(j%10+.5)*s,y+(Math.floor(j/10)+.5)*s,s*.36,0,2*Math.PI); c.fill(); } }
function rTile(c,lab,val,sub,x,y,w,h){ rRR(c,x,y,w,h,12); c.fillStyle=RC.soft; c.fill(); c.strokeStyle=RC.line; c.lineWidth=1.5; c.stroke(); c.textAlign='left'; c.fillStyle=RC.mu; c.font='700 15px '+FB; c.fillText(lab.toUpperCase(),x+14,y+27); c.fillStyle=RC.fg; c.font='800 27px '+FD; c.fillText(val,x+14,y+60); if(sub){ c.fillStyle=RC.mu; c.font='16px '+FB; let s=sub; while(c.measureText(s).width>w-28&&s.length>6) s=s.slice(0,-2); c.fillText(s,x+14,y+84); } }
async function sectorReport(f){
  const p=f.properties, B=bairroDe(f), temB=!!p.bairro&&B.length>1, i0=byK[st.ind], kind=p.bairro?'b':'s';
  say('Montando o relatório…', 0);
  try{
    try{ await Promise.all(['800 29px Montserrat','700 20px "Source Sans 3"','400 20px "Source Sans 3"','700 19px "JetBrains Mono"'].map(s=>document.fonts.load(s))); }catch(e){}
    const title=p.bairro ? p.bairro : (p.dist||'Setor')+' · setor '+p.id.slice(-4);
    const pages=[], TOP=244, BOT=RH-166, CW=RW-2*RM, GAP=22, PAD=22;
    let x, y;
    const newPage=()=>{ const c=document.createElement('canvas'); c.width=RW; c.height=RH; x=c.getContext('2d'); repHeader(x,p,title,kind); x.fillStyle=RC.bg; x.fillRect(0,215,RW,RH-215-156); pages.push(c); y=TOP; };
    const need=h=>{ if(y+h>BOT) newPage(); };
    const nome=p.bairro||p.dist||'o setor';
    // =============== página 1: mapa, localização, IVSA, leitura ===============
    newPage();
    const LW=930, RX=RM+LW+GAP, RWd=CW-LW-GAP, H1=920;
    rCard(x,RM,y,LW,H1); rHead(x,null,p.bairro?`Setores censitários do bairro (${B.length})`:'Setor censitário','',RM+PAD,y+46,LW);
    const sc=document.createElement('canvas'); sc.width=LW-2*PAD; sc.height=640; drawBairroMap(sc,f,{lw:3,font:20}); x.drawImage(sc,RM+PAD,y+66);
    const escN=sig3(sc._mpp*1000/(210/RW));
    let ly=y+66+640+30; x.textAlign='left'; x.fillStyle=RC.fg; x.font='700 18px '+FB;
    ly+=rWrap(x,`Cores: ${i0.n}${i0.u&&i0.u!=='%'?' ('+i0.u+')':''} · ${st.cls==='q'?'quintis':'intervalos iguais'} do recorte ${filtroTxt()}`,RM+PAD,ly,LW-2*PAD,23,2)+4;
    { const {th,c,ext}=binsArr, edges=[ext[0],...th,ext[1]], stp=(LW-2*PAD)/(c.length+1); x.font='17px '+FB;
      c.forEach((col,j)=>{ const lx=RM+PAD+j*stp; x.globalAlpha=Math.max(.35,OPA.set/100); x.fillStyle=col; x.fillRect(lx,ly-14,24,18); x.globalAlpha=1; x.fillStyle=RC.fg; x.fillText(`${fv(i0.k,edges[j])}–${fv(i0.k,edges[j+1])}`,lx+30,ly); });
      x.fillStyle='#c9cfca'; x.fillRect(RM+PAD+c.length*stp,ly-14,24,18); x.fillStyle=RC.fg; x.fillText('sem dado',RM+PAD+c.length*stp+30,ly); ly+=30; }
    x.fillStyle=RC.mu; x.font='17px '+FB;
    ly+=rWrap(x,'Contorno escuro: setor selecionado · números: final do código de cada setor · cinza: outros bairros · azul: rios e córregos.',RM+PAD,ly,LW-2*PAD,22,2);
    ly+=rWrap(x,`Norte para cima. Escala gráfica no mapa; escala numérica 1:${ptBR(fmtN(escN))} na folha A4 impressa em tamanho real (100%).`,RM+PAD,ly,LW-2*PAD,22,2);
    { const eqOn=Object.entries(EQC).filter(([k])=>document.getElementById('eq-'+k)?.checked); let ex=RM+PAD; x.font='17px '+FB;
      for(const [k,v] of eqOn){ const tw=x.measureText(v.n).width+42; if(ex+tw>RM+LW-PAD) break; const p2=new Path2D(sym(v.s,8)); x.save(); x.translate(ex+9,ly-5); x.fillStyle=v.c; x.fill(p2); x.restore(); x.fillStyle=RC.mu; x.fillText(v.n,ex+24,ly); ex+=tw; } }
    // localização
    const HL1=452; rCard(x,RX,y,RWd,HL1); rHead(x,null,'Localização','',RX+PAD,y+46,RWd);
    locator(x,f,RX+PAD,y+66,RWd-2*PAD,HL1-66-70);
    // IVSA
    const y2=y+HL1+GAP, HV=H1-HL1-GAP; rCard(x,RX,y2,RWd,HV); rHead(x,'ind','Vulnerabilidade (IVSA)','',RX+PAD,y2+46,RWd);
    gaugeCanvas(x,RX+118,y2+178,78,p.ivsa);
    x.textAlign='left'; x.fillStyle=RC.fg; x.font='800 62px '+FD; x.fillText(p.ivsa==null?'—':ptBR(fmt1(p.ivsa)),RX+226,y2+150);
    let vy=y2+212;
    if(p.ivsa!=null){ const j=d3.bisectRight(IVSA_Q,p.ivsa); rRR(x,RX+226,y2+168,RWd-226-PAD,36,8); x.fillStyle=ramp5(j); x.fill(); x.fillStyle=j<2?'#3a2a00':'#fff'; x.font='700 18px '+FB; x.fillText('Vulnerabilidade '+CLASSE[j].toLowerCase(),RX+238,y2+192);
      const pos=IVSA_ALL.length-d3.bisectLeft(IVSA_ALL,p.ivsa); x.fillStyle=RC.mu; x.font='18px '+FB; vy=y2+250; x.fillText(`${pos}º mais vulnerável entre ${ptBR(fmtN(IVSA_ALL.length))} setores com índice.`,RX+PAD,vy); vy+=28; }
    else { x.fillStyle=RC.mu; x.font='18px '+FB; vy=y2+250; vy+=rWrap(x,'Sem índice: menos de 50 moradores ou dados insuficientes.',RX+PAD,vy,RWd-2*PAD,24); }
    x.fillStyle=RC.fg; x.font='18px '+FB;
    if(temB){ x.fillText(`Média do bairro: ${fv('ivsa',agg(B,byK.ivsa))}`,RX+PAD,vy); vy+=28; }
    x.fillText(`Mediana de ${MUNC[p.mun]||p.mun}: ${fv('ivsa',munMed('ivsa',p.mun))} · RMVRC: ${fv('ivsa',rmMed('ivsa'))}`,RX+PAD,vy); vy+=34;
    x.fillStyle=RC.mu; x.font='16px '+FB; rWrap(x,'De 0 (menor vulnerabilidade) a 100 (maior). Classe = quintil entre os setores com índice.',RX+PAD,vy,RWd-2*PAD,21,3);
    y+=H1+GAP;
    // ---- leitura do setor (texto)
    const ev=IND.filter(i=>i.pol!=='n'&&i.k!=='ivsa'&&!i.k.startsWith('ipt_')&&p[i.k]!=null).map(i=>({i,c:cond(i,p[i.k])})).filter(e=>e.c!=null);
    const bad=ev.filter(e=>e.c<=.2).sort((a,b)=>a.c-b.c), good=ev.filter(e=>e.c>=.8).sort((a,b)=>b.c-a.c);
    const lista=(a,n)=>{ const s=a.slice(0,n).map(e=>e.i.n.toLowerCase()); return s.length>1?s.slice(0,-1).join(', ')+' e '+s[s.length-1]:s[0]||''; };
    const pars=[];
    pars.push([[`${title}`,1],[` fica em ${p.mun}, em área ${p.sit.toLowerCase()}. O setor ${p.id} tem `,0],[`${fv('pop',p.pop)} moradores`,1],[` em ${fv('pop',p.dppo)} domicílios, numa área de ${fmtArea(p.area)}${p.dens!=null?' (densidade de '+fv('dens',p.dens)+' hab./km²)':''}.`,0],
      ...(temB?[[` O bairro reúne ${B.length} setores e ${fv('pop',d3.sum(B,g=>g.properties.pop))} moradores.`,0]]:[]), ...(p.fcu?[[` O setor faz parte da favela ou comunidade urbana ${p.fcu}.`,0]]:[])]);
    if(p.ivsa!=null){ const j=d3.bisectRight(IVSA_Q,p.ivsa), menos=Math.round(100*d3.bisectLeft(IVSA_ALL,p.ivsa)/IVSA_ALL.length);
      const comp=WC.filter(c=>WT[c.k]>0&&p._ic&&p._ic[c.k]!=null).map(c=>[c.n.toLowerCase(),p._ic[c.k]]).sort((a,b)=>b[1]-a[1]).slice(0,3).filter(c=>c[1]>=40);
      pars.push([['Vulnerabilidade. ',1],[`O IVSA do setor é ${ptBR(fmt1(p.ivsa))}, na classe `,0],[CLASSE[j].toLowerCase(),1],[`: ${menos}% dos setores da RMVRC são menos vulneráveis que ele.`,0],
        ...(comp.length?[[` O que mais pesa no índice: ${comp.map(c=>c[0]+' (nota '+Math.round(c[1])+')').join(', ')}.`,0]]:[])]); }
    else pars.push([['Vulnerabilidade. ',1],['O setor não recebe IVSA: tem menos de 50 moradores ou não tem dados suficientes (menos de 60% do peso dos componentes).',0]]);
    pars.push([['Comparação com a região. ',1], [bad.length?`O setor está entre os 20% piores da RMVRC em ${bad.length} indicador${bad.length>1?'es':''}`+(bad.length?', entre eles '+lista(bad,5):'')+'.':'O setor não está entre os 20% piores da RMVRC em nenhum indicador.',0],
      [good.length?` Está entre os 20% melhores em ${good.length}: ${lista(good,4)}${good.length>4?', entre outros':''}.`:'',0]]);
    { const amb=[]; if(p.inund!=null) amb.push(`${fv('inund',p.inund)} da área em suscetibilidade alta a inundação${p.inund_pop?' (cerca de '+fv('inund_pop',p.inund_pop)+' moradores)':''}`);
      if(p.app_pct!=null) amb.push(`${fv('app_pct',p.app_pct)} da área em APP`); if(p.verde!=null) amb.push(`cobertura vegetal de ${fv('verde',p.verde)}`);
      if(p.lst!=null) amb.push(`temperatura de superfície de ${fv('lst',p.lst)}${p.lst_anom!=null?' ('+(p.lst_anom>0?'+':'')+ptBR(fmt1(p.lst_anom))+' °C em relação à média urbana de Cuiabá e Várzea Grande)':''}`);
      if(amb.length) pars.push([['Ambiente e risco. ',1],[amb.join('; ')+'.',0]]); }
    { const lz=IND.filter(i=>i.ax==='gov'&&p[i.k]!=null).map(i=>[i.n,p[i.k]]).sort((a,b)=>b[1]-a[1]).slice(0,3);
      if(lz.length) pars.push([['Prioridade territorial. ',1],[`Nos objetivos do Laboratório de Governança, os índices de prioridade mais altos do setor são: ${lz.map(l=>l[0]+' ('+ptBR(fmt1(l[1]))+')').join(', ')}.`,0]]); }
    { const cx2=[p.solo?'solo predominante '+p.solo:'', p.micro?'microbacia '+p.micro:'', p.subbac?'sub-bacia '+p.subbac.replace(/^Bacia (do |da |de )?/,''):'', p.bac||''].filter(Boolean);
      if(cx2.length) pars.push([['Meio físico. ',1],[cx2.join('; ')+'.',0]]); }
    { const tw=CW-2*PAD, hh=pars.reduce((s,sg)=>s+rRich(x,sg,0,0,tw,27,20,true)+10,0), hc=70+hh+8; need(hc);
      rCard(x,RM,y,CW,hc); rHead(x,null,'Leitura do setor','resumo em texto, gerado a partir dos indicadores',RM+PAD,y+46,CW); let ty=y+86; x.fillStyle=RC.fg;
      for(const sg of pars){ x.fillStyle=RC.fg; ty+=rRich(x,sg,RM+PAD,ty,tw,27,20)+10; } y+=hc+GAP; }
    // ---- o que pesa no índice + resumo
    { const comp=WC.filter(c=>WT[c.k]>0), rows=Math.ceil(comp.length/2), hc=70+rows*56+52; need(hc);
      rCard(x,RM,y,LW,hc); rHead(x,'ind','O que pesa no IVSA','nota de cada componente, de 0 (melhor) a 100 (pior)',RM+PAD,y+46,LW);
      const cw2=(LW-2*PAD-40)/2;
      comp.forEach((c,j)=>{ const cx=RM+PAD+(j%2)*(cw2+40), cy=y+92+Math.floor(j/2)*56, v=p._ic?p._ic[c.k]:null; x.textAlign='left'; x.fillStyle=RC.fg; x.font='19px '+FB; x.fillText(c.n+(WT[c.k]!==1?' (×'+String(WT[c.k]).replace('.',',')+')':''),cx,cy);
        x.textAlign='right'; x.font='700 19px '+FM; x.fillStyle=v==null?RC.mu:RC.fg; x.fillText(v==null?'sem dado':String(Math.round(v)),cx+cw2,cy); x.textAlign='left';
        rRR(x,cx,cy+11,cw2,10,5); x.fillStyle=RC.track; x.fill(); if(v!=null&&v>0.5){ rRR(x,cx,cy+11,Math.max(10,cw2*v/100),10,5); x.fillStyle=d3.interpolateYlOrRd(.15+.8*v/100); x.fill(); } });
      x.fillStyle=RC.mu; x.font='16px '+FB; rWrap(x,'Cada componente é normalizado entre os percentis 2 e 98 dos setores com 50 ou mais moradores; o IVSA é a média ponderada das notas (Metodologia, item 2).',RM+PAD,y+hc-36,LW-2*PAD,20,2);
      rCard(x,RX,y,RWd,hc); rHead(x,null,p.bairro?'Resumo do bairro':'Resumo do setor','',RX+PAD,y+46,RWd);
      const res=[['Setores',String(B.length)],['Moradores',fv('pop',d3.sum(B,g=>g.properties.pop))],['Domicílios',fv('pop',d3.sum(B,g=>g.properties.dppo))],['Área',fmtArea(d3.sum(B,g=>g.properties.area))],['Renda média',fv('renda',agg(B,byK.renda))],['Esgoto na rede',fv('esgoto',agg(B,byK.esgoto))]];
      const tw2=(RWd-2*PAD-12)/2, th2=Math.min(86,(hc-76-24)/3);
      res.forEach(([k,v],j)=>{ const cx=RX+PAD+(j%2)*(tw2+12), cy=y+68+Math.floor(j/2)*(th2+10); rRR(x,cx,cy,tw2,th2,10); x.fillStyle=RC.soft; x.fill(); x.strokeStyle=RC.line; x.lineWidth=1.5; x.stroke(); x.textAlign='left'; x.fillStyle=RC.mu; x.font='700 14px '+FB; x.fillText(k.toUpperCase(),cx+12,cy+24); x.fillStyle=RC.fg; x.font='800 25px '+FD; x.fillText(v,cx+12,cy+th2-16); });
      y+=hc+GAP; }
    // =============== indicadores por tema ===============
    newPage();
    { const rows=IND.filter(i=>i.ax==='amb'&&!['ndvi','arv5'].includes(i.k)), nr=Math.ceil(rows.length/3), note=typeof satNote==='function'?satNote(p):'', hc=70+150+nr*62+(note?44:0)+14;
      rCard(x,RM,y,CW,hc); rHead(x,'amb',AX.amb.nome,'valor do setor, com a mediana da RMVRC como marcador de referência',RM+PAD,y+46,CW);
      // como ler as barras
      const kx=RM+PAD, ky=y+68, kw=CW-2*PAD; rRR(x,kx,ky,kw,132,12); x.fillStyle=RC.soft; x.fill(); x.strokeStyle=RC.line; x.lineWidth=1.5; x.stroke();
      x.fillStyle=RC.mu; x.font='700 14px '+FB; x.textAlign='left'; x.fillText('COMO LER AS BARRAS',kx+14,ky+24);
      const keys=[['bar','Barra colorida = valor deste setor; quanto mais comprida, maior o valor.'],['mark','Marcador de referência (linha vertical) = mediana da RMVRC: metade dos setores tem menos, metade tem mais.'],['track','Faixa de fundo = escala do indicador: 0 a 100% nas porcentagens; nos demais, de zero aos valores mais altos da região.'],['cor','Cor = posição entre os setores: amarelo, situação melhor; vermelho, pior. As etiquetas marcam os 20% piores e os 20% melhores.']];
      keys.forEach(([t,s],j)=>{ const cx=kx+14+(j%2)*(kw/2), cy=ky+52+Math.floor(j/2)*44; rRR(x,cx,cy-9,60,10,5); x.fillStyle=RC.track; x.fill();
        if(t==='bar'){ rRR(x,cx,cy-9,36,10,5); x.fillStyle='#e31a1c'; x.fill(); } if(t==='mark'){ x.fillStyle=RC.fg; x.fillRect(cx+24,cy-14,3,20); } if(t==='cor'){ rRR(x,cx,cy-9,60,10,5); const g=x.createLinearGradient(cx,0,cx+60,0); g.addColorStop(0,'#fee08b'); g.addColorStop(1,'#bd0026'); x.fillStyle=g; x.fill(); }
        x.fillStyle=RC.fg; x.font='16px '+FB; rWrap(x,s,cx+72,cy-4,kw/2-100,19,2); });
      const cw3=(CW-2*PAD-2*36)/3;
      rows.forEach((i,j)=>rBullet(x,i,p,RM+PAD+(j%3)*(cw3+36),y+70+150+24+Math.floor(j/3)*62,cw3));
      if(note){ x.fillStyle=RC.mu; x.font='16px '+FB; rWrap(x,note,RM+PAD,y+hc-34,CW-2*PAD,20,2); }
      y+=hc+GAP; }
    const HWd=(CW-GAP)/2;
    const donuts=(ax,sub,ks,X)=>{ const hc=70+2*232+6; rCard(x,X,y,HWd,hc); rHead(x,ax,AX[ax].nome,sub,X+PAD,y+46,HWd); const cw=(HWd-2*PAD)/3;
      ks.forEach((k,j)=>{ if(byK[k]) rDonut(x,k,p,X+PAD+(j%3+.5)*cw,y+70+62+Math.floor(j/3)*232,cw); }); return hc; };
    { const hc=70+2*232+6; need(hc); donuts('san','% dos domicílios',['agua','agua_enc','esgoto','esg_prec','lixo','sem_banh'],RM); donuts('ent','% dos domicílios com o item na face de quadra',['arvore','pav','calcada','bueiro','luz','onibus'],RM+HWd+GAP); y+=hc+GAP; }
    { const hc=70+2*262+12; need(hc);
      rCard(x,RM,y,HWd,hc); rHead(x,'ace',AX.ace.nome,'linha reta · setor × município × RMVRC',RM+PAD,y+46,HWd); const tw=(HWd-2*PAD-14)/2;
      ['d_ubs','d_saude','d_esc','d_parque'].forEach((k,j)=>{ if(byK[k]) rTrio(x,k,p,RM+PAD+(j%2)*(tw+14),y+66+Math.floor(j/2)*262,tw,250); });
      const X=RM+HWd+GAP; rCard(x,X,y,HWd,hc); rHead(x,'ren',AX.ren.nome,'setor × município × RMVRC',X+PAD,y+46,HWd);
      rTrio(x,'renda',p,X+PAD,y+66,HWd-2*PAD,250);
      const wy=y+66+262, i=byK.analf, v=p.analf; rRR(x,X+PAD,wy,HWd-2*PAD,250,12); x.fillStyle=RC.card; x.fill(); x.strokeStyle=RC.line; x.lineWidth=1.5; x.stroke();
      if(v==null){ x.fillStyle=RC.fg; x.font='700 20px '+FB; x.fillText(i.n,X+PAD+14,wy+30); x.fillStyle=RC.mu; x.font='17px '+FB; x.fillText('sem dado',X+PAD+14,wy+60); }
      else { rWaffle(x,'analf',p,X+PAD+16,wy+22,206); const tx=X+PAD+16+206+24, tw3=HWd-2*PAD-16-206-24-14; x.textAlign='left'; x.fillStyle=RC.fg; x.font='700 20px '+FB; x.fillText(i.n,tx,wy+44); rFlag(x,cond(i,v),tx+x.measureText(i.n).width+8,wy+44);
        x.fillStyle=RC.fg; x.font='800 34px '+FD; x.fillText(String(Math.round(v)),tx,wy+92); const nw=x.measureText(String(Math.round(v))).width; x.fillStyle=RC.mu; x.font='18px '+FB; x.fillText('em cada 100',tx+nw+10,wy+92);
        x.font='17px '+FB; let ty=wy+124; ty+=rWrap(x,'pessoas com 15 anos ou mais não sabem ler e escrever. Mediana RMVRC: '+fv('analf',rmMed('analf'))+'.',tx,ty,tw3,22,4)+6; x.fillText(rTxt(frase(i,v)),tx,ty); }
      y+=hc+GAP; }
    // demografia
    { const hc=70+4*104+12; need(hc); rCard(x,RM,y,CW,hc); rHead(x,'dem',AX.dem.nome,'setor, com a mediana do município e da RMVRC',RM+PAD,y+46,CW);
      const tw=318, ks=['pop','dens','criancas','idosos','negros','indig','mor'].filter(k=>byK[k]);
      ks.forEach((k,j)=>rTile(x,byK[k].n,fv(k,p[k]),`${MUNC[p.mun]||p.mun}: ${fv(k,munMed(k,p.mun))} · RMVRC: ${fv(k,rmMed(k))}`,RM+PAD+(j%2)*(tw+12),y+66+Math.floor(j/2)*104,tw,94));
      const px=RM+PAD+2*tw+12+40, pw=CW-2*PAD-2*tw-12-40;
      x.textAlign='left'; x.fillStyle=RC.fg; x.font='700 19px '+FB; x.fillText('Pirâmide etária (% dos moradores)',px,y+84); x.fillStyle=RC.mu; x.font='16px '+FB; x.fillText('tracejado = perfil da RMVRC',px+pw-200,y+84);
      if(p.pm&&(d3.sum(p.pm)+d3.sum(p.pf))>0) pyramidCanvas(x,p,px,y+100,pw,hc-120); else { x.fillStyle=RC.mu; x.font='18px '+FB; x.fillText('Sem dados de idade para este setor (sigilo do IBGE).',px,y+130); }
      y+=hc+GAP; }
    // índices: setor, bairro, mediana
    { const rows=IND.filter(i=>i.ax==='ind'||i.ax==='gov'), half=Math.ceil(rows.length/2), hc=70+34+half*58+16; need(hc);
      rCard(x,RM,y,CW,hc); rHead(x,'gov','Índices do setor','IVSA e prioridade territorial (Laboratório) · setor'+(temB?', bairro':'')+' e mediana da RMVRC',RM+PAD,y+46,CW);
      const cw2=(CW-2*PAD-60)/2;
      for(let c=0;c<2;c++){ const cx=RM+PAD+c*(cw2+60); x.fillStyle=RC.mu; x.font='700 14px '+FB; x.textAlign='right'; x.fillText('SETOR',cx+cw2*.64,y+92); if(temB) x.fillText('BAIRRO',cx+cw2*.82,y+92); x.fillText('MEDIANA',cx+cw2,y+92); x.textAlign='left';
        rows.slice(c*half,(c+1)*half).forEach((i,j)=>barRow(x,cx,y+130+j*58,cw2,i,p,temB?B:null)); }
      y+=hc+GAP; }
    // pontos de atenção e destaques
    const chips=(list,bg,fg,tit,sub,vazio)=>{ x.font='600 19px '+FB; const maxW=CW-2*PAD; let lines=1, cx=0; const items=list.map(e=>{ const t=`${e.i.n}: ${fv(e.i.k,p[e.i.k])}`, tw=x.measureText(t).width+24; if(cx+tw>maxW&&cx>0){ lines++; cx=0; } const o={t,tw,l:lines-1,x:cx}; cx+=tw+10; return o; });
      const hc=70+(list.length?lines*44:34)+14; need(hc); rCard(x,RM,y,CW,hc); rHead(x,null,tit,sub,RM+PAD,y+46,CW);
      if(!list.length){ x.fillStyle=RC.mu; x.font='19px '+FB; x.fillText(vazio,RM+PAD,y+92); }
      else for(const o of items){ const yy=y+72+o.l*44; rRR(x,RM+PAD+o.x,yy,o.tw,34,8); x.fillStyle=bg; x.fill(); x.fillStyle=fg; x.font='600 19px '+FB; x.textAlign='left'; x.fillText(o.t,RM+PAD+o.x+12,yy+24); }
      y+=hc+GAP; };
    chips(bad,RC.badb,RC.badf,'Pontos de atenção','indicadores em que o setor está entre os 20% piores da RMVRC','Nenhum indicador entre os 20% piores.');
    chips(good,RC.goodb,RC.goodf,'Destaques positivos','indicadores em que o setor está entre os 20% melhores','Nenhum indicador entre os 20% melhores.');
    // ODS ligados aos pontos de atenção
    { const ns=[...new Set(bad.flatMap(e=>(typeof IND_ODS!=='undefined'&&IND_ODS[e.i.k])||[]))].sort((a,b)=>a-b), os=ns.map(n=>ODS.find(o=>o.n===n)).filter(Boolean);
      if(os.length){ const per=3, hc=70+Math.ceil(os.length/per)*50+12; need(hc); rCard(x,RM,y,CW,hc); rHead(x,null,'Objetivos de Desenvolvimento Sustentável','ODS ligados aos pontos de atenção do setor',RM+PAD,y+46,CW);
        const cw=(CW-2*PAD)/per; os.forEach((o,j)=>{ const cx=RM+PAD+(j%per)*cw, cy=y+70+Math.floor(j/per)*50; rRR(x,cx,cy,40,40,6); x.fillStyle=o.c; x.fill(); x.fillStyle='#fff'; x.font='800 20px '+FD; x.textAlign='center'; x.fillText(String(o.n),cx+20,cy+28); x.textAlign='left'; x.fillStyle=RC.fg; x.font='600 19px '+FB; let t=o.t; while(x.measureText(t).width>cw-60&&t.length>6) t=t.slice(0,-2); x.fillText(t,cx+52,cy+27); });
        y+=hc+GAP; } }
    // notas de leitura
    { const notas=['“20% piores” e “20% melhores” indicam a posição do setor entre todos os setores da RMVRC com dado no indicador; a cor das barras e dos círculos segue a mesma comparação, em cinco faixas.',
        'Medianas do município consideram os setores urbanos; a mediana da RMVRC considera todos os setores com dado.',
        'Moradores em APP, em suscetibilidade a inundação e nas manchas de cheia são estimativas: população do setor × fração da área. Não localizam pessoas nem edificações.',
        'Distâncias são em linha reta, do centro do setor ao equipamento mais próximo dentro da RMVRC.',
        ...(typeof satNote==='function'&&satNote(p)?[satNote(p)]:[]),
        'Fórmulas, fontes e aferição de cada indicador estão nas páginas Metodologia e Método e fontes do Atlas.'];
      x.font='17px '+FB; const tw=CW-2*PAD-22, hs=notas.map(t=>wrapText(x,t,tw).length*22+8), hc=70+d3.sum(hs)+10; need(hc);
      rCard(x,RM,y,CW,hc); rHead(x,null,'Como ler este relatório','',RM+PAD,y+46,CW); let ty=y+88; x.textAlign='left';
      notas.forEach((t,j)=>{ x.fillStyle=RC.ochre; x.beginPath(); x.arc(RM+PAD+6,ty-6,4,0,2*Math.PI); x.fill(); x.fillStyle=RC.fg; x.font='17px '+FB; rWrap(x,t,RM+PAD+22,ty,tw,22); ty+=hs[j]; });
      y+=hc+GAP; }
    // numeração e PDF
    pages.forEach((c,j)=>{ const g=c.getContext('2d'); g.fillStyle='#56607a'; g.font='18px Arial'; g.textAlign='right'; g.fillText(`página ${j+1} de ${pages.length}`, RW-RM, RH-48); });
    window.__repInfo={pages:pages.length, esc:escN, mpp:sc._mpp};
    window.__repPages=pages;
    const pagesImg=[];
    for(const cv of pages) pagesImg.push(new Uint8Array(await (await canvasBlob(cv,'image/jpeg',.92)).arrayBuffer()));
    const pdf=buildPDF(pagesImg.map(b=>({w:595,h:842,content:'q 595 0 0 842 0 0 cm /Im1 Do Q',images:[{name:'Im1',bytes:b,w:RW,h:RH}]})));
    const base=(p.bairro?'relatorio_bairro_'+p.bairro:'relatorio_setor_'+p.id).normalize('NFD').replace(/[^A-Za-z0-9]+/g,'_').toLowerCase().replace(/_+$/,'');
    await saveFile(base+(p.bairro?'_setor_'+p.id.slice(-4):'')+'.pdf', pdf);
  }catch(e){ console.error(e); window.__repErr=String(e&&e.stack||e); say('Não foi possível montar o relatório.'); }
}
