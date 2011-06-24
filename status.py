import matplotlib.pyplot as plt
import time
import os
import numpy as nm
import subprocess
import lxml.etree as etree


tree = etree.parse('auto_conv.xml')

fig = plt.figure()
ax = fig.add_subplot(211)
line, = ax.plot([], [], animated=True, lw=2)
#ax.set_ylim(-1.1, 1.1)
#ax.set_xlim(0, 5)
ax.grid()
xdata, ydata = [], []



def refresh():
    #read nata via xpath:
    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox)
    fig.canvas.restore_region(background)
    
    
    
    pars = ['rgkmax','ngridk','swidth']
    for par in pars:
        valstack = []
        energy = tree.xpath("//conv[@par='%s']/@energy"%par)
        
        B = tree.xpath("//conv[@par='%s']/@B"%par)
        V = tree.xpath("//conv[@par='%s']/@V"%par)
        val = tree.xpath("//conv[@par='%s']/@parval"%par)
        
        i=0
        for vlues in val:
            if len(eval(vlues)[par]) > 1:
                valstack.append(float(str(eval(vlues)[par][i]).rstrip()))
                if i<len(eval(vlues)[par])-1: i+=1
                else: i=0
            else:
                
                valstack.append(float(str(eval(vlues)[par][0]).rstrip()))
        if par == 'rgkmax':
            line.set_data(valstack, B)
            ax.draw_artist(line)
        fig.canvas.blit(ax.bbox)

    
for i in range(100):
    print 'plotting'
    refresh()
    time.sleep(10)  
plt.show()
    