"""Convert volume of primitive cell to lattice parameter.

    arguments:  -inputpar ..... parameters of calculation (containing lattice parameter)
                    type::dictionary, lists as values
                -structure .... structure of unit cell
                    type::string
                -covera ....... c/a for hexagonal lattice
                    type::float
    returns:    -latt ......... lattice parameter
                    type::list
                -vol .......... volume of primitive unit cell
                    type::list
"""
class Convert(object):
    def __init__(self, structure):
        self.structure = structure
        
    def lattToVolume(self, inputpar, l = []):
        vol = []
        if len(l) != 0:
            latt = l
        else:
            latt = inputpar['scale']
        for a in latt:
            if self.structure == 'hcp':
                covera = inputpar['covera']
                vol.append(float(a)**3. * covera * 3.**(1./2.)/2.)
            if self.structure == 'fcc':
                vol.append(float(a)**3./4.)
            if self.structure == 'bcc':
                vol.append(float(a)**3./2.)
            if self.structure == 'diamond':
                vol.append(float(a)**3./8.)
        
        return latt, vol
    
    def volumeToLatt(self, vol, covera):
        latt = []
        for v in vol:
            if self.structure == 'hcp':
                latt.append((2.*v/(3.**(1./2.)*covera))**(1./3.))
            if self.structure == 'fcc':
                latt.append((4.*v)**(1./3.))
            if self.structure == 'bcc':
                latt.append((2.*v)**(1./3.))
            if self.structure == 'diamond':
                latt.append((8*v)**(1./3.))
        return latt, vol
    
#test = Convert('fcc') 
#print test.lattToVolume({'scale':[1,2,3,4]})
#print test.volumeToLatt([1,2,3,4],{'covera':[1]})