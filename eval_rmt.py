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
        vectors = self.basis + [[map(float,latt) for latt in self.lattice]]
        m=len(vectors)   #number of species + lattice vector

        dist = [[ [] for i in range(m)] for i in range(m)]
        ri_rj = [[ [] for i in range(m)] for i in range(m)]
        
        op = Operations()
        #Get ratio of muffin tin radii.
        for i in range(m):
            for j in range(m):
                if i == m-1: k=0
                elif j == m-1: l=0
                else: k=i; l=j;
                ri_rj[i][j] = op.ri_div_rj(Z[k],Z[l],self.mindist)
        
        #Loop all basis vectors + lattice vectors:
        for i in range(m):
            n = len(vectors[i])
            for k in range(n):
                op.vector1 = op.latt_to_cartesian(vectors[i][k], self.lattice)
                for j in range(m):
                    n = len(vectors[j])
                    for l in range(n):
                        op.vector2 = op.latt_to_cartesian(vectors[j][l], self.lattice)
                        if op.vector2 != op.vector1: dist[i][j].append(op.vect_dist()*ri_rj[i][j]/2)
                        else: dist[i][j].append(100)

        rmt_min = op.get_array_min(dist)
        
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
            while j<len(xb): s.append(self.rmt[i][j]); j+=1
            
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
    
    def ri_div_rj(self,Z_i,Z_j,eta):
        """Calculate ratio of muffin tin radii."""
        return (1. + eta*Z_j**(1./3.))/(1. + eta*Z_i**(1./3.))
        
    def latt_to_cartesian(self,base_vect,latt):
        """Calculate cartesian basis from lattice coordinates."""
        lattice_vect = [map(float,l) for l in latt]
        if base_vect in lattice_vect : return base_vect      
        else: return list(np.dot(base_vect,lattice_vect))
        
    def get_array_min(self,array):
        """Get minimal value and index of entry in multidimensional array."""
        #Recursive array search:
        for i in range(len(array)):
            if type(array[i]) == list: self.get_array_min(array[i])
            else: self.minarray.append(min(array)); continue 
        return min(self.minarray)
            
if __name__=='__main__':                
    RMT('input.xml', 0.95, [2,10])