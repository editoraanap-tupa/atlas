# precisão de escala e completude das exportações: mapa em PDF/PNG, mapa do bairro e relatório do setor
def _x(a,b,n=1):
    global H
    assert H.count(a)==n,(H.count(a),a[:90]); H=H.replace(a,b)
# ---- 1. escala: elipsoide GRS80/WGS84 na latitude do centro da vista
_x("const R_T=6371008.8, LAT0=proj.invert([W/2,H/2])[1]*Math.PI/180;",
"""const R_T=6371008.8, LAT0=proj.invert([W/2,H/2])[1]*Math.PI/180;
// comprimento de 1 grau de longitude e de latitude no elipsoide (m), na latitude f (rad)
const mLonDeg=f=>111412.84*Math.cos(f)-93.5*Math.cos(3*f)+0.118*Math.cos(5*f);
const mLatDeg=f=>111132.92-559.82*Math.cos(2*f)+1.175*Math.cos(4*f)-0.0023*Math.cos(6*f);
// latitude do centro da vista atual e metros por unidade do mapa (direção leste-oeste) nessa latitude
function viewLat(){ const t=d3.zoomTransform(svg.node()); const q=proj.invert([(W/2-t.x)/t.k,(H/2-t.y)/t.k]); return (q&&isFinite(q[1])?q[1]:LAT0*180/Math.PI)*Math.PI/180; }
const mPerUnit=f=>mLonDeg(f)*(180/Math.PI)/proj.scale();
const sig3=v=>{ if(!(v>0)) return 0; const p=Math.pow(10,Math.max(0,Math.floor(Math.log10(v))-2)); return Math.round(v/p)*p; };
const fmtArea=a=>a==null?'—':(a<0.1?ptBR(d3.format(',.3f')(a)):a<10?ptBR(d3.format(',.2f')(a)):ptBR(fmt1(a)))+' km²';""")
_x("const mPerPx = R_T*Math.cos(LAT0)*(Math.PI/180)/(proj.scale()*Math.PI/180)/pxPerUnit;","const mPerPx = mPerUnit(viewLat())/pxPerUnit;")
# ---- 2. mapa em PDF/PNG
# sempre no tema claro (a cópia de estilos é síncrona: a tela não chega a mudar)
_x("  const node=svg.node();\n  const clone=node.cloneNode(true);","  const node=svg.node();\n  const _root=document.documentElement, _pt=_root.getAttribute('data-theme'); _root.setAttribute('data-theme','light');\n  const clone=node.cloneNode(true);")
_x("  const str=new XMLSerializer().serializeToString(clone);","  const str=new XMLSerializer().serializeToString(clone);\n  if(_pt==null) _root.removeAttribute('data-theme'); else _root.setAttribute('data-theme',_pt);")
_x("  const cv=document.createElement('canvas'); cv.width=PW; cv.height=PH; const ctx=cv.getContext('2d');\n  ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,PW,PH);\n  const i=byK[st.ind]",
   "  const cv=document.createElement('canvas'); cv.width=PW; cv.height=PH; let ctx=cv.getContext('2d');\n  ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,PW,PH);\n  const i=byK[st.ind]")
# descrição completa (sem cortar), em até 2 linhas
_x("  ctx.fillStyle='#56607a'; ctx.font='26px Arial'; ctx.fillText(`${bgr ? bgName.split(' · ')[1] : AX[i.ax].nome + ' · ' + i.d.replace(' Ver metodologia abaixo.','').replace(' Veja a página Metodologia.','')}`.slice(0,150), PM, PM+114);\n  ctx.fillText(filtroTxt(), PM, PM+146);",
"""  ctx.fillStyle='#56607a'; ctx.font='23px Arial';
  const _dsc=`${bgr ? bgName.split(' · ').slice(1).join(' · ') : AX[i.ax].nome + ' · ' + i.d.replace(' Ver metodologia abaixo.','').replace(' Veja a página Metodologia.','')}`, _dl=wrapText(ctx,_dsc,PW-2*PM), _hx=(_dl.length-1)*27;
  _dl.forEach((t,j)=>ctx.fillText(t, PM, PM+114+j*27)); ctx.fillText('Recorte: '+filtroTxt(), PM, PM+146+_hx);
  ctx.font='16px Arial';
  const _foot=[...wrapText(ctx,'Fontes: '+fontesTxt().join(' · ')+'.', PW-2*PM), ...wrapText(ctx,`Projeção de Mercator; coordenadas geográficas em SIRGAS 2000 (compatível com WGS 84); norte geográfico para cima. ${!bgr&&(i.k==='ivsa'||i.k.startsWith('ipt_'))?'Índice calculado com os pesos publicados na Metodologia. ':''}${bgr?'':binsArr.vs.length+' setores com dado no recorte. '}Elaboração: Prof. Dr. Ricardo Miranda dos Santos e Profa. Dra. Sandra Medina Benini · PPGAU-UNIVAG. Mapa gerado em ${hoje()}.`, PW-2*PM)], _fh=_foot.length*21;""")
_x("const fx=PM, fy=PM+176, fw=1560, fh=PH-fy-120;","const fx=PM, fy=PM+176+_hx, fw=1560, fh=PH-fy-(_fh+62);")
# coordenadas dos cantos em graus, minutos e segundos (sem "60 minutos")
_x("const dms=(v,pos,neg)=>{ const a=Math.abs(v), d=Math.floor(a), m=Math.round((a-d)*60); return `${d}°${String(m).padStart(2,'0')}'${v<0?neg:pos}`; };",
   "const dms=(v,pos,neg)=>{ let t=Math.round(Math.abs(v)*3600); const d=Math.floor(t/3600); t-=d*3600; const m=Math.floor(t/60), s=t-m*60; return `${d}°${String(m).padStart(2,'0')}'${String(s).padStart(2,'0')}\"${v<0?neg:pos}`; };")
# escala gráfica e numérica na latitude central da folha
_x("  const mPerPrintPx = R_T*Math.cos(LAT0)/proj.scale()/tr.k*vw/mw;","  const latC=viewLat(), mPerPrintPx = mPerUnit(latC)/tr.k*vw/mw; window.__mapInfo={lonA,latA,lonB,latB,mPerPrintPx,mw,mh,latC:latC*180/Math.PI,tela:mPerUnit(latC)/(Math.min(node.clientWidth/W,node.clientHeight/H)*tr.k),barra:document.querySelector('.scalebar .bars').style.width,rot:document.getElementById('sticks').textContent};")
_x("  ctx.textAlign='left'; ctx.fillStyle='#56607a'; ctx.fillText(`Escala aproximada 1:${ptBR(fmtN(Math.round(escala/1000)*1000))} (impresso em A4)`, cx, y+66);\n  y+=110;",
"""  ctx.textAlign='left'; ctx.fillStyle='#0f1d3a'; ctx.font='700 19px Arial'; ctx.fillText(`Escala numérica 1:${ptBR(fmtN(sig3(escala)))}`, cx, y+68);
  ctx.fillStyle='#56607a'; ctx.font='16px Arial';
  wrapText(ctx,`Vale para a folha A4 paisagem impressa em tamanho real (100%, sem "ajustar à página"). Em outro tamanho, use a escala gráfica. Exata na direção leste–oeste na latitude ${dms(latC*180/Math.PI,'N','S')}; na direção norte–sul e nas bordas da folha o desvio é menor que 1% (projeção de Mercator).`,colW).forEach((t,j)=>ctx.fillText(t,cx,y+92+j*20));
  ctx.font='18px Arial';
  y+=200;""")
# legenda completa: desenhada à parte e reduzida, se preciso, para caber sem cortar
_x("  // legenda\n  ctx.fillStyle='#0f1d3a'; ctx.font='700 20px Arial'; ctx.fillText('LEGENDA', cx, y); y+=34;",
"""  // legenda
  const _main=ctx, _y0=y-30, _lc=document.createElement('canvas'); _lc.width=Math.ceil(colW)+12; _lc.height=3600; ctx=_lc.getContext('2d'); ctx.translate(-cx+4,-_y0);
  ctx.fillStyle='#0f1d3a'; ctx.font='700 20px Arial'; ctx.fillText('LEGENDA', cx, y); y+=34;""")
_x("for(const [n,c] of L.slice(0,14)){","for(const [n,c] of L){")
_x("""  if(on('mun-on')){ ctx.strokeStyle='#0f1d3a'; ctx.lineWidth=3; ctx.setLineDash([10,6]);""",
"""  const _ln=(col,w,dash,txt)=>{ ctx.strokeStyle=col; ctx.lineWidth=w; ctx.setLineDash(dash||[]); ctx.beginPath(); ctx.moveTo(cx,y-7); ctx.lineTo(cx+34,y-7); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle='#0f1d3a'; ctx.fillText(txt, cx+48, y); y+=32; };
  if(on('bac-on')) _ln('#b10026',5,null,'Bacia hidrográfica (IBGE)');
  if(on('sbac-on')) _ln('#e31a1c',3,[9,5],'Sub-bacia (IBGE)');
  if(on('mbac-on')) _ln('#6a1b9a',3,null,'Microbacia urbana (ANADEM)');
  if(on('utm-on')) _ln('#56607a',1.5,null,'Grade UTM · SIRGAS 2000, fuso 21 S');
  if(on('mun-on')){ ctx.strokeStyle='#0f1d3a'; ctx.lineWidth=3; ctx.setLineDash([10,6]);""")
_x("  // rodapé\n  ctx.fillStyle='#56607a'; ctx.font='18px Arial'; ctx.textAlign='left';",
"""  { const used=y-_y0+10, foot0=fy+fh, avail=foot0-_y0, fz=Math.min(1,avail/used); ctx=_main; ctx.drawImage(_lc,0,0,_lc.width,Math.ceil(used),cx-4,_y0,_lc.width*fz,Math.ceil(used)*fz); }
  // rodapé
  ctx.fillStyle='#56607a'; ctx.font='18px Arial'; ctx.textAlign='left';""")
_a=H.find("  // rodapé\n  ctx.fillStyle='#56607a'; ctx.font='18px Arial'; ctx.textAlign='left';"); _b=H.find("  return cv;",_a); assert 0<_a<_b
H=H[:_a]+"  // rodapé (ancorado na base da folha; a moldura do mapa já reservou o espaço)\n  ctx.fillStyle='#56607a'; ctx.font='16px Arial'; ctx.textAlign='left';\n  _foot.forEach((t,j)=>ctx.fillText(t, PM, PH-24-(_foot.length-1-j)*21));\n"+H[_b:]
# ---- 3. mapa do bairro em metros (escala exata na latitude do bairro)
_x("""  let wx=(b[2]-b[0])*KCOS, hy=(b[3]-b[1]); const mn=0.004; wx=Math.max(wx,mn); hy=Math.max(hy,mn);
  let cx=(b[0]+b[2])/2, cy=(b[1]+b[3])/2; wx*=1+2*pad; hy*=1+2*pad;
  const asp=W2/H2; if(wx/hy<asp) wx=hy*asp; else hy=wx/asp;
  const lon0=cx-wx/KCOS/2, lon1=cx+wx/KCOS/2, lat0=cy-hy/2, lat1=cy+hy/2, s=W2/wx;
  const P=(lon,lat)=>[(lon-lon0)*KCOS*s, (lat1-lat)*s];""",
"""  let cx=(b[0]+b[2])/2, cy=(b[1]+b[3])/2; const _ph=cy*Math.PI/180, MX=mLonDeg(_ph), MY=mLatDeg(_ph);
  let wx=(b[2]-b[0])*MX, hy=(b[3]-b[1])*MY; const mn=440; wx=Math.max(wx,mn); hy=Math.max(hy,mn); wx*=1+2*pad; hy*=1+2*pad;
  const asp=W2/H2; if(wx/hy<asp) wx=hy*asp; else hy=wx/asp;
  const lon0=cx-wx/MX/2, lon1=cx+wx/MX/2, lat0=cy-hy/MY/2, lat1=cy+hy/MY/2, s=W2/wx;
  const P=(lon,lat)=>[(lon-lon0)*MX*s, (lat1-lat)*MY*s];""")
_x("const mpp=wx*111320/W2,","const mpp=wx/W2; cv._mpp=mpp; const")
# ---- 4. ficha: área com casas decimais suficientes; pontos de atenção sem os índices compostos
_x("${ptBR(fmt1(p.area))} km²","${fmtArea(p.area)}",2)
_x("const ev=IND.filter(i=>i.pol!=='n'&&i.k!=='ivsa'&&p[i.k]!=null)","const ev=IND.filter(i=>i.pol!=='n'&&i.k!=='ivsa'&&!i.k.startsWith('ipt_')&&p[i.k]!=null)",2)
# ---- 5. relatório do setor/bairro: nada cortado, páginas conforme o conteúdo
_a=H.find('function repHeader(ctx, p, title, page, pages, kind){'); _b=H.find('function gaugeCanvas(',_a); assert 0<_a<_b
H=H[:_a]+r"""function repHeader(ctx, p, title, kind){
  ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,RW,RH);
  ctx.fillStyle='#001640'; ctx.fillRect(0,0,RW,210); ctx.fillStyle='#ffc000'; ctx.fillRect(0,210,RW,5);
  ctx.fillStyle='#ffc000'; ctx.font='700 24px Arial'; ctx.textAlign='left'; ctx.fillText('ATLAS SOCIOAMBIENTAL · '+ATLAS_NOME.toUpperCase()+' · RELATÓRIO '+(kind==='b'?'DO BAIRRO':'DO SETOR'), RM, 72);
  ctx.fillStyle='#ffffff'; ctx.font='700 56px Arial'; let tt=title; while(ctx.measureText(tt).width>RW-2*RM&&tt.length>8){ ctx.font=`700 ${parseInt(ctx.font.match(/(\d+)px/)[1])-4}px Arial`; if(parseInt(ctx.font.match(/(\d+)px/)[1])<30) break; } ctx.fillText(tt, RM, 140);
  ctx.fillStyle='#bfcbe6'; ctx.font='24px Arial';
  ctx.fillText(`${p.mun} · ${kind==='b'?'setor selecionado':'setor'} ${p.id} (${p.sit.toLowerCase()}) · ${fmtArea(p.area)} · ${fv('pop',p.pop)} moradores · ${fv('pop',p.dppo)} domicílios`, RM, 186);
  ctx.fillStyle='#56607a'; ctx.font='18px Arial';
  const fl=wrapText(ctx,'Fontes: IBGE, Censo Demográfico 2022 (setores censitários) e BDiA (solos, geologia, bacias); SGB/CPRM (carta de suscetibilidade e setores de risco); ANA/UFRGS (ANADEM); Copernicus Sentinel-2 e GLO-30; USGS Landsat 9; MapBiomas col. 9; OpenStreetMap; CNES/DATASUS. Índices com os pesos publicados na Metodologia do Atlas.', RW-2*RM);
  fl.forEach((t,j)=>ctx.fillText(t, RM, RH-48-24*(fl.length-j)));
  ctx.fillText(`Elaboração: Prof. Dr. Ricardo Miranda dos Santos e Profa. Dra. Sandra Medina Benini · PPGAU-UNIVAG · gerado em ${hoje()}`, RM, RH-48);
}
function sectionTitle(ctx, t, x, y){ ctx.fillStyle='#9a6f00'; ctx.font='700 22px Arial'; ctx.textAlign='left'; ctx.fillText(t.toUpperCase(), x, y); ctx.fillStyle='#9a6f00'; ctx.fillRect(x, y+10, 50, 3); }
// localização do setor dentro do seu município (sempre contém o setor, urbano ou rural), com escala
function locator(ctx, f, x, y, w, h){
  ctx.fillStyle='#f1f4fa'; ctx.fillRect(x,y,w,h);
  const mf=MUN.features.find(m=>m.properties.nome===f.properties.mun); const b=featBBox(mf?[mf]:F);
  const ph=(b[1]+b[3])/2*Math.PI/180, MX=mLonDeg(ph), MY=mLatDeg(ph);
  const s=Math.min((w-44)/((b[2]-b[0])*MX),(h-44)/((b[3]-b[1])*MY));
  const ox=x+(w-(b[2]-b[0])*MX*s)/2, oy=y+(h-(b[3]-b[1])*MY*s)/2;
  const P=(lon,lat)=>[ox+(lon-b[0])*MX*s, oy+(b[3]-lat)*MY*s];
  const tr=g=>{ ctx.beginPath(); for(const p of ringsOf(g)) for(const r of p){ r.forEach(([a,c],i)=>{ const q=P(a,c); i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]); }); ctx.closePath(); } };
  ctx.save(); ctx.beginPath(); ctx.rect(x,y,w,h); ctx.clip();
  if(mf){ tr(mf.geometry); ctx.fillStyle='#ffffff'; ctx.fill(); }
  ctx.fillStyle='#c3cbd9'; for(const g of F){ if(g.properties.sit!=='Urbana') continue; const bb=g._bb||(g._bb=featBBox([g])); if(bb[2]<b[0]||bb[0]>b[2]||bb[3]<b[1]||bb[1]>b[3]) continue; tr(g.geometry); ctx.fill(); }
  ctx.strokeStyle='#2f7fc1'; for(const hh of HL.filter(q=>q.properties.t==='r')){ ctx.lineWidth=hh.properties.n==='Rio Cuiabá'?3:1.5; ctx.beginPath(); hh.geometry.coordinates.forEach(([a,c],i)=>{ const q=P(a,c); i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]); }); ctx.stroke(); }
  ctx.setLineDash([8,5]); ctx.strokeStyle='#0f1d3a'; ctx.lineWidth=1.6; for(const m of MUN.features){ tr(m.geometry); ctx.stroke(); } ctx.setLineDash([]);
  tr(f.geometry); ctx.fillStyle='#d6332a'; ctx.fill(); ctx.strokeStyle='#7a1410'; ctx.lineWidth=2; ctx.stroke();
  const bb=featBBox([f]), c=P((bb[0]+bb[2])/2,(bb[1]+bb[3])/2); ctx.strokeStyle='#d6332a'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(c[0],c[1],18,0,2*Math.PI); ctx.stroke();
  // escala
  const mpp=1/s, target=w*.3*mpp, p10=Math.pow(10,Math.floor(Math.log10(target))), nice=[1,2,5,10].map(q=>q*p10).filter(q=>q<=target).pop()||p10, bw=nice/mpp;
  ctx.fillStyle='rgba(255,255,255,.88)'; ctx.fillRect(x+8,y+h-44,bw+24,36); ctx.fillStyle='#0f1d3a'; ctx.fillRect(x+16,y+h-18,bw,4); ctx.font='600 16px Arial'; ctx.textAlign='left';
  ctx.fillText(nice>=1000?ptBR(fmt1(nice/1000)).replace(/,0$/,'')+' km':fmtN(nice)+' m', x+16, y+h-24);
  ctx.restore();
  ctx.strokeStyle='#c8d0ca'; ctx.lineWidth=2; ctx.strokeRect(x,y,w,h);
  ctx.fillStyle='#56607a'; ctx.font='18px Arial'; ctx.textAlign='left'; ctx.fillText('Localização em '+f.properties.mun, x, y+h+26); ctx.fillText('cinza: área urbana · tracejado: divisa municipal', x, y+h+50);
}
"""+H[_b:]
_a=H.find('async function sectorReport(f){'); _b=H.find('\n// -------',_a); assert 0<_a<_b
H=H[:_a]+r"""async function sectorReport(f){
  const p=f.properties, B=bairroDe(f), temB=!!p.bairro, i0=byK[st.ind], kind=temB?'b':'s';
  say('Montando o relatório…', 0);
  try{
    const title=temB ? p.bairro : (p.dist||'Setor')+' · setor '+p.id.slice(-4);
    const pages=[], BOT=RH-150;
    const newPage=()=>{ const c=document.createElement('canvas'); c.width=RW; c.height=RH; const g=c.getContext('2d'); repHeader(g,p,title,kind); pages.push(c); return g; };
    // ---------- página 1: contexto, mapa do bairro, localização, IVSA ----------
    let x=newPage(), y=262;
    x.fillStyle='#56607a'; x.font='20px Arial'; x.textAlign='left';
    const ctxl=[p.fcu?'Favela ou comunidade urbana: '+p.fcu:'', p.solo?'Solo predominante: '+p.solo:'', p.micro?'Microbacia: '+p.micro:'', p.subbac?'Sub-bacia: '+p.subbac.replace(/^Bacia (do |da |de )?/,''):'', p.bac||''].filter(Boolean).join(' · ');
    if(ctxl){ wrapText(x,ctxl,RW-2*RM).forEach(t=>{ x.fillText(t,RM,y); y+=26; }); y+=20; }
    sectionTitle(x, temB?`Setores censitários do bairro (${B.length})`:'Setor censitário', RM, y); sectionTitle(x, 'Localização', 1080, y); y+=34;
    const sc=document.createElement('canvas'); sc.width=940; sc.height=820; drawBairroMap(sc,f,{lw:3,font:20}); x.drawImage(sc, RM, y);
    const escN=sig3(sc._mpp*1000/(210/RW));
    // legenda do indicador usado nas cores
    let ly=y+850; x.fillStyle='#0f1d3a'; x.font='700 20px Arial'; x.fillText(`Cores: ${i0.n}${i0.u&&i0.u!=='%'?' ('+i0.u+')':''} · ${st.cls==='q'?'quintis':'intervalos iguais'} do recorte: ${filtroTxt()}`, RM, ly); ly+=12;
    const {th,c,ext}=binsArr, edges=[ext[0],...th,ext[1]];
    x.font='18px Arial'; c.forEach((col,j)=>{ const lx=RM+j*160; x.globalAlpha=Math.max(.35,OPA.set/100); x.fillStyle=col; x.fillRect(lx,ly+10,26,20); x.globalAlpha=1; x.fillStyle='#0f1d3a'; x.fillText(`${fv(i0.k,edges[j])}–${fv(i0.k,edges[j+1])}`, lx+32, ly+26); });
    x.fillStyle='#c9cfca'; x.fillRect(RM+c.length*160,ly+10,26,20); x.fillStyle='#0f1d3a'; x.fillText('sem dado', RM+c.length*160+32, ly+26);
    x.fillStyle='#56607a'; x.fillText('Contorno escuro: setor selecionado · números: final do código de cada setor · cinza: outros bairros · azul: rios e córregos', RM, ly+58);
    x.fillText(`Norte para cima. Escala gráfica no mapa; escala numérica 1:${ptBR(fmtN(escN))} na folha A4 impressa em tamanho real (100%).`, RM, ly+84);
    const eqOn=Object.entries(EQC).filter(([k])=>document.getElementById('eq-'+k)?.checked);
    if(eqOn.length){ let ex=RM; x.font='18px Arial'; for(const [k,v] of eqOn){ const tw=x.measureText(v.n).width+44; if(ex+tw>RW-RM) break; const p2=new Path2D(sym(v.s,9)); x.save(); x.translate(ex+10,ly+104); x.fillStyle=v.c; x.fill(p2); x.restore(); x.fillStyle='#56607a'; x.fillText(v.n, ex+26, ly+110); ex+=tw; } ly+=26; }
    locator(x, f, 1080, y, 484, 484);
    // IVSA do setor
    sectionTitle(x, 'Vulnerabilidade do setor (IVSA)', 1080, y+590);
    gaugeCanvas(x, 1180, y+730, 80, p.ivsa);
    x.fillStyle='#0f1d3a'; x.font='700 64px Arial'; x.fillText(p.ivsa==null?'—':ptBR(fmt1(p.ivsa)), 1290, y+720);
    if(p.ivsa!=null){ const j=d3.bisectRight(IVSA_Q,p.ivsa); x.fillStyle=ramp5(j); x.fillRect(1290,y+736,270,36); x.fillStyle=j<2?'#3a2a00':'#fff'; x.font='700 20px Arial'; x.fillText('Vulnerabilidade '+CLASSE[j].toLowerCase(), 1300, y+761);
      const pos=IVSA_ALL.length-d3.bisectLeft(IVSA_ALL,p.ivsa); x.fillStyle='#56607a'; x.font='18px Arial'; x.fillText(`${pos}º mais vulnerável de ${IVSA_ALL.length}`, 1290, y+800); }
    else { x.fillStyle='#56607a'; x.font='18px Arial'; x.fillText('Sem índice: menos de 50 moradores ou dados insuficientes.', 1080, y+800); }
    if(temB&&B.length>1){ const vb=agg(B,byK.ivsa); x.fillStyle='#0f1d3a'; x.font='20px Arial'; x.fillText(`IVSA médio do bairro: ${fv('ivsa',vb)}`, 1080, y+834); }
    y=ly+130;
    // resumo do bairro
    if(temB){ sectionTitle(x, 'Resumo do bairro', RM, y); y+=50;
      const res=[['Setores',String(B.length)],['Moradores',fv('pop',d3.sum(B,g=>g.properties.pop))],['Domicílios',fv('pop',d3.sum(B,g=>g.properties.dppo))],['Área',fmtArea(d3.sum(B,g=>g.properties.area))],['Renda média',fv('renda',agg(B,byK.renda))],['Esgoto na rede',fv('esgoto',agg(B,byK.esgoto))]];
      res.forEach(([k,v],j)=>{ const cx=RM+(j%3)*490, cy=y+Math.floor(j/3)*70; x.fillStyle='#56607a'; x.font='18px Arial'; x.fillText(k.toUpperCase(), cx, cy); x.fillStyle='#0f1d3a'; x.font='700 32px Arial'; x.fillText(v, cx, cy+36); });
      y+=160; }
    // pontos de atenção e destaques do setor (todos; continuam na página seguinte se preciso)
    const ev=IND.filter(i=>i.pol!=='n'&&i.k!=='ivsa'&&!i.k.startsWith('ipt_')&&p[i.k]!=null).map(i=>({i,c:cond(i,p[i.k])}));
    const bad=ev.filter(e=>e.c<=.2).sort((a,b)=>a.c-b.c), good=ev.filter(e=>e.c>=.8).sort((a,b)=>b.c-a.c);
    const chips=(list,bg,fg,tit,vazio)=>{ if(y+110>BOT){ x=newPage(); y=262; }
      sectionTitle(x, tit, RM, y); y+=58;
      if(!list.length){ x.fillStyle='#56607a'; x.font='21px Arial'; x.fillText(vazio, RM, y); y+=50; return; }
      let cx=RM; for(const e of list){ x.font='600 21px Arial'; const t=`${e.i.n}: ${fv(e.i.k,p[e.i.k])}`; const tw=x.measureText(t).width+26;
        if(cx+tw>RW-RM){ cx=RM; y+=46; }
        if(y>BOT){ x=newPage(); y=262; sectionTitle(x, tit+' (continuação)', RM, y); y+=58; cx=RM; x.font='600 21px Arial'; }
        x.fillStyle=bg; x.fillRect(cx,y-28,tw,38); x.fillStyle=fg; x.fillText(t,cx+13,y-2); cx+=tw+10; }
      y+=62; };
    chips(bad,'#fbe3df','#9b2415','Pontos de atenção do setor (entre os 20% piores da RMVRC)','Nenhum indicador entre os 20% piores.');
    chips(good,'#dff1e6','#1d6b3a','Destaques positivos do setor (entre os 20% melhores)','Nenhum indicador entre os 20% melhores.');
    // ---------- páginas de indicadores: duas colunas, quantas páginas forem necessárias ----------
    x=newPage(); y=262; const cw=(RW-2*RM-70)/2;
    x.fillStyle='#56607a'; x.font='18px Arial'; x.textAlign='left';
    x.fillText(`Colunas: valor do setor (negrito)${temB&&B.length>1?', do bairro':''} e mediana dos setores da RMVRC. Barra do setor: amarelo = melhor, vermelho = pior; marcador vertical = mediana.`, RM, y); y+=44;
    let topY=y, col=0, yy=topY; const cxOf=()=>RM+col*(cw+70);
    const head=()=>{ const cx=cxOf(); x.fillStyle='#56607a'; x.font='700 15px Arial'; x.textAlign='right'; x.fillText('SETOR', cx+cw*.64, yy); if(temB&&B.length>1) x.fillText('BAIRRO', cx+cw*.82, yy); x.fillText('MEDIANA', cx+cw, yy); x.textAlign='left'; yy+=40; };
    const adv=()=>{ col++; if(col>1){ x=newPage(); col=0; topY=262; } yy=topY; head(); };
    head();
    for(const ax of ['ind','gov','amb','ace','ren','san','ent','dem']){ const rows=IND.filter(i=>i.ax===ax&&!['renda_med','arv5'].includes(i.k)); if(!rows.length||!AX[ax]) continue;
      if(yy+50+56>BOT) adv();
      sectionTitle(x, AX[ax].nome, cxOf(), yy); yy+=50;
      for(const i of rows){ if(yy+24>BOT){ adv(); sectionTitle(x, AX[ax].nome+' (continuação)', cxOf(), yy); yy+=50; } barRow(x, cxOf(), yy, cw, i, p, temB?B:null); yy+=56; }
      yy+=12; }
    if(p.pm && (d3.sum(p.pm)+d3.sum(p.pf))>0){ if(yy+500>BOT) adv();
      sectionTitle(x, 'Pirâmide etária do setor', cxOf(), yy); x.fillStyle='#56607a'; x.font='18px Arial'; x.fillText('% dos moradores; tracejado = perfil da RMVRC', cxOf(), yy+40); pyramidCanvas(x, p, cxOf(), yy+56, cw, 420); }
    // numeração e PDF
    pages.forEach((c,j)=>{ const g=c.getContext('2d'); g.fillStyle='#56607a'; g.font='18px Arial'; g.textAlign='right'; g.fillText(`página ${j+1} de ${pages.length}`, RW-RM, RH-48); });
    window.__repInfo={pages:pages.length, esc:escN, mpp:sc._mpp};
    const pagesImg=[];
    for(const cv of pages) pagesImg.push(new Uint8Array(await (await canvasBlob(cv,'image/jpeg',.9)).arrayBuffer()));
    const pdf=buildPDF(pagesImg.map(b=>({w:595,h:842,content:'q 595 0 0 842 0 0 cm /Im1 Do Q',images:[{name:'Im1',bytes:b,w:RW,h:RH}]})));
    const base=(temB?'relatorio_bairro_'+p.bairro:'relatorio_setor_'+p.id).normalize('NFD').replace(/[^A-Za-z0-9]+/g,'_').toLowerCase().replace(/_+$/,'');
    await saveFile(base+(temB?'_setor_'+p.id.slice(-4):'')+'.pdf', pdf);
  }catch(e){ console.error(e); say('Não foi possível montar o relatório.'); }
}
"""+H[_b:]
_x("// ------- relatório do setor: A4 retrato, 2 páginas, 200 dpi -------","// ------- relatório do setor: A4 retrato, 200 dpi, páginas conforme o conteúdo -------")

# símbolos dos equipamentos com tamanho constante na tela (antes cresciam sem limite ao aproximar o mapa)
_x("sym(EQC[e.c].s,Math.max(1.4,7.5/k))","sym(EQC[e.c].s,(7.5/k)*Math.min(1.7,1+Math.log2(Math.max(1,k))/8))")

# relatório: nome do indicador nunca encosta no valor (a fonte reduz até caber)
_x("const cV=x+w*.58, cB=x+w*.78, cM=x+w;\n  ctx.textAlign='left'; ctx.fillStyle='#0f1d3a'; ctx.font='22px Arial'; ctx.fillText(i.n, x, y);",
"""const cV=x+w*.64, cB=x+w*.82, cM=x+w;
  const c0=v==null?null:cond(i,v), tagT=c0!=null&&(c0<=.2||c0>=.8)?(c0<=.2?'20% piores':'20% melhores'):'';
  ctx.font='700 22px Arial'; const vW=ctx.measureText(fv(i.k,v)).width; ctx.font='700 15px Arial'; const tW=tagT?ctx.measureText(tagT).width+24:0;
  let fsN=22; ctx.font=fsN+'px Arial'; while(fsN>12&&ctx.measureText(i.n).width+tW>cV-x-vW-12){ fsN--; ctx.font=fsN+'px Arial'; }
  ctx.textAlign='left'; ctx.fillStyle='#0f1d3a'; ctx.fillText(i.n, x, y);""")
_x("ctx.textAlign='left'; ctx.font='22px Arial'; const nx=x+ctx.measureText(i.n).width+10;","ctx.textAlign='left'; ctx.font=fsN+'px Arial'; const nx=x+ctx.measureText(i.n).width+10;")
