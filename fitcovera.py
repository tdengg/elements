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
try:
    import xml.etree.ElementTree as etree
except:
    import elementteree.ElementTree as etree
import numpy as np
try:
    import matplotlib.pyplot as plt
    mpl = True
except:
    mpl = False
    print 'python library matplotlib not installed'
class Polyfit(object):
    def __init__(self, covera, toten, deg, volume,calchome):
        self.volume = volume
        self.covera = covera
        self.toten = toten
        self.deg = deg
        self.calchome = calchome
        self.fit()
        
    def fit(self):
        
        #check and remove points that do not seam to have reasonable energy values
        """
        poly = []
        res = []
        devsq = []
        rm = []
        coabad = []
        ebad = []
        deg = 2
        nstep = int(len(self.covera)/(deg+1))
        span = nstep*(deg+1)
        remaining = len(self.covera)-nstep*(deg+1)
        
        for j in range(nstep):
            coverapoly = []
            epoly = []
            for i in range(deg+1):
                coverapoly.append(self.covera[nstep*i+j])
                epoly.append(self.toten[nstep*i+j])
            coeff = np.polyfit(coverapoly, epoly, deg)
            poly.append(np.poly1d(coeff))
        j=0
        for p in poly:
            ressq = 0
            devsq.append([])
            for i in range(len(self.covera)):
                ressq = ressq + (p(self.covera[i])-self.toten[i])**2.
                devsq[j].append((p(self.covera[i])-self.toten[i])**2.)
            res.append(ressq)
            j=j+1
        ind = res.index(min(res))
        for i in range(len(self.covera)):
            if devsq[ind][i]*(len(self.covera)) > 5*res[ind]:
                rm.append(self.covera[i])
            print devsq[ind][i]*(len(self.covera)),res[ind]
        for valcoa in rm:
            index = self.covera.index(valcoa)
            coabad.append(valcoa)
            ebad.append(self.toten[index])
            self.covera.remove(valcoa)
            del self.toten[index]
        """
        coabad=[]
        #############
        coveramin = 0
        coaminima = []
        totenmin = []

        newcovera = []
        coeff = np.polyfit(self.covera, self.toten, self.deg)
        poly = np.poly1d(coeff)
        dpoly = np.poly1d.deriv(poly)
        ddpoly = np.poly1d.deriv(dpoly)
        minx = np.roots(dpoly)#
        curv = np.roots(ddpoly)
        mincoa = minx[0].real
        maxcoa = minx[0].real
        for minima in minx:
            if float(minima.real) >= min(self.covera)+0.02 and float(minima.real) <= max(self.covera)-0.02 and ddpoly(minima) > 0:
                coveramin = minima.real
                print 'Emin(c/a) = ' + str(coveramin) + '\n' 
                coamingood = (coveramin)
                totenmingood = (poly(coveramin))
                recalculate = False
                newcovera = coamingood
                break
            else:
                if float(minima.real) < min(self.covera)+0.02 and ddpoly(minima) > 0:
                    errmin = minima.real
                    coamingood = errmin
                    totenmingood = (poly(errmin))
                    recalculate = True
                    newcovera = errmin
                    print 'Volume: %(vol)s; minimum of c/a not in calculation range (lower):  setting new range --> shift mean of calculation range to %(errmin)s'%{'errmin':errmin,'vol':self.volume}
                elif float(minima.real) > max(self.covera)-0.02 and ddpoly(minima) > 0:
                    errmin = minima.real
                    coamingood = errmin
                    totenmingood = (poly(errmin))
                    recalculate = True
                    newcovera = errmin
                    print 'Volume: %(vol)s; minimum of c/a not in calculation range (higher):  setting new range --> shift mean of calculation range to %(errmin)s'%{'errmin':errmin,'vol':self.volume}
                    
                else:
                    errmin = minima.real
                    coamingood = errmin
                    totenmingood = (poly(errmin))

                    newcovera = errmin
                    print 'Not able to determine minimum of c/a-fit', errmin, totenmingood

            if coamingood < mincoa:
                mincoa = coamingood
            if coamingood > maxcoa:
                maxcoa = coamingood

        self.recalculate = recalculate
        self.newcovera = newcovera
        
        
        
        x = np.linspace(min(self.covera),max(self.covera),100)
        if mpl:
            plt.cla()
            plt.plot(self.covera,self.toten,'.',label = str(self.volume))
            plt.plot(x,poly(x))
            plt.xlabel(r'$c/a$')
            plt.ylabel(r'$total$ $energy$   $[{Hartree}]$')
            plt.legend(title = 'Volume in $[Bohr^3]$')
            plt.savefig(self.calchome + 'covera_'+str(min(self.covera))+'_'+str(coveramin)+ '.png')
        
        
        
        self.reschild = etree.Element('graph')
        for i in range(len(x)):
            point = etree.SubElement(self.reschild, 'point')
            point.set('covera',str(x[i]))
            point.set('energy',str(poly(x)[i]))
        self.reschild.set('volume',str(self.volume))
        self.reschild2 = etree.Element('graph_exp')
        for i in range(len(self.covera)):
            point2 = etree.SubElement(self.reschild2, 'point')
            point2.set('covera',str(self.covera[i]))
            point2.set('energy',str(self.toten[i]))
        self.reschild2.set('volume',str(self.volume))
        self.reschild3 = etree.Element('graph_exp_bad')
        for i in range(len(coabad)):
            point3 = etree.SubElement(self.reschild3, 'point')
            point3.set('covera',str(coabad[i]))
            point3.set('energy',str(ebad[i]))
        self.reschild3.set('volume',str(self.volume))
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
