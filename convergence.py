import numpy as np
import matplotlib.pyplot as plt

import calc
import fitev
import check_calc

class ConvergenceTest(object):
    def __init__(self, structure, calcnr, calctype, **kwargs):
        self.structure = structure
        self.calcnr = calcnr
        self.calctype = calctype
        self.kwargs = kwargs
    
    def convergence(self):
        scale = []
        values = []
        a = []
        v = []
        ein = []
        vol0 = []
        b0 = []
        db0 = []
        emin = []
        azero = self.kwargs['scale'][0]
        etamax = 0.05
        i=10
        while i > -1:
            scale.append(azero - (i-5)*etamax)
            i = i-1
        
        self.kwargs['scale'] = scale
        calculation = self.calcnr + '/convergence'
        calculation = calc.CreateCalc(self.structure, calculation, self.calctype, calculate = True, **self.kwargs)
        paramlist = calculation.calc()
        
        rest = check_calc.check(paramlist)
        for param in paramlist:
            if param['eospath'] in values:
                continue
            values.append(param['eospath'])
            eosFit = fitev.Birch(param, self.calcnr, self.structure)
            
            a.append(eosFit.a)
            v.append(eosFit.v)
            ein.append(eosFit.ein)
            
               
            vol0.append(eosFit.out0)
            b0.append(eosFit.out1)
            db0.append(eosFit.out2)
            emin.append(eosFit.out3)
            
        
        #for param in paramlist:
        #    n = len(param[key])
        #    for i in range(1:(n-2)):
        #        par[key]
            
            
            
            
        
        
        
        