'''search_dir.py - Search sub directories for files recursively.'''   

import os
import glob
from xml.dom.minidom import Document
import xml.etree.ElementTree as ET

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
        dirx = []                                                                       #1
        doc = Document()                                                                #1
        rootx = (doc.createElement("dirlist"))                                          #1
        doc.appendChild(rootx)                                                          #1
        currDir = os.listdir(os.curdir)
        ctxtinfo  = []
        
        print '______________________________________________\nSearching calculation directory for info files.' 
        
        def recsearch(self, currDir):
            for dir in currDir:
                if os.path.isdir(dir):
                    os.chdir(os.getcwd() + '/' + dir)
                    subDir = os.listdir(os.curdir)
                    
                    if os.path.exists('info.xml'):
                        infostatus = 'OK'
                    else:
                        infostatus = 'NO info.xml'
                    
                    i=0
                    while i < len(self.files):
                        if os.path.exists(self.files[i]) and os.path.exists("info.xml") and os.path.exists("input.xml"):
                            docinfo = ET.parse(self.files[i])   #reading xml-file
                            ctxtinfo.append(docinfo)
                            if self.files[i] == 'info.xml':
                                status = docinfo.find('/groundstate').get('status')
                            #print(os.stat("info.xml"))
                        #    print(self.files[i] + " exists")
                        elif os.path.exists(self.files[i]) and not os.path.exists("info.xml"):
                            print("no info file " + os.getcwd())
                        elif os.path.exists(self.files[i]) and not os.path.exists("input.xml"):
                            print("no input file " + os.getcwd())
                        i=i+1
                    
                        try:
                            error = glob.glob('*.err')[0]
                        except:
                            error = None
                    
                    if os.path.exists("input.xml") and self.xmlout == True:      #1                        
                        dirx.append(doc.createElement("dir%i" %(self.n)))               #1
                        dirx[self.n].setAttribute("id", "calc %i" %(self.n))            #1
                        dirx[self.n].setAttribute("path", "%s" %(os.getcwd() + '/'))    #1
                        dirx[self.n].setAttribute("info.xml", str(infostatus))
                        if os.path.exists("info.xml"):
                            dirx[self.n].setAttribute("status", str(status))                     #1
                        if error:
                            dirx[self.n].setAttribute("error", str(error)) 
                        rootx.appendChild(dirx[self.n])                                 #1                        
                        self.n=self.n+1                                                 #1
                    recsearch(self, subDir)    
                    
            os.chdir(os.pardir)
            return  ctxtinfo
        recsearch(self, currDir)
        if self.xmlout == True:
            #print(doc.toprettyxml(indent="  "))
            xmlfile = open(self.root + 'calc_filelist.xml', 'w+')
            xmlfile.write(doc.toprettyxml(indent="  "))  
            xmlfile.close()
            print 'Filelist written to calc_filelist.xml\n______________________________________________'#1
        return  ctxtinfo          

##test        
#search = SearchDir(["info.xml"],"/fshome/tde/cluster/Be_convergence/", True)    # usage: SearchDir([file1,file2,...])    
#search.search()


