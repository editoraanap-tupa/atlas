import json, numpy as np, cv2, collections
exec(open('env.py').read().split('# municipios')[0])
F3=3
mun=np.load('mun.npy'); sl=np.load('sl.npy')
H3,W3=H//F3,W//F3
mun3=mun[:H3*F3:F3,:W3*F3:F3]; inR=mun3>0
R3=RES*F3
def pix3(c): c=np.asarray(c,float); return np.stack([(c[:,0]-L0)/R3,(T0-c[:,1])/R3],-1)
def fill3(arr,geom,val):
    for p in polys(geom):
        rings=[pix3(r) for r in p if len(r)>=3]
        if not rings: continue
        cv2.fillPoly(arr,[ipts(rings[0])],val,shift=3)
        for h in rings[1:]: cv2.fillPoly(arr,[ipts(h)],0,shift=3)
def nm(p): return p['nome_bacia'].replace('Bacia de nome não identificado','Bacia sem nome (IBGE)')
lv={l:json.load(open(f'ibge_bacias_nivel_{l}.json' if l!=3 else '/mnt/user-data/uploads/Downloads/ibge_bacias_nivel_3.json'))['features'] for l in (3,4,5,6)}
PAR=None
def build(levels):
    lab=np.zeros((H3,W3),np.int32); props=[None]
    for l in levels:  # do mais detalhado ao menos detalhado; so preenche onde vazio
        for f in lv[l]:
            m=np.zeros((H3,W3),np.uint8); fill3(m,f['geometry'],1)
            m=(m==1)&(lab==0)&inR
            if PAR is not None:
                plab,pprops=PAR; cod=f['properties']['cod_otto']
                okp=np.array([False]+[cod.startswith(p['cod_otto']) for p in pprops[1:]])
                m&=okp[plab]
            if m.sum()*PXA*F3*F3<1: continue
            props.append(dict(f['properties'],nivel=l)); lab[m]=len(props)-1
    return lab,props
out={}
for key,levels in (('bacias',(4,3,5)),('sub',(6,5,4,3,5))):
    lab,props=build(levels)
    if key=='bacias': PAR=(lab.copy(),props)
    feats=[]
    for k in range(1,len(props)):
        m=(lab==k).astype(np.uint8)
        if not m.any(): continue
        cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        rings=[]
        for c in cs:
            if cv2.contourArea(c)<3: continue
            c=cv2.approxPolyDP(c,0.8,True)[:,0,:].astype(float)
            ll=[[round(L0+(x+.5)*R3,4),round(T0-(y+.5)*R3,4)] for x,y in c]; ll.append(ll[0]); rings.append([ll[::-1]])
        if not rings: continue
        # rotulo: ponto interior mais distante da borda
        dt=cv2.distanceTransform(m,cv2.DIST_L2,5); y,x=np.unravel_index(np.argmax(dt),dt.shape)
        p=props[k]
        feats.append({'type':'Feature','properties':{'cod':p['cod_otto'],'nivel':p['nivel'],'nome':nm(p),'rio':p['curso_prin'],'area':round(float(p['area_total'])),'area_rm':round(float(m.sum()*PXA*F3*F3)),'lx':round(L0+(x+.5)*R3,4),'ly':round(T0-(y+.5)*R3,4)},
                      'geometry':{'type':'MultiPolygon','coordinates':rings}})
    out[key]=feats
    sl3=sl[:H3*F3:F3,:W3*F3:F3]; per={}
    # setor -> bacia (moda na grade 90 m; setores pequenos: centroide)
    order=np.argsort(sl3.ravel()); sv=sl3.ravel()[order]; lvv=lab.ravel()[order]
    bounds=np.searchsorted(sv,np.arange(len(F)+2))
    for k,f in enumerate(F):
        v=lvv[bounds[k+1]:bounds[k+2]]; v=v[v>0]
        if not len(v):
            c=np.mean(np.array(polys(f['geometry'])[0][0]),0); x,y=pix3([c])[0].astype(int)
            v=np.array([lab[min(max(y,0),H3-1),min(max(x,0),W3-1)]]); v=v[v>0]
        if len(v): per[f['properties']['id']]=nm(props[int(np.bincount(v).argmax())])
    out['per_'+key]=per
    tot=sum(x['properties']['area_rm'] for x in feats)
    print(key,len(feats),'km2',tot,[(x['properties']['nome'],x['properties']['nivel'],x['properties']['area_rm']) for x in feats])
json.dump(out,open('bacias_out.json','w'),ensure_ascii=False)
print('KB',len(json.dumps(out['bacias']))//1024,len(json.dumps(out['sub']))//1024)
