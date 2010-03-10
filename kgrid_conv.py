import matplotlib.pyplot as plt
import fitev_conv as fit
import os


structure = 'hcp'
calcpath = "/shared/transfer/tde/template/"
#path = "/fshome/tde/template/eos-test-Be-4.3187-1.56677-0.05-8-0.02"

currDir = os.listdir(calcpath)
#print currDir
list = []
filelist = []
for dir in currDir:
    if dir.find('eos-convtest-Be') != -1:
        list.append(dir)

i=0
for file in list:
    
    kgrid = [2,4,6,8,10,12]     # used x-labels

    f = fit.Birch(calcpath + file, 'hcp')
    plt.subplot(131)
    plt.plot(kgrid, f.out0, label = file)
    plt.xlabel(r'$kgrid$')
    plt.ylabel(r'$V_0$   $[{Bohr^3}]$')
    plt.subplot(132)
    plt.plot(kgrid, f.out1, label = file)
    plt.xlabel(r'$kgrid$')
    plt.ylabel(r'$B_0$   $[{GPa}]$')
    plt.subplot(133)
    plt.plot(kgrid, f.out2, label = file)
    plt.xlabel(r'$kgrid$')
    plt.ylabel(r"$B_0^'$")
    
    i=i+1
    #plt.plot(a,ein,'', label = file)
plt.legend(loc='best')
plt.show()