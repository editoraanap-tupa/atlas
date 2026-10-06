# ================= bacias, solos, erosão, vegetação, grade UTM, fontes =================
import json as _j
H=open('/home/claude/d/atlas_rmvrc.html').read()
R2=_j.load(open('/home/claude/g/rast2.json')); BAC=_j.load(open('/home/claude/g/bacias_out.json'))
EM=_j.load(open('/home/claude/g/ero_mun.json')); MV=_j.load(open('/home/claude/g/mun_veg.json'))
def r4(old,new,n=1):
    global H
    c=H.count(old); assert c==n,(c,old[:100]); H=H.replace(old,new)
def nm_solo(n):
    if n=="CORPO D'ÁGUA CONTINENTAL": return "Corpo d'água continental"
    return ' '.join('-'.join(p.capitalize() for p in w.split('-')) for w in n.lower().split())
leg_solos=[[nm_solo(n.upper()),c] for n,c in R2['leg']['solos']]
R2['leg']['solos']=leg_solos
R2['leg']['erosao']=[['Estável (1,0–1,3)','#1a9850'],['Moderadamente estável (1,4–1,7)','#91cf60'],['Medianamente estável/vulnerável (1,8–2,2)','#fee08b'],['Moderadamente vulnerável (2,3–2,6)','#fc8d59'],['Vulnerável (2,7–3,0)','#d73027']]
dumps=lambda o:_j.dumps(o,ensure_ascii=False,separators=(',',':'))
MIC=_j.load(open('/home/claude/g/micro_out.json')); MICJ={'type':'FeatureCollection','features':MIC['feats']}
BACJ={'type':'FeatureCollection','features':BAC['bacias']}; SUBJ={'type':'FeatureCollection','features':BAC['sub']}
# ---- constantes
i=H.index('const RAST = '); j=H.index('\n',i)
H=H[:j+1]+'const RAST2 = '+dumps(R2)+';\nconst BACIAS = '+dumps(BACJ)+';\nconst SUBBACIAS = '+dumps(SUBJ)+';\nconst MICRO = '+dumps(MICJ)+';\n'+H[j+1:]
# ---- CSS
r4('footer a{color:var(--accent)}','''footer a{color:var(--accent)}
#map path.bac{fill:none;stroke:#b10026;stroke-width:2.8;vector-effect:non-scaling-stroke;stroke-linejoin:round;pointer-events:none}
#map path.sbac{fill:none;stroke:#e31a1c;stroke-width:1.3;stroke-dasharray:6 3;vector-effect:non-scaling-stroke;pointer-events:none}
:root[data-theme="dark"] #map path.bac{stroke:#ff5a5f}
#map text.bact{font-family:var(--f-display);font-weight:700;fill:#b10026;paint-order:stroke;stroke:var(--panel);stroke-linejoin:round;pointer-events:none;letter-spacing:.02em}
#map text.sbact{font-family:var(--f-body);font-weight:600;font-style:italic;fill:#c4161c;paint-order:stroke;stroke:var(--panel);stroke-linejoin:round;pointer-events:none}
#map path.mbac{fill:rgba(106,27,154,.06);stroke:#6a1b9a;stroke-width:1;vector-effect:non-scaling-stroke;pointer-events:none}
#map text.mbact{font-family:var(--f-body);font-weight:600;fill:#6a1b9a;paint-order:stroke;stroke:var(--panel);stroke-linejoin:round;pointer-events:none}
#map path.utm{fill:none;stroke:var(--fg);stroke-opacity:.35;stroke-width:.8;vector-effect:non-scaling-stroke;pointer-events:none}
#map text.utmt{font-family:var(--f-mono);fill:var(--fg);opacity:.75;paint-order:stroke;stroke:var(--panel);stroke-linejoin:round;pointer-events:none}
.mapfontes{padding:7px 14px 8px;border-top:1px solid var(--line);font-size:11.5px;line-height:1.4;color:var(--muted);background:var(--panel)}
.mapfontes b{color:var(--fg);font-weight:600}
.fml{display:block;margin-top:4px;font-family:var(--f-mono);font-size:12px;color:var(--fg);background:var(--panel-2);border:1px solid var(--line);border-radius:6px;padding:4px 8px}''')
# ---- camadas (fundo)
r4('      <div class="grp-t">Sobrepor</div>','''      <label class="opt" for="bg-solos"><input type="radio" name="bg" id="bg-solos" value="solos"><span>Solos predominantes<small>IBGE · pedologia 1:250.000</small></span><i class="sw2" style="background:linear-gradient(90deg,#e0863a,#7d5a8c,#f5ecb0,#a88b5b)"></i></label>
      <label class="opt" for="bg-erosao"><input type="radio" name="bg" id="bg-erosao" value="erosao"><span>Vulnerabilidade à erosão hídrica<small>método Crepani et al. (2001)</small></span><i class="sw2" style="background:linear-gradient(90deg,#1a9850,#91cf60,#fee08b,#fc8d59,#d73027)"></i></label>
      <label class="opt" for="bg-mbveg"><input type="radio" name="bg" id="bg-mbveg" value="mbveg"><span>Cobertura e uso da terra<small>MapBiomas coleção 9 · 2023</small></span><i class="sw2" style="background:linear-gradient(90deg,#1f8d49,#7dc975,#d6bc74,#edde8e,#f5b3c8,#d4271e)"></i></label>
      <div class="grp-t">Sobrepor</div>''')
r4('<label class="opt" for="mun-on">','''<label class="opt" for="bac-on"><input type="checkbox" id="bac-on"><span>Bacias hidrográficas<small>IBGE · bacias ottocodificadas</small></span></label>
      <label class="opt" for="sbac-on"><input type="checkbox" id="sbac-on"><span>Sub-bacias<small>IBGE · nível 6 (5 onde não há)</small></span></label>
      <label class="opt" for="mbac-on"><input type="checkbox" id="mbac-on"><span>Microbacias urbanas<small>delimitadas pelo MDT ANADEM</small></span></label>
      <label class="opt" for="utm-on"><input type="checkbox" id="utm-on"><span>Grade UTM<small>SIRGAS 2000 · fuso 21 S</small></span></label>
      <label class="opt" for="mun-on">''')
# ---- rodape do mapa com fontes
r4('      <div class="tip" id="tip" hidden></div>\n    </div>\n  </section>','      <div class="tip" id="tip" hidden></div>\n    </div>\n    <div class="mapfontes" id="mapfontes"></div>\n  </section>')
# ---- rasters regionais
r4("for(const k of ['ndvi','lst','inund','cheias','sgbc','cheias2']) rimg[k]=",
   "const RB2=RAST2.bounds, [jx0,jy0]=proj([RB2[0],RB2[1]]), [jx1,jy1]=proj([RB2[2],RB2[3]]);\nfor(const k of ['ndvi','lst','inund','cheias','sgbc','cheias2']) rimg[k]=")
r4("const gS = g.append('g');","for(const k of ['solos','erosao','mbveg']) rimg[k]=gR.append('image').attr('href',RAST2.img[k]).attr('x',jx0).attr('y',jy0).attr('width',jx1-jx0).attr('height',jy1-jy0).attr('preserveAspectRatio','none').attr('display','none');\nconst gS = g.append('g');")
# ---- bacias, sub-bacias e grade UTM
r4("gN.raise();","""// ------- bacias e sub-bacias (IBGE) -------
const gMb = g.append('g').attr('display','none');
gMb.selectAll('path').data(MICRO.features).join('path').attr('class','mbac').attr('d',path);
const mbLab = gMb.selectAll('text').data(MICRO.features).join('text').attr('class','mbact').attr('text-anchor','middle').text(f=>f.properties.nome.replace(/^Microbacia sem nome$/,'s/n'));
const gB = g.append('g').attr('display','none'), gSb = g.append('g').attr('display','none');
gSb.selectAll('path').data(SUBBACIAS.features).join('path').attr('class','sbac').attr('d',path);
gB.selectAll('path').data(BACIAS.features).join('path').attr('class','bac').attr('d',path);
const sbLab = gSb.selectAll('text').data(SUBBACIAS.features).join('text').attr('class','sbact').attr('text-anchor','middle').text(f=>f.properties.nome.replace(/^Bacia (do |da |de )?/,''));
const bLab = gB.selectAll('text').data(BACIAS.features).join('text').attr('class','bact').attr('text-anchor','middle').text(f=>f.properties.nome.toUpperCase());
function placeBac(k){
  mbLab.attr('x',f=>proj([f.properties.lx,f.properties.ly])[0]).attr('y',f=>proj([f.properties.lx,f.properties.ly])[1]).attr('font-size',10.5/k).attr('stroke-width',3/k)
    .attr('display',f=>{ const px=Math.sqrt(f.properties.area)*k*(proj.scale()/6371); return px>(f.properties.nome.startsWith('Córrego')||f.properties.nome.startsWith('Ribeirão')?55:95)?null:'none'; });
  bLab.attr('x',f=>proj([f.properties.lx,f.properties.ly])[0]).attr('y',f=>proj([f.properties.lx,f.properties.ly])[1]).attr('font-size',15/k).attr('stroke-width',4/k);
  sbLab.attr('x',f=>proj([f.properties.lx,f.properties.ly])[0]).attr('y',f=>proj([f.properties.lx,f.properties.ly])[1]).attr('font-size',11.5/k).attr('stroke-width',3/k)
    .attr('display',f=>{ const px=Math.sqrt(f.properties.area_rm)*k*(proj.scale()/6371)*1.0; return px>45?null:'none'; });
}
document.getElementById('mbac-on').addEventListener('change',e=>{ gMb.attr('display',e.target.checked?null:'none'); setFontes(); });
document.getElementById('bac-on').addEventListener('change',e=>{ gB.attr('display',e.target.checked?null:'none'); setFontes(); });
document.getElementById('sbac-on').addEventListener('change',e=>{ gSb.attr('display',e.target.checked?null:'none'); setFontes(); });
// ------- grade UTM (SIRGAS 2000 / UTM 21 S) -------
const UTM={a:6378137, f:1/298.257222101, k0:0.9996, lon0:-57};
function ll2utm(lon,lat){ const a=UTM.a,e2=UTM.f*(2-UTM.f),ep2=e2/(1-e2),k0=UTM.k0; const phi=lat*Math.PI/180, lam=(lon-UTM.lon0)*Math.PI/180;
  const N=a/Math.sqrt(1-e2*Math.sin(phi)**2), T=Math.tan(phi)**2, C=ep2*Math.cos(phi)**2, A=Math.cos(phi)*lam;
  const M=a*((1-e2/4-3*e2*e2/64-5*e2**3/256)*phi-(3*e2/8+3*e2*e2/32+45*e2**3/1024)*Math.sin(2*phi)+(15*e2*e2/256+45*e2**3/1024)*Math.sin(4*phi)-(35*e2**3/3072)*Math.sin(6*phi));
  const E=k0*N*(A+(1-T+C)*A**3/6+(5-18*T+T*T+72*C-58*ep2)*A**5/120)+500000;
  const Nn=k0*(M+N*Math.tan(phi)*(A*A/2+(5-T+9*C+4*C*C)*A**4/24+(61-58*T+T*T+600*C-330*ep2)*A**6/720))+10000000; return [E,Nn]; }
function utm2ll(E,Nn){ const a=UTM.a,e2=UTM.f*(2-UTM.f),ep2=e2/(1-e2),k0=UTM.k0; const e1=(1-Math.sqrt(1-e2))/(1+Math.sqrt(1-e2));
  const x=E-500000, y=Nn-10000000, M=y/k0, mu=M/(a*(1-e2/4-3*e2*e2/64-5*e2**3/256));
  const p1=mu+(3*e1/2-27*e1**3/32)*Math.sin(2*mu)+(21*e1*e1/16-55*e1**4/32)*Math.sin(4*mu)+(151*e1**3/96)*Math.sin(6*mu)+(1097*e1**4/512)*Math.sin(8*mu);
  const C1=ep2*Math.cos(p1)**2, T1=Math.tan(p1)**2, N1=a/Math.sqrt(1-e2*Math.sin(p1)**2), R1=a*(1-e2)/(1-e2*Math.sin(p1)**2)**1.5, D=x/(N1*k0);
  const lat=p1-(N1*Math.tan(p1)/R1)*(D*D/2-(5+3*T1+10*C1-4*C1*C1-9*ep2)*D**4/24+(61+90*T1+298*C1+45*T1*T1-252*ep2-3*C1*C1)*D**6/720);
  const lon=(D-(1+2*T1+C1)*D**3/6+(5-2*C1+28*T1-3*C1*C1+8*ep2+24*T1*T1)*D**5/120)/Math.cos(p1);
  return [UTM.lon0+lon*180/Math.PI, lat*180/Math.PI]; }
const gU = g.append('g').attr('display','none');
let utmStep=0;
function viewBoxVisible(){ const cw=svg.node().clientWidth||W, ch=svg.node().clientHeight||H, s=Math.min(cw/W,ch/H);
  return {x0:W/2-cw/(2*s), x1:W/2+cw/(2*s), y0:H/2-ch/(2*s), y1:H/2+ch/(2*s), s}; }
function drawUTM(){
  if(gU.attr('display')==='none') return;
  const t=d3.zoomTransform(svg.node()), k=t.k, vb=viewBoxVisible();
  const toMap=(vx,vy)=>[(vx-t.x)/k,(vy-t.y)/k];
  const m0=toMap(vb.x0,vb.y0), m1=toMap(vb.x1,vb.y1);
  const corners=[[m0[0],m0[1]],[m1[0],m0[1]],[m0[0],m1[1]],[m1[0],m1[1]]].map(p=>ll2utm(...proj.invert(p)));
  const E0=d3.min(corners,d=>d[0]),E1=d3.max(corners,d=>d[0]),N0=d3.min(corners,d=>d[1]),N1=d3.max(corners,d=>d[1]);
  const span=Math.min(E1-E0,N1-N0);
  const steps=[100,200,250,500,1000,2000,2500,5000,10000,20000,25000,50000,100000];
  const st=steps.find(q=>span/q<=7)||100000; utmStep=st;
  const pad=st, lines=[];
  for(let e=Math.floor((E0-pad)/st)*st;e<=E1+pad;e+=st) lines.push({t:'E',v:e,pts:d3.range(0,41).map(q=>utm2ll(e,N0-pad+(N1-N0+2*pad)*q/40))});
  for(let n=Math.floor((N0-pad)/st)*st;n<=N1+pad;n+=st) lines.push({t:'N',v:n,pts:d3.range(0,41).map(q=>utm2ll(E0-pad+(E1-E0+2*pad)*q/40,n))});
  gU.selectAll('path').data(lines).join('path').attr('class','utm').attr('d',d=>d3.line()(d.pts.map(p=>proj(p))));
  // rótulos na borda visível: E no topo, N à esquerda (posição em unidades do mapa, tamanho constante na tela)
  const px=1/(vb.s*k);            // 1 pixel de tela em unidades do mapa
  const yTop=m0[1]+16*px, xLeft=m0[0]+6*px;
  const fmtU=v=>ptBR(d3.format(',.0f')(v));
  const labs=[];
  for(const d of lines){
    const pp=d.pts.map(p=>proj(p));
    if(d.t==='E'){ // interseção com a linha horizontal y=yTop
      for(let i=1;i<pp.length;i++){ const a=pp[i-1],b=pp[i]; if((a[1]-yTop)*(b[1]-yTop)<=0 && a[1]!==b[1]){ const f=(yTop-a[1])/(b[1]-a[1]); const x=a[0]+f*(b[0]-a[0]); if(x>m0[0]+40*px&&x<m1[0]-20*px) labs.push({x:x+3*px,y:yTop,txt:fmtU(d.v)+' E',a:'start'}); break; } }
    } else {
      for(let i=1;i<pp.length;i++){ const a=pp[i-1],b=pp[i]; if((a[0]-xLeft)*(b[0]-xLeft)<=0 && a[0]!==b[0]){ const f=(xLeft-a[0])/(b[0]-a[0]); const y=a[1]+f*(b[1]-a[1]); if(y>m0[1]+30*px&&y<m1[1]-10*px) labs.push({x:xLeft,y:y-3*px,txt:fmtU(d.v)+' N',a:'start'}); break; } }
    }
  }
  gU.selectAll('text').data(labs).join('text').attr('class','utmt').attr('x',d=>d.x).attr('y',d=>d.y).attr('text-anchor',d=>d.a)
    .attr('font-size',10.5*px).attr('stroke-width',3*px).text(d=>d.txt);
  setFontes();
}
window.addEventListener('resize',()=>drawUTM());
let utmRaf=0; function schedUTM(){ if(utmRaf) return; utmRaf=requestAnimationFrame(()=>{utmRaf=0; drawUTM();}); }
document.getElementById('utm-on').addEventListener('change',e=>{ gU.attr('display',e.target.checked?null:'none'); drawUTM(); setFontes(); });
gN.raise();""")
r4("const zoom = d3.zoom().scaleExtent([.04,60]).on('zoom',e=>{ g.attr('transform',e.transform); placeLabels(e.transform.k); placeEq(e.transform.k); scaleBar(e.transform.k); });",
   "const zoom = d3.zoom().scaleExtent([.04,60]).on('zoom',e=>{ g.attr('transform',e.transform); placeLabels(e.transform.k); placeEq(e.transform.k); scaleBar(e.transform.k); placeBac(e.transform.k); schedUTM(); });")
r4("placeLabels(1); placeEq(1); scaleBar(1);","placeLabels(1); placeEq(1); scaleBar(1); placeBac(1); setFontes();")
# ---- fontes dinamicas
r4("function render(){","""// ------- fontes da base cartográfica em uso -------
const FONTE_BG={set:null,ndvi:'Vegetação: NDVI Sentinel-2 (Copernicus/ESA), 23/08/2026',lst:'Temperatura de superfície: Landsat 9 (USGS), 13/08/2026',inund:'Suscetibilidade a inundação: modelo HAND sobre Copernicus GLO-30 (ESA)',
  cheias:'Cheias do Rio Cuiabá: cotas SUDEC-MT, régua ANA 66260001; terreno Copernicus GLO-30',cheias2:'Cheias do Rio Cuiabá: cotas SUDEC-MT, régua ANA 66260001; terreno MDT ANADEM (ANA/UFRGS)',
  sgbc:'Suscetibilidade a inundação: Cartas de Suscetibilidade SGB/CPRM 1:25.000 (Cuiabá 2021; Várzea Grande)',solos:'Solos: IBGE, Base Contínua de Pedologia 1:250.000 (BDiA)',
  erosao:'Erosão: elaboração própria (Crepani et al., 2001) com IBGE BDiA (geologia, geomorfologia, pedologia 1:250.000) e MapBiomas coleção 9 (2023)',mbveg:'Cobertura e uso: MapBiomas coleção 9, ano 2023 (30 m)'};
function fontesTxt(){
  const on=id=>{ const e=document.getElementById(id); return e&&e.checked; };
  const f=['Setores censitários e indicadores: IBGE, Censo Demográfico 2022','Limites municipais: IBGE, malha municipal'];
  if(st.bg==='set'){ const i=byK[st.ind]; if(i.ax==='amb'||i.ax==='ace') f.push('Indicador: '+(FONTE_IND[i.k]||'elaboração própria')); }
  if(FONTE_BG[st.bg]) f.push(FONTE_BG[st.bg]);
  if(on('hid-on')||on('nmr-on')||on('nmc-on')) f.push('Hidrografia: OpenStreetMap (ODbL)');
  if(on('app-on')) f.push('APP: Lei 12.651/2012 sobre hidrografia OpenStreetMap');
  if(on('sgb-on')) f.push('Setores de risco: SGB/CPRM e Defesa Civil');
  if(on('fcu-on')) f.push('Favelas e comunidades urbanas: IBGE, Censo 2022');
  if(on('bac-on')||on('sbac-on')) f.push('Bacias: IBGE, Bacias Hidrográficas ottocodificadas (BHB250)');
  if(on('mbac-on')) f.push('Microbacias urbanas: elaboração própria com MDT ANADEM (ANA/UFRGS) e hidrografia OpenStreetMap');
  if(Object.keys(EQC).some(k=>on('eq-'+k))) f.push('Equipamentos: CNES/DATASUS e OpenStreetMap');
  if(on('utm-on')) f.push('Grade UTM: SIRGAS 2000, fuso 21 S'+(utmStep?`, intervalo de ${utmStep>=1000?ptBR(String(utmStep/1000))+' km':utmStep+' m'}`:''));
  return f;
}
function setFontes(){ const el=document.getElementById('mapfontes'); if(el) el.innerHTML='<b>Fontes:</b> '+fontesTxt().map(esc).join(' · ')+' · Elaboração: Santos &amp; Benini, PPGAU-UNIVAG (2026).'; }
document.getElementById('pane-cam').addEventListener('change',()=>setTimeout(setFontes,0));
function render(){""")
r4("  drawHist(); renderKpis(); renderCmp(); renderDetail(); renderTable();","  drawHist(); renderKpis(); renderCmp(); renderDetail(); renderTable(); setFontes();")
# rodape do mapa exportado
r4("  const foot=['Fontes: IBGE, Censo Demográfico 2022 (agregados por setores; malhas); OpenStreetMap (hidrografia, escolas, parques); CNES/DATASUS; Copernicus GLO-30; Sentinel-2; Landsat 9 (USGS).',",
   "  const foot=[...wrapText(ctx,'Fontes: '+fontesTxt().join(' · ')+'.', PW-2*PM)],\n    foot2=[")
r4("  foot.forEach((t,j)=>ctx.fillText(t, PM, PH-PM+4+j*26));","  foot.push(...foot2); const lh=foot.length>2?21:26; if(foot.length>2) ctx.font='16px Arial'; foot.forEach((t,j)=>ctx.fillText(t, PM, PH-PM+4+j*lh));")
# ---- legenda categorica (tela e export)
r4("  if(bgr&&st.bg==='cheias2'){","  if(bgr&&CATLEG[st.bg]){ rp.innerHTML=`<b>${CATLEG[st.bg][0]}</b><div class=\"chl\">`+CATLEG[st.bg][1].map(([n,c])=>`<span><i style=\"background:${c}\"></i>${esc(n)}</span>`).join('')+'</div>'; }\n  else if(bgr&&st.bg==='cheias2'){")
r4("  const RAMPS = {","  const CATLEG={solos:['Solos predominantes (IBGE, 1:250.000)',RAST2.leg.solos],erosao:['Vulnerabilidade natural à erosão hídrica (Crepani et al., 2001)',RAST2.leg.erosao],mbveg:['Cobertura e uso da terra · MapBiomas 2023',RAST2.leg.mbveg]};\n  const RAMPS = {")
r4("  } else if(st.bg==='cheias'){","  } else if({solos:1,erosao:1,mbveg:1}[st.bg]){\n    const L={solos:RAST2.leg.solos,erosao:RAST2.leg.erosao,mbveg:RAST2.leg.mbveg}[st.bg];\n    ctx.font='19px Arial'; for(const [n,c] of L.slice(0,14)){ ctx.globalAlpha=OPA.ras/100; sw(c,y); ctx.globalAlpha=1; ctx.fillStyle='#0f1d3a'; wrapText(ctx,n,colW-50).forEach((t,q)=>{ ctx.fillText(t,cx+48,y+q*24); y+=q?24:0; }); y+=30; }\n    ctx.font='21px Arial'; y+=6;\n  } else if(st.bg==='cheias'){")
r4("cheias2:'Cheias do Rio Cuiabá · cotas históricas, MDT ANADEM recalibrado', sgbc:","cheias2:'Cheias do Rio Cuiabá · cotas históricas, MDT ANADEM recalibrado', solos:'Solos predominantes · IBGE, pedologia 1:250.000', erosao:'Vulnerabilidade à erosão hídrica · Crepani et al. (2001)', mbveg:'Cobertura e uso da terra · MapBiomas 2023', sgbc:")
r4(",sgbc:'Carta SGB, classe alta: '+fv('sgb_alta',p.sgb_alta)+' da área'}[st.bg]",",sgbc:'Carta SGB, classe alta: '+fv('sgb_alta',p.sgb_alta)+' da área',solos:'Solo predominante: '+(p.solo||'—'),erosao:'Vulnerabilidade à erosão: '+fv('erosao',p.erosao),mbveg:'Vegetação nativa: '+fv('veg_nat',p.veg_nat)}[st.bg]")
# ---- indicadores novos
r4(" {k:'ndvi',ax:'amb',"," {k:'veg_nat',ax:'amb',n:'Vegetação nativa (MapBiomas)',u:'%',pol:'b',d:'Parte da área do setor (fora da água) coberta por vegetação nativa (formações florestal, savânica, campestre e áreas úmidas) no MapBiomas 2023. Disponível para toda a RMVRC.',w:'area'},\n {k:'erosao',ax:'amb',n:'Vulnerabilidade à erosão hídrica',u:'',pol:'r',d:'Índice de vulnerabilidade natural à perda de solo (1 = estável, 3 = vulnerável), média do setor. Método de Crepani et al. (2001).',w:'area'},\n {k:'eros_alta',ax:'amb',n:'Área moderadamente vulnerável ou vulnerável à erosão',u:'%',pol:'r',d:'Parte da área do setor com índice de vulnerabilidade à erosão ≥ 2,25.',w:'area'},\n {k:'ndvi',ax:'amb',")
r4("  if(k==='ndvi') return ptBR(d3.format('.2f')(v));","  if(k==='ndvi'||k==='erosao') return ptBR(d3.format('.2f')(v));")
r4("  {k:'sgb_alta', n:'Suscetibilidade (carta SGB)', s:1, env:1},","  {k:'sgb_alta', n:'Suscetibilidade (carta SGB)', s:1, env:1},\n  {k:'veg_nat', n:'Pouca vegetação nativa (MapBiomas)', s:-1, env:1},\n  {k:'erosao', n:'Vulnerabilidade à erosão', s:1, env:1},")
# ficha: solo e bacias
r4("${p.fcu?' · Favela/comunidade urbana: '+esc(p.fcu):''}</div>`;","${p.fcu?' · Favela/comunidade urbana: '+esc(p.fcu):''}${(p.solo||p.bac)?`<br>${p.solo?'Solo predominante: <b>'+esc(p.solo)+'</b>':''}${p.micro?' · Microbacia: '+esc(p.micro):''}${p.subbac?' · Sub-bacia: '+esc(p.subbac.replace(/^Bacia (do |da |de )?/,'')):''}${p.bac?' · '+esc(p.bac):''}`:''}</div>`;")
# ---- secao ambiente por municipio
ORD=['Cuiabá','Várzea Grande','Nossa Senhora do Livramento','Santo Antônio de Leverger','Acorizal','Chapada dos Guimarães','Campo Verde']
def br(x,d=1): return (f'{x:,.{d}f}').replace(',','#').replace('.',',').replace('#','.')
AOF={'Cuiabá':4327.448,'Várzea Grande':724.279,'Nossa Senhora do Livramento':5537.413,'Santo Antônio de Leverger':9469.139,'Acorizal':850.763,'Chapada dos Guimarães':6603.252,'Campo Verde':4770.631}
rows=''
for m in ORD:
    e=EM[m]; v=MV[m]; s1=e['solos'][0]
    rows+=f"<tr><td class='l'>{m}</td><td class='num'>{br(AOF[m],1)} km²</td><td class='num'>{br(v['veg'])}%</td><td class='l'>{nm_solo(s1[0])} ({br(s1[1])}%)</td><td class='num'>{br(e['vmed'],2)}</td><td class='num'>{br(e['ero'][3]+e['ero'][4])}%</td></tr>"
tot_area=sum(MV[m]['km2'] for m in ORD); tot_veg=sum(MV[m]['veg']*MV[m]['km2'] for m in ORD)/tot_area
bac_rows=''.join(f"<tr><td class='l'>{f['properties']['nome']}</td><td class='num'>{br(f['properties']['area_rm'],0)} km²</td><td class='num'>{br(100*f['properties']['area_rm']/tot_area)}%</td></tr>" for f in sorted(BAC['bacias'],key=lambda f:-f['properties']['area_rm']))
sub_top=''.join(f"<tr><td class='l'>{f['properties']['nome']}</td><td class='num'>{br(f['properties']['area_rm'],0)} km²</td></tr>" for f in sorted(BAC['sub'],key=lambda f:-f['properties']['area_rm'])[:12])
mic_rows=''.join(f"<tr><td class='l'>{f['properties']['nome']}</td><td class='num'>{br(f['properties']['area'],1)} km²</td><td class='num'>{br(f['properties']['urb'],1)} km²</td><td class='num'>{br(f['properties']['pct_urb'])}%</td></tr>" for f in sorted([f for f in MIC['feats'] if not f['properties']['nome'].startswith(('Microbacia','Afluente'))],key=lambda f:-f['properties']['urb'])[:25])
sec=f"""<div class="sec-h" id="ambiente" style="scroll-margin-top:calc(var(--tb) + 12px)"><span class="kick">Meio físico · toda a RMVRC</span><h2>Bacias, solos, erosão e vegetação</h2><p>Camadas disponíveis para os sete municípios: bacias e sub-bacias hidrográficas (IBGE), solos predominantes (IBGE, 1:250.000), vulnerabilidade natural à erosão hídrica (método de Crepani et al., 2001) e cobertura e uso da terra (MapBiomas 2023), com o percentual de vegetação nativa calculado para cada setor e município.</p></div>
<section class="block">
  <div class="kpis vk">
    <div class="kpi"><div class="lab">Vegetação nativa na RMVRC</div><div class="val">{br(tot_veg)}%</div><div class="sub">da área dos 7 municípios (MapBiomas 2023)</div></div>
    <div class="kpi"><div class="lab">Bacia do Rio Cuiabá</div><div class="val">{br(100*[f for f in BAC['bacias'] if f['properties']['nome']=='Bacia do Rio Cuiabá'][0]['properties']['area_rm']/tot_area)}%</div><div class="sub">do território metropolitano</div></div>
    <div class="kpi"><div class="lab">Sub-bacias delimitadas</div><div class="val">{len(BAC['sub'])}</div><div class="sub">IBGE, bacias ottocodificadas</div></div>
    <div class="kpi"><div class="lab">Área moderadamente vulnerável+</div><div class="val">{br(sum((EM[m]['ero'][3]+EM[m]['ero'][4])*MV[m]['km2'] for m in ORD)/tot_area)}%</div><div class="sub">índice de erosão ≥ 2,25</div></div>
  </div>
  <h3 style="margin:18px 0 8px;font:700 11.5px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)">Síntese por município</h3>
  <div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th class="l">Município</th><th>Área (IBGE)</th><th>Vegetação nativa</th><th class="l">Solo predominante (% da área)</th><th>Índice médio de erosão</th><th>Área moderadamente vulnerável ou vulnerável</th></tr></thead><tbody>{rows}</tbody></table></div>
  <div class="split" style="margin-top:18px">
    <div><h3>Bacias hidrográficas na RMVRC</h3><div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th class="l">Bacia</th><th>Área na RMVRC</th><th>% do território</th></tr></thead><tbody>{bac_rows}</tbody></table></div>
      <p class="msg" style="margin-top:8px">Áreas da bacia do Rio Cuiabá sem subdivisão no nível 6 do IBGE aparecem nas sub-bacias com o nome da própria bacia (curso principal e interbacias).</p></div>
    <div><h3>Maiores sub-bacias</h3><div class="tblwrap" style="max-height:none"><table class="dt"><thead><tr><th class="l">Sub-bacia</th><th>Área na RMVRC</th></tr></thead><tbody>{sub_top}</tbody></table></div></div>
  </div>
  <h3 style="margin:18px 0 8px;font:700 11.5px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)">Microbacias urbanas (córregos com nome)</h3>
  <p class="msg">{len(MIC['feats'])} microbacias drenam áreas urbanas da RMVRC. Abaixo, as 25 com mais área urbana. Afluentes sem nome aparecem no mapa identificados pelo curso d'água que recebem.</p>
  <div class="tblwrap" style="max-height:420px"><table class="dt"><thead><tr><th class="l">Microbacia</th><th>Área total</th><th>Área urbana</th><th>% urbanizada</th></tr></thead><tbody>{mic_rows}</tbody></table></div>
</section>
"""
r4('<div class="sec-h" id="metodo"',sec+'<div class="sec-h" id="metodo"')
r4('<a href="#refino">Refinamento</a>','<a href="#refino">Refinamento</a><a href="#ambiente">Meio físico</a>')
r4("['Nossa Senhora do Livramento':'N. Sra. do Livramento'","['Nossa Senhora do Livramento':'N. Sra. do Livramento'",0) if False else None
open('/home/claude/d/atlas_rmvrc.html','w').write(H)
print('layers ok',len(H)/1e6)
