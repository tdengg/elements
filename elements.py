import os
import eos_calc_use_templ as calc
import series
import my_calcsetup
import pickle

if os.path.exists('autoshift.setup'):
    s = open('autoshift.setup','rb')
    setup = pickle.load(s)
    s.close()
else:
    setup = my_calcsetup.element
    
expand = series.Series(setup['structure'])      #instance of series expansion class
if type(setup['param']['scale']) is dict: 
    azero = setup['param']['scale']['azero']
    da = setup['param']['scale']['da']
    asteps = setup['param']['scale']['steps']
    del setup['param']['scale']
    scale = expand.latt_steps(azero, da, asteps)    #generate steps in lattice parameter
else: scale = setup['param']['scale']
if type(setup['param']['covera']) is dict:
    coverazero = setup['param']['covera']['coverazero']
    dcovera = setup['param']['covera']['dcovera']
    coasteps = setup['param']['covera']['steps']
    del setup['param']['covera']
else: covera = setup['param']['covera']


if type(setup['param']['covera']) is dict and type(setup['param']['scale']) is dict:
    if setup['structure'] in ['hcp','hex'] and setup['mod'] != 'simple_conv':
        vzero = azero**3 * coverazero * 3**(1/2.)/2 #initial volume 
        dvolume = vzero/50                          #volume steps
        scale, covera = expand.volume_steps(vzero, dvolume, asteps, coverazero, dcovera, coasteps)    #generate steps in volume and c/a
    elif setup['mod'] == 'simple_conv':
        covera = [coverazero]
        scale = [azero]
    else:
        covera = [1.0]

setup['param']['scale'] = scale
setup['param']['covera'] = covera

calc.CALC(setup)
