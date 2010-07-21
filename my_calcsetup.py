import sys
root = '/home/tde/elements/'
sys.path.append(root)
import eos_calc_use_templ as calc

param = {}
usr = "tde"
scale = []
covera = []

azero = 4.319       #lattice parameter
etamax = 0.05       #steps in lattice parameter
coverazero = 1.6    #c/a ratio
dcovera = 1.6/50    #steps in c/a
param['structure'] = ['hcp']

#create lattice parameter steps
i=10
while i > -1:
    scale.append(azero - (i-5)*etamax)
    i = i-1
if param['structure'][0] == 'hcp':
    #create c/a steps
    i=10    
    while i > -1:
        covera.append(coverazero - (i-5)*dcovera)
        i = i-1
else:
    covera = [1.0]

param['scale'] = scale
param['rgkmax'] = [8]
param['ngridk'] = [8]
param['swidth'] = [0.01]
param['species'] = ['Be']
param['covera'] = covera
param['rootdir'] = ["/home/tde/test/calc6/"]
param['speciespath'] = ["/appl/EXCITING/versions/hydrogen/species/"]
param['templatepath'] = [root + "templates/"]
param['mod'] = ['parallel']

calc.CALC(param)