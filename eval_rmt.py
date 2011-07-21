import numpy as np
import lxml.etree as etree
import os
import matplotlib.pyplot as plt

class RMT(object):
    def __init__(self, inputfile, dist):
        self.inputfile = inputfile
        self.dist = dist
        
        self.treein = etree.parse(inputfile)
        geometry = self.get_structure()
        print geometry
    def get_rmt(self):
        return
    def get_structure(self):
        basis = np.array([])
        crystal = self.treein.xpath('//crystal')
        species = self.treein.xpath('//species')
        speciesname = self.treein.xpath('//species/@speciesfile')
        for element in species:
            basevect = np.array([])
            base = element.xpath('//basevect')
            
            vect = base.split()
            for comp in vect:
                basevest.append(comp)
            basis.append(basevect)
            
        return basis
            
        
        return 
    def plot_structure(self):
        return

if __name__=='__main__':                
    RMT('input.xml', 2)