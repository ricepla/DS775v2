from ipywidgets import *
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np
from pyomo.environ import *

def WyndorInteractProfit( coefSlider = False, constraintSlider = False):

    # create model instance
    model = ConcreteModel( name = "Wyndor" )

    # decision variables
    model.doors = Var( domain = NonNegativeReals )
    model.windows = Var( domain = NonNegativeReals )

    # objective function
    model.c1 = Param(default=3,mutable=True)
    model.c2 = Param(default=5,mutable=True)
    model.profit = Objective(expr = model.c1 * model.doors + 
                             model.c2 * model.windows, sense = maximize )

    # constraints
    model.b1 = Param(default=4,mutable=True)
    model.b2 = Param(default=12,mutable=True)
    model.b3 = Param(default=18,mutable=True)
    model.ct_plant1 = Constraint( expr = model.doors <= model.b1 )
    model.ct_plant2 = Constraint( expr = 2*model.windows <= model.b2 )
    model.ct_plant3 = Constraint( expr = 3*model.doors + 2*model.windows <= model.b3 )

    # solver
    solver = SolverFactory('glpk')

    # use seaborn to change the default graphics to something nicer
    # and set a nice color palette
    import seaborn as sns
    sns.set_palette('Set1')

    d = np.linspace(0, 12)
    
    plim = (.5,1.5,.05)
    
    if coefSlider:
        c1lim = (0,10,.5)
        c2lim = (0,10,.5)
    else:
        c1lim = fixed(3)
        c2lim = fixed(5)
        
    if constraintSlider:
        b1lim = (1,7)
        b2lim = (6,18)
        b3lim = (12,24)
    else:
        b1lim = fixed(4)
        b2lim = fixed(12)
        b3lim = fixed(18)

    def update( profScl = .5, c1 = 3, c2 = 5, b1 = 4, b2 = 12, b3 = 18):
        model.c1 = c1
        model.c2 = c2
        model.b1 = b1
        model.b2 = b2
        model.b3 = b3
        solver.solve(model)
        mxprofit = model.profit()
        profit = mxprofit*profScl
 
        plt.figure(figsize=(6,6))
        plt.plot(d, (profit-c1*d)/(c2+0.0001), 'k--', lw = 3, label = 'profit')
        plt.plot(b1 * np.ones_like(d), d, lw=3, label='Plant 1',color='b')
        plt.fill_betweenx(d, 0, b1, alpha=0.1,color='b')
        
        plt.plot(d, b2/2*np.ones_like(d), lw=3, label='Plant 2',color='r')
        plt.fill_between(d, 0, b2/2, alpha=0.1,color='r')
        
        plt.plot(d, (b3-3*d)/2, lw=3, label='Plant 3',color='g')
        plt.fill_between(d, 0, (b3-3*d)/2, alpha=0.1,color='g')   
        
        plt.plot(np.zeros_like(d), d, lw=3, label='d non-negative',color='c')
        plt.plot(d, np.zeros_like(d), lw=3, label='w non-negative',color='m')
        
        plt.xlabel('batches of doors', fontsize=16)
        plt.ylabel('batches of windows', fontsize=16)
        plt.xlim(-0.05, 12)
        plt.ylim(-0.05, 12)
        plt.legend(loc = 'upper right',fontsize=12)
        
        plt.text( 6.2, 6.4, f'Profit = ${1000*profit:,.2f}', fontsize = 12)
        plt.show()  
        
    interact(update,profScl=plim,c1=c1lim,c2=c2lim,b1=b1lim,b2=b2lim,b3=b3lim)