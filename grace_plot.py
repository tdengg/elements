import numpy as np
import subprocess

class Plot(object):
    def __init__(self, xdata, ydata, calchome):
        self.xdata = xdata
        self.ydata = ydata
        self.calchome = calchome
    def simple2D(self):
        temp = open(self.calchome + 'temp','w')
        for i in range(len(self.xdata[0])):
            line = str(i) + ' '
            for var in self.ydata:
                line = line + str(var[i]) + ' '
            print line
            temp.writelines((line,'\n'))
        temp.close()
        
        ngraph = len(self.ydata)
        
        proc = subprocess.Popen(["xmgrace -block %stemp -pexec 'arrange(4,1,.1,.1,.1,ON,ON,ON)' -graph 0 -bxy 1:2 -graph 1 -bxy 1:3 -graph 2 -bxy 1:4 -graph 3 -bxy 1:5"%self.calchome], shell=True)
        proc.communicate()
        