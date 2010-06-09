import xml.etree.ElementTree as etree

import convert_latt_vol
import fitev
import fitcovera

class XmlToFit(object):
    def __init__(self, root):
        structure = 'hcp'
        self.root = root
        self.coveramin = []
        self.totencoamin = []
        coamin = []
        tmin = []
        plt = []
        l1coa = []
        v1coa = []
        if structure == 'hcp':
            
            conv = convert_latt_vol.Convert(structure)
            
            self.numb_coa = 0
            param1 = self.covera()
            lcoa, vcoa = conv.lattToVolume(param1)
            print vcoa, lcoa
            ncoa = len(param1['covera'])/self.numb_coa
            j=0
            while j<self.numb_coa:
                self.fitcoa(param1['covera'][j*ncoa:(j+1)*ncoa],param1['toten'][j*ncoa:(j+1)*ncoa])
                
                j=j+1
            
            self.numb = 0
            
            param = self.birch()
            l, v = conv.lattToVolume(param)
            nvol = len(l)/self.numb
            i=0
            while i<len(vcoa):
                l1coa.append(lcoa[i])
                v1coa.append(vcoa[i])
                i=i+ncoa

            #i=0
            #while i<self.numb:
            try:
                self.fiteos(l1coa, v1coa, self.totencoamin, structure)
            except:
                print 'Fitting with Birch-Murnaghan not possible. Check calculation parameters and c/a range!'
                return
                #self.fiteos(l[i*nvol:(i+1)*nvol], v[i*nvol:(i+1)*nvol], param['toten'][i*nvol:(i+1)*nvol], structure)
            #    i=i+1
        
    def covera(self):
        param = {}
        scale = []
        toten = []
        covera = []
        volume = []
        f = etree.parse(self.root + 'coa_data.xml')
        root = f.getroot()
        graphs = f.getiterator('graph')
        self.numb_coa = len(graphs)
        for graph in graphs:
            points = graph.getiterator('point')
            for point in points:
                scale.append(float(point.get('scale')))
                covera.append(float(point.get('covera')))
                toten.append(float(point.get('totalEnergy')))
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
        #print a, v
    def fitcoa(self, coa, toten):
        fitcoa = fitcovera.Polyfit(coa,toten,3)
        self.coveramin.append(fitcoa.coamin)
        self.totencoamin.append(fitcoa.totenmin)
    

test = XmlToFit('/fshome/tde/cluster/calc2/')
#test.covera()
