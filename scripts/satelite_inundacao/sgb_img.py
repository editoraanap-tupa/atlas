import sys,io,base64; sys.path.insert(0,'/home/claude/x')
from s2lib import *
from PIL import Image
G=np.load('sgbch_grid.npy'); M=json.load(open('sgbch_grid.json')); E0,N1,RS=M['E0'],M['N1'],M['RS']
from common import ll2utm
# limites geográficos da grade
sys.path.insert(0,'/home/claude/f'); from geo import utm2ll
lo,la=utm2ll(np.array([E0,E0+M['W']*RS,E0,E0+M['W']*RS]),np.array([N1,N1,N1-M['H']*RS,N1-M['H']*RS]))
b=[round(float(lo.min()),4),round(float(la.max()),4),round(float(lo.max()),4),round(float(la.min()),4)]; d=0.0003
nx=int(round((b[2]-b[0])/d)); ny=int(round((b[1]-b[3])/d)); lon=b[0]+(np.arange(nx)+.5)*d; lat=b[1]-(np.arange(ny)+.5)*d
LO,LA=np.meshgrid(lon,lat); X,Y=ll2utm(LO,LA); c=np.floor((X-E0)/RS).astype(int); r=np.floor((N1-Y)/RS).astype(int); ok=(c>=0)&(c<M['W'])&(r>=0)&(r<M['H'])
# classe dominante numa vizinhança de 3x3 pixels de 10 m (≈ o pixel de 33 m da imagem)
K=np.zeros((ny,nx),np.uint8); K[ok]=G[r[ok],c[ok]]
IC=np.array([[0,0,0,0],[254,224,139,120],[244,109,67,175],[165,0,38,215]],np.uint8)
bio=io.BytesIO(); Image.fromarray(IC[K],'RGBA').save(bio,'WEBP',lossless=True,method=6)
uri='data:image/webp;base64,'+base64.b64encode(bio.getvalue()).decode()
json.dump({'b':[b[0],b[1],b[0]+nx*d,b[1]-ny*d],'sgbc':uri},open('rast_sgbch.json','w')); print(b,nx,ny,len(uri)//1024,'KB', [(K==k).sum() for k in (1,2,3)])
Image.fromarray(IC[K],'RGBA').resize((nx//3,ny//3)).save('pv_sgbch.png')
