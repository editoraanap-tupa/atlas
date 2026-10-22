# Gera os arquivos do site no repositório GitHub a partir do build do Atlas:
# index.html (cabeçalho com metadados) + atlas-dados-1.js e atlas-dados-2.js (dados embutidos, cada um < 10 MB)
import re, os
R='/home/claude/repo/atlas-rmvrc'
B=open('/home/claude/d/atlas_rmvrc.html',encoding='utf-8').read()
old=open(R+'/index.html',encoding='utf-8').read()
HEAD=old[:old.find('<body>\n\n')+len('<body>\n\n')]
HEAD=HEAD.replace('inundação, APP, saúde ambiental e ODS.','inundação, APP, saúde ambiental, ODS e série histórica dos Censos de 1991 a 2022.')
assert B.startswith('<title>')
body=B[B.find('\n')+1:]
s=HEAD+body+'\n\n</body>\n</html>\n'
a0=s.find('<script>const DATA = '); assert a0>0
a=a0+8; b=s.find('</script>',a); js=s[a:b]
m=re.search(r';\s*const EQUIP = ',js); cut=m.start(); assert js.count('const EQUIP = ')==1
p1=js[:cut]+';\n'; p2=js[cut+1:].lstrip(); assert p2.startswith('const EQUIP = ')
hdr='/* Atlas Socioambiental da RMVRC — dados embutidos (parte %d de 2). Gerado a partir do arquivo único do Atlas; não editar à mão. */\n'
open(R+'/atlas-dados-1.js','w',encoding='utf-8').write(hdr%1+p1)
open(R+'/atlas-dados-2.js','w',encoding='utf-8').write(hdr%2+p2+'\n')
new=s[:a0]+'<script src="atlas-dados-1.js"></script>\n<script src="atlas-dados-2.js"></script>'+s[b+len('</script>'):]
open(R+'/index.html','w',encoding='utf-8').write(new)
# cópia de arquivo único (para abrir fora do GitHub)
open('/home/claude/d/atlas_rmvrc_unico.html','w',encoding='utf-8').write(s)
for f in ['index.html','atlas-dados-1.js','atlas-dados-2.js']: print(f,os.path.getsize(R+'/'+f))
