import os

def check(allpar):
    remaining = []
    for param in allpar:
        os.chdir(param['rootdir'] + param['calcpath'])
        if os.path.isfile('./TOTENERGY.OUT'):
            infile = open('./TOTENERGY.OUT', 'r')
            totenlines = infile.readlines()
            for lines in totenlines:
                toten = lines
            param['toten'] = toten
            os.chdir(param['eospath'])
            #print param['eospath']
            ev = open('./ev', 'a')
            ev.writelines(str(param['scale']) + '    ' + str(param['toten']))
            ev.close()
        else:
            remaining.append(param)
    #print allpar
    return remaining