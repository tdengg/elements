import sys
elementshome = '/fshome/tde/git/my_calc/gen/elements/'      # define location of elements home here!
sys.path.append(elementshome)
import eos_calc_use_templ as calc
import series

param = {}
usr = "tde"
scale = []
covera = []
volume = []

azero = 4.319                                   #lattice parameter
etamax = 0.05                                   #steps in lattice parameter
coverazero = 1.6                                #c/a ratio
dcovera = 1.6/50                                #steps in c/a
param['structure'] = ['hcp']
param['mod'] = ['simple_conv']

expand = series.Series(param['structure'])      #instance of series expansion class

scale = expand.latt_steps(azero, etamax, 11)    #generate 11 steps in lattice parameter

if param['structure'][0] == 'hcp' and param['mod'][0] != 'simple_conv':
    vzero = azero**3 * coverazero * 3**(1/2.)/2 #initial volume 
    dvolume = vzero/50                          #volume steps
    scale, covera = expand.volume_steps(vzero, dvolume, 11, coverazero, dcovera, 11)    #generate 11*11 steps in volume and c/a
elif param['mod'][0] == 'simple_conv':
    covera = [coverazero]
    scale = [azero]
else:
    covera = [1.0]

param['scale'] = scale
#param['rmt'] = [2.85]
param['rgkmax'] = [6,7,8,9,10]
param['ngridk'] = [8]
param['swidth'] = [0.01]
param['species'] = ['Be']
param['covera'] = covera
param['calchome'] = ["/fshome/tde/cluster/test3/"]
param['speciespath'] = ["/appl/EXCITING/versions/hydrogen/species/"]
param['templatepath'] = [elementshome + "templates/"]
param['calculate'] = ['False']
calc.CALC(param)
