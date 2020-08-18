from ipywidgets import *
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np

def MaxMinInteractiveGraph( coefSlider = True, coefx = 2, coefy = 3 ):

    import seaborn as sns
    sns.set_palette('Set1')

    x = np.linspace(-3, 24)
    zlim = (-.4,1.5,.05)

    if coefSlider:
        c1lim = (-3,3,.5)
        c2lim = (-3,3,.5)
    else:
        c1lim = fixed(coefx)
        c2lim = fixed(coefy)

    def update( zMult = .5, c1 = coefx, c2 = coefy  ):

        fig,ax = plt.subplots(figsize=(12,6))
        
        # constraint 1
        plt.plot(x, 0*x + 5, lw=3, label='y <= 5',color='b')
        plt.fill_between(x, 0, 5, alpha=0.1,color='b')
        
        # constraint 2
        plt.plot(x, 2-x, lw=3, label='x + y >= 2',color='r')
        plt.fill_between(x, 2-x, 12, alpha=0.1,color='r')
        
        # add non-negativity constraints
        plt.plot(np.zeros_like(x), x, lw=3, label='x >= 0',color='c')
        plt.fill_betweenx(x,0,24,alpha=0.1,color='c')
        plt.plot(x, np.zeros_like(x), lw=3, label='y >= 0',color='m')
        plt.fill_between(x,0,12,alpha=0.1,color='m')

        # highlight the feasible region
        path = Path([(2,0),(24,0),(24,5),(0,5),(0,2),(2,0)])
        patch = PathPatch(path, label='feasible region', alpha=0.5)
        ax.add_patch(patch)

        # level curve for profit P
        if (c1 == 0 and c2 == 0):
            obj_line = 0*x -4
        else:
            xcps = np.array([2,24,24,0,0])
            ycps = np.array([0, 0, 5,5,2])
            zcps = c1*xcps + c2*ycps
            zmin = np.min(zcps)
            zmax = np.max(zcps)
            z = ((1-zMult)*zmin + zMult*zmax)
            obj_line = (z-c1*x)/(c2+.0001)

        plt.plot(x, obj_line, 'k--', lw = 3, label = 'Z')

        if (c2 >= 0):
            txt = f'Z = {c1:2.1f} x + {c2:2.1f} y = {z:3.1f}'
        else:
            txt = f'Z = {c1:2.1f} x - {-c2:2.1f} y = {z:3.1f}'
        plt.text( 6, 11, txt, fontsize = 12)
        
        plt.xlabel('x', fontsize=16)
        plt.ylabel('y', fontsize=16)
        plt.xlim(-3, 24)
        plt.ylim(-3, 12)
        plt.legend(loc = 'upper right',fontsize=12)

        plt.show()

    interact(update,zMult=zlim,c1=c1lim,c2=c2lim);