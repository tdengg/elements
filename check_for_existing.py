""" Compare two .xml files and write the difference (for attribute 'path' in filelist.xml and parset.xml) to a new one
"""

import xml.etree.ElementTree as etree
import os

import search_dir

class Manipulate(object):
    def __init__(self,filelist_old, params_old, rootdir):
        self.fl_old = filelist_old
        self.pm_old = params_old
        self.rootdir = rootdir
    def append_calc(self):
        search_dir.SearchDir(['info.xml'], self.rootdir, True).search()
        f = etree.parse(self.fl_old)
        p = etree.parse(self.pm_old)
        
        root_f = f.getroot()
        paths_f = root_f.getiterator('dir')
        
        path_p = []
        path_f = []
        root_p = p.getroot()
        paths_p = root_p.getiterator('set')
        
        for paths in paths_p:
            path_p.append(self.rootdir + paths.get('path'))
        for paths in paths_f:
            path_f.append(paths.get('path'))
        
        diff = set(path_p) - set(path_f)


        for pathp in paths_p:
            if (self.rootdir + pathp.get('path')) not in diff:
                try:
                    root_p.remove(pathp)
                except:
                    continue

        fname = self.pm_old
        p.write(fname)
        root_p = p.getroot()
        new = root_p.getiterator('set')
        combined = etree.parse(self.rootdir + 'parset.xml')
        pi = etree.ProcessingInstruction('xml', "version='1.0' encoding='UTF-8'") 
           
        root_combined = combined.getroot()
        root_combined.append(pi)
        for element in new:
            root_combined.append(element)
        combined.write(self.rootdir + 'parset.xml')
            
                
        print 'written new parameterfile to ' + self.pm_old


##usage:
#test = Manipulate('/fshome/tde/cluster/Ti_convergence_ngridk/calc_filelist.xml', '/fshome/tde/cluster/Ti_convergence_ngridk/parset.xml')
#test.append_calc()
        
        