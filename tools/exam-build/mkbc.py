import figlib, matplotlib.pyplot as plt
from figlib import INK,_frame
def bl(path,xi,yi,xl,yl,pts):
    fig,ax=plt.subplots(figsize=(5.4,4.5))
    ax.plot([0,xi],[yi,0],color=INK,lw=2.8)
    for x,y in pts: ax.plot(x,y,'o',color=INK,ms=7)
    sx=max(1,xi//5); sy=max(1,yi//4)
    for v in range(0,yi+1,sy): ax.text(-xi*0.045,v,str(v),fontsize=11,ha='right',va='center')
    for v in range(0,xi+1,sx): ax.text(v,-yi*0.055,str(v),fontsize=11,ha='center',va='top')
    _frame(ax,'',yl,xi*1.16,yi*1.26)
    ax.set_xlabel(xl,fontsize=12,fontweight='bold',loc='center',labelpad=22)
    fig.tight_layout(); fig.savefig(path,dpi=190,facecolor='white'); plt.close(fig)
bl('fig_c05_bc_tp01.png',10,8,'Units of good X','Units of\ngood Y',[(0,8),(10,0),(5,4)])
bl('fig_c05_bc_cq05.png',12,8,'Units of good A','Units of\ngood B',[(0,8),(12,0)])
print('ok')
