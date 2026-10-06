# Reestrutura o Atlas como "site": mapa em largura maior, ficha do setor abaixo do mapa,
# e cada bloco de conteúdo vira uma página própria aberta pelo menu/índice.
import re
H=open('/home/claude/d/atlas_rmvrc.html').read()
def rep(a,b,cnt=1):
    global H
    assert H.count(a)>=1, a[:80]
    H=H.replace(a,b,cnt)

exec(open('/home/claude/d/ods.py').read())
# ---------- 1. ficha do setor (lateral) + painel de indicadores por eixo abaixo do mapa ----------
FICHA=open('/home/claude/d/eixos_sec.html').read()
k=H.find('<div class="sec-h" hidden>')
app_end=H.rfind('</div>',0,k)+len('</div>')
H=H[:app_end]+FICHA+H[app_end:]

H=H.replace('<b>Escolha um indicador, clique num setor</b> e ajuste com a equipe os pesos do índice de vulnerabilidade.','<b>Escolha um indicador e clique num setor</b>: a ficha abre ao lado e os indicadores por tema logo abaixo do mapa, e tabelas, análises e metodologia ficam em páginas próprias no menu.')
H=H.replace(' Ver metodologia abaixo.',' Veja a página Metodologia.')
H=H.replace("i.d.replace(' Veja a página Metodologia.','')","i.d.replace(' Ver metodologia abaixo.','').replace(' Veja a página Metodologia.','')")
# ---------- 2. páginas ----------
PAGES=[ # (id, rótulo do menu, título, kicker, descrição do índice) — na ordem de navegação
 ('mapa','Mapa','Mapa interativo','Início','Indicadores por setor, camadas ambientais e ficha do setor.'),
 ('lab','Governança','Laboratório de Governança Territorial','Laboratório','Onde agir e com qual prioridade: índice de prioridade por objetivo de política, diagnóstico territorial e simulador de metas.'),
 ('ods','ODS','Indicadores e os ODS','Agenda 2030','Cada indicador ligado ao objetivo e à meta dos ODS que ajuda a monitorar, com painel comparativo dos sete municípios.'),
 ('saude','Saúde','Saúde ambiental','Saúde','Internações por doenças ligadas ao saneamento, respiratórias e dengue, por município e por ano (DATASUS).'),
 ('metodo','Fontes','Método e fontes','Fontes','De onde vem cada dado, como as camadas foram feitas e o tratamento aplicado.'),
 ('formulas','Metodologia','Metodologia detalhada','Fórmulas','Fórmulas, dicionário dos indicadores e, nos subitens, a aferição, os dados abertos e as calibrações.'),
 ('afericao','Aferição dos indicadores','Aferição dos indicadores','Auditoria','Como cada família de indicadores foi conferida, com qual resultado, e as pendências declaradas.'),
 ('tabelas','Dados abertos','Tabelas e dados abertos','Dados abertos','Ranking de setores, favelas e comunidades e equipamentos, com download em CSV e GeoJSON para conferência.'),
 ('validacao','Cheias: calibração','Cheias do Rio Cuiabá e validação','Calibração','Cenários de cheia calibrados com as cotas históricas e os bairros atingidos em 1974 e 1995.'),
 ('refino','Carta SGB: validação','Carta oficial do SGB e terreno ANADEM','Validação','Comparação do modelo com a carta de suscetibilidade do SGB e com o terreno sem vegetação.'),
 ('ambiente','Meio físico: bases','Bacias, solos, erosão e vegetação','Bases físicas','Síntese por município, bacias, microbacias urbanas, solos e vulnerabilidade à erosão.'),
 ('sobre','Sobre','Sobre o Atlas','Institucional','Apresentação, recorte territorial, elaboração, vínculo com o PPGAU-UNIVAG e como citar.'),
]
SUBS=['afericao','tabelas','validacao','refino','ambiente']   # subitens da Metodologia
METG=['formulas']+SUBS
# página do mapa: do início do <div class="app"> até o fim da ficha
a=H.find('<div class="app">'); b=H.find('<div class="sec-h" hidden>')
H=H[:a]+'<div class="page" data-page="mapa">\n'+H[a:b]+'@@INDICE@@\n</div>\n'+H[b:]
# demais páginas: cada sec-h até o próximo sec-h (ou o footer)
starts={}
for pid in [p[0] for p in PAGES[1:]]:
    if pid=='tabelas':
        m=H.find('<div class="sec-h">'); assert m>0 and '<h2>Tabelas</h2>' in H[m:m+200]
    else:
        m=H.find(f'<div class="sec-h" id="{pid}"')
    starts[pid]=m
order=sorted(starts,key=lambda p:starts[p])
assert set(order)=={p[0] for p in PAGES[1:]},order
foot=H.find('<footer>')
# insere de trás para frente
bounds=[(p,starts[p],(starts[order[n+1]] if n+1<len(order) else foot)) for n,p in enumerate(order)]
meta={p[0]:p for p in PAGES}
for n,(p,s,e) in reversed(list(enumerate(bounds))):
    prev=PAGES[[x[0] for x in PAGES].index(p)-1]; nxt=PAGES[[x[0] for x in PAGES].index(p)+1] if p!='sobre' else PAGES[0]
    seg=H[s:e]
    if p!='tabelas':
        seg=seg.replace(f'<div class="sec-h" id="{p}"','<div class="sec-h"',1)
    _sub=''.join(f'<a href="#{q}"'+(' aria-current="page"' if q==p else '')+f'>{"Fórmulas e dicionário" if q=="formulas" else meta[q][1]}</a>' for q in METG)
    _crumb=(f'<a href="#formulas">Metodologia</a><span>›</span>' if p in SUBS else '')
    top=f'''<div class="page" data-page="{p}" hidden>
<div class="crumb"><a href="#mapa">Atlas RMVRC</a><span>›</span>{_crumb}<b>{meta[p][2]}</b></div>
'''+(f'<div class="subnav" role="navigation" aria-label="Subitens da Metodologia"><span>Metodologia</span>{_sub}</div>\n' if p in METG else '')
    bot=f'''<div class="pnav"><a class="pv" href="#{prev[0]}"><small>← Anterior</small>{prev[2]}</a><a class="nx" href="#{nxt[0]}"><small>Próxima →</small>{nxt[2]}</a></div>
</div>
'''
    H=H[:s]+top+seg.rstrip()+'\n'+bot+H[e:]
# pesos (oculto) continua fora das páginas, sem efeito visual

# índice "Explore o Atlas" no fim da página do mapa
ICO={'afericao':'<path d="M9 12l2 2 4-4M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/>','tabelas':'<path d="M3 5h18v14H3zM3 10h18M3 15h18M9 5v14"/>','lab':'<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3M7.5 14h9"/>','ods':'<circle cx="12" cy="12" r="9"/><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M18.4 5.6l-2.8 2.8M8.4 15.6l-2.8 2.8"/>','saude':'<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10zM9 11h2V9h2v2h2v2h-2v2h-2v-2H9z"/>','tabelas':'<path d="M3 5h18v14H3zM3 10h18M3 15h18M9 5v14"/>',
 'validacao':'<path d="M2 15c3-3 5 3 8 0s5 3 8 0 3-1 4-1M2 19c3-3 5 3 8 0s5 3 8 0 3-1 4-1M12 3l3 6H9z"/>',
 'refino':'<path d="M3 20l6-11 4 6 3-4 5 9zM16 4a2 2 0 1 0 0 .1"/>',
 'ambiente':'<path d="M4 20c6-1 9-5 9-11 0-2-1-4-1-4s-8 3-8 11c0 2 0 4 0 4zM4 20l7-8"/>',
 'metodo':'<path d="M5 3h10l4 4v14H5zM15 3v4h4M8 12h8M8 16h8"/>',
 'formulas':'<path d="M5 6h9l-5 6 5 6H5M17 9l4 6M21 9l-4 6"/>',
 'sobre':'<path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 10v6M12 7v.1"/>'}
_card=lambda p,_,t,k,d: f'<a class="xcard" href="#{p}"><svg viewBox="0 0 24 24" aria-hidden="true">{ICO[p]}</svg><span class="xk">{k}</span><b>{t}</b><span class="xd">{d}</span><span class="xgo">Abrir página →</span></a>'
cards=''.join(_card(*x) for x in PAGES[1:] if x[0] not in SUBS)
subcards=''.join(f'<a class="xsub" href="#{p}"><b>{l}</b><span>{d}</span></a>' for p,l,t,k,d in PAGES if p in SUBS)
IND_HTML=f'''<section class="explore" aria-label="Índice do Atlas">
  <div class="ficha-h"><div><span class="kick">Índice</span><h2>Explore o Atlas</h2></div><p>As análises ficam em páginas próprias. A aferição dos dados, os dados abertos e as calibrações são subitens da Metodologia. Os filtros de município e área valem em todas as páginas.</p></div>
  <div class="xgrid">{cards}</div>
  <div class="xsubh"><span class="kick">Metodologia · subitens</span><p>Como os dados foram conferidos e calibrados, para que possam ser auditados.</p></div>
  <div class="xsubg">{subcards}</div>
</section>'''
H=H.replace('@@INDICE@@',IND_HTML)

# menu
nav='<nav aria-label="Páginas">'+''.join(f'<a href="#{p}" data-nav="{p}">{l}</a>' for p,l,*_ in PAGES if p not in SUBS)+'</nav>'
H=re.sub(r'<nav aria-label="Seções">.*?</nav>',nav,H,count=1,flags=re.S)

# chamadas que rolavam até o mapa passam antes pela página do mapa
rep("document.querySelector('.mapcard').scrollIntoView(","(window.goPage&&goPage('mapa',1),document.querySelector('.mapcard')).scrollIntoView(",2)

# ---------- 3. CSS ----------
CSS='''
/* ---- layout de site ---- */
.page[hidden]{display:none!important}
body.sub .hero{display:none}
nav a[aria-current="page"]{color:var(--navy-fg,var(--fg));background:var(--panel-2);box-shadow:inset 0 -2px 0 var(--gold,#ffc000)}
.ficha-h{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:6px 24px;margin-bottom:14px}
.ficha-h h2{text-transform:none;letter-spacing:-.01em;margin:2px 0 0;font:800 clamp(20px,2.2vw,26px)/1.15 var(--f-display);color:var(--fg)}
.ficha-h p{margin:0;max-width:62ch;color:var(--muted);font-size:14px;line-height:1.5}
.ficha-h .kick{font:700 11px var(--f-body);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.gofic{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);z-index:6;border:0;cursor:pointer;background:var(--navy,#002060);color:#fff;font:700 13px var(--f-body);padding:9px 16px;border-radius:999px;box-shadow:0 6px 18px rgba(0,0,0,.25);display:flex;gap:8px;align-items:center;max-width:calc(100% - 140px);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.gofic b{color:#ffc000;overflow:hidden;text-overflow:ellipsis}
.explore{margin-top:16px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px 20px;box-shadow:var(--shadow)}
.xgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:1000px){.xgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.xgrid{grid-template-columns:minmax(0,1fr)}}
.xcard{display:flex;flex-direction:column;gap:4px;text-decoration:none;color:var(--fg);background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:14px 16px 12px;transition:border-color .15s,transform .15s}
.xcard:hover{border-color:var(--gold,#ffc000);transform:translateY(-2px)}
.xcard svg{width:26px;height:26px;fill:none;stroke:var(--accent,#002060);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;margin-bottom:4px}
.xk{font:700 10.5px var(--f-body);letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.xcard b{font:800 15.5px/1.25 var(--f-display)}
.xd{font-size:13px;line-height:1.45;color:var(--muted);flex:1}
.xgo{font:700 12.5px var(--f-body);color:var(--accent,#002060);margin-top:6px}
.subnav{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin:34px 0 -30px;position:relative;z-index:2}
.subnav span{font:700 11px var(--f-body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-right:4px}
.subnav a{font:600 13px var(--f-body);color:var(--accent);text-decoration:none;border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:5px 13px}
.subnav a:hover{border-color:var(--gold,#ffc000)}
.subnav a[aria-current="page"]{background:var(--accent);border-color:var(--accent);color:var(--panel)}
body.pdfmode .subnav{display:none!important}
.xsubh{margin:18px 0 8px;display:flex;flex-wrap:wrap;gap:4px 16px;align-items:baseline}
.xsubh .kick{font:700 11px var(--f-body);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.xsubh p{margin:0;font-size:13.5px;color:var(--muted)}
.xsubg{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
@media (max-width:1100px){.xsubg{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.xsubg{grid-template-columns:minmax(0,1fr)}}
.xsub{display:flex;flex-direction:column;gap:3px;text-decoration:none;color:var(--fg);border:1px dashed var(--line);border-radius:10px;padding:10px 12px;background:var(--panel)}
.xsub:hover{border-color:var(--gold,#ffc000);border-style:solid}
.xsub b{font:800 13.5px var(--f-display);color:var(--accent)}
.xsub span{font-size:12.5px;line-height:1.4;color:var(--muted)}
.crumb{display:flex;gap:8px;align-items:center;margin:22px 0 -26px;font-size:13px;color:var(--muted)}
.crumb a{color:var(--muted);text-decoration:none;font-weight:600}.crumb a:hover{color:var(--fg);text-decoration:underline}
.crumb b{color:var(--fg);font-weight:600}
.pnav{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:28px 0 8px}
.pnav a{display:flex;flex-direction:column;gap:2px;text-decoration:none;color:var(--fg);font:700 15px var(--f-display);background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
.pnav a:hover{border-color:var(--gold,#ffc000)}
.pnav .nx{text-align:right}
.pnav small{font:600 12px var(--f-body);color:var(--muted)}
'''
k=H.find('</style>',H.find('<title>')); H=H[:k]+CSS+H[k:]

# ---------- 4. roteador ----------
JS=r'''<script>
(function(){
  const pages=[...document.querySelectorAll('.page')], ids=pages.map(p=>p.dataset.page);
  const TIT={mapa:'Atlas Socioambiental RMVRC'};
  let cur='mapa';
  function pageOf(id){ if(ids.includes(id)) return id; const el=id&&document.getElementById(id); const pg=el&&el.closest('.page'); return pg?pg.dataset.page:null; }
  window.goPage=function(id,noScroll){
    const pid=pageOf(id)||'mapa'; const changed=pid!==cur; cur=pid;
    pages.forEach(p=>p.hidden=p.dataset.page!==pid);
    document.body.classList.toggle('sub',pid!=='mapa');
    const par=({afericao:1,tabelas:1,validacao:1,refino:1,ambiente:1})[pid]?'formulas':pid; document.querySelectorAll('[data-nav]').forEach(a=>a.dataset.nav===par?a.setAttribute('aria-current','page'):a.removeAttribute('aria-current'));
    if(changed) window.dispatchEvent(new Event('resize'));
    if(noScroll) return;
    const el=(id&&!ids.includes(id))?document.getElementById(id):null;
    requestAnimationFrame(()=>{ if(el) el.scrollIntoView({block:'start'}); else window.scrollTo(0,0); });
  };
  document.addEventListener('click',e=>{
    const a=e.target.closest('a[href^="#"]'); if(!a) return;
    const id=decodeURIComponent(a.getAttribute('href').slice(1)); if(!id||!pageOf(id)) return;
    e.preventDefault(); goPage(id);
    try{ history.pushState(null,'','#'+id); }catch(_){}
  });
  window.addEventListener('popstate',()=>goPage(location.hash.slice(1)||'mapa'));
  window.addEventListener('hashchange',()=>goPage(location.hash.slice(1)||'mapa'));
  // botão flutuante "ver ficha"
  const mw=document.querySelector('.mapwrap'), fic=document.getElementById('ficha');
  const btn=document.createElement('button'); btn.className='gofic'; btn.hidden=true; /* botão flutuante retirado da área do mapa */
  btn.addEventListener('click',()=>fic.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'}));
  let vis=false;
  try{ new IntersectionObserver(es=>{ vis=es[0].isIntersecting&&es[0].intersectionRatio>.25; if(vis) btn.hidden=true; },{threshold:[0,.25,.5]}).observe(fic); }catch(_){}
  new MutationObserver(()=>{ const n=document.querySelector('#detail .sname'); if(!n) return; btn.innerHTML='Indicadores do setor ↓ <b>'+n.textContent+'</b>'; btn.hidden=vis; }).observe(document.getElementById('detail'),{childList:true});
  // abre na página pedida pelo link, depois que o mapa terminou de desenhar
  const h=location.hash.slice(1);
  goPage('mapa',1);
  if(h&&h!=='mapa') setTimeout(()=>goPage(h),400);
})();
</script>
'''
k=H.rfind('</body>') if '</body>' in H else len(H)
H=H[:k]+JS+H[k:]
exec(open('/home/claude/d/eixos.py').read())
exec(open('/home/claude/d/pagepdf.py').read())
exec(open('/home/claude/d/fontlay.py').read())
exec(open('/home/claude/d/legfoot.py').read())
exec(open('/home/claude/d/selmode.py').read())
exec(open('/home/claude/d/expfix.py').read())
exec(open('/home/claude/d/ovleg.py').read())
exec(open('/home/claude/d/theme.py').read())
exec(open('/home/claude/d/help.py').read())
t=H.find('<title>'); H=H[t:]
if H.rstrip().endswith('</body></html>'): H=H.rstrip()[:-len('</body></html>')]
open('/home/claude/d/atlas_rmvrc.html','w').write(H)
print('site ok', len(H))
