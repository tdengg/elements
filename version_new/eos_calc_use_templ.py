import subprocess
import os
import time

#import search_dir as search

class CALC(object):
    def __init__(self, parameters):
        #param = parameters
        
        rootdir = "/home/tde/test/calc5/"
        execpath = "/home/tde/elements/templates/"
        usr = "tde"
        if len(parameters) == 0: 
            param = {}
        scale = []
        covera = []
        
        azero = 4.319 #for W #7.653 for Al
        etamax = 0.05
        coverazero = 1.6
        dcovera = 1.6/50
        param['structure'] = ['hcp']
	
        #create lattice parameters
        i=10
        while i > -1:
            scale.append(azero - (i-5)*etamax)
            i = i-1
        if param['structure'][0] == 'hcp':
            i=10    
            while i > -1:
                covera.append(coverazero - (i-5)*etamax)
                i = i-1
        else:
            covera = [1.0]
        
        param['scale'] = scale
        param['rgkmax'] = [8]
        param['ngridk'] = [8]
        param['swidth'] = [0.01]
        param['species'] = ['Be']
        param['covera'] = covera
        param['root'] = ["/home/tde/test/calc5/"]
        param['speciespath'] = ["/appl/EXCITING/versions/hydrogen/species/"]
        param['executable'] = ["/home/tde/elements/templates/"]
        param['mod'] = ['parallel']
        
        
        inpar = {}
        
        for key in param.keys():
            inpar[key] = ""
            for value in param[key]:
                if key not in ['root','structure', 'speciespath','executable','mod']:           #constant parameters
                    inpar[key] = inpar[key] + "<val>%s</val>" % value
                else:
                    inpar[key] = value
        
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
        
        try:
            os.mkdir(rootdir)
        except:
            print 'dir exists'
            
        os.chdir(rootdir)
        
        f = open('./set.xml', 'w')
        f.write(paramset)
        f.close()
        
        
        # write constant calculation parameters to xml file:
        const_param = """
        <calc>
            <rootdir dir='%(root)s'/>
            <structure str='%(structure)s'/>
            <speciespath spa = '%(speciespath)s'/>
            <executable exe ='%(executable)s'/>
            <mode mod='%(mod)s'/>
        </calc>
        """ %inpar
        
        f1 = open('./const_parameters.xml', 'w')
        f1.write(const_param)
        f1.close()
        
        
        proc1 = subprocess.Popen(['xsltproc ' + execpath + 'permute_set.xsl ' + rootdir + 'set.xml > ' + rootdir +  'parset.xml'], shell=True)
        proc1.communicate()
        print "created paramset.xml"
        
        proc2 = subprocess.Popen(['xsltproc ' + execpath + 'input_' + param['structure'][0] + '.xsl ' + rootdir + 'parset.xml'], shell=True)
        proc2.communicate()
        print "created dir tree-structure and inputs"
        
        if inpar['mod'] == 'parallel':
            proc3 = subprocess.Popen(['xsltproc ' + execpath + 'loadleveler.xsl ' + rootdir + 'parset.xml'], shell=True)
            proc3.communicate()
            print "created lljob script"
            
            proc4 = subprocess.Popen(['llsubmit lljob_tree'], shell=True)
            proc4.communicate()
            print "submitted lljob to cluster"
            
            j=0
            while j<100:
                proc5 = subprocess.Popen(['llq -u %s'%usr], shell=True, stdout=subprocess.PIPE)
                out = proc5.communicate()
                print out
                if len(out) == 0:
                    print "calculations finished on cluster"
                    break   
                time.sleep(120)
                j=j+1

            #search.SearchDir(['info.xml' ,'input.xml'], root)
            #ctxtinfo, infos = search.search()
        elif inpar['mod'] == 'serial':
            return
        else:
            print 'ERROR: calculation mode not defined (mod = serial/parallel)'
            
test = CALC([])
