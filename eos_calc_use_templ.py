"""Set up calculations and submit to loadleveler

    arguments:  -parameters ..... optional calculation parameters
                    type::dictionary
    returns:    none
    
    set calculation parameters here!
"""
try:
    import xml.etree.ElementTree as etree
except:
    import elementtree.ElementTree as etree
import subprocess
import os
import time

import search_dir
import check_for_existing
import collect_data

class CALC(object):
    def __init__(self, setup):
        ######################################################
        #      == Define calculation parameters here ==      #
        ######################################################

        ###########################################################
        ###########################################################
        #remove old status file:
        if os.path.exists('./finished'): 
            proc = subprocess.Popen(['rm ' + setup['calchome'] +'finished'], shell=True)
            proc.communicate()
        
        #if os.path.exists('./lljob_tree'):
        #    proc = subprocess.Popen(['rm ' + setup['calchome'] +'lljob_tree'], shell=True)
        #    proc.communicate()
                       
        inpar = {}
        convpar = {}
        
        scale = setup['param']['scale']
        for key in setup['param'].keys():
            if setup['structure'] in ['hcp','hex','wurtzite'] and key == 'scale' and setup['mod'] != 'simple_conv':
                continue
            inpar[key] = "<param name='%s'>"%key #new old inpar['key'] = ""
            if key not in ['scale','covera']:
                convpar[key] = setup['param'][key]

            for value in setup['param'][key]:
                
                if setup['structure'] in ['hcp','hex','wurtzite'] and key == 'covera' and setup['mod'] != 'simple_conv':
                    for alatt in scale[str(value)]:
                        inpar[key] = inpar[key] + "<val>%s" % value
                        inpar[key] = inpar[key] + "<dep name='scale' val='%s'/>" % str(alatt)
                        inpar[key] = inpar[key] + "</val>"
                else:
                    inpar[key] = inpar[key] + "<val>%s</val>" % value
            inpar[key] = inpar[key] + "</param>"
        for key in setup.keys():
            
            if key not in ['param','species','species2']:
                #inpar[key] = setup[key]
                continue
            elif key == 'species':
                inpar[key] = "<param name='species'><val>%s</val></param>" % setup[key]
            elif key == 'species2':
                inpar[key] = "<param name='species2'><val>%s</val></param>" % setup[key]
        ###########################################################
        #            == Set new parameters here! ==               #
        #              also modify input template                 #
        ###########################################################
        paramset = """<?xml version="1.0" encoding="UTF-8"?><setup path="%s">"""%setup['calchome']
        paramset = paramset + inpar['species']
        try:
            paramset = paramset + inpar['species2']
        except:
            print 'Elemental'
        for parkey in inpar.keys():
            if setup['structure'] in ['hcp','hex','wurtzite'] and setup['mod'] != 'simple_conv' and parkey == 'scale' or parkey == 'species' or parkey == 'species2':
                continue
            elif parkey in ['species','species2']:
                continue
            paramset = paramset + inpar[parkey]
        paramset = paramset + '</setup>'

        ############################################################
        ############################################################
        try:
            os.mkdir(setup['calchome'])
        except:
            print 'dir exists'
            
        os.chdir(setup['calchome'])
        
        f = open('./set.xml', 'w')
        f.write(paramset)
        f.close()
        # write constant calculation parameters to xml file:
        const_param = """
        <calc>
            <calchome path='%(calchome)s'/>
            <species spc='%(species)s'/>
            <structure str='%(structure)s'/>
            <speciespath spa = '%(speciespath)s'/>
            <elementshome elementsdir ='%(elementshome)stemplates/'/>
            <mode mod='%(mod)s'/>
            <autoconv_root root = ''/>
            <setupname sun = '%(setupname)s'/>
        </calc>
        """ %setup
        if not os.path.exists('./const_parameters.xml'):
            f1 = open('./const_parameters.xml', 'w')
            f1.write(const_param)
            f1.close()
        
        print setup['elementshome'] + 'templates/'
        
        convroot = etree.Element('convergence')

        for key in convpar.keys():
            convchild = etree.SubElement(convroot, 'n_param')
            if len(convpar[key]) > 1:
                convchild = etree.SubElement(convroot, 'n_param')
                convchild.set('name',str(key))
                convchild.set('val',str(convpar[key]))
        
        

        convroot.append(convchild)
        convtree = etree.ElementTree(convroot)
        convtree.write('./convergence.xml')
        if not os.path.exists(setup['calchome'] +  'parset.xml'):
            proc1 = subprocess.Popen(['xsltproc ' + setup['templatepath'] + 'permute_set.xsl ' + setup['calchome'] + 'set.xml > ' + setup['calchome'] +  'parset.xml'], shell=True)
            proc1.communicate()
            print "created parset.xml"
            curr_calc = 'parset.xml'
        else:
            #usr_or = raw_input('Calculations in same directory found.\nFor overwriting old calculations type: OVERWRITE. Otherwise new calculations will be appended to old ones.\n>>>')
            for i in range(1000):
                if os.path.exists(setup['calchome'] +  'parset_%s.xml'%str(i)):
                    continue
                else:    
                    proc1 = subprocess.Popen(['xsltproc ' + setup['templatepath'] + 'permute_set.xsl ' + setup['calchome'] + 'set.xml > ' + setup['calchome'] +  'parset_%s.xml'%str(i)], shell=True)
                    proc1.communicate()
                    newcalc = check_for_existing.Manipulate(setup['calchome'] +  'calc_filelist.xml', setup['calchome'] +  'parset_%s.xml'%str(i), setup['calchome'])
                    newcalc.append_calc()

                    curr_calc = 'parset_%s.xml'%str(i)
                    print 'New parameter file: ' + curr_calc
                    print 'appended new calculations to parset.xml'
                    break
        
        structure = setup['structure']
        if structure == 'hcp_fixedcoa': structure == 'hcp'
        
        proc2 = subprocess.Popen(['xsltproc ' + setup['templatepath'] + 'input_' + structure + '.xsl ' + setup['calchome'] + curr_calc], shell=True)
        proc2.communicate()
        print "created dir tree-structure and inputs"
        

            
        exec_template = setup['exectemplate']

        proc4 = subprocess.Popen(['xsltproc ' + setup['templatepath'] + exec_template + ' ' + setup['calchome'] + curr_calc], shell=True, stdout=subprocess.PIPE)
        exec_out = proc4.communicate()[0]
        if exec_template == 'shelcommand.xsl':
            print '\n#################################################'
            print '##### Preparing the following calculations: #####'
            print '#################################################\n'
            print exec_out
            execute = open(setup['calchome'] + 'execute','w')
            execute.write(exec_out)
            execute.close()
            proc5 = subprocess.Popen(['chmod u+x ' + setup['calchome'] + 'execute'], shell=True)
            proc5.communicate()
            proc6 = subprocess.Popen([setup['calchome'] + 'execute'], shell=True)
            proc6.communicate()
            
    

            if setup['isautoconv']:
                collect_data.XmlToFit(setup['calchome'])
    
        if setup['calculate'] == 'True':
            
            if exec_template == 'loadleveler.xsl':
                clusterpath = '/calc/tde/auto/Al_test/' #EDIT CALCULATION PATH ON CLUSTER!!! (TODO)
                print "created lljob script"
                finished = False
                proc6 = subprocess.Popen(["ssh g40cluster 'llsubmit %slljob_tree'"%clusterpath], shell=True)
                proc6.communicate()
                print "submitted lljob to cluster"
                
                while 1:
                    proc7 = subprocess.Popen(["ssh g40cluster 'llq -u tde'"], shell=True, stdout=subprocess.PIPE)
                    status = proc7.communicate()[0]
                    print status
                    if status.startswith('llq:'): break
                    time.sleep(10)
                print 'No more calculations in queue.'
                try:
                    os.rename(setup['calchome'] + 'lljob_tree',setup['calchome'] + 'lljob_tree_prev')
                    print 'Moving old lljob.'
                except:
                    print 'No lljob, creating new one.'
            if setup['isautoconv']:
                collect_data.XmlToFit(setup['calchome'])
            
            
            #check for calculation to be finished:
            #for i in range(100):
            #    if os.path.exists('finished'):
            #        print 'Calclation steps finished on cluster.'
            #        break
            #    time.sleep(60)
            
        elif setup['calculate'] == 'False':
            return
        else:
            print 'ERROR: calculation mode not defined (calculate = True/False)'
            
            
#test = CALC([])
