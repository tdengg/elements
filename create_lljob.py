import libxml2
import os

class Create(object):
    def __init__(self, param, initpath, calcnr, calcpath, excitingdir, i):
        
        self.initpath = initpath
        self.calcnr = calcnr
        self.param = param
        self.excitingdir = excitingdir
        self.initpathCluster = param['rootdir_cluster']
        #print param['rootdir_cluster']
        self.fullcalcpath = param['rootdir_cluster'] + calcpath
        self.i = i
        #os.chdir(self.initpath + '/' + self.calcnr + '/')
        #docinfo = libxml2.parseFile('./calc_filelist.xml')   #reading xml-file
        #ctxtinfo = docinfo.xpathNewContext()

        #for xpath in ctxtinfo.xpathEval("//@dir"):
            #out = xmlNode.getContent(xpath)

    def lljob(self):
        os.chdir(self.initpath + '/' + self.calcnr + '/')
        if self.i == 0:
            lljob0 = """# @ job_type = parallel
# @ job_name  = JOBNAME
# @ class = lesstday
# @ node           = 1
# @ tasks_per_node = 1
# @ executable = %(path_cluster)s
 
### begin job steps ############################################################
"""%self.param


        lljob = """# @ initialdir = """+ self.fullcalcpath +"""
# @ step_name  = """+ self.fullcalcpath +"""
# @ output = $(job_name).out
# @ error = $(job_name).err
# @ resources = ConsumableCpus(1)
# @ queue

"""%self.param
        
        if self.i == 0:
            lljob = lljob0 + lljob
            
        f = open('./lljob', 'a+')
        f.write(lljob)
        f.close()