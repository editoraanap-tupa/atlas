# Série histórica municipal (Censos 1991–2022): página "Evolução dos municípios" e dados (executado no fim de ods.py)
_HJ=open('/home/claude/d/serie/hist.json').read()
k=H.find('<div class="sec-h" id="metodo"'); assert k>0
H=H[:k]+open('/home/claude/d/hist_sec.html').read()+'\n'+H[k:]
k=H.find('</style>',H.find('<title>')); H=H[:k]+open('/home/claude/d/hist.css').read()+H[k:]
k=H.find('// ------- IVSA com pesos ajustáveis -------'); assert k>0
H=H[:k]+'const HIST='+_HJ+';\n'+open('/home/claude/d/hist.js').read()+'\n'+H[k:]
assert H.count('renderODS(); renderSaude();')==1
H=H.replace('renderODS(); renderSaude();','renderODS(); renderSaude(); renderHist(); renderMunHist();')
print('hist ok')
