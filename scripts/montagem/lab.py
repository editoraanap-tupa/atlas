# Laboratório de Governança Territorial (executado em ods.py, antes da montagem das páginas)
import json as _jl, re as _rl
exec(open('/home/claude/d/lab_def.py').read())
_LJS=[{'k':k,'n':n,'d':d,'ods':ods,'c':[[c,s,lg] for c,s,lg in comps]} for k,n,d,ods,comps in LENS]
# indicadores IPT no menu do mapa
_ind=''.join(f" {{k:'ipt_{k}',ax:'gov',n:'{n}',u:'',pol:'r',d:'Índice de Prioridade Territorial (0 a 100): {d.replace(chr(39),' ')} Maior = maior prioridade.',w:'pop'}},\n" for k,n,d,ods,comps in LENS)
_a=H.find('const IND = ['); _b=H.find('\n',_a); H=H[:_b+1]+_ind+H[_b+1:]
assert "  ind:{nome:'Índice composto', cor:'#b24a3a'}," in H
H=H.replace("  ind:{nome:'Índice composto', cor:'#b24a3a'},","  ind:{nome:'Índice composto', cor:'#b24a3a'},\n  gov:{nome:'Prioridade territorial (Laboratório)', cor:'#8a1c4a'},",1)
_o="for(const ax of ['ind','amb','ace','dem','san','ren','ent'])"; assert H.count(_o)>=1
H=H.replace(_o,"for(const ax of ['ind','gov','amb','ace','dem','san','ren','ent'])")
# código
_k=H.find('// ------- IVSA com pesos ajustáveis -------'); assert _k>0
H=H[:_k]+'const LENS='+_jl.dumps(_LJS,ensure_ascii=False)+';\n'+open('/home/claude/d/lab.js').read()+'\n'+H[_k:]
_m=_rl.search(r'recomputeIVSA\(\);\s*const wgrid',H); assert _m
H=H[:_m.start()]+'recomputeIVSA(); computeLenses();\n\nconst wgrid'+H[_m.end():]
assert H.count('renderODS(); renderSaude();')==1
H=H.replace('renderODS(); renderSaude();','renderODS(); renderSaude(); renderLab();')
_o2="drawHist(); renderKpis(); renderCmp(); renderDetail(); renderTable(); setFontes();"; assert H.count(_o2)==1
H=H.replace(_o2,_o2+" if(window.__labRefresh&&document.querySelector('.page[data-page=\"lab\"]:not([hidden])')) __labRefresh();")
# seção da página (antes do ODS)
_k=H.find('<div class="sec-h" id="ods"'); assert _k>0
H=H[:_k]+open('/home/claude/d/lab_sec.html').read()+'\n'+H[_k:]
CSSL="""
.labflow{list-style:none;margin:0 0 18px;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;counter-reset:lf}
.labflow li{position:relative;border:1px solid var(--line);border-radius:10px;padding:8px 10px;background:var(--panel-2);font-size:12px;color:var(--muted);display:flex;flex-direction:column}
.labflow li b{font:800 13.5px var(--f-display);color:var(--fg)}
.labflow li.ok{border-top:3px solid var(--accent)}
.labflow li.fut{border-top:3px dashed var(--line);opacity:.75}
@media (max-width:900px){.labflow{grid-template-columns:repeat(2,minmax(0,1fr))}}
.labstep{display:flex;gap:12px;align-items:flex-start;margin:24px 0 10px}
.labstep h3{margin:0;font:800 18px/1.2 var(--f-display);color:var(--fg);text-transform:none;letter-spacing:0}
.labstep p{margin:3px 0 0;color:var(--muted);font-size:14px;max-width:90ch}
.lenses{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px}
.lensb{text-align:left;border:1px solid var(--line);background:var(--panel);border-radius:10px;padding:9px 12px;cursor:pointer;display:flex;flex-direction:column;gap:2px;color:var(--fg)}
.lensb b{font:800 14px var(--f-display)}.lensb span{font-size:12px;color:var(--muted)}
.lensb:hover{border-color:var(--gold,#ffc000)}
.lensb[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--panel)}
.lensb[aria-pressed="true"] span{color:var(--panel);opacity:.85}
.lensinfo{margin-top:12px;background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.li-h{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:flex-start;margin-bottom:8px}
.li-h h4{margin:0;font:800 17px var(--f-display);color:var(--fg)}.li-h p{margin:3px 0 6px;font-size:14px;color:var(--muted);max-width:75ch}
.li-ods{display:flex;flex-wrap:wrap;gap:4px}
.iptb{display:inline-block;min-width:54px;padding:2px 6px;border-radius:5px;font-weight:800;background:linear-gradient(90deg,#fdbb84 var(--v),transparent var(--v));border:1px solid var(--line)}
.rbt{display:inline-block;font:700 10.5px var(--f-body);padding:1px 6px;border-radius:999px;margin-left:4px;white-space:nowrap}
.rbt.hi{background:var(--bad-bg);color:var(--bad-fg)}.rbt.md{background:var(--panel-2);color:var(--fg);border:1px solid var(--line)}.rbt.lo{color:var(--muted)}
#lab-rank small.mu,.diag .mu,.lensinfo small.mu{color:var(--muted);font-weight:400}
#lab-rank button.lnk{font-size:12.5px}
#lab-rank td.l{white-space:normal}
#lab-rank td:last-child{white-space:nowrap}
#lab-q{border:1px solid var(--line);border-radius:8px;padding:6px 10px;font:inherit;min-width:min(340px,100%);background:var(--panel);color:var(--fg)}
.diag{background:var(--panel-2);border:1px solid var(--line);border-top:4px solid #d73027;border-radius:12px;padding:12px 14px}
.diag header{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:flex-start}
.diag h4{margin:2px 0;font:800 19px var(--f-display);color:var(--fg)}
.diag .xk{font:700 10.5px var(--f-body);letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.dg-pop{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin:12px 0}
.dg-pop div{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:8px 10px;display:flex;flex-direction:column}
.dg-pop b{font:800 20px var(--f-display);color:var(--fg);font-variant-numeric:tabular-nums}.dg-pop span{font-size:12px;color:var(--muted)}
.dg-cols{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:16px}
@media (max-width:820px){.dg-cols{grid-template-columns:minmax(0,1fr)}}
.dg-cols h5{margin:0 0 6px;font:700 11.5px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.dg-l{list-style:none;margin:0;padding:0}
.dg-l li{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:2px 8px;align-items:baseline;padding:5px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.dg-l li em{grid-column:2/4;font-style:normal;font-size:11.5px;color:var(--muted)}
.dg-l b{font-variant-numeric:tabular-nums}
.sevb{font:800 10.5px var(--f-body);padding:2px 7px;border-radius:999px;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
.simg{background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:10px}
.simk .xk{font:700 10.5px var(--f-body);letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.simbar{position:relative;height:18px;background:var(--line);border-radius:5px;margin:8px 0 4px}
.simbar i{position:absolute;left:0;top:0;bottom:0;background:var(--accent);border-radius:5px}
.simbar b{position:absolute;top:-4px;bottom:-4px;width:3px;background:#d73027;border-radius:2px}
.simlg{display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 12px;font-size:13px}
.labfut{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:900px){.labfut{grid-template-columns:minmax(0,1fr)}}
.labfut article{border:1.5px dashed var(--line);border-radius:12px;padding:12px 14px;background:var(--panel)}
.labfut h4{margin:0 0 4px;font:800 15px var(--f-display);color:var(--fg)}.labfut p{margin:0 0 6px;font-size:13.5px}.labfut .req{color:var(--muted);font-size:12.5px}
#lab-b .sdsel{margin:6px 0 10px}
.pdfwrap{position:relative;margin-left:auto}
.pdfpop{position:absolute;right:0;top:calc(100% + 8px);z-index:30;width:min(380px,calc(100vw - 48px));background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--gold,#ffc000);border-radius:12px;box-shadow:0 12px 32px rgba(0,20,60,.24);padding:10px 12px 12px;display:flex;flex-direction:column;gap:8px}
.pdfpop[hidden]{display:none}
.pdfpop-h{display:flex;justify-content:space-between;align-items:center}
.pdfpop-h b{font:800 14.5px var(--f-display);color:var(--fg)}
.pdfopt{text-align:left;border:1px solid var(--line);background:var(--panel-2);border-radius:10px;padding:9px 12px;cursor:pointer;display:flex;flex-direction:column;gap:2px;color:var(--fg);font:inherit}
.pdfopt b{font:800 14px var(--f-display);color:var(--accent)}
.pdfopt span{font-size:12.5px;font-weight:600}
.pdfopt em{font-style:normal;font-size:12px;color:var(--muted);line-height:1.4}
.pdfopt:hover:not(:disabled){border-color:var(--gold,#ffc000)}
.pdfopt:disabled{opacity:.55;cursor:not-allowed}
body.pdfmode .pdfwrap{display:none!important}
"""
_k=H.find('</style>',H.find('<title>')); H=H[:_k]+CSSL+H[_k:]
exec(open('/home/claude/d/labmet.py').read())
