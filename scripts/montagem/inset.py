# mapa do bairro como janela sobre o mapa (executado dentro de site.py)
rep("  h+=satCardHTML(p);\n","  { const bm=document.getElementById('bmini'); bm.querySelector('.bm-body').innerHTML=satCardHTML(p); bm.querySelector('.bm-t').textContent=p.bairro||p.dist||'Setor'; bm.hidden=false; }\n")
rep('<div class="tip" id="tip" hidden></div>','''<div class="bmini" id="bmini" hidden aria-label="Mapa do bairro do setor selecionado">
        <div class="bm-h"><span class="bm-k">Mapa do bairro</span><b class="bm-t"></b><button class="bm-x" id="bm-min" aria-label="Minimizar" title="Minimizar">–</button><button class="bm-x" id="bm-close" aria-label="Fechar" title="Fechar">×</button></div>
        <div class="bm-body"></div>
      </div>
      <div class="tip" id="tip" hidden></div>''')
CSS2="""
.bmini{position:absolute;left:12px;bottom:56px;z-index:5;width:min(300px,calc(100% - 24px));background:color-mix(in srgb,var(--panel) 96%,transparent);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);overflow:hidden}
.bm-h{display:flex;align-items:center;gap:6px;padding:7px 8px 6px 12px;border-bottom:1px solid var(--line);background:var(--panel-2)}
.bm-k{font:700 10.5px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.bm-t{font:700 12.5px var(--f-body);color:var(--fg);flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bm-x{border:0;background:transparent;color:var(--muted);font:700 16px/1 var(--f-body);width:24px;height:24px;border-radius:6px;cursor:pointer}
.bm-x:hover{background:var(--line);color:var(--fg)}
.bm-body{padding:8px 10px 10px}
.bm-body .satcard{border:0;background:none;padding:0;margin:0;box-shadow:none}
.bm-body .satcard h4{display:none}
.bm-body .minilegend{font-size:11px;gap:2px 10px;margin-top:6px}
.bm-body .btnrow{margin-top:6px!important;gap:6px}
.bm-body .btn{font-size:12px;padding:6px 10px}
.bmini.min .bm-body{display:none}
.bmini.min{width:auto;max-width:calc(100% - 24px)}
@media (max-width:820px){.bmini{width:min(220px,calc(100% - 24px))}.bm-body .minilegend{display:none}}
"""
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSS2+H[k:]
JS2="""<script>
(function(){ const bm=document.getElementById('bmini'); if(!bm) return;
  document.getElementById('bm-close').addEventListener('click',()=>{ bm.hidden=true; });
  document.getElementById('bm-min').addEventListener('click',e=>{ const m=bm.classList.toggle('min'); e.currentTarget.textContent=m?'+':'–'; e.currentTarget.setAttribute('aria-label',m?'Expandir':'Minimizar'); });
})();
</script>
"""
k=H.rfind('</body>'); H=H[:k]+JS2+H[k:]
