import matplotlib.pyplot as plt

import calc
import fitev
import convert_latt_vol

import check_calc

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
param['path_cluster'] = ['/fshome/tde/exciting/bin/']

param['element'] = ['V']

structure = 'fcc'

mode = 'serial'
#-----------------------------------------
#calculation 1
azero = 5.77458#7.70744 for Au#5.981 for W #7.653 for Al
etamax = 0.05

i=10
while i > -1:
    scale.append(azero - (i-5)*etamax)
    i = i-1

# set parameters for calculations here:

calcnr = 'calc6' #calcnr = ['calc1']
param['covera'] = [1]
param['ngridk'] = [4,6,10]#ngridk = [2,4,6,8,10]
param['scale'] = scale#scale = []
param['swidth'] = [0.01,0.03,0.05]#swidth = [0.01,0.03,0.05,0.1]
param['rgkmax'] = [4,6,8,10]
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
    scale2 = []
    covera = []
    vol = []
    deltacovera = 0.16/6.
    coverazero = 1.6
    
    i=6
    while i > -1:
        covera.append(coverazero - (i-3)*deltacovera)
        i=i-1
    
    
    conv = convert_latt_vol(structure)
    scale2, dump = conv.lattToVolume(param)
        
    param['covera'] = covera
    calcnr = 'calc2' #calcnr = ['calc1']
    param['ngridk'] = [2,4,6,8,10]#ngridk = [2,4,6,8,10]
    param['rgkmax'] = [4,6,8,10]
    param['scale'] = scale2#scale = []
    param['swidth'] = [0.01,0.03,0.05,0.1]#swidth = [0.01,0.03,0.05,0.1]
    
    calculation = calc.CreateCalc()
    calculation.calc(structure, calcnr, mode, **param)