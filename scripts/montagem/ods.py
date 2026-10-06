# páginas ODS e Saúde ambiental (executado no início de site.py)
import json as _js
_S=open('/home/claude/d/saude/saude.json').read()
k=H.find('<div class="sec-h" id="metodo"'); assert k>0
H=H[:k]+open('/home/claude/d/saude_sec.html').read()+'\n'+H[k:]
k=H.find('<div class="sec-h">'); assert '<h2>Tabelas</h2>' in H[k:k+200]
H=H[:k]+open('/home/claude/d/ods_sec.html').read()+'\n'+H[k:]
k=H.find('</style>',H.find('<title>')); H=H[:k]+open('/home/claude/d/ods.css').read()+H[k:]
_js_code=open('/home/claude/d/ods.js').read().replace('renderODS(); renderSaude();','')
k=H.find('// ------- IVSA com pesos ajustáveis -------'); assert k>0
H=H[:k]+'const SAUDE='+_S+';\n'+_js_code+'\n'+H[k:]
assert H.count('setTimeout(()=>fitTo(visible()),60);')==1
H=H.replace('setTimeout(()=>fitTo(visible()),60);','setTimeout(()=>fitTo(visible()),60); renderODS(); renderSaude();')

exec(open('/home/claude/d/sdmet.py').read())

exec(open('/home/claude/d/lab.py').read())

exec(open('/home/claude/d/afer_build.py').read())
_k=H.find('<div class="sec-h" id="sobre"'); assert _k>0
H=H[:_k]+open('/home/claude/d/afer_sec.html').read()+'\n'+H[_k:]
_aj=["  h2('10. Aferição dos indicadores');","  para('"+_pp('Cada família de indicadores foi conferida com a fonte oficial ou com fonte independente (conferido), ajustada a fatos observados (calibrado) ou tem um limite de método declarado (com ressalva). Auditoria de 01/10/2026.')+"',{gap:4});"]
for _i in IT: _aj.append("  para('"+_pp(f"{_i['n']} [{ST[_i['st']]}]. Como foi aferido: {_i['tec']} Resultado: {_i['res']} Como refazer: {_i['refazer']}")+"',{bullet:true,indent:6,size:9.2,gap:2});")
_aj.append("  para('Pendências nas médias de município, bairro e microbacia (os valores por setor reproduzem o Censo):',{bold:true,size:10,gap:2});")
for _a,_b,_c,_d,_e in PEND: _aj.append("  para('"+_pp(f"{_a}. Hoje: {_c} Exato: {_d} Efeito: {_e}")+"',{bullet:true,indent:6,size:9.2,gap:2});")
_o="  h2('10. Limitações');"; assert H.count(_o)==1
H=H.replace(_o,'\n'.join(_aj)+"\n  h2('11. Limitações');")
_o="  h2('11. Referências metodológicas');"; assert H.count(_o)==1
H=H.replace(_o,"  h2('12. Referências metodológicas');")
_k=H.find('</style>',H.find('<title>')); H=H[:_k]+'''
.afer td{vertical-align:top;white-space:normal!important;font-size:13px;line-height:1.45}
.afer td:first-child{min-width:170px}
.afs{display:inline-block;font:800 10.5px var(--f-body);padding:2px 8px;border-radius:999px;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
.afs.ok{background:var(--good-bg);color:var(--good-fg);border:1px solid var(--good-line)}
.afs.cal{background:var(--accent-soft);color:var(--fg);border:1px solid var(--line)}
.afs.res{background:var(--bad-bg);color:var(--bad-fg);border:1px solid var(--bad-line)}
.afer small.mu{color:var(--muted)}
.aferhow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:14px}
@media (max-width:820px){.aferhow{grid-template-columns:minmax(0,1fr)}}
.aferhow div{background:var(--panel-2);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.aferhow p{margin:6px 0 0;font-size:13px;line-height:1.45;color:var(--fg)}
.acard summary{align-items:center}
.acard summary .afs{margin-left:auto}
.ac-q,.ac-a{margin:0 14px 8px;padding:9px 12px;border-radius:8px;font-size:14px;line-height:1.5}
.ac-q{background:var(--panel-2);border-left:3px solid var(--accent);font-weight:600}
.ac-a{background:var(--good-bg);border-left:3px solid var(--good-fg);color:var(--fg)}
.ac-q span,.ac-a span{display:block;font:700 10.5px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:2px}
'''+H[_k:]
