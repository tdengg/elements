'''search_dir.py - Search sub directories for files recursively.'''   

import os
import libxml2
from xml.dom.minidom import Document

class SearchDir(object):
    def __init__(self, files, root, xmlout=False):
        self.files = files
        self.root = root
        os.chdir(self.root)
        self.xmlout = xmlout
    def search(self):
        ''' 
        Attributes: 
        -----------
        files : array_like
            files to be searched for
        root : string
            root directory of calculations
        
        Returns:
        --------
        ctxtinfo : array_like
            parsed xml files
                                                         
        note: lines maked with #1 are only for generating
              xml output                                     
        '''
        self.n=0
        infos = {}
        dirx = []                                                                       #1
        doc = Document()                                                                #1
        rootx = (doc.createElement("dirlist"))                                          #1
        doc.appendChild(rootx)                                                          #1
        currDir = os.listdir(os.curdir)
        ctxtinfo  = []
        
        infos['info'] = [False]
        infos['subdirs'] = [None]
        infos['dirname'] = [os.path.basename(os.getcwd())]
        infos['path'] = [self.root]
        infos['depth'] = [0]
        infos['pardir'] = [None]
        
        self.depth = 0
        
        def recsearch(self, currDir):
            for dir in currDir:
                if os.path.isdir(dir):
                    os.chdir(os.getcwd() + '/' + dir)
                    self.depth = self.depth + 1
                    subDir = os.listdir(os.curdir)
                    i=0
                    while i < len(self.files):
                        if os.path.exists(self.files[i]) and os.path.exists("info.xml") and os.path.exists("input.xml"):
                            docinfo = libxml2.parseFile(self.files[i])   #reading xml-file
                            ctxtinfo.append(docinfo.xpathNewContext())
                            #print(os.stat("info.xml"))
                        #    print(self.files[i] + " exists")
                        elif os.path.exists(self.files[i]) and not os.path.exists("info.xml"):
                            print("no info file " + os.getcwd())
                        elif os.path.exists(self.files[i]) and not os.path.exists("input.xml"):
                            print("no input file " + os.getcwd())
                        i=i+1
                    if os.getcwd() not in infos['path']:
                        infos['path'].append(os.getcwd())
                        if os.path.exists("info.xml"): infos['info'].append(True)
                        else: infos['info'].append(False)
                        infos['dirname'].append(os.path.basename(os.getcwd()))
                        infos['depth'].append(self.depth)
                        infos['pardir'].append(os.path.split(os.path.split(os.getcwd())[0])[1])
                        suDir = os.listdir(os.pardir)
                        inf = []
                        for dirs in suDir:
                            if os.path.isdir(os.path.dirname(os.getcwd()) + '/'  + dirs): inf.append(dirs)
                        infos['subdirs'].append(inf)
                    if os.path.exists("info.xml") and os.path.exists("input.xml") and self.xmlout == True:      #1                        
                        dirx.append(doc.createElement("dir%i" %(self.n)))               #1
                        dirx[self.n].setAttribute("id", "main %i" %(self.n))            #1
                        dirx[self.n].setAttribute("depth", "%i" %self.depth)            #1
                        dirx[self.n].setAttribute("path", "%s" %(os.getcwd() + '/'))    #1
                        rootx.appendChild(dirx[self.n])                                 #1                        
                        self.n=self.n+1                                                 #1
                    recsearch(self, subDir) 
                       
            self.depth = self.depth - 1        
            os.chdir(os.pardir)
            return  ctxtinfo
        recsearch(self, currDir)
        if self.xmlout == True:
            #print(doc.toprettyxml(indent="  "))
            xmlfile = open(self.root + 'calc_filelisttest.xml', 'w+')
            xmlfile.write(doc.toprettyxml(indent="  "))  
            xmlfile.close()  
        #print infos                                                           #1
        return  ctxtinfo, infos         

##test        
#search = SearchDir(["input.xml"],"/home/tom/test/calc1/", True)    # usage: SearchDir([file1,file2,...])    
#search.search()


