class ReadData(object):
    def __init__(self ,filename):
        self.filename = filename
        
    def read(self):
        """ open file, read in lines and separate columns --> x, y """
        infile = open(self.filename, 'r')
        
        eoslines = infile.readlines()
        
        x = []
        y = []
        for line in eoslines:
            if len(line.split()) == 2:
                xval, yval = line.split()
                
                if self.structure == 'fcc':
                    vol = float(xval)**3./4.
                elif self.structure == 'bcc':
                    vol = float(xval)**3./2.
                x.append(float(vol))
                y.append(float(yval))
            if len(line.split()) == 3:
                dump, xval, yval = line.split()
                x.append(float(xval))
                y.append(float(yval))                
        #print(x)
        #print(y)       
        return x, y, structure, covera
