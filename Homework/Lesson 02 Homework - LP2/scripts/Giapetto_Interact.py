from ipywidgets import *
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np
from pyomo.environ import *

def GiapettoInteractiveGraph( coefSlider = False, constraintSlider = False):

    # create model instance
    model = ConcreteModel( name = "Giapetto" )

    # decision variables
    model.soldiers = Var( domain = NonNegativeReals )
    model.trains = Var( domain = NonNegativeReals )

    # objective function
    model.c1 = Param(default=3,mutable=True)
    model.c2 = Param(default=2,mutable=True)
    model.profit = Objective( expr = model.c1 * model.soldiers + model.c2 * model.trains, sense = maximize )

    # constraints
    model.b1 = Param(default=80,mutable=True)
    model.b2 = Param(default=100,mutable=True)
    model.b3 = Param(default=40,mutable=True)
    model.labor_hours = Constraint( expr = model.soldiers + model.trains <= model.b1 )
    model.finishing_hours = Constraint( expr = 2 * model.soldiers + model.trains <= model.b2 )
    model.soldier_demand = Constraint( expr = model.soldiers <= model.b3 )

    # solver
    solver = SolverFactory('glpk')

    # use seaborn to change the default graphics to something nicer
    # and set a nice color palette
    import seaborn as sns
    sns.set_palette('Set1')

    s = np.linspace(0, 100)

    plim = (.5,1.5,.05)

    if coefSlider:
        c1lim = (0,5,.5)
        c2lim = (0,5,.5)
    else:
        c1lim = fixed(3)
        c2lim = fixed(2)

    if constraintSlider:
        b1lim = (60,120)
        b2lim = (70,130)
        b3lim = (15,50)
    else:
        b1lim = fixed(80)
        b2lim = fixed(100)
        b3lim = fixed(40)

    def update( profScl = .5, c1 = 3, c2 = 2, b1 = 80, b2 = 100, b3 = 40):
        model.c1 = c1
        model.c2 = c2
        model.b1 = b1
        model.b2 = b2
        model.b3 = b3
        solver.solve(model)
        mxprofit = model.profit()
        profit = mxprofit*profScl

        plt.figure(figsize=(6,6))
        plt.plot(s, b1 - s, lw=3, label='carpentry',color='r')
        plt.fill_between(s, 0, b1 - s, alpha=0.1,color='r')

        plt.plot(s, b2 - 2 * s, lw=3, label='finishing',color='g')
        plt.fill_between(s, 0, b2 - 2 * s, alpha=0.1,color='g')

        plt.plot(b3 * np.ones_like(s), s, lw=3, label='demand',color='b')
        plt.fill_betweenx(s, 0, b3, alpha=0.1,color='b')

        plt.plot(np.zeros_like(s), s, lw=3, label='t non-negative',color='c')
        plt.plot(s, np.zeros_like(s), lw=3, label='s non-negative',color='m')

        plt.plot(s, (profit-c1*s)/(c2+.0001), 'k--', lw = 3, label = 'profit')

        plt.xlabel('soldiers', fontsize=16)
        plt.ylabel('trains', fontsize=16)
        plt.xlim(-0.5, 100)
        plt.ylim(-0.5, 100)
        plt.legend(loc = 'upper right',fontsize=12)

        plt.text( 81, 66, f'= {profit:.0f}', fontsize = 14, zorder=10)

    interact(update,profScl=plim,c1=c1lim,c2=c2lim,b1=b1lim,b2=b2lim,b3=b3lim)