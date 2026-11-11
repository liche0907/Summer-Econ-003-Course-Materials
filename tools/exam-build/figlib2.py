"""ECON 003 final — figure library, v2.
Label discipline:
  * every value the student must read is an AXIS TICK, never floating text — matplotlib lays ticks
    out on one line so they cannot collide with each other;
  * integer ticks within `guard` of a callout are suppressed;
  * curve names sit INSIDE the axes at the curve's end, with headroom reserved on the right;
  * axis titles are centred (never loc='right'), so they cannot run into a curve label.
"""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from matplotlib import rcParams
rcParams.update({'font.family':'DejaVu Sans','font.size':11})
INK='#111111'; MUT='#666666'; SH='#D2D2D2'; SH2='#EDEDED'; SH3='#BBBBBB'
OUT='figs/'

def ticks(base, calls, guard=None):
    """base ticks + callouts, with base ticks too close to a callout removed.
    guard defaults to 40% of the base tick spacing, so it scales with the axis
    range instead of being a fixed number of data units."""
    base=sorted(base)
    if guard is None:
        steps=[b-a for a,b in zip(base,base[1:]) if b>a]
        guard=0.40*min(steps) if steps else 0.45
    keep=[t for t in base if all(abs(t-c)>guard for c in calls)]
    return sorted(set(keep)|set(calls))

def axes(figsize=(6.2,4.7)):
    fig,ax=plt.subplots(figsize=figsize); return fig,ax

def frame(ax,xl,yl,xmax,ymax,xticks=None,yticks=None,grid=False,xfmt=None,yfmt=None):
    ax.set_xlim(0,xmax); ax.set_ylim(0,ymax)
    if xticks is None: ax.set_xticks([])
    else:
        ax.set_xticks(xticks)
        ax.set_xticklabels([(xfmt(t) if xfmt else ('%g'%t)) for t in xticks],fontsize=10)
    if yticks is None: ax.set_yticks([])
    else:
        ax.set_yticks(yticks)
        ax.set_yticklabels([(yfmt(t) if yfmt else ('%g'%t)) for t in yticks],fontsize=10)
    ax.set_xlabel(xl,fontsize=11.5,fontweight='bold',labelpad=8)
    ax.set_ylabel(yl,fontsize=11.5,fontweight='bold',labelpad=8)
    for s in ('top','right'): ax.spines[s].set_visible(False)
    ax.spines['left'].set_linewidth(1.5); ax.spines['bottom'].set_linewidth(1.5)
    ax.tick_params(length=3.5)
    if grid: ax.grid(alpha=.22,lw=.7); ax.set_axisbelow(True)

def name(ax,x,y,txt,dx=0,dy=0,ha='left',va='center',size=11.5):
    """curve name, placed inside the axes"""
    ax.annotate(txt,xy=(x,y),xytext=(dx,dy),textcoords='offset points',
                fontsize=size,fontweight='bold',ha=ha,va=va,zorder=6,
                bbox=dict(boxstyle='round,pad=0.18',fc='white',ec='none',alpha=0.85))

def readoff(ax,x,y,xmax=None,ymax=None,dot=True):
    """dotted guides from the axes to a point"""
    if dot: ax.plot([x],[y],'o',color=INK,ms=6,zorder=5)
    ax.plot([0,x],[y,y],ls=':',color=MUT,lw=1.1,zorder=1)
    ax.plot([x,x],[0,y],ls=':',color=MUT,lw=1.1,zorder=1)

def save(fig,n):
    fig.tight_layout(); fig.savefig(OUT+n+'.png',dpi=190,facecolor='white'); plt.close(fig)
    print('   ',n)
