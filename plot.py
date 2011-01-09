import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as etree

class Plot(object):
    def __init__(self, autompl=False):

        self.params = etree.parse('./const_parameters.xml')
        self.eos_data = etree.parse('./eos_data.xml')
        self.convergence = etree.parse('./convergence.xml')
        self.autompl = autompl
        
        structure = self.params.getroot().find('structure').get('str')
        if structure in ['hcp','hex']:
            coaplot=True
        else:
            coaplot=False

        if not self.autompl:
            for i in range(5):
                msg = {}
                if coaplot:
                    msg['msg_coa'] = '\nFor energy vs. c/a type: covera'
                else:
                    msg['msg_coa'] = ''
                msg['msg_eos'] = '\nFor energy vs. volume type: eos'
                msg['msg_conv'] = '\nFor convergence type: conv'
                type = raw_input('What do you want to plot?%(msg_coa)s%(msg_eos)s%(msg_conv)s\n>>>'%msg)
                if type == 'eos':
                    self.eosplot_mpl()
                    break
                elif type == 'covera':
                    self.coaplot_mpl()
                    break
                elif type == 'conv':
                    self.conv_mpl()
                    break
                else:
                    print 'Please try again and type one of: eos%s'%coaplot
        else:
            self.eosplot_mpl()

                
        #template = f.getroot().find('elementshome')
    def eosplot_mpl(self):
        vol = []
        energy = []
        expvol = []
        expenergy = []
        expvol_bad = []
        expenergy_bad = []
        par = []
        parname = []
        colLabel = []
        e_min = []
        v_min = []
        b0_min = []
        db0_min = []
        rowLabel = []
        cellText = []
            
        eosdata = etree.parse('./eosplot.xml')
        root = eosdata.getroot()
        graphs = root.getiterator('graph')
        n=0
        for graph in graphs:
            vol.append([])
            energy.append([])
            par.append(graph.get('param'))
            parname.append(graph.get('parname'))
            e_min.append(graph.get('energy_min'))
            v_min.append(graph.get('vol_min'))
            b0_min.append(graph.get('B0'))
            db0_min.append(graph.get('dB0'))
            points = graph.getiterator('point')
            for point in points:
                vol[n].append(float(point.get('volume')))
                energy[n].append(float(point.get('energy')))
            n=n+1
        if len(par)>1:
            diff_parname = []
            for name in parname:
                if name not in diff_parname:
                    diff_parname.append(name)
            ind = []
            names = []
            par_to_plot = []
            for name in diff_parname:
                if name not in names:
                    p = ('[' + raw_input("Specify which values of %s to plot. e.g.2,4\n>>>"%name) + ']')
                    if p == '[all]':
                        par_to_plot.append('all')
                    else:
                        par_to_plot.append(eval(p))
                    names.append(name)

            for pars_to_plot in par_to_plot:
                if pars_to_plot == 'all':
                    ind = range(len(graphs))
                    continue
                for diff_pars in pars_to_plot:
                    try:
                        ind.append(par.index(str(diff_pars)))
                    except:
                        print 'One or more parameters you chose are not in the calculated ones!'
                        return

        else:
            ind = range(len(graphs))
                       
        graphs = root.getiterator('graph_exp')
        n=0
        for graph in graphs:
            expvol.append([])
            expenergy.append([])
            points = graph.getiterator('point')
            npoints = len(points)
            for point in points:
                expvol[n].append(float(point.get('volume')))
                expenergy[n].append(float(point.get('energy')))
            n=n+1
            
        graphs = root.getiterator('graph_exp_bad')
        n=0
        for graph in graphs:
            expvol_bad.append([])
            expenergy_bad.append([])
            points = graph.getiterator('point')
            npoints = len(points)
            for point in points:
                expvol_bad[n].append(float(point.get('volume')))
                expenergy_bad[n].append(float(point.get('energy')))
            n=n+1
            
        structure = self.params.getroot().find('structure').get('str')
        species = self.params.getroot().find('species').get('spc')
        
        n=0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Equation of state plot of %(spc)s (%(str)s)'%{'spc':species,'str':structure})

        colors = ['b','g','r','c','m','k','FF9933','006600','66CCFF','y']
        for graph in graphs:
            if n in ind:
                ax.plot(vol[n], energy[n], '', label='%(name)s = %(val)s'%{'name':parname[n], 'val':str(par[n])}, color=colors[n])
                ax.plot(expvol[n], expenergy[n], '.', color=colors[n])
                point, = ax.plot(v_min[n], e_min[n], 'o',picker=5)
                ax.plot(expvol_bad[n], expenergy_bad[n], '.')
                ax.set_xlabel(r'Volume   [Bohr$^3$]')
                ax.set_ylabel(r'Total energy   [Hartree]')
                ax.legend(loc='best')
                #ax.annotate('optimal volume '+str(min[0]), xy=(min,curve(min)), xycoords='data' ,
                #            xytext=(min-10,curve(min)+0.002) ,  arrowprops=dict(arrowstyle="->"))
                #plt.title('Equation of state plot of %(spc)s (%(str)s)'%{'spc':species,'str':structure})
                rowLabel.append('%(name)s = %(val)s'%{'name':parname[n], 'val':str(par[n])})
            n=n+1
        
        #def onpick(event):
        #    if isinstance(event.artist, Line2D):
        #        thisline = event.artist
        #        xdata = thisline.get_xdata()
        #        ydata = thisline.get_ydata()
        #        ind = event.ind
        #        print 'onpick1 line:', zip(npy.take(xdata, ind), npy.take(ydata, ind))
        #fig.canvas.mpl_connect('pick_event', onpick)


        width = 100

        cell = [v_min,e_min,b0_min,db0_min]
        for column in cell:
            cellText.append(['%s' % (x) for x in column])
        cellText.reverse()
        #table = plt.table(cellText=cellText, cellColours=None,
        #          cellLoc='right',colWidths=[0.1,0.1,0.1,0.1,0.1],
        #          rowLabels=[r'$(c/a)_min$',r'$V_0$',r'$E_tot$$_,min$',r'$(c/a)_min$'], rowColours=None, rowLoc='right',
        #          colLabels=rowLabel, colColours=None, colLoc='center',
        #          loc='right', bbox=None)
        #for column in cell:
        #table.scale(2,2)
        #table.auto_set_font_size()
        if not self.autompl:
            plt.show()
        else:
            plt.savefig('eos.ps')

        #table.auto_set_font_size()
    def coaplot_mpl(self):
        vol = []
        volume = []
        energy = []
        expvol = []
        expenergy = []
        expvol_bad = []
        expenergy_bad = []
        par = []
        parname = []
        
        eosdata = etree.parse('./eosplot.xml')
        rooteos = eosdata.getroot()
        graphs_eos = rooteos.getiterator('graph')
        npar = len(graphs_eos)
        
        coadata = etree.parse('./coaplot.xml')
        root = coadata.getroot()
        graphs = root.getiterator('graph')
        n=0
        for graph in graphs:
            vol.append([])
            energy.append([])
            par.append(graph.get('param'))
            parname.append(graph.get('parname'))
            points = graph.getiterator('point')
            for point in points:
                vol[n].append(float(point.get('covera')))
                energy[n].append(float(point.get('energy')))
            n=n+1
        graphs = root.getiterator('graph_exp')
        n=0
        for graph in graphs:
            expvol.append([])
            expenergy.append([])
            points = graph.getiterator('point')
            npoints = len(points)
            for point in points:
                expvol[n].append(float(point.get('covera')))
                expenergy[n].append(float(point.get('energy')))
            n=n+1
            
        graphs = root.getiterator('graph_exp_bad')
        n=0
        for graph in graphs:
            expvol_bad.append([])
            expenergy_bad.append([])
            points = graph.getiterator('point')
            npoints = len(points)
            volume.append(graph.get('volume'))
            for point in points:
                expvol_bad[n].append(float(point.get('covera')))
                expenergy_bad[n].append(float(point.get('energy')))
            n=n+1
            
        if len(par)>1:
            diff_parname = []
            for name in parname:
                if name not in diff_parname:
                    diff_parname.append(name)
            ind = []
            names = []
            par_to_plot = []
            for name in diff_parname:
                if name not in names:
                    p = ('[' + raw_input("Specify which values of %s to plot. e.g.2,4\n>>>"%name) + ']')
                    if p == '[all]':
                        par_to_plot.append('all')
                    else:
                        par_to_plot.append(eval(p))
                    names.append(name)
            for pars_to_plot in par_to_plot:
                if pars_to_plot == 'all':
                    ind = range(npar)
                    continue
                for diff_pars in pars_to_plot:
                    try:
                        ind.append(par.index(str(diff_pars)))
                    except:
                        print 'One or more parameters you chose are not in the calculated ones!'
                        return

        else:
            ind = range(len(graphs))
            
        structure = self.params.getroot().find('structure').get('str')
        species = self.params.getroot().find('species').get('spc')

        n=0
        j=0
        for j in range(len(parname)):
            if j in ind:
                ind.append(j+npar)
                plt.plot(vol[ind[n]], energy[ind[n]], '', label='V: %(vol)s '%{'vol':str(int(round(float(volume[n])))),'parname':parname[n],'par':par[n]})
                plt.plot(expvol[ind[n]], expenergy[ind[n]], '.',color='k')
                plt.plot(expvol_bad[ind[n]], expenergy_bad[ind[n]], '.')
                plt.xlabel(r'c/a')
                plt.ylabel(r'Total energy   [Hartree]')
                plt.legend(loc='best')
                plt.title('c/a - plot of %(spc)s (%(str)s)'%{'spc':species,'str':structure})
                n=n+1
            j=j+1

        plt.show()
        
    def conv_mpl(self):
        vol = []
        energy = []
        expvol = []
        expenergy = []
        expvol_bad = []
        expenergy_bad = []
        par = []
        parname = []
        colLabel = []
        e_min = []
        v_min = []
        b0_min = []
        db0_min = []
        
        eosdata = etree.parse('./eosplot.xml')
        root = eosdata.getroot()
        graphs = root.getiterator('graph')
        
        structure = self.params.getroot().find('structure').get('str')
        species = self.params.getroot().find('species').get('spc')
        
        n=0
        for graph in graphs:
            vol.append([])
            energy.append([])
            par.append(graph.get('param'))
            parname.append(graph.get('parname'))
            e_min.append(graph.get('energy_min'))
            v_min.append(graph.get('vol_min'))
            b0_min.append(graph.get('B0'))
            db0_min.append(graph.get('dB0'))
            points = graph.getiterator('point')
            for point in points:
                vol[n].append(float(point.get('volume')))
                energy[n].append(float(point.get('energy')))
            n=n+1
        
        
        fig = plt.figure()
        
        ax1 = fig.add_subplot(221)
        ax1.set_title('Convergence for %(spc)s (%(str)s)'%{'spc':species,'str':structure})
        colors = ['b','g','r','c','m','k','FF9933','006600','66CCFF','y']
        ax1.plot(par, v_min, '-', par, v_min, '.', color=colors[n])
        ax1.set_ylabel(r'Volume   [Bohr$^3$]')
        ax1.set_xlabel(parname[0])
        ax1.axis('tight')
        
        ax3 = fig.add_subplot(222)
        #ax2.set_title('Convergence of energy for %(spc)s (%(str)s)'%{'spc':species,'str':structure})
        colors = ['b','g','r','c','m','k','FF9933','006600','66CCFF','y']
        ax3.plot(par, e_min, '-',par, e_min, '.', color=colors[n])
        ax3.set_ylabel(r'Energy   [Hartree]')
        ax3.set_xlabel(parname[0])
        ax3.axis('tight')
        ax4 = fig.add_subplot(223)
        #ax3.set_title('Convergence of bulk - modulus for %(spc)s (%(str)s)'%{'spc':species,'str':structure})
        colors = ['b','g','r','c','m','k','FF9933','006600','66CCFF','y']
        ax4.plot(par, b0_min, '-',par, b0_min, '.', color=colors[n])
        ax4.set_ylabel(r'B$_0$   [GPa]')
        ax4.set_xlabel(parname[0])
        
        ax6 = fig.add_subplot(224)
        #ax4.set_title('Convergence of derivative of bulk -modulus for %(spc)s (%(str)s)'%{'spc':species,'str':structure})
        
        colors = ['b','g','r','c','m','k','FF9933','006600','66CCFF','y']
        ax6.plot( par, db0_min, '-',par, db0_min, '.', color=colors[n])
        ax6.set_ylabel(r"B$_0$'")
        ax6.set_xlabel(parname[0])
        fig.subplots_adjust(left=0.1)
        plt.show()


if __name__=='__main__':            
    Plot().eosplot_mpl()

