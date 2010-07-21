"""analyse, plot and fit data 

    arguments:  -root ..... root directory of calculation tree structure
                    type::string
    returns:    none
    
"""
import xml.etree.ElementTree as etree
import subprocess
import os
try:
    import matplotlib.pyplot as plt
    mpl = True
except:
    mpl = False
import convert_latt_vol
import fitev
import fitcovera

class XmlToFit(object):
    def __init__(self, root):
        #root = str(input('Enter path of calculations directory: '))
        #structure = 'hcp'
        self.root = root
        self.coveramin = []
        self.totencoamin = []
        
        self.vol0_eos = [] 
        self.b0_eos = []
        self.db0_eos = []
        self.emin_eos = []
        self.p = []
        
        coamin = []
        tmin = []
        plt = []
        l1coa = []
        v1coa = []
        
        f = etree.parse(self.root + 'const_parameters.xml')
        template = f.getroot().find('executable')
        structure = f.getroot().find('structure').get('str')
        if os.path.exists(self.root + 'coa_data.xml') == False:
            proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fitcovera.xsl ' + self.root + 'parset.xml > ' + self.root +  'coa_data.xml'], shell=True)
            proc1.communicate()
            
        if os.path.exists(self.root + 'eos_data.xml') == False:
            proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fiteos.xsl ' + self.root + 'parset.xml > ' + self.root +  'eos_data.xml'], shell=True)
            proc1.communicate()
            
        if structure == 'hcp':
            
            conv = convert_latt_vol.Convert(structure)
            
            self.numb_coa = 0
            param1 = self.covera()
            self.i=0
            for self.i < len(self.ncovera*self.neos/):
            lcoa, vcoa = conv.lattToVolume(param1, param1['scale'][self.i])
            param1['volume'].append([])
            param1['volume'][self.i] = vcoa
            #print vcoa, lcoa
            ncoa = len(param1['covera'])/self.numb_coa
            j=0
            while j<self.numb_coa:
                self.fitcoa(param1['covera'][j*ncoa:(j+1)*ncoa],param1['toten'][j*ncoa:(j+1)*ncoa],param1['volume'][j*ncoa])
                j=j+1
            
            self.numb = 0
            param = self.birch()
            l, v = conv.lattToVolume(param, param['scale'][0])
            nvol = len(l)/self.numb
            i=0
            while i<len(vcoa):
                l1coa.append(lcoa[i])
                v1coa.append(vcoa[i])
                i=i+ncoa
            self.write_covera()
            #i=0
            #while i<self.numb:
            try:
                self.fiteos(l1coa, v1coa, self.totencoamin, structure)
                
            except:
                print 'Fitting with Birch-Murnaghan not possible. Check calculation parameters and c/a range!'
                return
            self.write_eos()
                #self.fiteos(l[i*nvol:(i+1)*nvol], v[i*nvol:(i+1)*nvol], param['toten'][i*nvol:(i+1)*nvol], structure)
            #    i=i+1
        else:
            conv = convert_latt_vol.Convert(structure)
            param2 = self.birch()
            self.n=0
            while self.n < len(param2['scale']):
                l, v = conv.lattToVolume(param2, param2['scale'][self.n])
                self.fiteos(l, v, param2['toten'][self.n], structure)
                self.write_eos()
                self.n=self.n+1
            if mpl:
                self.p[3].show()
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
        n=0
        for graph in graphs:
            scale.append([])
            toten.append([])
            covera.append([])
            points = graph.getiterator('point')
            self.pointscovera = len(points)
            for point in points:
                scale[n].append(float(point.get('scale')))
                covera[n].append(float(point.get('covera')))
                toten[n].append(float(point.get('totalEnergy')))
                n=n+1
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
                scale.append([])
                toten.append([])
    		points = graph.getiterator('point')
            self.pointseos = len(points)
    		for point in points:
    			scale[n].append(float(point.get('scale')))
    			toten[n].append(float(point.get('totalEnergy')))
                
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
        
        eosFit = fitev.Birch(structure, scale,volume,toten)
            
        a.append(eosFit.a)
        v.append(eosFit.v)
        ein.append(eosFit.ein)
        
        self.vol0_eos.append(eosFit.out0)
        self.b0_eos.append(eosFit.out1)
        self.db0_eos.append(eosFit.out2)
        self.emin_eos.append(eosFit.out3)
        self.p.append(eosFit.p)
        print self.vol0_eos
        #print a, v
    def fitcoa(self, coa, toten, volume):
        fitcoa = fitcovera.Polyfit(coa,toten,3,volume)
        self.coveramin.append(fitcoa.coamin)
        self.totencoamin.append(fitcoa.totenmin)
        print self.coveramin
    
    def write_covera(self):
        f = etree.parse(self.root + 'coa_data.xml')
        root = f.getroot()
        graphs = root.getiterator('graph')
        self.numb_coa = len(graphs)
        i=0
        for graph in graphs:
            graph.attrib['coamin'] = str(self.coveramin[i])
            graph.attrib['totenmin'] = str(self.totencoamin[i])
            i = i+1
        etree.ElementTree(root).write(self.root + 'coa_data.xml')
    
    def write_eos(self):
        f = etree.parse(self.root + 'eos_data.xml')
        root = f.getroot()
        graphs = root.getiterator('graph')
        i=0
        for graph in graphs:
            if i==self.n:
                graph.attrib['bulk_mod'] = str(self.b0_eos[i])
                graph.attrib['equi_volume'] = str(self.vol0_eos[i])
                graph.attrib['d_bulk_mod'] = str(self.db0_eos[i])
                graph.attrib['min_energy'] = str(self.emin_eos[i])
            i = i+1
        node = etree.SubElement(root,'eos')
        node.attrib['bulk_mod'] = str(self.b0_eos[0])
        node.attrib['equi_volume'] = str(self.vol0_eos[0])
        node.attrib['d_bulk_mod'] = str(self.db0_eos[0])
        node.attrib['min_energy'] = str(self.emin_eos[0])
        etree.ElementTree(root).write(self.root + 'eos_data.xml')
                
test = XmlToFit('/fshome/tde/cluster/calc6/')
#test.covera()
