import json, csv, re, math
from shp import *
M={'5100102','5102678','5103007','5103403','5106109','5107800','5108402'}

def load(fn):
    L=[l.rstrip('\n') for l in open(fn,encoding='utf-8',errors='replace') if not l.startswith('#')]
    hdr=[h.strip('"').upper() for h in L[0].split(';')]
    out={}
    for l in L[1:]:
        v=[x.strip('"') for x in l.split(';')]
        if len(v)<2: continue
        out[v[0]]=dict(zip(hdr,v))
    return out
T={k:load(f'rmvrc_{k}.csv') for k in ['basico','demografia','cor_ou_raca','alfabetizacao','domicilio2','renda','entorno_moradores']}

def g(d,k):
    """value or None (X = sigilo)"""
    if d is None: return None
    v=d.get(k)
    if v in (None,'','X','.'): return None
    try: return float(v.replace(',','.'))
    except: return None
def s(d,ks):
    """sum treating X as zero; None if all missing / row absent"""
    if d is None: return None
    vals=[g(d,k) for k in ks]
    if all(v is None for v in vals): return None
    return sum(v or 0 for v in vals)
def pct(a,b):
    if a is None or not b: return None
    return round(100*a/b,1)

def indicators(cd, b):
    p={}
    B=T['basico'].get(cd); D=T['demografia'].get(cd); C=T['cor_ou_raca'].get(cd); A=T['alfabetizacao'].get(cd)
    H=T['domicilio2'].get(cd); R=T['renda'].get(cd); E=T['entorno_moradores'].get(cd)
    pop=g(B,'V0001') or 0; dppo=g(B,'V0007') or 0
    p['pop']=int(pop); p['dppo']=int(dppo)
    p['mor']=g(B,'V0005')
    ages=[f'V010{n}' for n in range(31,42)]
    tot=s(D,ages)
    p['idosos']=pct(s(D,['V01040','V01041']),pop)
    p['criancas']=pct(s(D,['V01031','V01032']),pop)
    p['mulheres']=pct(g(D,'V01008'), s(D,['V01007','V01008']))
    ctot=s(C,['V01317','V01318','V01319','V01320','V01321'])
    p['negros']=pct(s(C,['V01318','V01320']),pop)
    p['indig']=pct(g(C,'V01321'),pop)
    ab=s(H,['V00111','V00112','V00113','V00114','V00115','V00116','V00117','V00118'])
    p['agua']=pct(g(H,'V00111'),dppo)
    ce=s(H,['V00199','V00200','V00201'])
    p['agua_enc']=pct(g(H,'V00199'),dppo)
    es=s(H,[f'V00{n}' for n in range(309,317)])
    p['esgoto']=pct(s(H,['V00309','V00310']),dppo)
    p['esg_prec']=pct(s(H,['V00312','V00313','V00314','V00315','V00316']),dppo)
    lx=s(H,[f'V00{n}' for n in range(397,403)])
    p['lixo']=pct(s(H,['V00397','V00398']),dppo)
    bn=s(H,['V00494','V00495'])
    p['sem_banh']=pct(g(H,'V00495'),dppo)
    p['renda']=g(R,'V06004'); p['renda_med']=g(R,'V06006')
    na=g(A,'V00901'); sa=g(A,'V00900')
    p['analf']=pct(na,(na or 0)+(sa or 0)) if na is not None else None
    if p['analf'] is not None: p['analf']=max(0,p['analf'])
    et=g(E,'V05200')
    def ep(ks): return pct(s(E,ks),et) if et else None
    p['pav']=ep(['V05206']); p['arvore']=ep(['V05231','V05232','V05233']); p['arv5']=ep(['V05233'])
    p['luz']=ep(['V05212']); p['calcada']=ep(['V05221']); p['bueiro']=ep(['V05209']); p['onibus']=ep(['V05215'])
    pm=[g(D,f'V010{n:02d}') for n in range(9,20)]; pf=[g(D,f'V010{n:02d}') for n in range(20,31)]
    p['pm']=[int(x or 0) for x in pm] if D else None; p['pf']=[int(x or 0) for x in pf] if D else None
    if not pop: p['pm']=p['pf']=None
    return p
