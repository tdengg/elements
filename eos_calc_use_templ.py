"""Set up calculations and submit to loadleveler

    arguments:  -parameters ..... optional calculation parameters
                    type::dictionary
    returns:    none
    
    set calculation parameters here!
"""

import subprocess
import os
import time

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
            if param['structure'][0] == 'hcp':
                #create c/a steps
                i=10    
                while i > -1:
                    covera.append(coverazero - (i-5)*dcovera)
                    i = i-1
            else:
                covera = [1.0]
            
            param['scale'] = scale
            param['rgkmax'] = [8]
            param['ngridk'] = [8]
            param['swidth'] = [0.01]
            param['species'] = ['Be']
            param['covera'] = covera
            param['root'] = ["/home/tde/test/calc6/"]
            param['speciespath'] = ["/appl/EXCITING/versions/hydrogen/species/"]
            param['templatepath'] = ["/home/tde/elements/version_new/templates/"]
            param['mod'] = ['parallel']
        ###########################################################
        ###########################################################
            
                
        inpar = {}
        convpar = {}
        for key in param.keys():
            inpar[key] = ""
            for value in param[key]:
                if key not in ['root','structure', 'speciespath','templatepath','mod']:           #other parameters
                    inpar[key] = inpar[key] + "<val>%s</val>" % value
                else:
                    inpar[key] = value
        ###########################################################
        #            == Set new parameters here! ==               #
        ###########################################################
        paramset = """<?xml version="1.0" encoding="UTF-8"?>
        
        <setup path="%(root)s">
          <param name="species">
            %(species)s
          </param>
          <param name="covera">
            %(covera)s
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
        </setup>
        """ %inpar
        ############################################################
        ############################################################
        try:
            os.mkdir(param['root'][0])
        except:
            print 'dir exists'
            
        os.chdir(param['root'][0])
        
        f = open('./set.xml', 'w')
        f.write(paramset)
        f.close()
        
        
        # write constant calculation parameters to xml file:
        const_param = """
        <calc>
            <rootdir dir='%(root)s'/>
            <structure str='%(structure)s'/>
            <speciespath spa = '%(speciespath)s'/>
            <elementshome elementsdir ='%(templatepath)s'/>
            <mode mod='%(mod)s'/>
        </calc>
        """ %inpar
        
        f1 = open('./const_parameters.xml', 'w')
        f1.write(const_param)
        f1.close()
        
        
        proc1 = subprocess.Popen(['xsltproc ' + param['templatepath'][0] + 'permute_set.xsl ' + param['root'][0] + 'set.xml > ' + param['root'][0] +  'parset.xml'], shell=True)
        proc1.communicate()
        print "created paramset.xml"
        
        proc2 = subprocess.Popen(['xsltproc ' + param['templatepath'][0] + 'input_' + param['structure'][0] + '.xsl ' + param['root'][0] + 'parset.xml'], shell=True)
        proc2.communicate()
        print "created dir tree-structure and inputs"
        
        if inpar['mod'] == 'parallel':
            proc3 = subprocess.Popen(['xsltproc ' + param['templatepath'][0] + 'loadleveler.xsl ' + param['root'][0] + 'parset.xml'], shell=True)
            proc3.communicate()
            print "created lljob script"
            
            proc4 = subprocess.Popen(['llsubmit lljob_tree'], shell=True)
            proc4.communicate()
            print "submitted lljob to cluster"
            
        elif inpar['mod'] == 'serial':
            return
        else:
            print 'ERROR: calculation mode not defined (mod = serial/parallel)'
            
#test = CALC([])
