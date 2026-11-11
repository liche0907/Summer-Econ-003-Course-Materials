"""ECON 003 exam figure library — winter-final idiom: heavy black line, no colour except one accent."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib import rcParams
rcParams.update({'font.family':'DejaVu Sans','font.size':11})
INK='#111111'; ACC='#FFE9A8'; MUT='#555555'
def _frame(ax,xl,yl,xmax,ymax):
    ax.set_xlim(0,xmax); ax.set_ylim(0,ymax); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel(xl,fontsize=12,fontweight='bold',loc='right')
    ax.set_ylabel(yl,fontsize=12,fontweight='bold',rotation=0,loc='top')
    for s in ('top','right'): ax.spines[s].set_visible(False)
    ax.spines['left'].set_linewidth(1.6); ax.spines['bottom'].set_linewidth(1.6)
    ax.tick_params(length=0)

def budget_line(path,x_int=20,y_int=5,xl='Song downloads',yl='Movie\ntickets',
                marks=True,title=None):
    fig,ax=plt.subplots(figsize=(5.6,4.4))
    ax.plot([0,x_int],[y_int,0],color=INK,lw=2.8)
    if marks:
        ax.plot([0,x_int],[y_int,0],'o',color=INK,ms=7)
        ax.text(-0.9,y_int,str(y_int),fontsize=12,fontweight='bold',ha='right',va='center')
        ax.text(x_int,-0.42,str(x_int),fontsize=12,fontweight='bold',ha='center',va='top')
    _frame(ax,xl,yl,x_int*1.25,y_int*1.30)
    if title: ax.set_title(title,fontsize=11.5,fontweight='bold',color=INK,pad=8)
    fig.tight_layout(); fig.savefig(path,dpi=190,facecolor='white'); plt.close(fig)

def budget_panels(path,x_int=20,y_int=5,xl='Song downloads',yl='Movie\ntickets',title=None):
    """A parallel out · B parallel in · C pivot on x · D pivot on y"""
    cfg=[('A',(x_int*1.5,y_int*1.5)),('B',(x_int*0.6,y_int*0.6)),
         ('C',(x_int*1.5,y_int)),     ('D',(x_int,y_int*1.5))]
    fig,axes=plt.subplots(2,2,figsize=(6.8,5.4))
    for (lab,(xi,yi)),ax in zip(cfg,axes.flat):
        ax.plot([0,x_int],[y_int,0],color=MUT,lw=1.9,ls='--')
        ax.plot([0,xi],[yi,0],color=INK,lw=2.8)
        _frame(ax,xl,'Movies',x_int*1.65,y_int*1.65)
        ax.text(0.93,0.93,lab,transform=ax.transAxes,fontsize=14,fontweight='bold',
                color=INK,ha='center',va='center')
    if title: fig.suptitle(title,fontsize=11.5,fontweight='bold',color=INK,y=0.985)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(path,dpi=190,facecolor='white'); plt.close(fig)

def mb_mc(path,marks=(2.0,4.0,6.0,8.0),xl='Hours studied',yl='$'):
    fig,ax=plt.subplots(figsize=(6.0,4.6))
    q=np.linspace(0.6,9.4,400)
    MB=lambda x:22-1.9*x
    MC=lambda x:2.8+1.3*x
    ax.plot(q,MB(q),color=INK,lw=2.8); ax.plot(q,MC(q),color=INK,lw=2.8)
    ax.text(9.6,MB(9.4),'MB',fontsize=12,fontweight='bold',va='center')
    ax.text(9.6,MC(9.4),'MC',fontsize=12,fontweight='bold',va='center')
    star=(22-2.8)/(1.9+1.3)
    for i,x in enumerate(marks,1):
        ax.plot([x,x],[0,max(MB(x),MC(x))],ls='--',color=MUT,lw=1.2)
        ax.text(x,-1.0,f'Q{i}',fontsize=12,fontweight='bold',ha='center',va='top')
    _frame(ax,xl,yl,11.2,25)
    fig.tight_layout(); fig.savefig(path,dpi=190,facecolor='white'); plt.close(fig)
    return star

def budget_shoes(path):
    """E3-C01-RQ05: $400/mo, shoes $100, jeans $50 -> intercepts 4 shoes / 8 jeans"""
    fig,ax=plt.subplots(figsize=(5.4,4.3))
    ax.plot([0,8],[4,0],color=INK,lw=2.8)
    for x,y in [(0,4),(2,3),(4,2),(6,1),(8,0)]:
        ax.plot(x,y,'o',color=INK,ms=7)
    for v in range(0,5): ax.text(-0.34,v,str(v),fontsize=11,ha='right',va='center')
    for v in range(0,9,2): ax.text(v,-0.30,str(v),fontsize=11,ha='center',va='top')
    _frame(ax,'Pairs of jeans','Pairs of\nshoes',9.6,5.0)
    fig.tight_layout(); fig.savefig(path,dpi=190,facecolor='white'); plt.close(fig)

def mb_bars(path,mb=(60,30,20,10,-10,-15),mc=25,xl='Hours open at night',yl='$',show_mc=True):
    """E3-C03-TP06: marginal benefit per extra hour against a flat marginal cost"""
    fig,ax=plt.subplots(figsize=(6.2,4.4))
    xs=range(1,len(mb)+1)
    ax.bar(xs,mb,width=0.62,color='#F2F2F2',edgecolor=INK,lw=1.8,zorder=3)
    ax.axhline(0,color=INK,lw=1.4,zorder=4)
    if show_mc:
        ax.plot([0.4,len(mb)+0.6],[mc,mc],color=INK,lw=2.6,ls='--',zorder=5)
        ax.text(len(mb)+0.72,mc,f'MC = ${mc}',fontsize=11.5,fontweight='bold',va='center')
    for x,v in zip(xs,mb):
        if show_mc and v>=0 and abs(v-mc)<8:        # would collide with the MC line -> label inside the bar
            ax.text(x,v-8.0,f'{v}',fontsize=10.5,fontweight='bold',ha='center',va='top')
        else:
            ax.text(x,v+(2.6 if v>=0 else -3.0),f'{v}',fontsize=10.5,fontweight='bold',
                    ha='center',va='bottom' if v>=0 else 'top')
    ax.set_xticks(list(xs)); ax.set_xticklabels([str(x) for x in xs],fontsize=11)
    ax.set_yticks([]); ax.set_xlim(0.35,len(mb)+2.4); ax.set_ylim(-30,72)
    ax.set_xlabel(xl,fontsize=12,fontweight='bold')
    ax.set_ylabel('Marginal\nbenefit ($)',fontsize=12,fontweight='bold',rotation=0,loc='top',labelpad=28)
    for s in ('top','right','left'): ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.6); ax.tick_params(length=0)
    fig.tight_layout(); fig.savefig(path,dpi=190,facecolor='white'); plt.close(fig)
