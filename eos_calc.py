import matplotlib.pyplot as plt
import os

import calc
import fitev
import convert_latt_vol
import check_calc
import fitcovera
import convergence

param1 = []
param2 = []
scale = []
vol0 = []
emin = []
b0 = []
db0 = []
param = {}

a = []
v = []
ein = []
values = []

#input
param['rootdir'] = ['/fshome/tde/test/'] #path
param['rootdir_cluster'] = ['/fshome/tde/test/']
param['path'] = ['/fshome/tde/git/exciting/']
param['path_cluster'] = ['/fshome/tde/git/exciting/bin/']

param['element'] = ['Be']

structure = 'hcp'

mode = 'parallel'
#-----------------------------------------
#calculation 1
azero = 5.5762#4.3187Be#7.70744 for Au#5.981 for W #7.653 for Al
etamax = 0.05
if structure != 'hcp':
    i=10
    while i > -1:
        scale.append(azero - (i-5)*etamax)
        i = i-1
    
    # set parameters for calculations here:
    
    calcnr = 'calc6' #calcnr = ['calc1']
    param['covera'] = [1]
    param['ngridk'] = [6,10]#ngridk = [2,4,6,8,10]
    param['scale'] = scale#scale = []
    param['swidth'] = [0.01]#swidth = [0.01,0.03,0.05,0.1]
    param['rgkmax'] = [8,10]
    #param['rgkmax'] = [4]
    
    
    calculation = calc.CreateCalc(structure, calcnr, mode, calculate = False, **param)#ngridk, swidth, element, scale)
    paramlist = calculation.calc()
    
    check_calc.check(paramlist)
    
    print('Volume [Bohr^3]'.rjust(25) + 'Bulk-Modulus [GPa]'.rjust(25) + 'deriv of Bulk-Modulus'.rjust(25))
    for par in paramlist:
        
        if par['eospath'] in values:
            continue
        values.append(par['eospath'])
        #print par1, par2
        eosFit = fitev.Birch(par, calcnr, structure, par['covera'])
            
        a.append(eosFit.a)
        v.append(eosFit.v)
        ein.append(eosFit.ein)
        
           
        vol0.append(eosFit.out0)
        b0.append(eosFit.out1)
        db0.append(eosFit.out2)
        emin.append(eosFit.out3)
    
    
    ### plot volume-energy curves
    ploteos = eosFit.p
    ploteos.savefig(str(param['rootdir'][0]) + '/' + calcnr + '/eosplot.png')
    #ploteos.show()
    
    
    ### write eos_out
    f = open(str(param['rootdir'][0]) + '/' + calcnr + '/eos_out', 'a+')
    i=0
    f.writelines('volume'.rjust(15) + 'dB0'.rjust(15) + 'B0'.rjust(15) + 'energy'.rjust(15) + '\n')
    print vol0
    print b0
    print db0
    print emin
    while i < len(vol0):
        f.writelines(str(round(vol0[i],4)).rjust(15) + str(round(db0[i],4)).rjust(15) + str(round(b0[i],4)).rjust(15) + str(round(emin[i],4)).rjust(15) + '\n\n')
        f.writelines('lattice param.'.rjust(15) + 'volume'.rjust(15) + 'energy'.rjust(15) + '\n')
        j = 0
        while j < len(a[i]):
            print a[i][j], v[i][j], ein[i][j]
            f.writelines(str(a[i][j]).rjust(15) + str(v[i][j]).rjust(15) + str(ein[i][j]).rjust(15)  + '\n\n')
            j = j+1
        i=i+1
    f.close()
#------------------------------------------
#calculation2
if structure == 'hcp':
    calcnr = 'calc10'
    convparam = {}
    convparam['rootdir'] = param['rootdir']
    convparam['rootdir_cluster'] = param['rootdir_cluster']
    convparam['path'] = param['path']
    convparam['path_cluster'] = param['path_cluster']
    convparam['element'] = param['element']
    
    convparam['covera'] = [1.5855]
    convparam['ngridk'] = [10]#ngridk = [2,4,6,8,10]
    convparam['scale'] = [5.5747]#scale = []
    convparam['swidth'] = [0.01,0.03,0.05,0.1]#swidth = [0.01,0.03,0.05,0.1]
    convparam['rgkmax'] = [4,6,8,10]
    conv = convergence.ConvergenceTest(structure, calcnr, mode, **convparam)
    
    conv.convergence()

    scale_const_vol = []
    dep_scale = []
    covera = []
    vol = []
    dep_vol = []
    dep_covera = []
    deltacovera = 0.16/6.
    coverazero = 1.6
    param['covera'] = 1.6
    
    i=10
    while i > -1:
        scale_const_vol.append(azero - (i-5)*etamax)
        i = i-1
    #create volume steps
    conv = convert_latt_vol.Convert(structure)
    dump, const_vol = conv.lattToVolume(param, scale_const_vol)
    
    #variation of c/a:
    i=6
    while i > -1:
        covera.append(coverazero - (i-3)*deltacovera)
        i=i-1
    
    #calculate lattice parameter for c/a steps with constant volume (steps)
    for volume in const_vol:
        for covera_step in covera:
            dep_scale.append((2.*volume/((3.)**(1./2.)*covera_step))**(1./3.))
            dep_vol.append(volume)
            dep_covera.append(covera_step)
        
        
    param['covera'] = dep_covera
    
    calcnr = 'calc10' #calcnr = ['calc1']
    
    param['ngridk'] = [6]#ngridk = [2,4,6,8,10]
    param['rgkmax'] = [8]
    param['scale'] = dep_scale#scale = []
    param['swidth'] = [0.01]#swidth = [0.01,0.03,0.05,0.1]
    

    
    calculation = calc.CreateCalc(structure, calcnr, mode, calculate = True, **param)
    paramlist = calculation.calcDependentParam(['covera','scale'])
    
    check_calc.check(paramlist)
    
    for par in paramlist:
        if par['eospath'] in values:
            continue
        values.append(par['eospath'])
    
    values = []
    totenmin = []
    coveramin = []
    scalemin = []
    volmin = []
    for volume in const_vol:
        k=0
        coa = []
        tote = []
        values = []
        
        for vol in dep_vol:
            if vol == volume:    
                scale = dep_scale[k]
                covera = dep_covera[k]
                for par in paramlist:
                    if par['scale'] == scale and par['covera'] == covera and par.values() not in values:
                        values.append(par.values())
                        os.chdir(par['eospath'] + str(par['scale']))
                        infile = open('./TOTENERGY.OUT', 'r')
                        totenlines = infile.readlines()
                        for lines in totenlines:
                            toten = lines
                                
                        os.chdir(par['rootdir'] + calcnr)
                        if os.path.isdir('./' + str(vol)) == False:
                            os.mkdir('./' + str(vol))
                        out = str(vol) + '    ' + str(covera) + '    ' + str(scale) + '    ' + str(toten) 
                        os.chdir(par['rootdir'] + calcnr + '/' + str(vol))
                        outfile = open('./energy_volume', 'a+')
                        outfile.writelines(out)
                        outfile.close()
        
            
                        coa.append(float(covera))
                        tote.append(float(toten))
                    else:
                        continue
                if k==0:
                    del coa[0]
                    del tote[0]    
                            
            k = k+1
        
        fit = fitcovera.Polyfit(coa,tote,4)
        c, t, plt1 = fit.fit()
        coveramin.append(c)
        totenmin.append(t)
        scalemin.append((2.*volume/(3.**(1/2.)*c))**(1/3.))
        volmin.append(volume)
    
    plt1.show()
    
    #Birch-Murnaghan:
    eosFit = fitev.Birch(param, calcnr, structure, scalemin, volmin, totenmin)
            
    a.append(eosFit.a)
    v.append(eosFit.v)
    ein.append(eosFit.ein)
        
           
    vol0.append(eosFit.out0)
    b0.append(eosFit.out1)
    db0.append(eosFit.out2)
    emin.append(eosFit.out3)
    
    plt2 = eosFit.p
    plt2.show()
        
        
        