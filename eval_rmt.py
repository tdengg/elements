"""Calculation of maximal muffin tin radius for given structure.
    contains:   class::RMT()
                    def::get_rmt
                    def::get_structure
                    def::plot_structure
                class::Operations()
                    def::vect_dist
                    def::ri_div_rj
                    def::latt_to_cartesian

"""
import numpy as np
import lxml.etree as etree
import os
import matplotlib.pyplot as plt
from enthought.mayavi import mlab

class RMT(object):
    """
    Calculate muffin tin radius.
                    
    arguments:  -inputfile ........ location of input file
                    type::string
                -mindist .......... distance between muffin tin spheres (not used)
                    type::float
                -Z ................ atomic number of species
                    type::list
                    
    returns:    -----
    
    output:     -self.rmt .... calculated muffin tin radius
                    type::float
    """
    def __init__(self, inputfile, mindist, Z):
        self.inputfile = inputfile
        self.mindist = mindist
        self.Z = Z
        
        self.treein = etree.parse(inputfile)
        self.basis, self.lattice, self.scale = self.get_structure()

        self.rmt = self.get_rmt(Z)
        #self.plot_structure()
        print self.rmt
        
    def get_rmt(self, Z):
        """Calculate maximal muffin tin radius"""
        rmt_min = []
        m=len(self.basis)   #number of species

        rmt = [[ [] for i in range(m)] for i in range(m)]
        
        op = Operations()
        
        #Loop all basis vectors:
        for i in range(m):
            n = len(self.basis[i])
            for k in range(n):
                op.vector1 = op.latt_to_cartesian(self.basis[i][k], self.lattice)
                for j in range(m):
                    n = len(self.basis[j])
                    for l in range(n):
                        op.vector2 = op.latt_to_cartesian(self.basis[j][l], self.lattice)
                        if op.vector2 != op.vector1: rmt[i][j].append(op.vect_dist())
                        else: rmt[i][j].append(100)
        print rmt
        rmt_min = op.get_array_min(rmt)
        #rmt_min = [min( np.array(rmt[i]) * op.ri_div_rj(Z[i],Z[i-1] )) for i in range(m)]                

        #factor = max(rmt_min) # scale muffin tin spheres
        #rmt_min = rmt_min/factor
        #print rmt
        
        return rmt_min
        

    def get_structure(self):
        """Get geometry from Exciting input file."""
        crystal = self.treein.xpath('//crystal/basevect/text()')
        scale = self.treein.xpath('//crystal/@scale')
        
        spcfiles = self.treein.xpath('//species/@speciesfile')
        basevect = (self.treein.xpath("//species[@speciesfile = '%s']/atom/@coord"%spcfile) for spcfile in spcfiles)
        
        split = lambda vect: map(float,vect.split())
        
        basis = [map(split,spc) for spc in basevect] 
        lattice = [vect.split() for vect in crystal]
 
        return basis, lattice, scale
            
            
    def plot_structure(self):
        """Plot structure using mayavi.mlab module."""
        fig = mlab.figure()
        x = [map(float,latt)[0] for latt in self.lattice]
        y = [map(float,latt)[1] for latt in self.lattice]
        z = [map(float,latt)[2] for latt in self.lattice]
        i=0
        for species in self.basis:
            s = []
            xb = [map(float,basev)[0] for basev in species]
            yb = [map(float,basev)[1] for basev in species]
            zb = [map(float,basev)[2] for basev in species]
            j=0
            while j<len(xb): s.append(self.rmt[i]); j+=1
            
            p = mlab.points3d(xb,yb,zb, s, scale_factor = 1)
            
            i+=1
        
        mlab.show()
        return


class Operations(object):
    """Vector operations
    
        input:  -self.vector1
                -self.vector2            
    """
    
    def __init__(self):
        self.vector1 = []
        self.vector2 = []
        self.minarray = []
        self.index = []
    def vect_dist(self):
        """Calculate vector norm."""
        diff_vect = np.array(self.vector1) - np.array(self.vector2)
        return np.sqrt(np.dot(diff_vect,diff_vect))
    
    def ri_div_rj(self,Z_i,Z_j):
        """Calculate ratio of muffin tin radii."""
        eta = 1
        return (1. + eta*Z_j**(1./3.))/(1. + eta*Z_i**(1./3.))
        
    def latt_to_cartesian(self,base_vect,latt):
        """Calculate cartesian basis from lattice coordinates."""
        return list(np.dot(base_vect,[map(float,l) for l in latt]))
    def get_array_min(self,array):
        """Get minimal value and index of entry in multidimensional array."""
        #Recursively search array:
        for i in range(len(array)):
            if type(array[i]) == list: self.get_array_min(array[i])
            else: self.minarray.append(min(array)); break 
        return min(self.minarray)
            
if __name__=='__main__':                
    RMT('input.xml', 1, [2,10])