import json, math, collections
import numpy as np, cv2, pickle
from build import dp, ring_area
L=open('../atlas_orig.html').read().split('\n')
HIDRO=json.loads(L[511][len('const HIDRO = '):].rstrip().rstrip(';'))
xs=[];ys=[]
def walk(c):
    if isinstance(c[0],(int,float)): xs.append(c[0]); ys.append(c[1])
    else: [walk(x) for x in c]
for f in HIDRO['features']: walk(f['geometry']['coordinates'])
HB=(min(xs),min(ys),max(xs),max(ys)); print('orig hidro bbox',HB)
OK=set()
for f in HIDRO['features']:
    g=f['geometry']
    if g['type']=='LineString': cs=g['coordinates']
    elif g['type']=='Polygon': cs=g['coordinates'][0]
    else: continue
    for p in cs: OK.add((round(p[0],4),round(p[1],4)))
def inside_orig(coords):
    hit=sum((round(x,4),round(y,4)) in OK for x,y in coords)
    return hit>=max(2,0.5*len(coords))
def rnd(c): return [[round(x,5),round(y,5)] for x,y in c]
def sline(c,eps): return rnd(dp([tuple(p) for p in c],eps))
def area_m2(r):
    lat=math.radians(sum(p[1] for p in r)/len(r)); k=111320
    return abs(ring_area([(x*k*math.cos(lat),y*110540) for x,y in r]))

NEW=[]
def app_w(n):
    if n=='Rio Cuiabá': return 100
    if n=='Rio Coxipó': return 50
    return 30
def geo(e): return [(p['lon'],p['lat']) for p in e['geometry']]

# stitch relation outer members
def stitch(ways):
    ways=[list(w) for w in ways]; rings=[]
    while ways:
        r=ways.pop(0)
        changed=True
        while r[0]!=r[-1] and changed:
            changed=False
            for i,w in enumerate(ways):
                if w[0]==r[-1]: r+=w[1:]; ways.pop(i); changed=True; break
                if w[-1]==r[-1]: r+=w[::-1][1:]; ways.pop(i); changed=True; break
                if w[-1]==r[0]: r=w[:-1]+r; ways.pop(i); changed=True; break
                if w[0]==r[0]: r=w[::-1][:-1]+r; ways.pop(i); changed=True; break
        if len(r)>=4 and r[0]==r[-1]: rings.append(r)
    return rings

R=json.load(open('rios.json'))['elements']
seen=set()
for e in R:
    t=e.get('tags',{})
    if e['type']=='way' and t.get('waterway')=='river':
        c=geo(e)
        if inside_orig(c): continue
        n=t.get('name','')
        NEW.append({'type':'Feature','properties':{'t':'r','n':n,'app':app_w(n)},'geometry':{'type':'LineString','coordinates':sline(c,0.00015)}})
    elif e['type']=='way' and t.get('natural')=='water':
        c=geo(e)
        if len(c)<4 or c[0]!=c[-1] or inside_orig(c): continue
        if area_m2(c)<50000: continue
        NEW.append({'type':'Feature','properties':{'t':'a','n':t.get('name',''),'w':t.get('water','')},'geometry':{'type':'Polygon','coordinates':[sline(c,0.0001)]}})
    elif e['type']=='relation':
        outs=[[(p['lon'],p['lat']) for p in m['geometry']] for m in e.get('members',[]) if m.get('role')=='outer' and m.get('geometry')]
        for r in stitch(outs):
            if inside_orig(r) or area_m2(r)<50000: continue
            NEW.append({'type':'Feature','properties':{'t':'a','n':t.get('name',''),'w':t.get('water','')},'geometry':{'type':'Polygon','coordinates':[sline(r,0.0001)]}})

C=json.load(open('corregos.json'))['elements']
starts=collections.Counter(); ends=collections.Counter()
STREAMS=[]
for e in C:
    t=e.get('tags',{}); c=geo(e)
    if inside_orig(c): continue
    ww=t.get('waterway')
    if ww in ('stream','drain','ditch','canal'):
        tt='c' if ww in ('canal','drain','ditch') else 's'
        NEW.append({'type':'Feature','properties':{'t':tt,'n':t.get('name',''),'app':0 if tt=='c' else 30},'geometry':{'type':'LineString','coordinates':sline(c,0.00003)}})
        if tt=='s': STREAMS.append(c); starts[c[0]]+=1; ends[c[-1]]+=1
    elif t.get('natural')=='water' and len(c)>=4 and c[0]==c[-1]:
        if area_m2(c)<2000: continue
        NEW.append({'type':'Feature','properties':{'t':'a','n':t.get('name',''),'w':t.get('water','')},'geometry':{'type':'Polygon','coordinates':[sline(c,0.00003)]}})
for s in STREAMS:
    if ends[s[0]]==0: NEW.append({'type':'Feature','properties':{'t':'n'},'geometry':{'type':'Point','coordinates':[round(s[0][0],5),round(s[0][1],5)]}})
print('hidro novos',collections.Counter(f['properties']['t'] for f in NEW), len(json.dumps(NEW))/1e6,'MB')
json.dump(NEW,open('hidro_new.json','w'),ensure_ascii=False)

# ---------- APP para setores urbanos novos ----------
rings=pickle.load(open('rings.pkl','rb'))
lines=[f for f in NEW if f['properties']['t'] in ('r','s')]
areas=[f for f in NEW if f['properties']['t']=='a']
nasc=[f['geometry']['coordinates'] for f in NEW if f['properties']['t']=='n']
PX=5.0
APP={}
for cd,rg,sit in rings:
    if sit!='Urbana': continue
    xs=[x for r in rg for x,y in r]; ys=[y for r in rg for x,y in r]
    lat0=math.radians((min(ys)+max(ys))/2); kx=111320*math.cos(lat0); ky=110540
    pad=0.0015
    X0,Y1=min(xs)-pad,max(ys)+pad; X1,Y0=max(xs)+pad,min(ys)-pad
    Wd=int((X1-X0)*kx/PX)+1; Hd=int((Y1-Y0)*ky/PX)+1
    if Wd*Hd>6e7: print('grande',cd); continue
    tp=lambda c: np.array([[int((x-X0)*kx/PX),int((Y1-y)*ky/PX)] for x,y in c],np.int32)
    ms=np.zeros((Hd,Wd),np.uint8)
    for r in rg: pass
    from shp import to_geojson
    for poly in to_geojson(rg):
        cv2.fillPoly(ms,[tp(poly[0])],1)
        for h in poly[1:]: cv2.fillPoly(ms,[tp(h)],0)
    wat=np.zeros_like(ms); ap=np.zeros_like(ms)
    bx=(X0-0.004,Y0-0.004,X1+0.004,Y1+0.004)
    near=lambda c: any(bx[0]<=x<=bx[2] and bx[1]<=y<=bx[3] for x,y in c[::max(1,len(c)//50)] ) or any(bx[0]<=x<=bx[2] and bx[1]<=y<=bx[3] for x,y in c)
    for f in areas:
        c=f['geometry']['coordinates'][0]
        if near(c): cv2.fillPoly(wat,[tp(c)],1)
    if wat.any():
        k=int(2*30/PX)+1; ap|=cv2.dilate(wat,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k)))
    for f in lines:
        c=f['geometry']['coordinates']
        if not near(c): continue
        w=f['properties']['app']
        if w: cv2.polylines(ap,[tp(c)],False,1,thickness=max(1,int(2*w/PX)))
    for x,y in nasc:
        if bx[0]<=x<=bx[2] and bx[1]<=y<=bx[3]: cv2.circle(ap,tuple(tp([(x,y)])[0]),int(50/PX),1,-1)
    land=(ms==1)&(wat==0)
    n=land.sum()
    APP[cd]=round(100*float((land&(ap==1)).sum())/n,1) if n else None
json.dump(APP,open('app_new.json','w'))
print('APP calculado',len(APP), sorted(APP.values())[-10:])
