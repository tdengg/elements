import numpy as np
import matplotlib.pyplot as plt

class Polyfit():
    def __init__(self, covera, toten, deg):
        self.covera = covera
        self.toten = toten
        self.deg = deg
        
    def fit(self):
        coveramin = 0
        
        coeff = np.polyfit(self.covera, self.toten, self.deg)
        poly = np.poly1d(coeff)
        minx = np.roots(np.poly1d.deriv(poly))
        for minima in minx:
            if float(minima.real) >= min(self.covera)+0.02 and float(minima.real) <= max(self.covera)-0.02 and float(minima.imag)==0.:
                coveramin = minima.real
                break
            else:
                if float(minima.real) < min(self.covera)+0.02 and float(minima.imag)==0.:
                    coveramin = +0.01
                    #print 'minimum of c/a not in calculation range (lower):  setting new range'
                elif float(minima.real) > max(self.covera)-0.02 and float(minima.imag)==0.:
                    coveramin = +0.02
                    #print 'minimum of c/a not in calculation range (higher):  setting new range'
        totenmin = poly(coveramin) 
        
        x = np.linspace(min(self.covera),max(self.covera),1000)

        plt.plot(self.covera,self.toten,'.')
        plt.plot(x,poly(x))
        
        return coveramin, totenmin, plt

#test  
#p = Polyfit([1,2,3,4],[44,33,31,47],3)
#p.fit()