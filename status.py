import matplotlib
matplotlib.use('GTKAgg')
from mpl_toolkits.mplot3d import Axes3D, axes3d
import matplotlib.pyplot as plt
import os
import numpy as nm
import lxml.etree as etree
import gobject

fig = plt.figure()

ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

#ax.set_ylim(100, 400)
#ax.set_xlim(6, 9)

fig2 = plt.figure()
ax = Axes3D(fig2)

def refresh():
    
    tree = etree.parse('auto_conv.xml')
    pars = ['rgkmax','ngridk','swidth']
    parval = tree.xpath("//conv/@parval")
    for par in pars:
        valstack = []
        B = []
        swidth = []
        rgkmax = []
        ngridk = []
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
            n = len(B)
            line, = ax2.plot(valstack[0:n],B,'r')
            fig.canvas.draw_idle()
            val1 = valstack
        elif par == 'ngridk':
            n = len(B)
            line, = ax3.plot(valstack[0:n],B,'g')
            fig.canvas.draw_idle()
            val2 = valstack
        elif par == 'swidth':
            n = len(B)
            line, = ax4.plot(valstack[0:n],B,'b')
            fig.canvas.draw_idle()
            val3 = valstack
            
    n=0
    for v in parval:
        ngk = eval(v)['ngridk']
        rkm = eval(v)['rgkmax']
        swd = eval(v)['swidth']
        
        if len(ngk) > 1: ngridk.append(ngk[n])
        else: ngridk.append(ngk[0])
        if len(rkm) > 1:rgkmax.append(rkm[n])
        else: rgkmax.append(rkm[0])
        if len(swd) > 1:swidth.append(swd[n])
        else: swidth.append(swd[0])
        if (len(ngk) + len(rkm) + len(swd)) > 3: n=n+1
        if n>=3: n=0
    
    cset = ax.scatter(ngridk,rgkmax,swidth, linewidths=2,linestyle = 'solid')
    
    lastpar = eval(tree.xpath("(//conv/@parval)[last()]")[0])
    point_ngk = [lastpar['ngridk'][-1]]
    point_rkm = [lastpar['rgkmax'][-1]]
    point_swd = [lastpar['swidth'][-1]]
    cset = ax.scatter(point_ngk, point_rkm, point_swd, marker='s',s=1000, c='r')
    
    
    return True

    
gobject.timeout_add(1000,refresh)
plt.show()
    