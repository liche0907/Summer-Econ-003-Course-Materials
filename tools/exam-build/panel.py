import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
BLUE='#003DA5'; GOLD='#B88300'; RED='#CC3333'; GREEN='#2E7D32'; INK='#333333'; GREY='#DDDDDD'
rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.edgecolor':'#888888',
                 'axes.linewidth':0.9,'xtick.color':INK,'ytick.color':INK})

def curves(ax, dshift=0.0, sshift=0.0, show_new=True):
    q=[0.6,9.4]
    D0=[9.0,1.2]; S0=[1.2,9.0]
    ax.plot(q,D0,color=BLUE,lw=2.0,zorder=3)
    ax.plot(q,S0,color=RED,lw=2.0,zorder=3)
    ax.text(9.5,1.15,'D',color=BLUE,fontsize=10,fontweight='bold',va='center')
    ax.text(9.5,9.0,'S',color=RED,fontsize=10,fontweight='bold',va='center')
    if show_new and dshift:
        ax.plot(q,[y+dshift for y in D0],color=BLUE,lw=2.0,ls='--',zorder=3)
        ax.text(9.5,1.15+dshift,"D'",color=BLUE,fontsize=10,fontweight='bold',va='center')
    if show_new and sshift:
        ax.plot(q,[y+sshift for y in S0],color=RED,lw=2.0,ls='--',zorder=3)
        ax.text(9.5,9.0+sshift,"S'",color=RED,fontsize=10,fontweight='bold',va='center')
    ax.set_xlim(0,11.4); ax.set_ylim(0,11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('Quantity',fontsize=8.5,color=INK)
    ax.set_ylabel('Price',fontsize=8.5,color=INK)
    for s in ('top','right'): ax.spines[s].set_visible(False)

PANELS=[('A', dict(sshift=-2.2)), ('B', dict(sshift= 2.2)),
        ('C', dict(dshift= 2.2)), ('D', dict(dshift=-2.2))]
fig,axes=plt.subplots(2,2,figsize=(6.6,5.4))
fig.suptitle('Market for solar panels — which panel shows the change?',
             color=BLUE,fontsize=11.5,fontweight='bold',y=0.975)
for (lab,kw),ax in zip(PANELS,axes.flat):
    curves(ax,**kw)
    ax.set_title(lab,loc='left',color=GOLD,fontsize=11,fontweight='bold',pad=4)
fig.tight_layout(rect=[0,0.01,1,0.94])
fig.savefig('panel_demo.png',dpi=190,facecolor='white')
print('ok')
