import json, gzip, math, heapq, sys, time, collections
import numpy as np, cv2
s=open('/home/claude/d/atlas_rmvrc.html').read()
def grab(pref):
    i=s.index(pref); j=s.index('\n',i); return json.loads(s[i+len(pref):j].rstrip().rstrip(';'))
DATA=grab('<script>const DATA = '); HID=grab('const HIDRO = ')
F=DATA['features']
def polys(g): return [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
OUT={'feats':[],'per':{}}
for win in ['anadem_urb1','anadem_cv']:
    t0=time.time()
    raw=open(f'/mnt/user-data/uploads/Downloads/{win}.bin','rb').read(); h=json.loads(raw[:512])
    Z=np.frombuffer(gzip.decompress(raw[512:]),np.float32).reshape(h['h'],h['w']).copy()
    Hh,Ww=Z.shape; L0,T0,R=h['lon0'],h['lat0'],h['res']
    lat_c=math.radians(T0-Hh*R/2); CA=(R*111320*math.cos(lat_c))*(R*110574)/1e6  # km2 por célula
    def pix(c): c=np.asarray(c,float); return np.stack([(c[:,0]-L0)/R,(T0-c[:,1])/R],-1)
    def ip(xy): return np.round(xy*8).astype(np.int32)
    Z[Z<-1000]=np.nan; Z=np.nan_to_num(Z,nan=float(np.nanmax(Z)))
    # ---- queima da hidrografia OSM (5 m) e ids de linhas nomeadas
    burn=np.zeros((Hh,Ww),np.uint8); lid=np.zeros((Hh,Ww),np.int32); aid=np.zeros((Hh,Ww),np.int32); names=[None]; anames=[None]
    for f in HID['features']:
        p=f['properties']
        if p.get('t') not in ('r','s','c'): continue
        c=pix(f['geometry']['coordinates'])
        if not ((c[:,0]>=0)&(c[:,0]<Ww)&(c[:,1]>=0)&(c[:,1]<Hh)).any(): continue
        cv2.polylines(burn,[ip(c)],False,1,1,shift=3)
        n=p.get('n') or ''
        if n:
            if n not in anames: anames.append(n)
            cv2.polylines(aid,[ip(c)],False,anames.index(n),3,shift=3)
        if n and not n.startswith('Rio '):
            if n not in names: names.append(n)
            cv2.polylines(lid,[ip(c)],False,names.index(n),1,shift=3)
    Zb=(Z-5.0*burn).astype(np.float64)
    # ---- priority-flood + direções (Barnes et al., 2014)
    N=Hh*Ww; zf=Zb.ravel(); rec=np.full(N,-1,np.int64); seen=np.zeros(N,bool); order=np.empty(N,np.int64)
    pq=[]; cnt=0
    for y in range(Hh):
        for x in (0,Ww-1):
            i=y*Ww+x; seen[i]=True; pq.append((zf[i],cnt,i)); cnt+=1
    for x in range(1,Ww-1):
        for y in (0,Hh-1):
            i=y*Ww+x; seen[i]=True; pq.append((zf[i],cnt,i)); cnt+=1
    heapq.heapify(pq)
    offs=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    k=0; zl=zf.tolist(); sl_=seen
    push=heapq.heappush; pop=heapq.heappop
    while pq:
        e,_,i=pop(pq); order[k]=i; k+=1
        y,x=divmod(i,Ww)
        for dy,dx in offs:
            yy=y+dy; xx=x+dx
            if 0<=yy<Hh and 0<=xx<Ww:
                j=yy*Ww+xx
                if not sl_[j]:
                    sl_[j]=True; rec[j]=i; ez=zl[j]
                    push(pq,(ez if ez>e else e,cnt,j)); cnt+=1
    print(win,'flood',round(time.time()-t0),'s')
    # ---- acumulação (células), na ordem inversa
    acc=np.ones(N,np.float64); rl=rec.tolist(); al=acc.tolist(); ol=order.tolist()
    for i in reversed(ol):
        r=rl[i]
        if r>=0: al[r]+=al[i]
    acc=np.array(al)
    print(win,'acc',round(time.time()-t0),'s')
    # ---- exutórios: ponto mais a jusante de cada córrego nomeado; e córregos sem nome ≥ 2 km² que chegam a um rio
    lidf=lid.ravel(); outlet=np.zeros(N,np.int32); onames=[None]
    idx=np.nonzero(lidf)[0]
    for nid in np.unique(lidf[idx]):
        m=(lid==nid).astype(np.uint8)
        m=cv2.dilate(m,np.ones((5,5),np.uint8))
        ncomp,comp=cv2.connectedComponents(m,connectivity=8)
        cf=comp.ravel()
        cells=idx[lidf[idx]==nid]
        for q in range(1,ncomp):
            cc=cells[cf[cells]==q]
            if not len(cc): continue
            c=cc[np.argmax(acc[cc])]
            if acc[c]*CA>=0.3: onames.append(names[nid]); outlet[c]=len(onames)-1
    # córregos sem nome: células de rede (acc ≥ 2 km²) cujo receptor tem acc ≥ 20 km² (chegam a um rio maior)
    net=acc*CA
    recv=np.where(rec>=0,rec,0)
    cand=np.nonzero((net>=2)&(net<20)&(net[recv]>=20)&(outlet==0)&(rec>=0))[0]
    aidf=aid.ravel()
    for c in cand:
        r=rec[c]; nm=''
        for _ in range(8):
            if r<0: break
            if aidf[r]: nm=anames[aidf[r]]; break
            r=rec[r]
        onames.append(('Afluente s/n do '+nm) if nm else ''); outlet[c]=len(onames)-1
    # ---- rótulo por bacia: da foz para montante (ordem de retirada)
    lab=np.zeros(N,np.int32); ll=lab.tolist(); outl=outlet.tolist()
    for i in ol:
        o=outl[i]
        if o: ll[i]=o
        else:
            r=rl[i]; ll[i]=ll[r] if r>=0 else 0
    lab=np.array(ll,np.int32).reshape(Hh,Ww)
    print(win,'lab',round(time.time()-t0),'s', len(onames)-1,'exutórios')
    # ---- setores urbanos na janela
    ul=np.zeros((Hh,Ww),np.int32); fl=[]
    for f in F:
        p=f['properties']
        if p['sit']!='Urbana': continue
        for pg in polys(f['geometry']):
            c=pix(pg[0])
            if ((c[:,0]>=0)&(c[:,0]<Ww)&(c[:,1]>=0)&(c[:,1]<Hh)).all():
                fl.append(p['id']); cv2.fillPoly(ul,[ip(c)],len(fl),shift=3); break
    urb=ul>0
    # microbacias com ≥ 0,05 km² de área urbana
    ua=np.bincount(lab[urb],minlength=len(onames))*CA
    totA=np.bincount(lab.ravel(),minlength=len(onames))*CA
    keep=[o for o in range(1,len(onames)) if ua[o]>=0.05 and (onames[o] or totA[o]>=1.0)]
    for o in keep:
        m=(lab==o).astype(np.uint8)
        area=float(m.sum()*CA)
        if area<0.1: continue
        cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        rings=[]
        for c in cs:
            if cv2.contourArea(c)<4: continue
            c=cv2.approxPolyDP(c,0.7,True)[:,0,:].astype(float)
            llp=[[round(L0+(x+.5)*R,5),round(T0-(y+.5)*R,5)] for x,y in c]; llp.append(llp[0]); rings.append([llp[::-1]])
        if not rings: continue
        dt=cv2.distanceTransform(m,cv2.DIST_L2,3); y,x=np.unravel_index(np.argmax(dt),dt.shape)
        nome=onames[o] or 'Microbacia sem nome'
        OUT['feats'].append({'type':'Feature','properties':{'nome':nome,'area':round(area,2),'urb':round(float(ua[o]),2),'pct_urb':round(100*float(ua[o])/area,1),'lx':round(L0+(x+.5)*R,5),'ly':round(T0-(y+.5)*R,5)},'geometry':{'type':'MultiPolygon','coordinates':rings}})
    # setor -> microbacia (moda)
    labu=lab[urb]; su=ul[urb]
    order2=np.argsort(su,kind='stable'); sv=su[order2]; lv=labu[order2]; b=np.searchsorted(sv,np.arange(len(fl)+2))
    kset=set(keep)
    for q,fid in enumerate(fl):
        v=lv[b[q+1]:b[q+2]]; v=v[np.isin(v,list(kset))]
        if len(v): OUT['per'][fid]=onames[int(np.bincount(v).argmax())] or 'Microbacia sem nome'
    print(win,'ok',round(time.time()-t0),'s',len(keep))
json.dump(OUT,open('micro_out.json','w'),ensure_ascii=False)
print('feats',len(OUT['feats']),'KB',len(json.dumps(OUT['feats']))//1024)
c=collections.Counter(f['properties']['nome'] for f in OUT['feats']); print(c.most_common(40))
