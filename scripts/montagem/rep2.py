# Relatório do setor/bairro com o desenho da página (cartões por tema), leitura em texto e notas
H=open('/home/claude/d/atlas_rmvrc.html').read()
a=H.index('async function sectorReport(f){'); b=H.index('\n// -------',a)
H=H[:a]+open('/home/claude/d/rep2.js').read()+H[b:]
n=H.count('USGS Landsat 9'); H=H.replace('USGS Landsat 9','USGS Landsat 8 e 9')
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('rep2 ok',len(H),n)
