"""Fit energy-volume data with Birch-Murnaghan equation of states
    contains:   class::Birch()
                    def::minIn
                    def::fitev
                    def::minimization
                    def::minimization2

    arguments:  -param ........ parameters of calculation (eg. ngridk, swidth, scale ...)
                    type::dictionary
                -calcnr ....... calculation number
                    type::string
                -structure .... structure of unit cell
                    type::string
                -verbose ...... verbosity of output (default = False)
                    type::boolean
                    
    returns:    -----
    
    output:     -self.out0 .... equilibrium volume [Bohr^3]
                -self.out1 .... bulk-modulus at equilibrium [GPa]
                -self.out2 .... derivative of bulk-modulus at equilibrium 
                -self.out3 .... minimum of total energy 
"""
import numpy.linalg as linalg
import numpy as np
import matplotlib.pyplot as plt
import random

import convert_latt_vol

class Birch(object):
    def __init__(self, *args):
        
        verbose = False
        self.verbose = verbose
        a = []
        ein = []
        v = []
        diff = []
        structure = 'bcc'
        ## start parameters:
        b0 = np.float32(0.004) # Bulk-Modulus
        db0 = np.float32(3.)   # derivative of Bulk-Modulus with respect to V 
        itmax = 500
        epsilon = 0.00007
        grad = -1
        
        #read volune and energy
        if len(args) == 0:
            self.path = param['eospath']
            readev = open(param['eospath'] + 'ev', 'r')
            for line in readev:
                la, enin = line.split()
                a.append(float(la))
                ein.append(float(enin))
            readev.close()
            conv = convert_latt_vol.Convert(structure)
            l, v = conv.lattToVolume(param, a)
        else:
            print args
            l = args[0]
            v = args[1]
            ein = args[2]
            
        v0, emin = self.minIn(ein,v)
        
        arec = np.array([[float(v0), float(b0), float(db0), float(emin)]])
        
        norm_diff1 = linalg.norm(arec)
        ressq0, fite0, res0 = (self.fitev(arec, v, ein))
        i=0
        while norm_diff1 > epsilon:
            if i<itmax:# aad < 0:
                
                diff0, parnew0 = self.minimization(arec, v, ein)
                ressq, fite, res = self.fitev(parnew0, v, ein)
                        
                diff1, parnew1 = self.minimization(parnew0, v, ein)
                ressq, fite, res = self.fitev(parnew1, v, ein)
                arec = parnew1
                        
                norm_diff0 = linalg.norm(diff0)
                norm_diff1 = linalg.norm(diff1)
                grad = norm_diff1 - norm_diff0
                #print norm_diff1
            else:
                break
            i=i+1
                
        parmin, deltamin = self.minimization2(parnew1, v, ein)
        #print deltamin
        if deltamin < norm_diff1:
            parnew1 = parmin
            print '2-Norm of residual vector: ' + str(deltamin)
        else:
            deltamin = norm_diff1
            print '2-Norm of residual vector: ' + str(deltamin)
        # convert volume to lattice parameter:
                    
        if structure == 'fcc':
            latt = (4. * parnew1[0,0])**(1./3.)
        elif structure == 'bcc':
            latt = (4. * parnew1[0,0])**(1./3.)
        #elif structure == 'hcp' and len(args) == 0:
            #covera = input('c over a ratio: ')
            #latta = (parnew1[0,0]/(param['covera']*0.866))**(1./3.)
            #lattc = latta * param['covera']
        """if verbose == True:
            print('---------------------------------------')
            print('volume:                     ' + str(parnew1[0,0]) + ' Bohr')
            print('---------------------------------------')
            if structure == 'fcc' or structure == 'bcc':
                print('equilibrium lattice parameter:   ' + str(latt*0.529177) + ' Angstroem')
                print('                                 ' + str(latt) + ' Bohr')
            elif structure == 'hcp':
                print('equilibrium lattice parameter a: ' + str(latta*0.529177) + ' Angstroem')
                print('                                 ' + str(latta) + ' Bohr')
                print('                              c: ' + str(lattc*0.529177) + ' Angstroem')
                print('                                 ' + str(lattc) + ' Bohr')
            print('---------------------------------------')
            print('Bulk-Modulus:               ' + str(parnew1[0,1]) + ' au.')
            print('                            ' + str(parnew1[0,1]*2.942104*10**4.) + ' GPa')
            print('---------------------------------------')
            print('derivative of Bulk-Modulus: ' + str(parnew1[0,2]))
            print('---------------------------------------')
            print('minimal energy:             ' + str(parnew1[0,3]) + ' Hartree')
            print('---------------------------------------')"""
        #else:
        if structure == 'fcc' or structure == 'bcc':
            print(str(round(parnew1[0,0], 4)).rjust(25) + str(round(parnew1[0,1]*2.942104*10**4., 4)).rjust(25) + str(round(parnew1[0,2],4)).rjust(25))
        elif structure == 'hcp':
            print(str(round(parnew1[0,0], 4)).rjust(25) + str(round(parnew1[0,1]*2.942104*10**4., 4)).rjust(25) + str(round(parnew1[0,2],4)).rjust(25))
        #plt.plot(v, fite0)#
        lv = np.linspace(min(v),max(v),100)
        dump, plote, dump = (self.fitev(parnew1, lv, ein))
        
        #print len(lv)
        #print len(plote)
        
        plt.plot(lv, plote, '', label = 'ngridk: ' + '8' + '  swidth: ' + '0.03')
        plt.plot(v, ein, '.')
        plt.xlabel(r'$volume$   $[{Bohr^3}]$')
        plt.ylabel(r'$total$ $energy$   $[{Hartree}]$')
        plt.legend(loc='best')
        
        #plt.show()
                
        #print(minIn([4,3,2,1,3,5],[2.2,3.2,4.2,5.2,6.2,7.2]))
        self.out0 = parnew1[0,0]
        self.out1 = parnew1[0,1]*2.942104*10**4.
        self.out2 = parnew1[0,2]
        self.out3 = parnew1[0,3]
        self.deltamin = deltamin
        
        self.a = a
        self.v = v
        self.ein = ein
        self.p = plt
            
    def minIn(self, ein, vin):
        """ find minimum of total energy
        """
        emin = min(ein)
        indexv = ein.index(emin)
        v0 = np.float32(vin[indexv])
        return v0, emin
        
    def fitev(self, par, v, ein):

        fite = []
        deltasq = []
        res = []
        v0 = np.float32(par[0,0])
        b0 = np.float32(par[0,1])
        db0 = np.float32(par[0,2])
        emin = np.float32(par[0,3])
        i=0
        while i < len(v):
                
            vov = (v0/np.float32(v[i]))**(2./3.)
            fite.append(float(emin + 9. * v0 * b0/16. * ((vov - 1.)**3. * db0 + (vov - 1.)**2. * (6. - 4. * vov))))
            if len(v) == len(ein):
                deltasq.append((fite[i] - ein[i])**2.)
                res.append(fite[i] - ein[i])
            #print (emin - ein[i])**2
            i = i+1
        return deltasq, fite, res
        
    def minimization(self, aold, v, ein):
        i=0
        defit_dV = []
        defit_dB = []
        defit_ddB = []
        defit_demin = []
        jacobian = []
        v0 = np.float32(aold[0,0])
        b0 = np.float32(aold[0,1])
        db0 = np.float32(aold[0,2])
        emin = np.float32(aold[0,3])
        while i < len(v):
	    vi = np.float32(v[i])
            ## Jacobian: 
            #  derivative of efit with respect to V0
            a = 3. * db0 * ((v0 / vi**(2./3.) - v0**(1./3.) )**2. * (1. / vi**(2./3.) - 1./3. * v0**(-2./3.)))
            b = 2. * ((v0**(7./6.) / vi**(2./3.) - v0**(1./2.)) * (7./6. * v0**(1./6.) / vi**(2./3.) - 0.5 * v0 ** (-1./2.)) * (6. - 4. * (v0/vi)**(2./3.)))
            c = (v0**(7./6.) / vi**(2./3.) - v0**(1./2.))**2. * (-8./3. * v0**(-1./3.) / vi**(2./3.))
                
            defit_dV.append((-9.)/16.* b0 * (a + b + c))
            #  derivative of efit with respect to B0
            vov = (v0/vi)**(2./3.)
            defit_dB.append((-9.) * v0 / 16. * ((vov - 1.)**3. * db0 + (vov - 1.)**2. * (6. - 4. * vov)))
            #  derivative of efit with respect to dB0
            defit_ddB.append((-9.) / 16. * b0 * (v0 / vi**(2./3.) - v0**(1./3.))**3.)
            #  derivative of efit with respect to emin    
            defit_demin.append(-1)
                
            jacobian.append([defit_dV[i],defit_dB[i],defit_ddB[i],defit_demin[i]])
            ##
            ## residuals:
            ressq, fite, res = self.fitev(aold, v, ein)
                
            i = i+1
        
        
        A = np.matrix(jacobian)
        r = np.array(res)
	print A, r
        B = np.dot(np.transpose(A),A)
        C = np.dot(np.transpose(A),(r))
        delta = np.transpose(linalg.solve(B,np.transpose(C)))
        anew = aold + 0.1*delta
        
        return res, anew
        
    def minimization2(self, aold, v, ein):
        delta = []
        anew = np.array([[0.,0.,0.,0.]])
        
        i=0
        while i < 50:
            anew[0,0] = aold[0,0] * (random.uniform(-1,1) * 0.00000001 + 1.)
            anew[0,1] = aold[0,1] * (random.uniform(-1,1) * 0.00000001 + 1.)
            anew[0,2] = aold[0,2] * (random.uniform(-1,1) * 0.00000001 + 1.)
            anew[0,3] = aold[0,3] * (random.uniform(-1,1) * 0.00000001 + 1.)
                
            ressq, fite, res = self.fitev(anew, v, ein)
            delta.append(linalg.norm(res))
            if delta[i]<delta[i-1]:
                deltamin = delta[i]
            
            else:
                amin = aold
                deltamin = delta[0]
            amin = anew
            i+=1
        	
        return amin, deltamin
        
#a = Birch("/home/tom/test/",'calc1','fcc')
#print a.out0
