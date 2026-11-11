import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib import rcParams
rcParams.update({'font.family':'DejaVu Sans','font.size':11})
INK='#111111'
# VC = aQ^3 - bQ^2 + cQ  ->  AVC = aQ^2 - bQ + c ; MC = 3aQ^2 - 2bQ + c ; MC meets AVC at its min
a,b,c,FC = 0.5,4.0,16.0,36.0
AVC=lambda Q: a*Q**2-b*Q+c
MC =lambda Q: 3*a*Q**2-2*b*Q+c
ATC=lambda Q: AVC(Q)+FC/Q
P=22.0; Q=6.0                       # MC(6)=22  -> profit-maximising output
atc,avc = ATC(Q), AVC(Q)            # 16 and 10
assert abs(MC(Q)-P)<1e-9 and atc<P

fig,ax=plt.subplots(figsize=(6.6,5.2))
ax.fill_between([0,Q],[atc,atc],[P,P],  color='#FFE9A8',zorder=1)
ax.fill_between([0,Q],[avc,avc],[atc,atc],color='#E8EEF7',zorder=1)
ax.fill_between([0,Q],[0,0],[avc,avc],  color='#F2F2F2',zorder=1)
RANGES=((ATC,'ATC',2.05,8.6,1.5),(AVC,'AVC',1.35,8.6,-1.0),(MC,'MC',1.35,6.45,0.6))
for f,lab,lo,hi,dy in RANGES:
    qq=np.linspace(lo,hi,400)
    ax.plot(qq,f(qq),color=INK,lw=2.6,zorder=4)
    ax.text(hi+0.18,f(hi)+dy,lab,fontsize=12,fontweight='bold',va='center',color=INK)
ax.plot([0,8.6],[P,P],color=INK,lw=2.0,zorder=4)
ax.text(8.78,P-0.9,'P = MR',fontsize=12,fontweight='bold',va='center',color=INK)
ax.plot([Q,Q],[0,P],ls='--',color='#555555',lw=1.4,zorder=3)
ax.plot(Q,P,'o',color=INK,ms=7,zorder=6)
for y0,y1,lab in ((atc,P,'A'),(avc,atc,'B'),(0,avc,'C')):
    ax.text(1.12,(y0+y1)/2,lab,fontsize=16,fontweight='bold',ha='center',va='center',color=INK,zorder=6)
ax.set_xticks([Q]); ax.set_xticklabels(['Q*'],fontsize=12,fontweight='bold')
ax.set_yticks([avc,atc,P]); ax.set_yticklabels(['','',''])
ax.set_xlim(0,10.6); ax.set_ylim(0,30)
ax.set_xlabel('Q',fontsize=13,fontweight='bold',loc='right')
ax.set_ylabel('P',fontsize=13,fontweight='bold',rotation=0,loc='top')
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.spines['left'].set_linewidth(1.6); ax.spines['bottom'].set_linewidth(1.6)
ax.tick_params(length=0)
fig.tight_layout(); fig.savefig('pattern2_demo.png',dpi=190,facecolor='white')
print(f'P={P} Q*={Q} ATC={atc} AVC={avc} | A=profit {(P-atc)*Q} | B=TFC {(atc-avc)*Q} | C=TVC {avc*Q}')
