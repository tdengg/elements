"""Create and execute calculations
    contains:   class::CreateCalc()
                    def::calc            
                    def::create_input
                    def::_mkdir
                    def::calcxml
                    def::readToten
                    def::writeOutput
                    def::lattToVolume
                    def::writeEnergyToXml

    arguments:  -**kwargs ........ parameters of calculation (eg. ngridk, swidth, scale ...)
                    type::dictionary
                -calcnr ....... calculation number
                    type::string
                -structure .... structure of unit cell
                    type::string
                -calctype ...... define if to perform serial or parallel calculations 
                    type::string
                    
    returns:    -----
    
    output:     
"""

import libxml2
import os
from xml.dom.minidom import Document
import subprocess
import time

import create_lljob
import check_calc
import submit_to_cluster

class CreateCalc(object):
    """Create calculations
    
        arguments:  -root directory(type::string)
                    -structure(type::string)
                    -parameters(type::list)
    """
    def __init__(self, structure, calcnr, calctype = 'serial', calculate = True, **kwargs):
        self.dirx = []
        self.values = []
        self.toten = []
        self.paramlist = []
        self.calcnr = calcnr
        self.calctype = calctype
        self.kwargs = kwargs
        self.initpath = kwargs['rootdir'][0]
        self.structure = structure
        self.excitingpath = str(kwargs['path'])
        self.calculate = calculate
    
    def calc(self):
        inputpar = {'scale':3,'covera':1,'xctype':'LSDAPerdew-Wang','stype':'Gaussian', 'path':'/home/tom/git/exciting/', 'rgkmax':8}
        
        i=0
        for key in self.kwargs:
            inputpar[key] = self.kwargs[key][0]
        #print inputpar
        #print kwargs
        for key in self.kwargs:
            for par in self.kwargs[key]:
                inputpar[key] = par
                #self.createInput(inputpar)
                
                for key2 in self.kwargs:
                    for par2 in self.kwargs[key2]:
                        inputpar[key2] = par2
                        self.calcpath = self.calcnr + '/' + str(inputpar['element']) + '/' + str(inputpar['covera']) + '/' + str(inputpar['rgkmax']) + '/' + str(inputpar['swidth']) + '/' + str(inputpar['ngridk']) + '/' + str(inputpar['scale']) + '/'
                        inputpar['eospath'] = inputpar['rootdir'] + self.calcnr + '/' + str(inputpar['element']) + '/' + str(inputpar['covera']) + '/' + str(inputpar['rgkmax']) + '/' + str(inputpar['swidth']) + '/' + str(inputpar['ngridk']) + '/'
                        inputpar['calcpath'] = self.calcpath
                        if inputpar.values() in self.values:
                            continue
                        self.paramlist.append(dict(zip(list(inputpar),inputpar.values())))
                        self.values.append(inputpar.values())
                        self.createInput(inputpar, i)
                        if self.calctype == 'serial':
                            self.toten.append(self.readToten(inputpar))
                            self.calcxml(inputpar, i, self.toten[i])
                            outfile = self.writeOutput(inputpar, self.toten[i])
                        elif self.calctype == 'parallel':
                            self.calcxml(inputpar, i, [])
                        i=i+1

        
        if self.calctype == 'parallel':
            #submit job
            submit_to_cluster.submit(self.kwargs['path_cluster'][0])
            # read total energy and check calculation status
            j=0
            while j<100:
                if j == 0:
                    remaining = check_calc.check(paramlist)
                else:
                    remaining = check_calc.check(remaining)
                if len(remaining) == 0:
                    print 'Status: calculations finished'
                    break
                time.sleep(120)
                j=j+1
        
        
        return self.paramlist
    
    def calcDependentParam(self, dependent_param = []):
        """Set up calculation with dependent Parameters
        """
        inputpar = {'xctype':'LSDAPerdew-Wang','stype':'Gaussian'}
    
        i=0
        for key in self.kwargs:
            inputpar[key] = self.kwargs[key][0]
        
        #print inputpar
        #print self.kwargs
        for key in self.kwargs:
            for par in self.kwargs[key]:
                inputpar[key] = par
                    
                for key2 in self.kwargs:
                    j=0
                    for par2 in self.kwargs[key2]:
                        if key2 in dependent_param:
                            for dep in dependent_param:
                                #print inputpar[dep]
                                inputpar[dep] = self.kwargs[dep][j]
                        else:
                            inputpar[key2] = par2
                        self.calcpath = self.calcnr + '/' + str(inputpar['element']) + '/' + str(inputpar['covera']) + '/' + str(inputpar['rgkmax']) + '/' + str(inputpar['swidth']) + '/' + str(inputpar['ngridk']) + '/' + str(inputpar['scale']) + '/'
                        inputpar['eospath'] = inputpar['rootdir'] + self.calcnr + '/' + str(inputpar['element']) + '/' + str(inputpar['covera']) + '/' + str(inputpar['rgkmax']) + '/' + str(inputpar['swidth']) + '/' + str(inputpar['ngridk']) + '/'
                        inputpar['calcpath'] = self.calcpath
                        if inputpar.values() in self.values:
                            continue
                        
                        self.paramlist.append(dict(zip(list(inputpar),inputpar.values())))
                        self.values.append(inputpar.values())
                        self.createInput(inputpar, i)
                        if self.calctype == 'serial' and self.calculate==True:
                            self.toten.append(self.readToten(inputpar))
                            self.calcxml(inputpar, i, self.toten[i])
                            outfile = self.writeOutput(inputpar, self.toten[i])
                        elif self.calctype == 'parallel':
                            self.calcxml(inputpar, i, [])
                        j=j+1
                        i=i+1
        
        return self.paramlist
        
    def createInput(self, param, i):
        #print param
        #print self.initpath
        #calcpath = self.calcnr + '/' + str(param['covera']) + '/' + str(param['rgkmax']) + '/' + str(param['swidth']) + '/' + str(param['ngridk']) + '/' + str(param['scale']) + '/'
        
        #if self.calctype == 'serial':
        self._mkdir(param['rootdir'] + self.calcpath)
        os.chdir(param['rootdir'] + self.calcpath)
        #elif self.calctype == 'parallel':
        #    self._mkdir(param['rootdir_cluster'] + calcpath)
        #    os.chdir(param['rootdir_cluster'] + calcpath)
        
        if self.structure == 'hcp':
            
            param['ngridkz'] = int(round(param['ngridk']/param['covera'],0))
            #print param['ngridkz']
            inputxml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href="inputtohtml.xsl" type="text/xsl"?>

<input xsi:noNamespaceSchemaLocation="../../xml/excitinginput.xsd"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsltpath="../../xml/">
  <title></title>
  <structure speciespath="%(path)sspecies">
    <crystal scale="%(scale)s">
      <basevect>0.5 -0.866025404 0.0     </basevect>
      <basevect>0.5  0.866025404 0.0     </basevect>
      <basevect>0.0  0.0         %(covera)s </basevect>
    </crystal>
    <species speciesfile="%(element)s.xml">
      <atom coord="0.33333334 0.66666667 0.25" />
      <atom coord="0.66666667 0.33333334 0.75" />
    </species>
  </structure>
  <groundstate ngridk="%(ngridk)s %(ngridk)s %(ngridkz)s" 
               rgkmax="%(rgkmax)s"
               vkloff="0.0 0.0 0.0"
           xctype="%(xctype)s"
           stype="%(stype)s"
           swidth="%(swidth)s"></groundstate>
  <properties>
  </properties>
</input>""" %param

        if self.structure == 'fcc':
            inputxml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href="inputtohtml.xsl" type="text/xsl"?>

<input xsi:noNamespaceSchemaLocation="../../xml/excitinginput.xsd"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsltpath="../../xml/">
  <title></title>
  <structure speciespath="%(path)sspecies">
    <crystal scale="%(scale)s">
      <basevect>0.5 0.5 0.0</basevect>
      <basevect>0.5 0.0 0.5</basevect>
      <basevect>0.0 0.5 0.5</basevect>
    </crystal>
    <species speciesfile="%(element)s.xml">
      <atom coord="0.00 0.00 0.00" />
    </species>
  </structure>
  <groundstate ngridk="%(ngridk)s %(ngridk)s %(ngridk)s" 
               rgkmax="%(rgkmax)s"
               vkloff="0.0 0.0 0.0"
           xctype="%(xctype)s"
           stype="%(stype)s"
           swidth="%(swidth)s"></groundstate>
  <properties>
  </properties>
</input>"""%param

        if self.structure == 'bcc':
            inputxml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href="inputtohtml.xsl" type="text/xsl"?>

<input xsi:noNamespaceSchemaLocation="../../xml/excitinginput.xsd"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsltpath="../../xml/">
  <title></title>
  <structure speciespath="%(path)sspecies">
    <crystal scale="%(scale)s">
      <basevect> -0.5  0.5  0.5</basevect>
      <basevect>  0.5 -0.5  0.5</basevect>
      <basevect>  0.5  0.5 -0.5</basevect>
    </crystal>
    <species speciesfile="%(element)s.xml">
      <atom coord="0.00 0.00 0.00" />
    </species>
  </structure>
  <groundstate ngridk="%(ngridk)s %(ngridk)s %(ngridk)s" 
               rgkmax="%(rgkmax)s"
               vkloff="0.0 0.0 0.0"
           xctype="%(xctype)s"
           stype="%(stype)s"
           swidth="%(swidth)s"></groundstate>
  <properties>
  </properties>
</input>"""%param
        
        if self.structure == 'diamond':
            inputxml = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href="inputtohtml.xsl" type="text/xsl"?>

<input xsi:noNamespaceSchemaLocation="../../xml/excitinginput.xsd"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsltpath="../../xml/">
  <title></title>
  <structure speciespath="%(path)sspecies">
    <crystal scale="%(scale)s">
      <basevect> -0.5  0.5  0.5</basevect>
      <basevect>  0.5 -0.5  0.5</basevect>
      <basevect>  0.5  0.5 -0.5</basevect>
    </crystal>
    <species speciesfile="%(element)s.xml">
      <atom coord="0.00 0.00 0.00" />
    </species>
  </structure>
  <groundstate ngridk="%(ngridk)s %(ngridk)s %(ngridk)s" 
               rgkmax="%(rgkmax)s"
               vkloff="0.0 0.0 0.0"
           xctype="%(xctype)s"
           stype="%(stype)s"
           swidth="%(swidth)s"></groundstate>
  <properties>
  </properties>
</input>"""%param
        
        
        
        f = open('./input.xml', 'w')
        f.write(inputxml)
        f.close()
        protocoll = open(param['rootdir'] + self.calcnr + '/' + 'protocoll', 'a')
        
        # start calculation (serial)
        if self.calctype == 'serial' and self.calculate == True:
            print '--------------------------------------------------------'
            print("""Element is %(element)s
Lattice constant a   =  %(scale)s  [Bohr]
c/a =                   %(covera)s
rgkmax =                %(rgkmax)s
k-points grid is        %(ngridk)s %(ngridk)s %(ngridk)s
XC from                 %(xctype)s
Broadening width =      %(swidth)s [Hartree] 
Broadening type is      %(stype)s""")%param

            print '--------------------------------------------------------'
            process = subprocess.Popen(param['path'] + 'bin/excitingser', shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
            
            output, dump = process.communicate()
            protocoll.write(str(output))
            protocoll.close()
            
        elif self.calctype == 'parallel' and self.calculate == True:
            job = create_lljob.Create(param, param['rootdir'], self.calcnr, self.calcpath, self.excitingpath, i)
            job.lljob()
    
    def _mkdir(self, newdir):
        """make new directory and parent directories
        """
        if os.path.isdir(newdir):
            pass
        elif os.path.isfile(newdir):
            raise OSError("a file with the same name as the desired " \
                          "dir, '%s', already exists." % newdir)
        else:
            head, tail = os.path.split(newdir)
            if head and not os.path.isdir(head):
                self._mkdir(head)
            #print "_mkdir %s" % repr(newdir)
            if tail:
                os.mkdir(newdir)
                
    def calcxml(self, param, i, toten):  
        latt, vol = self.lattToVolume(param)
        
        if i == 0:                                                   #only first calculation             
            self.doc = Document()                                                                
            self.rootx = (self.doc.createElement("calculation "))                                          
            self.doc.appendChild(self.rootx)
        self.dirx.append(self.doc.createElement("calc"))
        for par in param:               
            self.dirx[i].setAttribute(str(par), str(param[par]))
        self.dirx[i].setAttribute("dir", os.getcwd())            
        self.rootx.appendChild(self.dirx[i])
        self.energy = self.doc.createElement("eos")
        if self.calctype == 'serial':
            self.energy.setAttribute("toten", str(toten))
        self.energy.setAttribute("latt", str(latt))
        self.energy.setAttribute("volume", str(vol))
        self.dirx[i].appendChild(self.energy)
        xmlfile = open(self.initpath + self.calcnr + '/' + 'calc_filelist.xml', 'w+')
        xmlfile.write(self.doc.toprettyxml(indent="  "))  
        xmlfile.close()    
        
    def readToten(self, inputpar):
        os.chdir(self.initpath + self.calcnr + '/'  + str(inputpar['element']) + '/' + str(inputpar['covera']) + '/' + str(inputpar['rgkmax']) + '/' + str(inputpar['swidth']) + '/' + str(inputpar['ngridk']) + '/' + str(inputpar['scale']) + '/')
        infile = open('./TOTENERGY.OUT', 'r')
        
        totenlines = infile.readlines()
        for lines in totenlines:
            toten = lines
            
        return toten
    
    def writeOutput(self, inputpar, toten):
        os.chdir(self.initpath + self.calcnr)
        latt, vol = self.lattToVolume(inputpar)
        out = str(latt) + '    ' + str(vol) + '    ' + str(toten)
        outfile = open('./energy_volume_out', 'a+')
        outfile.writelines(out)
        outfile.close()
        
    def lattToVolume(self,inputpar):
        latt = inputpar['scale']
        if self.structure == 'hcp':
            covera = inputpar['covera']
            vol = latt**3. * covera * 3.**(1./2.)/2.
        if self.structure == 'fcc':
            vol = latt**3./4.
        if self.structure == 'bcc':
            vol = latt**3./2.
        if self.structure == 'diamond':
            vol = latt**3./8.
        
        return latt, vol
    
    def writeEnergyToXml(self):
        for param in self.paramlist:
            
            xmlfile = open(self.initpath + self.calcnr + '/' + 'calc_filelist.xml', 'w+')
            #xmlfile.write(self.doc.toprettyxml(indent="  "))  
            xmlfile.close()
                                                             

#test            
#a = CreateCalc('/home/tom/test/', '/home/tom/git/exciting/', 'fcc', 'calc1',  'serial', ngridk = [2], swidth = [0.1], scale = [7.653], element = ['Al'])