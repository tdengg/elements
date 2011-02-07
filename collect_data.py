"""analyse, plot and fit data 

    arguments:  -root ..... root directory of calculation tree structure
                    type::string
    returns:    none
    
"""
import xml.etree.ElementTree as etree
import subprocess
import os
from copy import deepcopy
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
import my_calcsetup
import auto_calc_setup
import analyze_conv

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
        self.coa_eos = []
        self.a_eos = []
        self.p = []
        self.results = []
        self.results_coa = []
        
        self.newcovera = []
        self.recalculate = []
        
        self.a0 = []
        self.recalculateeos = []
        
        self.par_out = []
        
        coamin = []
        tmin = []
        plt = []
        l1coa = []
        v1coa = []
        self.conv_params = []
        self.conv_params_names = []
        
        self.dir = str(os.getcwd()) + '/'
        tempf = open(self.dir + 'eosplot.xml','w')
        tempf.write('<plot></plot>')
        tempf.close()
        f = etree.parse(self.dir + 'const_parameters.xml')
        template = f.getroot().find('elementshome')
        self.structure = f.getroot().find('structure').get('str')
        self.species = f.getroot().find('species').get('spc')
        mode = f.getroot().find('mode').get('mod')
        self.calchome = f.getroot().find('calchome').get('path')
        setupname = f.getroot().find('setupname').get('sun')
        #search for calculations and create filelist
        search_dir.SearchDir(['info.xml'], self.dir, True).search()
        
        #create output
        if os.path.exists(self.dir + 'coa_data.xml'):
            remove = subprocess.Popen(['rm ' + self.dir + 'coa_data.xml'], shell=True)
            remove.communicate()
            
        proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fitcovera.xsl ' + self.dir + 'parset.xml > ' + self.dir +  'coa_data.xml'], shell=True)
        proc1.communicate()
            
        if os.path.exists(self.dir + 'eos_data.xml'):
            remove = subprocess.Popen(['rm ' + self.dir + 'eos_data.xml'], shell=True)
            remove.communicate()
            
        proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fiteos.xsl ' + self.dir + 'parset.xml > ' + self.dir +  'eos_data.xml'], shell=True)
        proc1.communicate()
            
        #Get number of convergence test parameters    
        fc = etree.parse(self.dir + 'convergence.xml')
        root = fc.getroot()
        params = fc.getiterator('n_param')
        nconv = 1
        for param in params:
            try:
                nconv = int(len(eval(param.attrib['val']))) * nconv
                self.conv_params.append(eval(param.attrib['val']))
                self.conv_params_names.append(param.attrib['name'])
            except:
                nconv = nconv
                self.convergence = False
          
        if self.structure in ['hcp', 'hex'] and mode == 'eos':
            
            conv = convert_latt_vol.Convert(self.structure)
            
            self.numb_coa = 0
            param1 = self.covera()
                
            ncoa = self.pointscovera
            nnconv = self.numb_coa/nconv
            k=0
            self.results = etree.Element('plot')
            self.results_coa = etree.Element('plot')
            while k<nconv:  
                print "\n#################################################################\n#Performing equation of state calculations for parameter set %s. #\n#################################################################\n"%str(k+1)       
                j=0
                
                while j<self.numb_coa/nconv:
                    
                    self.fitcoa(param1['covera'][k+j*nconv],param1['toten'][k+j*nconv],param1['volume'][k+j*nconv],k)
                    j=j+1
                    
                scalecoa, volumecovera  = conv.volumeToLatt(self.volumecoa[k], self.coveramin[k])
                
                self.fiteos(scalecoa,volumecovera,self.totencoamin[k], self.coveramin[k], self.structure, self.species)
                k=k+1
                print "\n#################################################################\n"
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
                if self.structure in ['hcp','hex']:
                    graph.attrib['equi_coa'] = str(self.coa_eos[k])
                graph.attrib['equi_a'] = str(self.a_eos[k])
                node.attrib['param'] = str()
                etree.ElementTree(root).write(self.dir + 'eos_data.xml')
                k=k+1
                    
        elif mode == 'simple_conv':
            param2 = self.birch()
            if mpl:
                plt.plot(param2['toten'], np.arange(len(param2['toten'])))
                plt.savefig(self.calchome + 'conv.png')
                #plt.show()
            else:
                print param2['toten']
                temp = open(self.calchome + 'temp','w')
                par = 0
                for energy in param2['toten']:
                    temp.writelines((str(par), ' ', str(energy[0]), '\n'))
                    par = par+1
                temp.close()
                #proc = subprocess.Popen(['xmgrace ' + self.calchome + 'temp'], shell=True)
                #proc.communicate()
        else:
            conv = convert_latt_vol.Convert(self.structure)
            param2 = self.birch()
            self.n=0
            self.results = etree.Element('plot')
            while self.n < len(param2['scale']):
                l, v = conv.lattToVolume(param2, param2['scale'][self.n])
                
                self.fiteos(l, v, param2['toten'][self.n],[1], self.structure,self.species)
                self.write_eos()
                self.n=self.n+1
        
        n=0
        for recalculate in self.recalculate:
            if recalculate:
                print 'Minimum c/a %s out of range: Recalculating '%(self.newcovera[n])
                newset = auto_calc_setup.Autosetup(setup, calcdir).setup(self.newcovera[n])
                auto_calc_setup.Autosetup(setup, calcdir).calculate(newset)
                n=n+1
            else:
                print 'Minimum c/a %s in accepted range.'(self.newcovera[n])
                n=n+1
        
        n=0
        for recalculate in self.recalculateeos:
            if recalculate:
                print 'Minimum volume %s out of range: Recalculating '%(self.vol0_eos[n])
                autoset = auto_calc_setup.Autosetup(setupname)
                newset = autoset.setup({'azero' : self.a0[n], 'calchome':self.calchome})
                autoset.calculate(newset)
                n=n+1
            else:
                print 'Minimum volume %s in accepted range.'%(self.vol0_eos[n])
                n=n+1
        
        analyze = analyze_conv(self.conv_params, self.conv_params_names)
        analyze.status
        if analyze.status:
            analyze.new_pars
            #if mpl:
            
            #    n=0
            #    for plots in self.p:
            #        plots.savefig(self.calchome + '%s_eos'%str(n))
            #        n=n+1
            #else:
            #    grace_plot.Plot([range(0,len(self.vol0_eos))],[self.vol0_eos,self.db0_eos,self.b0_eos,self.emin_eos], self.calchome).simple2D()
                
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
        
        curr_par = {}
        
        
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
                for name in self.conv_params_names:
                    curr_par[name] = point.get(name)
                 
                try:
                    covera[n].append(float(point.get('covera')))
                except:
                    covera[n].append(0)
            
            self.par_out.append(deepcopy(curr_par))
            n=n+1
        param['scale'] = scale
        param['toten'] = toten
        param['covera'] = covera
        
    	return param
        
    def fiteos(self, scale, volume, toten, coveramin, structure, species):
        a=[]
        v = []
        ein = []
        
        eosFit = fitev.Birch(self.structure, scale,coveramin,volume,toten,self.calchome)
        
        #write important parameters to eosplot.xml#
        eosFit.reschild.set('structure',str(self.structure))
        eosFit.reschild.set('species',str(self.species))
        
        for name in self.conv_params_names:
            eosFit.reschild.set(name,str(self.par_out[self.n][name]))
        eosFit.reschild.set('structure',str(self.structure))
        self.results.append(eosFit.reschild)
        self.results.append(eosFit.reschild2)
        self.results.append(eosFit.reschild3)
        restree = etree.ElementTree(self.results)
        restree.write(self.dir + 'eosplot.xml')
        #eosplot = etree.parse(self.dir + 'eosplot.xml')
        #root = eosplot.getroot()
        #graphs = root.getiterator('graph')
        #i=0

        #for graph in graphs:
        #    graph.attrib['structure'] = str(self.structure)
        #    graph.attrib['species'] = str(self.species)
            
        #    for name in self.curr_par:
        #        #graphs[-1].attrib[self.curr_par[name]] = str(self.conv_params[j][i])
        #        graph.attrib[name] = self.curr_par[name]

        
        #etree.ElementTree(root).write(self.dir + 'eosplot.xml')
        
        
        ###########################################    
        
        a.append(eosFit.a)
        v.append(eosFit.v)
        ein.append(eosFit.ein)
        
        self.vol0_eos.append(eosFit.out0)
        self.b0_eos.append(eosFit.out1)
        self.db0_eos.append(eosFit.out2)
        self.emin_eos.append(eosFit.out3)
        self.res_eos.append(eosFit.deltamin)
        self.recalculateeos.append(eosFit.recalculate)
        self.a0.append(eosFit.a0)
        if structure in ['hcp','hex']:
            self.coa_eos.append(eosFit.out4)
        self.a_eos.append(eosFit.out5)
        try:
            self.p.append(eosFit.p)
        except:
            return

    def fitcoa(self, coa, toten, volume, i):
        fitcoa = fitcovera.Polyfit(coa,toten,3,volume,self.calchome)
        
        self.coveramin.append([])
        self.totencoamin.append([])
        self.volumecoa.append([])
        
        self.results_coa.append(fitcoa.reschild)
        self.results_coa.append(fitcoa.reschild2)
        self.results_coa.append(fitcoa.reschild3)
        restree = etree.ElementTree(self.results_coa)
        restree.write(self.dir + 'coaplot.xml')
        coaplot = etree.parse(self.dir + 'coaplot.xml')
        root = coaplot.getroot()
        graphs = root.getiterator('graph')
        k=0
        number_all = 0
        for l in self.conv_params:
            number_all = number_all + len(l)
        for graph in graphs:
            if k == number_all:
                k=0
            graph.attrib['structure'] = str(self.structure)
            graph.attrib['species'] = str(self.species)
            for j in range(len(self.conv_params)):
                graph.attrib['param'] = str(self.conv_params[j][k])
                graph.attrib['parname'] = str(self.conv_params_names[j])
            k=k+1
        etree.ElementTree(root).write(self.dir + 'coaplot.xml')
        

        self.coveramin.append(fitcoa.coamin)
        self.totencoamin.append(fitcoa.totenmin)
        self.volumecoa.append(fitcoa.volume)
        self.recalculate.append(fitcoa.recalculate)
        self.newcovera.append(fitcoa.newcovera)

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
                if self.structure in ['hcp','hex']:
                    graph.attrib['equi_coa'] = str(self.coa_eos[i])
                graph.attrib['equi_a'] = str(self.a_eos[i])
            i = i+1
        #node = etree.SubElement(root,'eos')
        #node.attrib['bulk_mod'] = str(self.b0_eos[0])
        #node.attrib['equi_volume'] = str(self.vol0_eos[0])
        #node.attrib['d_bulk_mod'] = str(self.db0_eos[0])
        #node.attrib['min_energy'] = str(self.emin_eos[0])
        #node.attrib['norm_res_vect'] = str(self.res_eos[0])
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

if __name__=='__main__':                
    XmlToFit('')
