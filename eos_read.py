import libxml2
from libxml2 import xmlAttr, xmlNode
import os

class Out(object):
    def __init__(self, calcnr, initpath, ngkgrid, swidth):
        self.param = {}
        self.param['ngridk'] = ngkgrid
        self.param['swidth'] = swidth
        self.initpath = initpath
        self.calcnr = calcnr
        
    def read(self):
        eos = []
        latt = []
        toten = []
        vol = []
        dirlist = []
        os.chdir(self.initpath + '/' + self.calcnr + '/')
        docinfo = libxml2.parseFile('./calc_filelist.xml')   #reading xml-file
        ctxtinfo = docinfo.xpathNewContext()
        i=0
        buffer = [0,0,0]
        for xpath in ctxtinfo.xpathEval("//calc[@ngridk = '%(ngridk)s' and @swidth='%(swidth)s']/eos/@toten | //calc[@ngridk = '%(ngridk)s' and @swidth ='%(swidth)s']/eos/@latt | //calc[@ngridk = '%(ngridk)s' and @swidth ='%(swidth)s']/eos/@volume"%self.param):
            out = xmlNode.getContent(xpath)
            if i==0:
                latt.append(float(out))
            elif i==1:
                toten.append(float(out))
            elif i==2:
                vol.append(float(out))
            buffer[i] = float(out)
            if i == 2:
                eos.append(buffer)
                i=-1
            i=i+1
        #print latt
        return latt, vol, toten
    
    #def readdict(self, paramlist):
#out = Out('calc1', '/home/tom/test/',2,0.03)
#out.read()