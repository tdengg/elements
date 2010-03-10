import libxml2

class CreateJobs(object):
    def init(self):
        
        os.chdir(self.initpath + '/' + self.calcnr + '/')
        docinfo = libxml2.parseFile('./calc_filelist.xml')   #reading xml-file
        ctxtinfo = docinfo.xpathNewContext()

        for xpath in ctxtinfo.xpathEval("//@dir"):
            out = xmlNode.getContent(xpath)

lljob = """# @ job_type = parallel
# @ job_name  = JOBNAME
# @ class = lesstday
# @ node           = 1
# @ tasks_per_node = 1
# @ executable = %(execPathCluster)s
 
### begin job steps ############################################################
"""%execPathCluster


lljobAppend = """# @ initialdir = %(initPathCluster)s%(calcPath)
# @ step_name  = _id89490201_id89490231_id89490251_id89491891
# @ output = $(job_name).out
# @ error = $(job_name).err
# @ resources = ConsumableCpus(1)
# @ queue
"""