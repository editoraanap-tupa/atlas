H=open('/home/claude/d/atlas_rmvrc.html').read()
a=H.index('<h2>Roteiro para desenvolvermos juntos</h2>'); s=H.rindex('<article>',0,a); e=H.index('</article>',a)+len('</article>')
H=H[:s].rstrip()+'\n'+H[e:].lstrip('\n')
old="roteiro.querySelectorAll('li').forEach("
assert H.count(old)==1
H=H.replace(old,"(roteiro?[...roteiro.querySelectorAll('li')]:[]).forEach(")
H=H.replace("h2('6. Limitações e próximos passos');","h2('6. Limitações');")
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('roteiro removido')
# ---- remove a seção "Pesos do IVSA" (fica oculta para o cálculo continuar com os pesos oficiais)
H=open('/home/claude/d/atlas_rmvrc.html').read()
old='<div class="sec-h"><span class="kick">Construção coletiva</span>'
assert H.count(old)==1
H=H.replace(old,'<div class="sec-h" hidden><span class="kick">Construção coletiva</span>')
H=H.replace('<section class="block" id="pesos">','<section class="block" id="pesos" hidden>')
H=H.replace('<a href="#pesos">Pesos do IVSA</a>','')
old2="try{ const s=JSON.parse(localStorage.getItem('atlas-rmvrc-w')||'null'); if(s) for(const c of WC) if(typeof s[c.k]==='number') WT[c.k]=s[c.k]; }catch(e){}"
assert H.count(old2)==1
H=H.replace(old2,"// pesos fixos (padrão oficial do Atlas)")
H=H.replace('Os pesos wⱼ são ajustáveis na seção “Pesos do IVSA”; o padrão é:','Os pesos wⱼ são fixos; os sete componentes censitários têm peso 1 e os componentes de satélite/modelo têm peso 0 (documentados, mas fora do índice, porque não cobrem toda a RMVRC):')
H=H.replace("'0 (opcional)'","'0'")
H=H.replace('IVSA com os pesos em uso nesta página.','IVSA com os pesos padrão do Atlas.').replace('IVSA com os pesos em uso na página.','IVSA com os pesos padrão do Atlas.')
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('pesos ocultos')

H=open('/home/claude/d/atlas_rmvrc.html').read()
H=H.replace('<h2>Método, fontes e próximos passos</h2>','<h2>Método e fontes</h2>')
H=H.replace('Vegetação, temperatura, inundação, cheias, setores de risco e FCU cobrem a conurbação Cuiabá–Várzea Grande. APP e rede hídrica cobrem também as sedes dos demais municípios.','NDVI, temperatura, HAND, cheias, carta do SGB, setores de risco e FCU cobrem só a conurbação Cuiabá–Várzea Grande. Solos, erosão, cobertura da terra, bacias, rede hídrica e divisas cobrem os 7 municípios; APP e microbacias, as áreas urbanas.')
H=H.replace('Elaboração: Santos &amp; Benini, PPGAU-UNIVAG (2026).','Elaboração: Santos &amp; Benini, PPGAU-UNIVAG (2026).')
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('textos ok')
