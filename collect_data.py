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
    import grace_plot
import convert_latt_vol
import fitev
import fitcovera
import search_dir

class XmlToFit(object):
    def __init__(self, dir):
        self.dir = dir
        self.coveramin = []
        self.totencoamin = []
        self.volumecoa = []
        
        self.vol0_eos = [] 
        self.b0_eos = []
        self.db0_eos = []
        self.emin_eos = []
        self.res_eos = []
        self.p = []
        
        coamin = []
        tmin = []
        plt = []
        l1coa = []
        v1coa = []
        conv_params = []
        self.dir = str(os.getcwd()) + '/'

        f = etree.parse(self.dir + 'const_parameters.xml')
        template = f.getroot().find('elementshome')
        structure = f.getroot().find('structure').get('str')
        mode = f.getroot().find('mode').get('mod')
        self.calchome = f.getroot().find('calchome').get('path')
        #search for calculations and create filelist
        search_dir.SearchDir(['info.xml'], self.dir, True).search()
        
        #create output
        if os.path.exists(self.dir + 'coa_data.xml'):
            remove = subprocess.Popen(['rm ' + self.dir + 'coa_data.xml'], shell=True)
            
        proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fitcovera.xsl ' + self.dir + 'parset.xml > ' + self.dir +  'coa_data.xml'], shell=True)
        proc1.communicate()
            
        if os.path.exists(self.dir + 'eos_data.xml'):
            remove = subprocess.Popen(['rm ' + self.dir + 'eos_data.xml'], shell=True)
            
        proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fiteos.xsl ' + self.dir + 'parset.xml > ' + self.dir +  'eos_data.xml'], shell=True)
        proc1.communicate()
            
        #Get number of convergence test parameters    
        fc = etree.parse(self.dir + 'convergence.xml')
        root = fc.getroot()
        params = fc.getiterator('n_param')
        nconv = 1
        for param in params:
            nconv = int(param.attrib.values()[0]) * nconv
            conv_params.append(param.keys()[0])
            
        if structure in ['hcp', 'hex'] and mode == 'eos':
            
            conv = convert_latt_vol.Convert(structure)
            
            self.numb_coa = 0
            param1 = self.covera()
                
            ncoa = self.pointscovera
            nnconv = self.numb_coa/nconv

            k=0
            while k<nconv:         
                j=0
                while j<self.numb_coa/nconv:
                    self.fitcoa(param1['covera'][nnconv*k+j],param1['toten'][nnconv*k+j],param1['volume'][nnconv*k+j])
                    j=j+1
                    
                scalecoa, volumecovera  = conv.volumeToLatt(self.volumecoa, self.coveramin)
                self.fiteos(scalecoa,volumecovera,self.totencoamin,structure)
                k=k+1
                
            k=0
            f = etree.parse(self.dir + 'eos_data.xml')
            root = f.getroot()
            graphs = root.getiterator('graph')
            for graph in graphs:
                node = etree.SubElement(graph,'eos')
                node.attrib['bulk_mod'] = str(self.b0_eos[k])
                node.attrib['equi_volume'] = str(self.vol0_eos[k])
                node.attrib['d_bulk_mod'] = str(self.db0_eos[k])
                node.attrib['min_energy'] = str(self.emin_eos[k])
                etree.ElementTree(root).write(self.dir + 'eos_data.xml')
                k=k+1
                    
        elif mode == 'simple_conv':
            param2 = self.birch()
            if mpl:
                plt.plot(param2['toten'], np.arange(len(param2['toten'])))
                plt.show()
            else:
                print param2['toten']
                temp = open(self.calchome + 'temp','w')
                par = 0
                for energy in param2['toten']:
                    temp.writelines((str(par), ' ', str(energy[0]), '\n'))
                    par = par+1
                temp.close()
                proc = subprocess.Popen(['xmgrace ' + self.calchome + 'temp'], shell=True)
                proc.communicate()
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
                n=0
                for plots in self.p:
                    plots.savefig(self.calchome + '%s_eos'%str(n))
                    n=n+1
            else:
                grace_plot.Plot([range(0,len(self.vol0_eos))],[self.vol0_eos,self.db0_eos,self.b0_eos,self.emin_eos], self.calchome).simple2D()
                
    def covera(self):
        param = {}
        scale = []
        toten = []
        covera = []
        volume = []
        keys = []
        
        f = etree.parse(self.dir + 'coa_data.xml')
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
                v = (float(point.get('scale'))**3. * float(point.get('covera')) * 3.**(1./2.)/2.)
            volume.append(v)
            n=n+1
        param['scale'] = scale
        param['toten'] = toten
        param['covera'] = covera
        param['volume'] = volume
        return param
        
    def birch(self):
        param = {}
        scale = []
        toten = []
        covera = []
        f = etree.parse(self.dir + 'eos_data.xml')
        root = f.getroot()
    	graphs = f.getiterator('graph')
        self.numb = len(graphs)
        n=0
    	for graph in graphs:
            scale.append([])
            toten.append([])
            covera.append([])
            points = graph.getiterator('point')
            self.pointseos = len(points)
            for point in points:
                scale[n].append(float(point.get('scale')))
                toten[n].append(float(point.get('totalEnergy')))
                try:
                    covera[n].append(float(point.get('covera')))
                except:
                    covera[n].append(0)
            n=n+1
        param['scale'] = scale
        param['toten'] = toten
        param['covera'] = covera
    	return param
        
    def fiteos(self, scale, volume, toten, structure):
        a=[]
        v = []
        ein = []
        
        eosFit = fitev.Birch(structure, scale,volume,toten,self.calchome)
            
        a.append(eosFit.a)
        v.append(eosFit.v)
        ein.append(eosFit.ein)
        
        self.vol0_eos.append(eosFit.out0)
        self.b0_eos.append(eosFit.out1)
        self.db0_eos.append(eosFit.out2)
        self.emin_eos.append(eosFit.out3)
        self.res_eos.append(eosFit.deltamin)
        try:
            self.p.append(eosFit.p)
        except:
            return

    def fitcoa(self, coa, toten, volume):
        fitcoa = fitcovera.Polyfit(coa,toten,3,volume)
        self.coveramin.append(fitcoa.coamin)
        self.totencoamin.append(fitcoa.totenmin)
        self.volumecoa.append(fitcoa.volume)
    
    def write_covera(self):
        f = etree.parse(self.dir + 'coa_data.xml')
        root = f.getroot()
        graphs = root.getiterator('graph')
        self.numb_coa = len(graphs)
        i=0
        for graph in graphs:
            graph.attrib['coamin'] = str(self.coveramin[i])
            graph.attrib['totenmin'] = str(self.totencoamin[i])
            i = i+1
        etree.ElementTree(root).write(self.dir + 'coa_data.xml')
    
    def write_eos(self):
        f = etree.parse(self.dir + 'eos_data.xml')
        root = f.getroot()
        graphs = root.getiterator('graph')
        i=0
        for graph in graphs:
            if i==self.n:
                graph.attrib['bulk_mod'] = str(self.b0_eos[i])
                graph.attrib['equi_volume'] = str(self.vol0_eos[i])
                graph.attrib['d_bulk_mod'] = str(self.db0_eos[i])
                graph.attrib['min_energy'] = str(self.emin_eos[i])                                
                graph.attrib['norm_res_vect'] = str(self.res_eos[i])
            i = i+1
        node = etree.SubElement(root,'eos')
        node.attrib['bulk_mod'] = str(self.b0_eos[0])
        node.attrib['equi_volume'] = str(self.vol0_eos[0])
        node.attrib['d_bulk_mod'] = str(self.db0_eos[0])
        node.attrib['min_energy'] = str(self.emin_eos[0])
        node.attrib['norm_res_vect'] = str(self.res_eos[0])
        etree.ElementTree(root).write(self.dir + 'eos_data.xml')
        
    def write_result(self):
        results = etree.Element('results')
        reschild = etree.SubElement(results, 'n_param')
        reschild.set(key,str(convpar[key]))
        reschild = etree.Element('n_param')
        reschild.set(key,str(convpar[key]))
        results.append(reschild)
        restree = etree.ElementTree(results)
        restree.write('./results.xml')
        
    def clean(self, clean_mode):
        #delete all .OUT files
        remove = subprocess.Popen(["find . -type f -name '*.OUT' -exec rm -f {} \;"],shell=True)
        remove.communicate()
                
test = XmlToFit('')
