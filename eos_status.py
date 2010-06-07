import matplotlib.pyplot as plt
import numpy as np

import search_dir as search

class Status(object):
    def __init__(self, root):
        self.root = root
        matrix = []
        sear = search.SearchDir(['input'], self.root)
        info, dict = sear.search()
        
        Rad = []
        rad = []
        thetazero = []
        thetapar = 0
        deltatheta = []
        label = []
        i=0
        while i < max(dict['depth'])+1:
            j=0
            k=0
            matrix.append([])
            while j < len(dict['depth']):
                if dict['depth'][j] == i:
                    #deltatheta.append(thetapar/len(dict['subdirs'][j]))
                    matrdict = {}
                    for key in dict.keys():
                        matrdict[key] = dict[key][j]

                    matrix[i].append([])
                    matrix[i][k] = matrdict
                    
                    k=k+1
                j=j+1
            i=i+1
        i=0
        
        while i < len(matrix):
            j=0
            dtheta = 0
            for element in matrix[i]:
                rad.append(element['depth'])
                Rad.append(1)
                if element['pardir'] == None:
                    element['dtheta'] = 2.*np.pi#/len(element['subdirs']))
                    element['thetazero'] = 0
                    thetazero.append(0)
                    deltatheta.append(2.*np.pi)
                    label.append(element['dirname'])
                else:
                    for e in matrix[i-1]:
                        if e['dirname'] == element['pardir']:
                            dthetapar = e['dtheta']
                            thetazeropar = e['thetazero']
                    element['dtheta'] = dthetapar/len(element['subdirs'])
                    element['thetazero'] = thetazeropar + j*element['dtheta']
                    
                    thetazero.append(thetazeropar + dtheta)
                    deltatheta.append(dthetapar/len(element['subdirs']))
                    label.append(element['dirname'])
                    dtheta = dtheta + element['dtheta']
                    #print element['dtheta']*180./np.pi, element['thetazero']*180./np.pi, j, i
                j=j+1
            i=i+1
            
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        
        bars = ax.bar(thetazero, Rad, width=deltatheta, bottom=rad, picker=True)
        #i=0
        #while i < len(label):
        #    ax.text(thetazero[i], rad[i], label[i])
        #    i=i+1
        for r,bar in zip(rad, bars):
            bar.set_facecolor( plt.cm.jet(r/10.))
            bar.set_alpha(0.5)
            bar.set_label(label)
        fig.canvas.mpl_connect('pick_event', self.onpick)
        plt.show()
    def onpick(self, event):

       if event.artist!=line: return True

       N = len(event.ind)
       if not N: return True

       # the click locations
       x = event.mouseevent.xdata
       y = event.mouseevent.ydata


       distances = np.hypot(x-xs[event.ind], y-ys[event.ind])
       indmin = distances.argmin()
       dataind = event.ind[indmin]

       self.lastind = dataind
       self.update()

    def update(self):
        if self.lastind is None: return

        dataind = self.lastind

        ax2.cla()
        ax2.plot(X[dataind])

        ax2.text(0.05, 0.9, 'mu=%1.3f\nsigma=%1.3f'%(xs[dataind], ys[dataind]),
                 transform=ax2.transAxes, va='top')
        ax2.set_ylim(-0.5, 1.5)
        self.selected.set_visible(True)
        self.selected.set_data(xs[dataind], ys[dataind])

        self.text.set_text('selected: %d'%dataind)
        fig.canvas.draw()

        
status = Status('/fshome/tde/test/calc10/')

   
