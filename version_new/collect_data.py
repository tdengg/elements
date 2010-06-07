import xml.etree.ElementTree as etree
import fitev

class XmlToFit(object):
    def __init__(self, root):
        self.root = root
        scale, volume, toten = self.birch()
        #print scale, volume, toten
        i=0
        while i<7:
            self.fiteos(scale, volume, toten)
        
    def covera(self):
        scale = []
        toten = []
        covera = []
        volume = []
        f = etree.parse(self.root + 'coa_data_new.xml')
        root = f.getroot()
        graphs = f.getiterator('graph')
        for graph in graphs:
            points = graph.getiterator('point')
            for point in points:
                scale.append(float(point.get('scale')))
                covera.append(float(point.get('covera')))
                toten.append(float(point.get('totalEnergy')))
                volume.append(float(point.get('volume')))
        return scale, covera, toten
        
    def birch(self):
        scale = []
        toten = []
        volume = []
        f = etree.parse(self.root + 'eos_data_new.xml')
        root = f.getroot()
    	graphs = f.getiterator('graph')
        n=0
    	for graph in graphs:
            #scale.append(graph.get('scale'))
            #toten.append(graph.get('totalEnergy'))
            #volume.append(graph.get('volume'))
    		points = graph.getiterator('point')
            	print graph
    		for point in points:
    			scale.append(point.get('scale'))
    			toten.append(point.get('totalEnergy'))
                volume.append(point.get('volume'))
                print point.get('volume')
                print point.get('scale')
                print n
                n=n+1
                
    	return scale, volume, toten
        
    def fiteos(self, scale, volume, toten):
        a=[]
        v = []
        ein = []
        vol0 = [] 
        b0 = []
        emin = []
        eosFit = fitev.Birch(scale,volume,toten)
            
        a.append(eosFit.a)
        v.append(eosFit.v)
        ein.append(eosFit.ein)
        
           
        vol0.append(eosFit.out0)
        b0.append(eosFit.out1)
        db0.append(eosFit.out2)
        emin.append(eosFit.out3)
test = XmlToFit('/fshome/tde/cluster/calc4/')
#test.covera()
