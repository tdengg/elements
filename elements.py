import os
import eos_calc_use_templ as calc
import series
import pickle
import sys
import defaults
import numpy as np
import subprocess
from copy import deepcopy

class Elements(object):
    def __init__(self):
        self.currdir = os.getcwd() + '/'
        print  len(sys.argv)
        if len(sys.argv)<=1:
            input = self.currdir + 'my_calcsetup.py'
        
        else:
            input = os.path.abspath(str(sys.argv[1]))
            sys.path.append(sys.argv[1])
        
        if os.path.exists('autoshift.setup'):
            s = open('autoshift.setup','r')
            sustr= s.read()
            setup = eval(sustr)
            s.close()
        else:
            s = open(input)
            sustr= s.read()
                
            setup = eval(sustr)
        
        defaults.set(setup)
        
        if 'elements' in setup.keys():
            path = os.getcwd()
            elements = setup.pop('elements')
            initsetup = deepcopy(setup)
            for element in elements.keys():
                proc1 = subprocess.Popen(['cd %s'%path], shell=True)
                proc1.communicate()
                del setup['param']['scale']
                setup['param']['scale'] = initsetup['param']['scale']
                setup['species'] = element
                name = '%s_'%element
                for key in elements[element].keys():
                    name = name + str(elements[element][key])
                    print initsetup
                    if key == 'azero':
                        setup['param']['scale']['azero'] = elements[element]['azero']
                    else:
                        
                        setup[key] = elements[element][key]
                
                if os.path.exists(path + '/' + name):
                    continue
                proc2 = subprocess.Popen(['mkdir %s'%name], shell=True)
                proc2.communicate()
                setup['calchome'] = path + '/' + name + '/'
                s = open(path + '/' + name + '/' + 'setup.py', 'w')
                s.write(str(setup))
                s.close()
                self.setup_element(setup)
        
        else:
            self.setup_element(setup) 

    def setup_element(self, setup):
        print setup
        expand = series.Series(setup['structure'])      #instance of series expansion class
        if type(setup['param']['scale']) is dict: 
            azero = setup['param']['scale']['azero']
            da = setup['param']['scale']['da']
            asteps = setup['param']['scale']['steps']
            #del setup['param']['scale']
            scale = expand.latt_steps(azero, da, asteps)    #generate steps in lattice parameter
        else: scale = setup['param']['scale']
        if type(setup['param']['covera']) is dict:
            coverazero = setup['param']['covera']['coverazero']
            dcovera = setup['param']['covera']['dcovera']
            coasteps = setup['param']['covera']['steps']
            #del setup['param']['covera']
        else: covera = setup['param']['covera']
        
        
        if type(setup['param']['covera']) is dict and type(setup['param']['scale']) is dict:
            if setup['structure'] in ['hcp','hex'] and setup['mod'] != 'simple_conv':
                vzero = azero**3 * coverazero * 3**(1/2.)/2 #initial volume 
                dvolume = (azero+da)**3 * coverazero * 3**(1/2.)/2 - vzero                        #volume steps
                scale, covera = expand.volume_steps(vzero, dvolume, asteps, coverazero, dcovera, coasteps)    #generate steps in volume and c/a
            elif setup['mod'] == 'simple_conv':
                covera = [coverazero]
                scale = [azero]
            elif setup['mod'] not in ['simple_conv','eos']:
                print 'Error: calculation mode (mod) should be one of: simple_conv, eos!'
            else:
                covera = [1.0]
        
        setup['param']['scale'] = scale
        setup['param']['covera'] = covera
        if 'calchome' not in setup.keys() or setup['calchome'] in ['./','.','']:
            setup['calchome'] = self.currdir
        if 'elementshome' not in setup.keys() or setup['elementshome'] in ['./','.','']:
            setup['elementshome'] = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'
        if 'templatepath' not in setup.keys():
            setup['templatepath'] = os.path.abspath(os.path.dirname(sys.argv[0])) + '/templates/'
        elif setup['templatepath'] in ['./','.','']:
            setup['templatepath'] = self.currdir
        
        calc.CALC(setup)

if __name__=='__main__':
    Elements()
    
           


