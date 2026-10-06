import sys,glob
from PIL import Image
tag,cols,w=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
fs=sorted(glob.glob(f's_{tag}_*.png')); ims=[Image.open(f).convert('RGB') for f in fs]
ims=[i.resize((w,int(i.height*w/i.width))) for i in ims]
per=int(sys.argv[4]) if len(sys.argv)>4 else cols*2
for n in range(0,len(ims),per):
    part=ims[n:n+per]; rows=(len(part)+cols-1)//cols; h=max(i.height for i in part)
    c=Image.new('RGB',(cols*w+(cols-1)*6,rows*h+(rows-1)*6),'#888')
    for k,i in enumerate(part): c.paste(i,((k%cols)*(w+6),(k//cols)*(h+6)))
    c.save(f'sh_{tag}_{n//per}.png'); print(f'sh_{tag}_{n//per}.png',[f[len(tag)+3:-4] for f in fs[n:n+per]])
