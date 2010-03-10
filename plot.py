import matplotlib.pyplot as plt
import read_numtext as rd
import os

import fitev as fit

structure = 'hcp'
calcpath = "/shared/transfer/tde/template/"
#path = "/fshome/tde/template/eos-test-Be-4.3187-1.56677-0.05-8-0.02"

currDir = os.listdir(calcpath)
#print currDir
list = []
filelist = []
for dir in currDir:
	if dir.find('eos-test-Be-4.3187') != -1:
		list.append(dir)

for file in list:
	read = rd.ReadData(calcpath + file, structure)
	a,ein = read.read()
	filelist.append(file)
	f = fit.Birch(calcpath + file)

	plt.plot(a,ein,'', label = file)
plt.legend()
print list
plt.show()
