try:
    import xml.etree.ElementTree as etree
except:
    import elementtree.ElementTree as etree
import subprocess
import os

def calculate(dir):
    f = etree.parse(dir + 'const_parameters.xml')
    template = f.getroot().find('elementshome').get('elementsdir')
    structure = f.getroot().find('structure').get('str')
    species = f.getroot().find('species').get('spc')
    mode = f.getroot().find('mode').get('mod')
    calchome = f.getroot().find('calchome').get('path')
    setupname = f.getroot().find('setupname').get('sun')
        
    for i in range(1000):
        if os.path.exists(calchome +  'parset_%s.xml'%str(i)):
            n=i
            continue
        else:
            break
    try:
        curr_calc = 'parset_%s.xml'%str(n)
    except:
        curr_calc = 'parset_0.xml'
    
    
    proc2 = subprocess.Popen(['xsltproc ' + template + 'input_' + structure + '.xsl ' + calchome + curr_calc], shell=True)
    proc2.communicate()
    print "created dir tree-structure and inputs"
    

        
    exec_template = 'shelcommand.xsl'

    proc4 = subprocess.Popen(['xsltproc ' + template + exec_template + ' ' + calchome + curr_calc], shell=True, stdout=subprocess.PIPE)
    exec_out = proc4.communicate()[0]
    if exec_template == 'shelcommand.xsl':
        print '\n#################################################'
        print '##### Preparing the following calculations: #####'
        print '#################################################\n'
        print exec_out
        execute = open(calchome + 'execute','w')
        execute.write(exec_out)
        execute.close()
        proc5 = subprocess.Popen(['chmod u+x ' + calchome + 'execute'], shell=True)
        proc5.communicate()
        proc6 = subprocess.Popen([calchome + 'execute'], shell=True)
        proc6.communicate()