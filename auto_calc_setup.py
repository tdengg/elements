import os
import eos_calc_use_templ as calc
import search_dir

class Autosetup(object):
    def __init__(self, parset, calcdir):
        self.parset = parset
        self.calcdir = calcdir
        
    def search_for_old(self):
        return
    def setup(self):
        
        return
    def calculate(self):
        calc.CALC(self.param)
        return
    