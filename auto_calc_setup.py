import os
import elements
import search_dir

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
                
        return setup
    def calculate(self, setup):
        print setup
        elements.Elements().setup_element(setup)
        return
    
    def ceck_err(self):
        return
    