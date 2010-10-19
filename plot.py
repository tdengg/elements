import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as etree

class Plot(object):
    def __init__(self):
        self.params = etree.parse('./const_parameters.xml')
        self.eos_data = etree.parse('./eos_data.xml')
        #template = f.getroot().find('elementshome')
    def eosplot_mpl(self):
        vol = []
        energy = []
        expvol = []
        expenergy = []
        eosdata = etree.parse('./eosplot.xml')
        root = eosdata.getroot()
        graphs = root.getiterator('graph')
        for graph in graphs:
            points = graph.getiterator('point')
            for point in points:
                vol.append(float(point.get('volume')))
                energy.append(float(point.get('energy')))
        graphs = root.getiterator('graph_exp')
        for graph in graphs:
            points = graph.getiterator('point')
            for point in points:
                expvol.append(float(point.get('volume')))
                expenergy.append(float(point.get('energy')))
        
        structure = self.params.getroot().find('structure').get('str')
        species = self.params.getroot().find('species').get('spc')
        
        plt.cla()
        plt.plot(vol, energy, '', label='Birch-Murnaghan')
        plt.plot(expvol, expenergy, '.', label='calculation')
        plt.xlabel(r'$volume$   $[{Bohr^3}]$')
        plt.ylabel(r'$total$ $energy$   $[{Hartree}]$')
        plt.legend(loc='best')
        plt.title('Equation of state plot of %(spc)s (%(str)s)'%{'spc':species,'str':structure})
        plt.show()

test = Plot().eosplot_mpl()