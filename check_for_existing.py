import xml.etree.ElementTree as etree

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
        
        diff = set(path_f) - set(path_p)
        for paths in diff:
            todel = root_p.find('/set/@path[paths]')
            print todel
            todel.remove()
test = Manipulate('/fshome/tde/cluster/Ti_convergence_ngridk/calc_filelist.xml', '/fshome/tde/cluster/Ti_convergence_ngridk/parset.xml')
test.append_calc()
        
        