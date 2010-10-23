import sys
import eos_calc_use_templ as calc
import series
import my_calcsetup

setup = my_calcsetup.element
azero = setup['param']['scale']['azero']
da = setup['param']['scale']['da']
asteps = setup['param']['scale']['steps']
coverazero = setup['param']['covera']['coverazero']
dcovera = setup['param']['covera']['dcovera']
coasteps = setup['param']['covera']['steps']

del setup['param']['scale']
del setup['param']['covera']

expand = series.Series(setup['structure'])      #instance of series expansion class

scale = expand.latt_steps(azero, da, 11)    #generate 11 steps in lattice parameter

if setup['structure'] in ['hcp','hex'] and setup['mod'] != 'simple_conv':
    vzero = azero**3 * coverazero * 3**(1/2.)/2 #initial volume 
    dvolume = vzero/50                          #volume steps
    scale, covera = expand.volume_steps(vzero, dvolume, asteps, coverazero, dcovera, coasteps)    #generate 11*11 steps in volume and c/a
elif setup['mod'] == 'simple_conv':
    covera = [coverazero]
    scale = [azero]
else:
    covera = [1.0]

setup['param']['scale'] = scale
setup['param']['covera'] = covera

calc.CALC(setup)
