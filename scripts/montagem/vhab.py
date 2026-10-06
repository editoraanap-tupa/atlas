# vegetação por habitante (m²/hab) — calculada a partir da cobertura vegetal NDVI já existente
H=open('/home/claude/d/atlas_rmvrc.html').read()
def r5(a,b):
    global H
    assert H.count(a)==1,(H.count(a),a[:90]); H=H.replace(a,b)
r5(" {k:'veg_nat',ax:'amb',"," {k:'verde_hab',ax:'amb',n:'Vegetação por habitante',u:'m²/hab',pol:'b',d:'Área com vegetação (NDVI ≥ 0,45) dividida pelos moradores do setor. Setores com menos de 50 moradores ficam sem valor.',w:'vhab'},\n {k:'veg_nat',ax:'amb',")
r5("const F = DATA.features;","const F = DATA.features;\nF.forEach(f=>{ const p=f.properties; p.verde_hab = (p.verde!=null && p.pop>=50 && p.area>0) ? p.verde/100*p.area*1e6/p.pop : null; });")
r5("for(const f of fs){ const p=f.properties, v=p[i.k]; if(v==null) continue;","for(const f of fs){ const p=f.properties, v=p[i.k]; if(i.w==='vhab'){ if(p.verde!=null&&p.pop>0&&p.area>0){ num+=p.verde/100*p.area*1e6; den+=p.pop; } continue; } if(v==null) continue;")
r5("  if(i.u==='m') return","  if(i.u==='m²/hab') return ptBR(fmtN(v))+' m²/hab';\n  if(i.u==='m') return")
open('/home/claude/d/atlas_rmvrc.html','w').write(H); print('vhab ok')
