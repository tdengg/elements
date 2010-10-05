"""Fit Etot - c/a curves.

    arguments:  -covera .... c/a values
                    type::list
                -toten ..... total energy
                    type::list
                -deg ....... order of polynomial
                    type::list
                -volume .... constant volume (only for legend of plot)
                    type::float
    returns:    none
    
"""

import numpy as np
try:
    import matplotlib.pyplot as plt
    mpl = True
except:
    mpl = False
    print 'python library matplotlib not installed'
class Polyfit(object):
    def __init__(self, covera, toten, deg, volume):
        self.volume = volume
        self.covera = covera
        self.toten = toten
        self.deg = deg
        self.fit()
        
    def fit(self):
        coveramin = 0
        coaminima = []
        totenmin = []
        coeff = np.polyfit(self.covera, self.toten, self.deg)
        poly = np.poly1d(coeff)
        dpoly = np.poly1d.deriv(poly)
        ddpoly = np.poly1d.deriv(dpoly)
        minx = np.roots(dpoly)#
        curv = np.roots(ddpoly)
        
        for minima in minx:
            if float(minima.real) >= min(self.covera)+0.02 and float(minima.real) <= max(self.covera)-0.02 and ddpoly(minima) > 0:
                coveramin = minima.real
                print 'min(c/a) = ' + str(coveramin)
                coamingood = (coveramin)
                totenmingood = (poly(coveramin))
                break
            else:
                if float(minima.real) < min(self.covera)+0.02 and ddpoly(minima) > 0:
                    errmin = minima.real
                    coamingood = errmin
                    totenmingood = (poly(errmin))
                    print 'minimum of c/a not in calculation range (lower):  setting new range --> shift calculation range to %s'%errmin
                elif float(minima.real) > max(self.covera)-0.02 and ddpoly(minima) > 0:
                    errmin = minima.real
                    coamingood = errmin
                    totenmingood = (poly(errmin))
                    print 'minimum of c/a not in calculation range (higher):  setting new range --> shift calculation range to %s'%errmin
                    
                else:
                    errmin = minima.real
                    coamingood = errmin
                    totenmingood = (poly(errmin))
                    print 'not able to determine minimum of c/a-fit'
            
             
        
        x = np.linspace(min(self.covera),max(self.covera),1000)
        if mpl:
            plt.cla()
            plt.plot(self.covera,self.toten,'.',label = str(self.volume))
            plt.plot(x,poly(x))
            plt.xlabel(r'$c/a$')
            plt.ylabel(r'$total$ $energy$   $[{Hartree}]$')
            plt.legend(title = 'Volume in $[Bohr^3]$')
            plt.savefig('./covera_'+str(min(self.covera))+'_'+str(coveramin)+ '.png')
        #try:
        self.coamin = coamingood
        self.totenmin = totenmingood
        #except:
        #    self.coamin = 0
        #    self.totenmin = 0
        #    self.volume = 0
        
        

#test  
#p = Polyfit([1,2,3,4],[44,33,31,47],3)
#p.fit()