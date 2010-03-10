
import numpy.linalg as linalg
import numpy as np
import matplotlib.pyplot as plt
import random

import read_numtext as rd

class Birch(object):
    def __init__(self, path, structure):

        self.path = path
        self.structure = structure
        self.out0 = []
        self.out1 = []
        self.out2 = []

        npoints = 11    # number of volume points
        
        ## start parameters:
        b0 = np.float32(0.004) # Bulk-Modulus
        db0 = np.float32(3.)   # derivative of Bulk-Modulus with respect to V 
        itmax = 1000
        epsilon = 0.00005
        grad = -1
        
        structure = self.structure
        
        read = rd.ReadData(self.path, structure)
        a,ein = read.read()
        
        calcs = int(len(a)/npoints)
        j=0
        while j < calcs:
            v = []
            diff = []
            einsub = ein[j*npoints:j*npoints+npoints]
            for latt in a[j*npoints:j*npoints+npoints]:
                v.append(np.float32(latt))
            v0, emin = self.minIn(einsub,v)
            #print(minimization(v0, v, b0, db0, ein, emin))
            arec = np.array([[v0, b0, db0, emin]])
            norm_diff1 = linalg.norm(arec)
            ressq0, fite0, res0 = (self.fitev(arec, v, einsub))
            i=0
            while norm_diff1 > epsilon:
                if i<itmax:# aad < 0:
                    #print arec
                    diff0, parnew0 = self.minimization(arec, v, einsub)
                    ressq, fite, res = self.fitev(parnew0, v, einsub)
                        
                    diff1, parnew1 = self.minimization(parnew0, v, einsub)
                    ressq, fite, res = self.fitev(parnew1, v, einsub)
                    arec = parnew1
                        
                    norm_diff0 = linalg.norm(diff0)
                    norm_diff1 = linalg.norm(diff1)
                    grad = norm_diff1 - norm_diff0
                    #print norm_diff1
                else:
                    break
                i=i+1
                
            parmin, deltamin = self.minimization2(parnew1, v, einsub)
            #print deltamin
            if deltamin < norm_diff1:
                parnew1 = parmin
                print deltamin
            # convert volume to lattice parameter:
                    
            #if structure == 'fcc':
            #    latt = (4. * parnew1[0,0])**(1./3.)
            #elif structure == 'bcc':
            #    latt = (4. * parnew1[0,0])**(1./3.)
            #elif structure == 'hcp':
            #    covera = input('c over a ratio: ')
            #    latta = (parnew1[0,0]/(covera*0.866))**(1./3.)
            #    lattc = latta * covera
                    
            print('---------------------------------------')
            print('volume:                     ' + str(parnew1[0,0]) + ' Bohr')
            print('---------------------------------------')
            #if structure == 'fcc' or structure == 'bcc':
            #    print('equilibrium lattice parameter:   ' + str(latt*0.529177) + ' Angstroem')
            #    print('                                 ' + str(latt) + ' Bohr')
            #elif structure == 'hcp':
            #    print('equilibrium lattice parameter a: ' + str(latta*0.529177) + ' Angstroem')
            #    print('                                 ' + str(latta) + ' Bohr')
            #    print('                              c: ' + str(lattc*0.529177) + ' Angstroem')
            #    print('                                 ' + str(lattc) + ' Bohr')
            #print('---------------------------------------')
            #print('Bulk-Modulus:               ' + str(parnew1[0,1]) + ' au.')
            print('Bulk-Modulus:               ' + str(parnew1[0,1]*2.942104*10**4.) + ' GPa')
            print('---------------------------------------')
            print('derivative of Bulk-Modulus: ' + str(parnew1[0,2]))
            print('---------------------------------------')
            print('minimal energy:             ' + str(parnew1[0,3]) + ' Hartree')
            print('---------------------------------------')
            #plt.plot(v, fite0)
            #plt.plot(v, fite, '')
            #plt.plot(v, ein[j*npoints:j*npoints+npoints], '.')
            #plt.show()
                
            #print(minIn([4,3,2,1,3,5],[2.2,3.2,4.2,5.2,6.2,7.2]))
            self.out0.append(parnew1[0,0])
            self.out1.append(parnew1[0,1]*2.942104*10**4.)
            self.out2.append(parnew1[0,2])
            
            j=j+1
            
    def minIn(self, ein, vin):
        emin = min(ein)
        indexv = ein.index(emin)
        v0 = np.float32(vin[indexv])
        return v0, emin
        
    def fitev(self, par, v, ein):
        fite = []
        deltasq = []
        res = []
        v0 = par[0,0]
        b0 = par[0,1]
        db0 = par[0,2]
        emin = par[0,3]
        i=0
        while i < len(v):
                
            vov = (v0/v[i])**(2./3.)
            fite.append(float(emin + 9. * v0 * b0/16. * ((vov - 1.)**3. * db0 + (vov - 1.)**2. * (6. - 4. * vov))))
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
        v0 = aold[0,0]
        b0 = aold[0,1]
        db0 = aold[0,2]
        emin = aold[0,3]
        while i < len(v):
            ## Jacobian: 
            #  derivative of efit with respect to V0
            a = 3. * db0 * ((v0 / v[i]**(2./3.) - v0**(1./3.) )**2. * (1. / v[i]**(2./3.) - 1./3. * v0**(-2./3.)))
            b = 2. * ((v0**(7./6.) / v[i]**(2./3.) - v0**(1./2.)) * (7./6. * v0**(1./6.) / v[i]**(2./3.) - 0.5 * v0 ** (-1./2.)) * (6. - 4. * (v0/v[i])**(2./3.)))
            c = (v0**(7./6.) / v[i]**(2./3.) - v0**(1./2.))**2. * (-8./3. * v0**(-1./3.) / v[i]**(2./3.))
                
            defit_dV.append((-9.)/16.* b0 * (a + b + c))
            #  derivative of efit with respect to B0
            vov = (v0/v[i])**(2./3.)
            defit_dB.append((-9.) * v0 / 16. * ((vov - 1.)**3. * db0 + (vov - 1.)**2. * (6. - 4. * vov)))
            #  derivative of efit with respect to dB0
            defit_ddB.append((-9.) / 16. * b0 * (v0 / v[i]**(2./3.) - v0**(1./3.))**3.)
            #  derivative of efit with respect to emin    
            defit_demin.append(-1)
                
            jacobian.append([defit_dV[i],defit_dB[i],defit_ddB[i],defit_demin[i]])
            ##
            ## residuals:
            ressq, fite, res = self.fitev(aold, v, ein)
                
            i = i+1
        
        
        A = np.matrix(jacobian)
        r = np.array(res)
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
            amin = anew
            i+=1
            
        return amin, deltamin
        
#a = Birch("/shared/transfer/tde/template/eos-convtest-Be-4.3187-1.56677-0.05-0.01-LSDAPerdew-Wang")
#print a.out0