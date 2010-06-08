import xml.etree.ElementTree as etree

import convert_latt_vol
import fitev

class XmlToFit(object):
    def __init__(self, root):
        structure = 'hcp'
        
        self.numb = 0
        self.root = root
        param = self.birch()
        conv = convert_latt_vol.Convert(structure)
        l, v = conv.lattToVolume(param)
        nvol = len(l)/self.numb
        i=0
        while i<self.numb:
            self.fiteos(l[i*nvol:(i+1)*nvol], v[i*nvol:(i+1)*nvol], param['toten'][i*nvol:(i+1)*nvol], structure)
            i=i+1

        
        
    def covera(self):
        param = {}
        scale = []
        toten = []
        covera = []
        volume = []
        f = etree.parse(self.root + 'coa_data.xml')
        root = f.getroot()
        graphs = f.getiterator('graph')
        for graph in graphs:
            points = graph.getiterator('point')
            for point in points:
                scale.append(point.get('scale'))
                covera.append(point.get('covera'))
                toten.append(point.get('totalEnergy'))
        param['scale'] = scale
        param['toten'] = toten
        param['covera'] = covera
        return param
        
    def birch(self):
        param = {}
        scale = []
        toten = []
        covera = []
        f = etree.parse(self.root + 'eos_data.xml')
        root = f.getroot()
    	graphs = f.getiterator('graph')
        self.numb = len(graphs)
        n=0
    	for graph in graphs:
    		points = graph.getiterator('point')
    		for point in points:
    			scale.append(float(point.get('scale')))
    			toten.append(float(point.get('totalEnergy')))
                try:
                    covera.append(float(point.get('covera')))
                except:
                    covera.append(0)
                n=n+1
        param['scale'] = scale
        param['toten'] = toten
        param['covera'] = covera
    	return param
        
    def fiteos(self, scale, volume, toten, structure):
        a=[]
        v = []
        ein = []
        vol0 = [] 
        b0 = []
        db0 = []
        emin = []
        eosFit = fitev.Birch(structure, scale,volume,toten)
            
        a.append(eosFit.a)
        v.append(eosFit.v)
        ein.append(eosFit.ein)
        
           
        vol0.append(eosFit.out0)
        b0.append(eosFit.out1)
        db0.append(eosFit.out2)
        emin.append(eosFit.out3)
        print a, v
        
test = XmlToFit('/home/tom/cluster/calcs/calc2/')
#test.covera()
