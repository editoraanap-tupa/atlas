CSSH="""
.hlp{flex:none;width:22px;height:22px;border-radius:50%;border:1.5px solid var(--accent);background:var(--panel);color:var(--accent);font:800 12px/1 var(--f-body);cursor:pointer;display:inline-grid;place-items:center;padding:0;margin-left:4px;align-self:center}
.hlp:hover,.hlp[aria-expanded="true"]{background:var(--accent);color:var(--panel)}
.hlpop{position:absolute;z-index:60;background:var(--panel);color:var(--fg);border:1px solid var(--line);border-top:3px solid var(--gold,#ffc000);border-radius:10px;box-shadow:0 10px 30px rgba(0,20,60,.22);font-size:13.5px;line-height:1.5}
.hlpop-h{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:9px 12px 4px}
.hlpop-h b{font:800 14px var(--f-display)}
.hlpx{border:0;background:none;color:var(--muted);font:700 18px/1 var(--f-body);cursor:pointer;width:24px;height:24px;border-radius:6px}
.hlpx:hover{background:var(--panel-2);color:var(--fg)}
.hlpop-b{padding:0 12px 11px}
.mhtools{align-items:center}
.ptabs+.hlp{margin:0 0 0 6px}
.phead{display:flex;align-items:center}
body.pdfmode .hlp{display:none!important}
"""
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSSH+H[k:]
k=H.rfind('</body>'); H=H[:k]+open('/home/claude/d/help.js').read()+H[k:]
H=H.replace('<button class="btn" id="rep-pdf">','<button class="btn" id="rep-pdf" title="Gera um relatório em PDF com o mapa e os indicadores do bairro">',1)
H=H.replace('<button class="btn ghost" id="rep-zoom">','<button class="btn ghost" id="rep-zoom" title="Aproxima o mapa principal neste bairro">',1)
