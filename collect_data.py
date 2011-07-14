"""Analyze, plot and fit data. 

    arguments:  -root ..... root directory of calculation tree structure
                    type::string
    returns:    none
    
"""
try:
    import xml.etree.ElementTree as etree
except:
    import elementtree.ElementTree as etree
import subprocess
import os
import re
import sys
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
import setCalc
#import manipulate_input
import calc_from_parset
#import read_eigval

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
        
        self.fit_OK = []
        
        coamin = []
        tmin = []
        plt = []
        l1coa = []
        v1coa = []
        self.conv_params = []
        self.conv_params_names = []
        if self.dir == '':
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
        
        #Remove aborted calculations to be recalculated:
        try:
            inp = sys.argv[1]
        except:
            inp = None
        if inp == 'continue':
            flist = etree.parse(self.dir + 'calc_filelist.xml')
            flroot = flist.getroot()
            dirs = flroot.getiterator('dir')
            for dir in dirs:
                if dir.get('info.xml') == 'NO info.xml':
                    removedir = subprocess.Popen(['rm -r ' + dir.get('path')], shell=True)
                    removedir.communicate()
                    recalculate = True
                else: recalculate = False
            if recalculate: calc_from_parset.calculate(self.dir)
        #search for calculations and create filelist
        search_dir.SearchDir(['info.xml'], self.dir, True).search()
        
        s = open(setupname)
        sustr= s.read()
        setup = eval(sustr)
        
        parlist = []
        stri = os.listdir(self.dir)
        for s in stri:
            if re.match('parset',s) != None and s.rstrip('.xml').lstrip('parset_') != '':
                parlist.append(int(s.rstrip('.xml').lstrip('parset_')))
        try:
            parnum = '_' + str(max(parlist))
        except:
            parnum = ''
            print ''
        

        #create output
        #if os.path.exists(self.dir + 'coa_data.xml'):
        #    remove = subprocess.Popen(['rm ' + self.dir + 'coa_data.xml'], shell=True)
        #    remove.communicate()
        if not os.path.exists(self.dir + 'coa_data.xml'):
            proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fitcovera.xsl ' + self.dir + 'parset.xml > ' + self.dir +  'coa_data.xml'], shell=True)
            proc1.communicate()
        else:    
            proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fitcovera.xsl ' + self.dir + 'parset%s.xml > '%str(parnum) + self.dir +  'coa_data_temp.xml'], shell=True)
            proc1.communicate()
            proc2 = subprocess.Popen(['cp ' + template.get('elementsdir') + 'merge.xsl ' + self.dir + 'merge.xsl'], shell=True)
            proc2.communicate()
            proc2 = subprocess.Popen(['xsltproc ' + self.dir + 'merge.xsl ' + self.dir + 'coa_data.xml > ' + self.dir +  'coa_data_temp2.xml'], shell=True)
            proc2.communicate()

            proc3 = subprocess.Popen(['cp ' + self.dir + 'coa_data_temp2.xml ' + self.dir +  'coa_data.xml'], shell=True)
            proc3.communicate()
        #if os.path.exists(self.dir + 'eos_data.xml'):
        #    remove = subprocess.Popen(['rm ' + self.dir + 'eos_data.xml'], shell=True)
        #    remove.communicate()
        if not os.path.exists(self.dir + 'eos_data.xml'):    
            proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fiteos.xsl ' + self.dir + 'parset.xml > ' + self.dir +  'eos_data.xml'], shell=True)
            proc1.communicate()
        else:
            proc1 = subprocess.Popen(['xsltproc ' + template.get('elementsdir') + 'dataconversion_fiteos.xsl ' + self.dir + 'parset%s.xml > '%str(parnum) + self.dir +  'eos_data_temp.xml'], shell=True)
            proc1.communicate()
            proc2 = subprocess.Popen(['cp ' + template.get('elementsdir') + 'merge.xsl ' + self.dir + 'merge.xsl'], shell=True)
            proc2.communicate()
            proc2 = subprocess.Popen(['xsltproc ' + self.dir + 'merge.xsl ' + self.dir + 'eos_data.xml > ' + self.dir +  'eos_data_temp2.xml'], shell=True)
            proc2.communicate()

            proc3 = subprocess.Popen(['cp ' + self.dir + 'eos_data_temp2.xml ' + self.dir +  'eos_data.xml'], shell=True)
            proc3.communicate()
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
          
        if self.structure in ['hcp', 'hex', 'wurtzite'] and mode == 'eos':
            
            conv = convert_latt_vol.Convert(self.structure)
            
            self.numb_coa = 0
            param1 = self.covera()
            param2 = self.birch()
            ncoa = self.pointscovera
            nnconv = self.numb_coa/nconv
            k=0
            self.results = etree.Element('plot')
            self.results_coa = etree.Element('plot')
            while k<len(param2['scale']):  
                print "\n#################################################################\n#Performing equation of state calculations for parameter set %s. #\n#################################################################\n"%str(k+1)       
                j=0
                self.coveramin.append([])
                self.totencoamin.append([])
                self.volumecoa.append([])

                while j<self.pointscovera:
                    self.fitcoa(param1['covera'][k*self.pointscovera+j],param1['toten'][k*self.pointscovera+j],param1['volume'][k*self.pointscovera+j],k)
                    j=j+1
                    
                scalecoa, volumecovera  = conv.volumeToLatt(self.volumecoa[k], self.coveramin[k])
                
                self.fiteos(scalecoa,volumecovera,self.totencoamin[k], self.coveramin[k], self.structure, self.species)
                print self.b0_eos
                k=k+1
                print "\n#################################################################\n"
            k=0
            f = etree.parse(self.dir + 'eos_data.xml')
            root = f.getroot()
            graphs = root.getiterator('graph')
            for graph in graphs:
                if self.fit_OK[k]:
                    #node = etree.SubElement(graph,'eos')
                    graph.attrib['bulk_mod'] = str(self.b0_eos[k])
                    graph.attrib['equi_volume'] = str(self.vol0_eos[k])
                    graph.attrib['d_bulk_mod'] = str(self.db0_eos[k])
                    graph.attrib['min_energy'] = str(self.emin_eos[k])
                    if self.structure in ['hcp','hex']:
                        graph.attrib['equi_coa'] = str(self.coa_eos[k])
                    graph.attrib['equi_a'] = str(self.a_eos[k])
                    graph.attrib['param'] = str()
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
                if self.structure == 'hcp_fixedcoa':
                    self.fiteos(l, v, param2['toten'][self.n],setup['param']['covera']['coverazero'],'hcp' ,self.species)
                else:
                    self.fiteos(l, v, param2['toten'][self.n],[1], self.structure,self.species)
                #self.write_eos()
                self.n=self.n+1
            self.write_eos()
        
        n=0
        if len(self.recalculate) >= 3:
            for recalculate in self.recalculate[len(self.recalculate)-3:-1]:
                if recalculate:
                    print 'Minimum c/a %s out of range: Recalculating '%(self.newcovera[n])
                    newset = auto_calc_setup.Autosetup(setup, calcdir).setup(self.newcovera[n])
                    auto_calc_setup.Autosetup(setup, calcdir).calculate(newset)
                    n=n+1
                else:
                    print 'Minimum c/a %s in accepted range.'%(self.newcovera[n])
                    n=n+1
        
        n=0
        if len(self.recalculateeos) >= 3:
            for recalculate in self.recalculateeos[len(self.recalculateeos)-3:-1]:
                if recalculate and self.recalculateeos[n-1] and self.recalculateeos[n-2]:
                    print 'Minimum volume %s out of range: Recalculating '%(self.vol0_eos[n])
                    autoset = auto_calc_setup.Autosetup(setupname)
                    
                    newset = autoset.setup({'azero' : self.a0[n], 'calchome':self.calchome})
                    print newset
                    autoset.calculate(newset)
                    n=n+1
                else:
                    print 'Minimum volume %s in accepted range.'%(self.vol0_eos[n])
                    n=n+1

        if __name__=='__main__' and inp != 'continue':
            return
        ##auto convergence:
        self.f = etree.parse(self.dir + 'auto_conv.xml')
        self.root = self.f.getroot()
        graphs = self.f.getiterator('conv')
        i=0
        j=0
        
        for graph in graphs:
            
            if self.fit_OK[j]:
                graph.set('energy',str(self.emin_eos[i]))
                graph.set('B',str(self.b0_eos[i]))
                graph.set('V',str(self.vol0_eos[i]))
                graph.set('err',str(self.res_eos[i]))
                i=i+1
            j=j+1
            lastpar = (graph.get('par'))
            lastvar = eval(graph.get('parval'))

            
        self.f.write(self.dir + 'auto_conv.xml')
        
        s = open(self.dir + 'autoconv.py')
        sustr= s.read()
        autosetup = eval(sustr)
        
        
            
        allelements = self.f.getiterator(tag='CONVERGED')
        elem = ''
        for element in allelements:
            elem = element
        if elem == '':
            lastpar = autosetup['order']['1']
        
        if autosetup['convmode'] == 'swidth+ngridk':
            converged,converged_all = analyze_conv.ANALYZE(self.dir, lastpar).converged
            
            print lastvar, lastpar
    
            if lastpar == 'swidth' and not converged and float(lastvar[lastpar][-1]) >= float(autosetup['end'][lastpar])-float(autosetup['end'][lastpar])*0.01:
                setCalc.setCalc(lastpar,lastvar,autosetup,setupname,self.f,self.root,self.dir).zeroD()
            elif lastpar == 'ngridk' and not converged:
                lastvar['par'] = 'ngridk'
                setCalc.setCalc('ngridk',lastvar,autosetup,setupname,self.f,self.root,self.dir).zeroD()
            elif not converged and float(lastvar[lastpar][-1]) < float(autosetup['end'][lastpar]):
                setCalc.setCalc(lastpar,lastvar,autosetup,setupname,self.f,self.root,self.dir).zeroD()
            else:
                etree.SubElement(self.root, 'CONVERGED',attrib={'par':lastpar,'val':str(lastvar)})
                self.f.write(self.dir + 'auto_conv.xml')
                
                if type(lastvar[lastpar]) == list: lastvar[lastpar] = [lastvar[lastpar][-1]]
                
                for index in autosetup['order'].keys():
                    if autosetup['order'][index] == lastpar and lastpar != 'ngridk':
                        newind = str(int(index) + 1)
                        
                        break
                    elif autosetup['order'][index] == lastpar and lastpar == 'ngridk':
                        newind = str(int(index) - 1)
                        break
                    elif converged_all and lastpar == 'ngridk':
                        try:
                            os.mkdir(self.dir + 'converged')
                        except:
                            print "Could not create directory 'converged'. Maybe already existing!"
                        val = eval(self.f.find("CONVERGED").get('val'))
                        print val
                        lastvar['ngridk'] = lastvar['ngridk'][-1]
                        lastvar['swidth'] = lastvar['swidth'][-1]
                        lastvar['rgkmax'] = val['rgkmax'][-1]
                        lastpar = 'rgkmax'
                        autoset = auto_calc_setup.Autosetup(setupname)
                        newset = autoset.setup({lastpar:[lastvar[lastpar]]})
                        autoset.calculate(newset)
                        
                        etree.SubElement(self.root, 'DONE')
                        self.f.write(self.dir + 'auto_conv.xml')
                        
                        return
                lastpar = autosetup['order'][newind]
                #lastvar[lastpar] = [autosetup['start'][str(lastpar)]]
                if lastpar == 'swidth':
                    #initial values of parameters for swidht convergence:
                    try: 
                        allelements[0]
                        print allelements
                        initsw = lastvar[lastpar]
                        steps = 3
                        initrgkmax = 6
                        initngridk = lastvar['ngridk'][-1]
                    except:
                        initsw = lastvar[lastpar]
                        steps = 3
                        initrgkmax = 6
                        initngridk = autosetup['start']['ngridk']
                    ###############
                    setCalc.setCalc('swidth',{'swidth':initsw,'rgkmax':[initrgkmax],'ngridk':[initngridk]},autosetup,setupname,self.f,self.root,self.dir).oneD(steps)
                elif lastpar == 'ngridk':
                    setCalc.setCalc(lastpar,lastvar,autosetup,setupname,self.f,self.root,self.dir).oneD(3)
                else:
                    setCalc.setCalc(lastpar,lastvar,autosetup,setupname,self.f,self.root,self.dir).zeroD()
                    
        elif autosetup['convmode'] == 'const_ngridk/swidth':
            print 'Convergence mode: ngridk/swidth = const.'
            
            read_eigval()
            
            if lastpar == 'rgkmax' and not converged and float(lastvar[lastpar][-1]) < float(autosetup['end'][lastpar]):
                setCalc.setCalc(lastpar,lastvar,autosetup,setupname,self.f,self.root,self.dir).zeroD()
                
                
    def setCalc(self,lastpar,lastvar,autosetup,setupname):
        
        def zeroD(self):
            su = open(setupname)
            sustr= su.read()
            setup = eval(sustr)
            new = {}
            newvar = []
            
            i=1
            if type(autosetup['order'][str(i)]) == str:
                n=1
                newvar = float(lastvar[lastpar][-1]) + float(autosetup['stepsize'][lastpar])
                new[lastpar]= str([newvar])
                for par in autosetup['order'].keys():
                    new[autosetup['order'][par]] = setup['param'][autosetup['order'][par]]
                    
                new['par'] = lastpar
            else:
                n=len(autosetup['order'][str(i)])
                while i<=n:
                    newvar = float(lastvar) + float(autosetup['stepsize'][lastpar[i]])
                    new['ngridk'] = setup['param']['ngridk']
                    new['swidth'] = setup['param']['swidth']
                    new[lastpar[i]]= str([newvar])
                    i+=1
    
            etree.SubElement(self.root, 'conv',{'par':str(lastpar), 'parval':str(new)})
            self.f.write(self.dir + 'auto_conv.xml')
            autoset = auto_calc_setup.Autosetup(setupname)
            newset = autoset.setup({lastpar:[float(newvar)]})
            autoset.calculate(newset)
            return
            
        def oneD(self,steps):
            su = open(setupname)
            sustr= su.read()
            setup = eval(sustr)
            new = {}
            newvar = []
            
            i=1
            if type(autosetup['order'][str(i)]) == str:
                n=1
                newvar = []
                init = float(lastvar[lastpar][-1])
                for j in range(steps):
                    newvar.append(init)
                    init = init + float(autosetup['stepsize'][lastpar])
                new[lastpar]= str(newvar)
                for par in lastvar.keys():
                    if par != lastpar:
                        new[par] = lastvar[par]
                    
                new['par'] = lastpar
            else:
                n=len(autosetup['order'][str(i)])
                while i<=n:
                    newvar = float(lastvar) + float(autosetup['stepsize'][lastpar[i]])
                    new['ngridk'] = setup['param']['ngridk']
                    new['swidth'] = setup['param']['swidth']
                    new[lastpar[i]]= str([newvar])
                    i+=1
    
            etree.SubElement(self.root, 'conv',{'par':str(lastpar), 'parval':str(new)})
            self.f.write(self.dir + 'auto_conv.xml')
            autoset = auto_calc_setup.Autosetup(setupname)
            newset = autoset.setup(new)
            autoset.calculate(newset)
            return
        def twoD():
            return
            
        
        
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
        try:
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
            self.a0.append(eosFit.a0[0])
            if structure in ['hcp','hex']:
                self.coa_eos.append(eosFit.out4)
            self.a_eos.append(eosFit.out5[0])
            self.fit_OK.append(True)
        except:
            self.fit_OK.append(False)
            print 'Failed to fit using Birch Murnaghan EOS!'
        try:
            self.p.append(eosFit.p)
        except:
            return

    def fitcoa(self, coa, toten, volume, i):
        fitcoa = fitcovera.Polyfit(coa,toten,3,volume,self.calchome)
        
        #self.coveramin.append([])
        #self.totencoamin.append([])
        #self.volumecoa.append([])
        self.results_coa.append(fitcoa.reschild)
        self.results_coa.append(fitcoa.reschild2)
        self.results_coa.append(fitcoa.reschild3)
        restree = etree.ElementTree(self.results_coa)
        restree.write(self.dir + 'coaplot.xml')
        #coaplot = etree.parse(self.dir + 'coaplot.xml')
        #root = coaplot.getroot()
        #graphs = root.getiterator('graph')
        #k=0
        #number_all = 0
        #for l in self.conv_params:
        #    number_all = number_all + len(l)
        #for graph in graphs:
        #    if k == number_all:
        #        k=0
        #    graph.attrib['structure'] = str(self.structure)
        #    graph.attrib['species'] = str(self.species)
        #    for j in range(len(self.conv_params)):
        #        graph.attrib['param'] = str(self.conv_params[j][k])
        #        graph.attrib['parname'] = str(self.conv_params_names[j])
        #    k=k+1
        #etree.ElementTree(root).write(self.dir + 'coaplot.xml')
        

        self.coveramin[i].append(fitcoa.coamin)
        self.totencoamin[i].append(fitcoa.totenmin)
        self.volumecoa[i].append(fitcoa.volume)
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
        j=0
        for graph in graphs:
            if self.fit_OK[j]:
                graph.attrib['bulk_mod'] = str(self.b0_eos[i])
                graph.attrib['equi_volume'] = str(self.vol0_eos[i])
                graph.attrib['d_bulk_mod'] = str(self.db0_eos[i])
                graph.attrib['min_energy'] = str(self.emin_eos[i])                                
                graph.attrib['norm_res_vect'] = str(self.res_eos[i])
                if self.structure in ['hcp','hex']:
                    graph.attrib['equi_coa'] = str(self.coa_eos[i])
                graph.attrib['equi_a'] = str(self.a_eos[i])
                graph.attrib['status'] = 'OK'
                i = i+1
            else:
                graph.attrib['status'] = 'failed'
            j=j+1
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
