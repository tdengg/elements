import os
def fermi(eigval):
    deltae = []
    for kpoint in eigval:
        i = 0
        for state in kpoint:
            if state[1]<0.001:
                deltae.append(kpoint[i][0] - kpoint[i-1][0])
            i+=1
    return min(deltae)

def fermidkpt(eigval,kvector):
    deltae = []
    n = 0
    for kpoint in eigval:
        if kvector[n][0] == kvector[n][1] == kvector[n][2]: print ''
        else: continue
        i=0
        for state in kpoint:
            if state[1]<0.001:#eigval[n][i-1][0]<0 and eigval[n][i][0]>0:
                deltae.append(abs(eigval[n][i][0] - eigval[n-1][i][0]))
            i+=1
        n+=1
    return min(deltae)
    
def readEig(file):
    #Read KPOINTS.OUT and determine neighboring k-vectors
    #Deltas of energy
    eigval = []
    kvector = []
    f = open(file,'r')
    line = ' '
    n=-1
    while line != '':
        line = f.readline()
        
        #print line
        kvec = line.strip().rstrip(': k-point,vkl').split()
        
        if len(kvec) == 4:
            n=n+1
            eigval.append([])
            kvector.append(kvec)
            
        try:
            kvec.pop(0)
            
            if len(kvec) == 2 and kvec[0] not in [':']:
                eigval[n].append([float(kvec[0]),float(kvec[1])])
                
        except:
            continue
    
    #print fermi(eigval)
    print (fermidkpt(eigval,kvector))
    
    

        
        
readEig('EIGVAL.OUT')
        