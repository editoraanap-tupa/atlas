// Priority-flood (Barnes, Lehman & Mulla, 2014) + direções D8 + acumulação + HAND
#include <stdlib.h>
#include <string.h>
typedef struct { double e; long s; int i; } node;
static node* hp; static long hn;
static inline int lt(node a, node b){ return a.e<b.e || (a.e==b.e && a.s<b.s); }
static void push(node x){ long i=hn++; while(i>0){ long p=(i-1)/2; if(lt(x,hp[p])){ hp[i]=hp[p]; i=p; } else break; } hp[i]=x; }
static node pop(void){ node top=hp[0]; node x=hp[--hn]; long i=0; for(;;){ long c=2*i+1; if(c>=hn) break; if(c+1<hn && lt(hp[c+1],hp[c])) c++; if(lt(hp[c],x)){ hp[i]=hp[c]; i=c; } else break; } hp[i]=x; return top; }
// z: elevação; fill: elevação preenchida; rec: receptor; order: ordem de inundação (exutório primeiro); d8=1 usa maior declive na superfície preenchida
void pflood(const double* z, int H, int W, double* fill, int* rec, int* order, int d8){
  long N=(long)H*W; hp=(node*)malloc(sizeof(node)*N); hn=0; char* seen=(char*)calloc(N,1); long s=0,k=0;
  for(int y=0;y<H;y++) for(int x=0;x<W;x++) if(y==0||x==0||y==H-1||x==W-1){ long i=(long)y*W+x; seen[i]=1; rec[i]=-1; fill[i]=z[i]; node n={z[i],s++,(int)i}; push(n); }
  static const int dy[8]={-1,-1,-1,0,0,1,1,1}, dx[8]={-1,0,1,-1,1,-1,0,1};
  while(hn>0){ node n=pop(); int i=n.i; order[k++]=i; int y=i/W, x=i%W;
    for(int d=0;d<8;d++){ int yy=y+dy[d], xx=x+dx[d]; if(yy<0||xx<0||yy>=H||xx>=W) continue; long j=(long)yy*W+xx; if(seen[j]) continue; seen[j]=1; rec[j]=i; double e=z[j]>n.e?z[j]:n.e; fill[j]=e; node m={e,s++,(int)j}; push(m); } }
  if(d8){ for(long i=0;i<N;i++){ if(rec[i]<0) continue; int y=i/W, x=i%W; double best=0; int bj=-1; for(int d=0;d<8;d++){ int yy=y+dy[d], xx=x+dx[d]; if(yy<0||xx<0||yy>=H||xx>=W) continue; long j=(long)yy*W+xx; double dist=(dy[d]&&dx[d])?1.41421356:1.0; double sl=(fill[i]-fill[j])/dist; if(sl>best){ best=sl; bj=(int)j; } } if(bj>=0) rec[i]=bj; } }
  free(hp); free(seen); }
void accum(const int* rec, const int* order, long N, double* acc){ for(long i=0;i<N;i++) acc[i]=1.0; for(long k=N-1;k>=0;k--){ int i=order[k]; int r=rec[i]; if(r>=0) acc[r]+=acc[i]; } }
// drain: 0 não é drenagem; >0 classe da drenagem. hand = z - z(drenagem a jusante); dcls = classe da drenagem alcançada; sem drenagem a jusante: hand=-1
void handc(const double* z, const int* rec, const int* order, const unsigned char* drain, long N, float* hand, unsigned char* dcls){
  double* base=(double*)malloc(sizeof(double)*N);
  for(long k=0;k<N;k++){ int i=order[k]; if(drain[i]){ base[i]=z[i]; dcls[i]=drain[i]; hand[i]=0; continue; } int r=rec[i]; if(r<0||dcls[r]==0){ dcls[i]=0; hand[i]=-1; base[i]=0; continue; } base[i]=base[r]; dcls[i]=dcls[r]; double h=z[i]-base[i]; hand[i]=(float)(h<0?0:h); }
  free(base); }
