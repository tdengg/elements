""" Compare two .xml files and write the difference (for attribute 'path' in filelist.xml and parset.xml) to a new one
"""

import xml.etree.ElementTree as etree
import os

class Manipulate(object):
    def __init__(self,filelist_old, params_old):
        self.fl_old = filelist_old
        self.pm_old = params_old
    def append_calc(self):
        f = etree.parse(self.fl_old)
        p = etree.parse(self.pm_old)
        
        root_f = f.getroot()
        paths_f = root_f.getiterator('dir')
        
        path_p = []
        path_f = []
        root_p = p.getroot()
        rootdir = root_p.get('path')
        paths_p = root_p.getiterator('set')
        for paths in paths_p:
            path_p.append(rootdir + paths.get('path'))
        for paths in paths_f:
            path_f.append(paths.get('path'))
        
        diff = set(path_p) - set(path_f)

        for paths in diff:
            for pathp in paths_p:
                #print rootdir + pathp.get('path'), paths
                if (rootdir + pathp.get('path')) != paths:
                    root_p.remove(pathp)
        if diff != set([]):
            for i in range(100):
                if os.path.exists(rootdir + 'parset_%s.xml'%str(i)):
                    continue
                else:
                    fname = 'parset_%s.xml'%str(i)
                    break
            p.write(rootdir + fname)
            print 'written new parameterfile to parset_%s.xml'%str(i)
            
        combined = etree.parse(rootdir + 'parset.xml')
        root_combined = combined.getroot()
        root_p = p.getroot()
        iter = root_p.getiterator('set')
        for element in iter:
            root_combined.append(element)
        combined.write(rootdir + 'parset.xml')
        

##usage:
#test = Manipulate('/fshome/tde/cluster/Ti_convergence_ngridk/calc_filelist.xml', '/fshome/tde/cluster/Ti_convergence_ngridk/parset.xml')
#test.append_calc()
        
        