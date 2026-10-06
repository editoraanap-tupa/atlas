# botão "Gerar PDF desta página" em cada página do índice (executado no fim de site.py)
import re as _re3
H=_re3.sub(r'(<div class="page" data-page="(\w+)" hidden>\n<div class="crumb">)(.*?)(</div>)',lambda m:m.group(1)+m.group(3)+f'<button class="ppdf" type="button" data-pg="{m.group(2)}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2h9l5 5v15H6zM14 2v6h6M9 13h6M9 17h6"/></svg>'+('Relatório PDF da tabela (todas as linhas)' if m.group(2)=='tabelas' else 'Gerar PDF desta página')+'</button>'+m.group(4),H)
assert H.count('class="ppdf"')>=9, H.count('class="ppdf"')
CSSP="""
.crumb{flex-wrap:wrap}
.ppdf{margin-left:auto;display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--panel);color:var(--accent);font:700 12.5px var(--f-body);padding:6px 12px;border-radius:8px;cursor:pointer;position:relative;z-index:2}
.ppdf:hover{border-color:var(--gold,#ffc000)}
.ppdf:disabled{opacity:.6;cursor:progress}
.ppdf svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linejoin:round}
body.pdfmode .page:not([hidden]) .tblwrap{max-height:none!important;overflow:visible!important}
body.pdfmode .page:not([hidden]) .dt th,body.pdfmode .page:not([hidden]) .dt td{padding:4px 6px!important;font-size:11.5px!important}
body.pdfmode .page:not([hidden]) .sdyc svg{min-width:0!important}
body.pdfmode .pnav{display:none!important}
body.pdfmode .page:not([hidden]) .split{grid-template-columns:minmax(0,1fr)!important}
body.pdfmode .page:not([hidden]) .sdyr{grid-template-columns:minmax(0,1fr)!important}
body.pdfmode .page:not([hidden]) .dt{width:100%!important}
body.pdfmode .page:not([hidden]) .dt th{white-space:normal!important}
"""
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSSP+H[k:]
k=H.rfind('</body>'); H=H[:k]+open('/home/claude/d/pagepdf.js').read()+H[k:]
assert H.count("document.getElementById('ex-met').addEventListener('click',")==1
H=H.replace("document.getElementById('ex-met').addEventListener('click',","window.saveFile=saveFile; window.say=say;\ndocument.getElementById('ex-met').addEventListener('click',")

assert H.count("  tableRows=rows; tableCols=cols;")==1
H=H.replace("  tableRows=rows; tableCols=cols;","  tableRows=rows; tableCols=cols;\n  window.__tableData=()=>({rows:tableRows,cols:tableCols,filtro:filtroTxt(),tab:st.tb,ind:byK[st.ind].n,fmt:(r,c)=>{ const v=r[c[0]]; if(c[2]==='l') return String(v??''); if(!c[2]) return String(v??'—'); return fv(c[2],v); }});")
