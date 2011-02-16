import xml.etree.ElementTree as etree


class ANALYZE(object):
    def __init__(self):
        self.deltas()
        return
    def deltas(self):
        self.delta = []

        param = []
        value = []
        conv = {'B':[],'V':[],'err':[],'energy':[]}
        converged = True
        delta = {}
        
        f = etree.parse('auto_conv.xml')
        root = f.getroot()
        tags = f.getiterator('conv')
        i=0
        for tag in tags:
            if i >= ( len(tags) - 3 ):
                conv['energy'].append(float(tag.get('energy')))
                conv['B'].append(float(tag.get('B')))
                conv['V'].append(float(tag.get('V')))
                conv['err'].append(float(tag.get('err')))
                param.append(tag.get('par'))
                value.append(tag.get('val'))
            i=i+1
        
        #Predefined deltas:
        s = open('autoconv.py')
        sustr= s.read()
        setup = eval(sustr)
        
        
        #Calculate deltas:
        for var in conv.keys():
            d = [abs(conv[var][2]-conv[var][0]),abs(conv[var][2]-conv[var][1]),abs(conv[var][1]-conv[var][0])]
            delta['d%s'%var]= max(d)
            
            max_delta = setup['err'][param[0]][var]
            if delta['d%s'%var] > max_delta: converged = False
            
        
        #Output
        print '\n#####################################################'
        print '## Maximal errors of last three convergence steps: ##'
        for out in delta:
            print '#' + ('%8s' %out) + ' :' + ('%15.5f' %delta[out])
        print '#####################################################\n'
        
        return converged

    def status(self):
        if self.ok:
            return True
        else:
            return False
            
if __name__=='__main__':
    ANALYZE()
                
        
    