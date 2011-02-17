import os
import elements


class Autosetup(object):
    def __init__(self, setuppath):
        self.setuppath = setuppath

    def setup(self, param):
        s = open(self.setuppath)
        sustr= s.read()
        setup = eval(sustr)
        
        for key in param.keys():
            if key == 'azero':
                setup['param']['scale'][key] = param[key]
            elif key == 'coazero':
                setup['param']['covera'][key] = param[key]
            elif key == 'calchome':
                setup[key] = param[key]
            else:
                setup['param'][key] = param[key]
                
                
        return setup
    def calculate(self, setup):
        elements.Elements().setup_element(setup)
        return
    
    def ceck_err(self):
        return
    
