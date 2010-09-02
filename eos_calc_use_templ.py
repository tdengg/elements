"""Set up calculations and submit to loadleveler

    arguments:  -parameters ..... optional calculation parameters
                    type::dictionary
    returns:    none
    
    set calculation parameters here!
"""
import xml.etree.ElementTree as etree
import subprocess
import os
import time

import search_dir
import check_for_existing

class CALC(object):
    def __init__(self, param):
        ######################################################
        #      == Define calculation parameters here ==      #
        ######################################################

        if len(param) == 0: 
                param = {}
        if param == {}:
            usr = "tde"
            scale = []
            covera = []
            
            azero = 4.319       #lattice parameter
            etamax = 0.05       #steps in lattice parameter
            coverazero = 1.6    #c/a ratio
            dcovera = 1.6/50    #steps in c/a
            param['structure'] = ['hcp']
    	
            #create lattice parameter steps
            i=10
            while i > -1:
                scale.append(azero - (i-5)*etamax)
                i = i-1
            if param['structure'][0] == 'hcp' and param['mod'] != 'siple_conv':
                #create c/a steps
                i=10    
                while i > -1:
                    covera.append(coverazero - (i-5)*dcovera)
                    i = i-1
            elif param['structure'][0] == 'hcp' and param['mod'] == 'siple_conv':
                covera = [coverazero]
            else:
                covera = [0]
            
            param['scale'] = scale
            param['rgkmax'] = [8,10]
            param['ngridk'] = [8,10]
            param['swidth'] = [0.01]
            param['species'] = ['Be']
            param['covera'] = covera
            param['calchome'] = ["/fshome/tde/cluster/test/"]
            param['speciespath'] = ["/appl/EXCITING/versions/hydrogen/species/"]
            param['templatepath'] = ["/fshome/tde/git/my_calc/gen/elements/templates/"]
            param['mod'] = ['parallel']
        ###########################################################
        ###########################################################
                   
        inpar = {}
        convpar = {}
        scale = param['scale']
        for key in param.keys():
            if param['structure'][0] == 'hcp' and key == 'scale' and param['mod'][0] != 'simple_conv':
                continue
            inpar[key] = ""
            if key not in ['scale','covera'] and len(param[key])>1:
                convpar[key] = len(param[key])
            else:
                convpar[key] = 1
            for value in param[key]:
                if key not in ['calchome','structure', 'speciespath','templatepath','mod','calculate']:           #other parameters
                    if param['structure'][0] == 'hcp' and key == 'covera' and param['mod'][0] != 'simple_conv':
                        for alatt in scale[str(value)]:
                            inpar[key] = inpar[key] + "<val>%s" % value
                            inpar[key] = inpar[key] + "<dep name='scale' val='%s'/>" % str(alatt)
                            inpar[key] = inpar[key] + "</val>"
                    else:
                        inpar[key] = inpar[key] + "<val>%s</val>" % value
            
                else:
                    inpar[key] = value
        ###########################################################
        #            == Set new parameters here! ==               #
        #              also modify input template                 #
        ###########################################################
        if param['structure'][0] == 'hcp' and param['mod'][0] != 'simple_conv':
            paramset = """<?xml version="1.0" encoding="UTF-8"?>
            
            <setup path="%(calchome)s">
              <param name="species">
                %(species)s
              </param>
              <param name="rgkmax">
                %(rgkmax)s
              </param>
              <param name="swidth">
                %(swidth)s
              </param>
              <param name="ngridk">
                %(ngridk)s
              </param>
              <param name="lmaxvr">
                <val>14</val>
              </param>
              <param name="covera">
                %(covera)s
              </param>
            </setup>
            """ %inpar
        else:
            paramset = """<?xml version="1.0" encoding="UTF-8"?>
            
            <setup path="%(calchome)s">
              <param name="species">
                %(species)s
              </param>
              <param name="rgkmax">
                %(rgkmax)s
              </param>
              <param name="swidth">
                %(swidth)s
              </param>
              <param name="ngridk">
                %(ngridk)s
              </param>
              <param name="lmaxvr">
                <val>14</val>
              </param>
              <param name="scale">
                %(scale)s
              </param>
              <param name="covera">
                %(covera)s
              </param>
            </setup>
            """ %inpar
        ############################################################
        ############################################################
        try:
            os.mkdir(param['calchome'][0])
        except:
            print 'dir exists'
            
        os.chdir(param['calchome'][0])
        
        f = open('./set.xml', 'w')
        f.write(paramset)
        f.close()
        
        
        # write constant calculation parameters to xml file:
        const_param = """
        <calc>
            <calchome path='%(calchome)s'/>
            <structure str='%(structure)s'/>
            <speciespath spa = '%(speciespath)s'/>
            <elementshome elementsdir ='%(templatepath)s'/>
            <mode mod='%(mod)s'/>
        </calc>
        """ %inpar
        
        f1 = open('./const_parameters.xml', 'w')
        f1.write(const_param)
        f1.close()
        
        convroot = etree.Element('convergence')
        i=0
        for key in convpar.keys():
            if i == 0:
                convchild = etree.SubElement(convroot, 'n_param')
                convchild.set(key,str(convpar[key]))
            else:
                convchild = etree.Element('n_param')
                convchild.set(key,str(convpar[key]))
            i=i+1
        convroot.append(convchild)
        convtree = etree.ElementTree(convroot)
        convtree.write('./convergence.xml')
        if not os.path.exists(param['calchome'][0] +  'parset.xml'):
            proc1 = subprocess.Popen(['xsltproc ' + param['templatepath'][0] + 'permute_set.xsl ' + param['calchome'][0] + 'set.xml > ' + param['calchome'][0] +  'parset.xml'], shell=True)
            proc1.communicate()
            print "created parset.xml"
        else:
            proc1 = subprocess.Popen(['xsltproc ' + param['templatepath'][0] + 'permute_set.xsl ' + param['calchome'][0] + 'set.xml > ' + param['calchome'][0] +  'parset_new.xml'], shell=True)
            proc1.communicate()
            newcalc = check_for_existing.Manipulate(param['calchome'][0] +  'calc_filelist.xml', param['calchome'][0] +  'parset_new.xml')
            newcalc.append_calc()
            print 'appended new calculations to parset.xml'
        
        proc2 = subprocess.Popen(['xsltproc ' + param['templatepath'][0] + 'input_' + param['structure'][0] + '.xsl ' + param['calchome'][0] + 'parset.xml'], shell=True)
        proc2.communicate()
        print "created dir tree-structure and inputs"
        
        if param['calculate'][0] == 'True':
            proc3 = subprocess.Popen(['xsltproc ' + param['templatepath'][0] + 'loadleveler.xsl ' + param['calchome'][0] + 'parset.xml'], shell=True)
            proc3.communicate()
            print "created lljob script"
            
            proc4 = subprocess.Popen(['llsubmit lljob_tree'], shell=True)
            proc4.communicate()
            print "submitted lljob to cluster"
            
            proc5 = subprocess.Popen(['cp '+ param['templatepath'][0] - 'templates/' + 'my_calcsetup.py ' + param['calchome'][0]], shell=True)
            proc5.communicate()
            
        elif param['calculate'][0] == 'False':
            return
        else:
            print 'ERROR: calculation mode not defined (mod = serial/parallel)'
            
#test = CALC([])
