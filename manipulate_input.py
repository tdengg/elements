import xml.etree.ElementTree as etree

def manipulate(dir,params):
    f = etree.parse(dir + 'input.xml')
    root = f.getroot()
    #tag = root.getiterator('graph')
    #self.numb_coa = len(graphs)
    
    i=0
    for param in params.keys():
        f.find('//@' + param).attrib[param] = params[param]
        
        #graph.attrib['coamin'] = str(self.coveramin[i])
        #graph.attrib['totenmin'] = str(self.totencoamin[i])
        i = i+1
    etree.ElementTree(root).write(dir + 'input.xml')
    
manipulate('/home/tom/git/exciting/examples/Al/',{'scale':7})