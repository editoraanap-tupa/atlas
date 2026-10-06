<script>
(function(){
  const LIBS=[['https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js','html2canvas'],['https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js','jspdf']];
  const load=(src,g)=>window[g]?Promise.resolve():new Promise((ok,err)=>{ const s=document.createElement('script'); s.src=src; s.onload=ok; s.onerror=()=>err(new Error('lib')); document.head.appendChild(s); });
  // html2canvas 1.4 não entende color(), oklab(), color-mix(): converte para rgba no clone
  function toRGBA(v){ const m=v.match(/color\(srgb ([\d.e-]+) ([\d.e-]+) ([\d.e-]+)(?: \/ ([\d.e-]+))?\)/); if(!m) return null; const c=x=>Math.round(Math.max(0,Math.min(1,+x))*255); return `rgba(${c(m[1])},${c(m[2])},${c(m[3])},${m[4]==null?1:+m[4]})`; }
  const PROPS=['color','background-color','border-top-color','border-right-color','border-bottom-color','border-left-color','text-decoration-color','outline-color','fill','stroke','stop-color'];
  function sanitize(docC){ const win=docC.defaultView; docC.querySelectorAll('*').forEach(el=>{ const cs=win.getComputedStyle(el);
      for(const p of PROPS){ const v=cs.getPropertyValue(p); if(v&&/color\(|oklab|oklch|lab\(|lch\(/.test(v)){ const r=toRGBA(v); el.style.setProperty(p, r||'transparent','important'); } }
      const bi=cs.getPropertyValue('background-image'); if(bi&&/color\(|oklab|color-mix/.test(bi)) el.style.setProperty('background-image','none','important');
      const sh=cs.getPropertyValue('box-shadow'); if(sh&&/color\(|oklab/.test(sh)) el.style.setProperty('box-shadow','none','important');
      el.style.setProperty('backdrop-filter','none','important'); }); }
  function inlineSvg(root){ // var(--x) em atributos SVG: fixa a cor calculada
    root.querySelectorAll('svg *').forEach(el=>{ const cs=getComputedStyle(el); for(const a of ['fill','stroke']){ const v=el.getAttribute(a); if(v&&v.includes('var(')){ el.dataset['pv'+a]=v; el.setAttribute(a,toRGBA(cs[a])||cs[a]); } } }); }
  function restoreSvg(root){ root.querySelectorAll('svg *').forEach(el=>{ for(const a of ['fill','stroke']){ const k='pv'+a; if(el.dataset[k]){ el.setAttribute(a,el.dataset[k]); delete el.dataset[k]; } } }); }
  async function pagePDF(pid,btn){
    const pg=document.querySelector(`.page[data-page="${pid}"]`); if(!pg) return;
    const say=window.say||(()=>{}); const old=btn.textContent; btn.disabled=true; btn.textContent='Gerando PDF…';
    const root=document.documentElement, prevT=root.getAttribute('data-theme'); root.setAttribute('data-theme','light');
    document.body.classList.add('pdfmode');
    const closed=[...pg.querySelectorAll('details:not([open])')]; closed.forEach(d=>d.open=true);
    const prevW=pg.style.width; pg.style.width='1080px';
    try{
      for(const [u,g] of LIBS) await load(u,g);
      await new Promise(r=>setTimeout(r,250));
      { const rr=pg.getBoundingClientRect(); const mx=Math.max(...[...pg.querySelectorAll('table,svg,img,.tblwrap')].map(e=>e.getBoundingClientRect().right)); if(mx>rr.right+1){ pg.style.width=Math.min(1500,Math.ceil(rr.width+(mx-rr.right)+24))+'px'; await new Promise(r=>setTimeout(r,150)); } }
      inlineSvg(pg);
      const r0=pg.getBoundingClientRect(), Wc=Math.max(r0.width,pg.scrollWidth), Hc=pg.scrollHeight;
      // blocos "atômicos": nenhum corte de página pode atravessá-los (linhas de texto, linhas de tabela, gráficos, imagens)
      const atoms=[];
      pg.querySelectorAll('*').forEach(el=>{ if(el.closest('.pnav,.crumb')) return; const tag=el.tagName.toLowerCase();
        const hasText=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
        if(hasText||['svg','img','canvas','tr','input','button','select','summary','dt','dd','li'].includes(tag)||el.matches('.kpi,.sdb,.odsb,.cpill,.flag,.chip')){
          if(tag!=='svg'&&el.closest('svg')) return; const r=el.getBoundingClientRect(); if(r.height>0&&r.width>0) atoms.push([r.top-r0.top,r.bottom-r0.top]); } });
      const safe=yy=>!atoms.some(([t,b])=>t<yy-0.5&&b>yy+0.5);
      const cands=[...new Set(atoms.map(a=>Math.ceil(a[1])+2))].filter(yy=>yy>0&&yy<Hc).sort((a,b)=>a-b);
      const SC=1.6;
      const canvas=await html2canvas(pg,{scale:SC,width:Wc,height:Hc,backgroundColor:'#ffffff',useCORS:true,logging:false,windowWidth:1400,
        ignoreElements:el=>el.classList&&(el.classList.contains('pnav')||el.classList.contains('ppdf')||el.classList.contains('crumb')),
        onclone:d=>sanitize(d)});
      const {jsPDF}=window.jspdf; const pdf=new jsPDF({unit:'pt',format:'a4',compress:true});
      const PW=pdf.internal.pageSize.getWidth(), PH=pdf.internal.pageSize.getHeight(), M=34, HD=26, FT=22;
      const s=(PW-2*M)/Wc, avail=(PH-2*M-HD-FT)/s;
      const slices=[]; let y=0; let guard=0; while(y<Hc-2&&guard++<500){ let e=Math.min(Hc,y+avail);
        if(e<Hc){ let pick=null; for(let q=cands.length-1;q>=0;q--){ const c=cands[q]; if(c>e) continue; if(c<=y+20) break; if(safe(c)){ pick=c; break; } }
          if(pick==null){ for(const c of cands){ if(c>y+20&&safe(c)){ pick=c; break; } } }
          if(pick!=null) e=pick; }
        slices.push([y,e]); y=e; }
      window.__pdfCheck={over:[...pg.querySelectorAll('table,svg,img,.tblwrap')].filter(e=>e.getBoundingClientRect().right>r0.right+1).length,n:slices.length,unsafe:slices.filter(([a,b])=>b<Hc&&!safe(b)).length,overs:slices.filter(([a,b])=>(b-a)>avail+1).length,wide:Wc>r0.width+1};
      // um bloco maior que a página (raro) é reduzido em escala na mesma folha, sem cortar

      const title=(pg.querySelector('.sec-h h2')||{}).textContent||'Atlas';
      const dt=new Date().toLocaleDateString('pt-BR');
      slices.forEach(([a,b],i)=>{ if(i) pdf.addPage();
        const c=document.createElement('canvas'); c.width=canvas.width; c.height=Math.ceil((b-a)*SC); const cx=c.getContext('2d'); cx.fillStyle='#fff'; cx.fillRect(0,0,c.width,c.height); cx.drawImage(canvas,0,Math.floor(a*SC),canvas.width,c.height,0,0,canvas.width,c.height);
        { let w=PW-2*M, h=(b-a)*s; const maxH=PH-2*M-HD-FT; if(h>maxH){ w=w*maxH/h; h=maxH; } pdf.addImage(c.toDataURL('image/jpeg',0.82),'JPEG',M+(PW-2*M-w)/2,M+HD,w,h,undefined,'FAST'); }
        pdf.setDrawColor(255,192,0); pdf.setLineWidth(2); pdf.line(M,M+HD-8,PW-M,M+HD-8);
        pdf.setFont('helvetica','bold'); pdf.setFontSize(9); pdf.setTextColor(0,32,96); pdf.text('Atlas Socioambiental da RMVRC · PPGAU-UNIVAG',M,M+6);
        pdf.setFont('helvetica','normal'); pdf.setTextColor(86,96,122); pdf.text(title,PW-M,M+6,{align:'right'});
        pdf.setFontSize(8); pdf.text(`Elaboração: Prof. Dr. Ricardo Miranda dos Santos e Profa. Dra. Sandra Medina Benini · gerado em ${dt}`,M,PH-M+6);
        pdf.text(`página ${i+1} de ${slices.length}`,PW-M,PH-M+6,{align:'right'}); });
      const blob=pdf.output('blob');
      if(window.saveFile) await window.saveFile(`atlas_rmvrc_${pid}.pdf`,blob); else { const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=`atlas_rmvrc_${pid}.pdf`; a.click(); }
    }catch(e){ console.error(e); say('Não foi possível gerar o PDF desta página.'); }
    finally{ restoreSvg(pg); pg.style.width=prevW; closed.forEach(d=>d.open=false); document.body.classList.remove('pdfmode'); if(prevT==null) root.removeAttribute('data-theme'); else root.setAttribute('data-theme',prevT); btn.disabled=false; btn.textContent=old; window.dispatchEvent(new Event('resize')); }
  }

  async function tablePDF(btn){
    const say=window.say||(()=>{}); const old=btn.textContent; btn.disabled=true; btn.textContent='Gerando relatório…';
    try{
      await load(LIBS[1][0],LIBS[1][1]);
      const T=window.__tableData(); const {jsPDF}=window.jspdf; const pdf=new jsPDF({unit:'pt',format:'a4',orientation:'landscape',compress:true});
      const PW=pdf.internal.pageSize.getWidth(), PH=pdf.internal.pageSize.getHeight(), M=30, FS=7.5, LH=9.2;
      const TN={fcu:'Favelas e comunidades urbanas',rank:'Ranking de setores · '+T.ind,eq:'Equipamentos'}[T.tab]||'Tabela';
      const cols=T.cols, rows=T.rows, cells=rows.map(r=>cols.map(c=>String(T.fmt(r,c)).replace(/−/g,'-').replace(/[^\x00-\xff–—]/g,'')));
      pdf.setFont('helvetica','normal'); pdf.setFontSize(FS);
      // largura de cada coluna pelo maior conteúdo, limitada; texto longo quebra em linhas (nada é cortado)
      let w=cols.map((c,k)=>Math.min(k===0?200:150,Math.max(pdf.getTextWidth(c[1])*0.62+8, ...cells.slice(0,3000).map(r=>pdf.getTextWidth(r[k])+8))));
      pdf.setFont('helvetica','bold'); const mw=cols.map(c=>Math.max(...c[1].split(/\s+/).map(s=>pdf.getTextWidth(s)))+9); pdf.setFont('helvetica','normal');
      w=w.map((x,k)=>Math.max(x,mw[k])); const avail=PW-2*M; let tot=w.reduce((a,b)=>a+b,0);
      if(tot<avail) w=w.map(x=>x*avail/tot); else { const ex=w.map((x,k)=>x-mw[k]), te=ex.reduce((a,b)=>a+b,0), need=tot-avail; w=w.map((x,k)=>x-(te?ex[k]/te*need:0)); }
      const dt=new Date().toLocaleDateString('pt-BR'); let page=1, y;
      const head=()=>{ pdf.setFont('helvetica','bold'); pdf.setFontSize(9); pdf.setTextColor(0,32,96); pdf.text('Atlas Socioambiental da RMVRC · PPGAU-UNIVAG',M,M);
        pdf.setFont('helvetica','normal'); pdf.setTextColor(86,96,122); pdf.text(`Tabela: ${TN} · ${T.filtro}`,PW-M,M,{align:'right'});
        pdf.setDrawColor(255,192,0); pdf.setLineWidth(1.6); pdf.line(M,M+6,PW-M,M+6); y=M+18;
        pdf.setFont('helvetica','bold'); pdf.setFontSize(FS); pdf.setTextColor(15,29,58);
        const hl=cols.map((c,k)=>pdf.splitTextToSize(c[1],w[k]-6)); const hh=Math.max(...hl.map(l=>l.length))*LH+4;
        pdf.setFillColor(227,233,246); pdf.rect(M,y-2,avail,hh,'F'); let x=M; hl.forEach((l,k)=>{ const al=cols[k][2]==='l'; pdf.text(l,al?x+3:x+w[k]-3,y+LH-2,{align:al?'left':'right'}); x+=w[k]; }); y+=hh+2; pdf.setFont('helvetica','normal'); };
      const foot=()=>{ pdf.setFontSize(7.5); pdf.setTextColor(86,96,122); pdf.text(`Elaboração: Prof. Dr. Ricardo Miranda dos Santos e Profa. Dra. Sandra Medina Benini · gerado em ${dt} · ${rows.length} linhas`,M,PH-16); };
      head();
      cells.forEach((r,j)=>{ const ls=r.map((v,k)=>pdf.splitTextToSize(v,w[k]-6)); const rh=Math.max(...ls.map(l=>l.length))*LH+3;
        if(y+rh>PH-30){ foot(); pdf.addPage(); page++; head(); }
        if(j%2){ pdf.setFillColor(244,246,250); pdf.rect(M,y-1,avail,rh,'F'); }
        pdf.setTextColor(15,29,58); pdf.setFontSize(FS); let x=M; ls.forEach((l,k)=>{ const al=cols[k][2]==='l'; pdf.text(l,al?x+3:x+w[k]-3,y+LH-2,{align:al?'left':'right'}); x+=w[k]; }); y+=rh; });
      foot();
      const n=pdf.internal.getNumberOfPages(); for(let i=1;i<=n;i++){ pdf.setPage(i); pdf.setFontSize(7.5); pdf.setTextColor(86,96,122); pdf.text(`página ${i} de ${n}`,PW-M,PH-16,{align:'right'}); }
      window.__pdfCheck={n,rows:rows.length};
      const blob=pdf.output('blob'), fn=`atlas_rmvrc_tabela_${T.tab}.pdf`;
      if(window.saveFile) await window.saveFile(fn,blob); else { const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=fn; a.click(); }
    }catch(e){ console.error(e); say('Não foi possível gerar o relatório da tabela.'); }
    finally{ btn.disabled=false; btn.textContent=old; }
  }
  window.__loadJsPDF=()=>load(LIBS[1][0],LIBS[1][1]);
  window.pagePDF=pagePDF;
  document.addEventListener('click',e=>{ const b=e.target.closest('button.ppdf'); if(b){ if(b.dataset.pg==='tabelas') tablePDF(b); else pagePDF(b.dataset.pg,b); } });
})();
</script>
