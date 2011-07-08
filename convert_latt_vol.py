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
        
    def lattToVolume(self, inputpar, l = [], coa = 1):
        vol = []
        if len(l) != 0:
            latt = l
        else:
            latt = inputpar['scale']
        for a in latt:
            if self.structure == 'hcp':
                covera = float(inputpar['covera'][0])
                vol.append(float(a)**3. * covera * 3.**(1./2.)/2.)
            if self.structure == 'hex':
                covera = float(inputpar['covera'][0])
                vol.append(float(a)**3. * covera * 3.**(1./2.)/2.)
            if self.structure == 'fcc':
                vol.append(float(a)**3./4.)
            if self.structure == 'bcc':
                vol.append(float(a)**3./2.)
            if self.structure in ['diamond','zincblende']:
                vol.append(float(a)**3./8.)
            if self.structure == 'rs':
                vol.append(float(a)**3.)
        
        return latt, vol
    
    def volumeToLatt(self, vol, covera):
        latt = []
        i=0
        for v in vol:
            if self.structure == 'hcp':
                latt.append((2.*v/(3.**(1./2.)*float(covera[i])))**(1./3.))
            if self.structure == 'hex':
                latt.append((2.*v/(3.**(1./2.)*float(covera[i])))**(1./3.))
            if self.structure == 'fcc':
                latt.append((4.*v)**(1./3.))
            if self.structure == 'bcc':
                latt.append((2.*v)**(1./3.))
            if self.structure in ['diamond','zincblende']:
                latt.append((8*v)**(1./3.))
            if self.structure == 'rs':
                latt.append((v)**(1./3.))
            if self.structure == 'wurtzite':
                latt.append((8*v)**(1./3.))
            i=i+1
        return latt, vol
    
#test = Convert('fcc') 
#print test.lattToVolume({'scale':[1,2,3,4]})
#print test.volumeToLatt([1,2,3,4],{'covera':[1]})