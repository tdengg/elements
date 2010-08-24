"""
Series expansion tool for generating different kinds of series.
"""
class Series(object):
    def __init__(self, structure):
        self.structure = structure
    def volume_steps(self, vzero, dv, vsteps, coverazero, dcovera, coasteps):
        #create volume steps
        volume = []
        covera = []
        i = vsteps - 1    
        while i > -1:
            volume.append(vzero - (i-5)*dv)
            i = i-1
        #create c/a steps
        i = coasteps - 1
        while i > -1:
            covera.append(coverazero - (i-5)*dcovera)
            i = i-1
            #create lattice parameters out of c/a steps
            scale = {}
            for coa in covera:
                scale[str(coa)] = []
                for v in volume:
                    scale[str(coa)].append((2./3.**(1/2.)*v/coa)**(1/3.))
    
        return scale, covera
    
    def covera_steps(self, coazero, dcoa, nsteps):
        #create c/a steps
        covera = []
        i = nsteps - 1
        while i > -1:
            covera.append(coverazero - (i-5)*dcovera)
            i = i-1
        return covera
    
    def latt_steps(self, lattzero, dlatt, nsteps):
        #create lattice parameter steps
        scale = []
        i = nsteps - 1
        while i > -1:
            scale.append(lattzero - (i-5)*dlatt)
            i = i-1
        return scale