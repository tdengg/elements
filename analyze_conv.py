try:
    import xml.etree.ElementTree as etree
except:
    import elementtree.ElementTree as etree
import os


class ANALYZE(object):
    def __init__(self, calcdir, convpar = ''):
        self.currdir = calcdir
        self.deltas(convpar)
        return
    
    def deltas(self, convpar):
        self.delta = []

        param = []
        value = []
        if convpar == 'rgkmax':
            conv = {'B':[],'err':[]}
        else:
            conv = {'B':[],'V':[],'err':[],'energy':[]}
        converged = True
        delta = {}
        
        f = etree.parse(self.currdir + 'auto_conv.xml')
        root = f.getroot()
        tags = f.getiterator('conv')
        i=0
        for tag in tags:
            if i >= ( len(tags) - 3 ):
                try:
                    conv['energy'].append(float(tag.get('energy')))
                    conv['B'].append(float(tag.get('B')))
                    conv['V'].append(float(tag.get('V')))
                    conv['err'].append(float(tag.get('err')))
                except:
                    print 'Bad fit'
                    self.converged = False
                    return
                param.append((tag.get('par')))
                
            i=i+1
        
        #Predefined maximum deltas:
        s = open(self.currdir + 'autoconv.py')
        sustr= s.read()
        setup = eval(sustr)
        
        
        #Calculate deltas:
        for var in conv.keys():
            d = [abs(conv[var][2]-conv[var][0]),abs(conv[var][2]-conv[var][1]),abs(conv[var][1]-conv[var][0])]
            delta['d%s'%var]= max(d)
            print max(d)
            max_delta = setup['err'][var]
            if delta['d%s'%var] > max_delta: converged = False
            
        
        #Output
        print '\n#####################################################'
        print '## Maximal errors of last three convergence steps: ##'
        for out in delta:
            print '#' + ('%8s' %out) + ' :' + ('%15.5f' %delta[out])
        print '#####################################################\n'
        
        self.converged = converged

    def status(self):
        if self.ok:
            return True
        else:
            return False
            
if __name__=='__main__':
    ANALYZE()
                
        
    