import os
import subprocess

def submit(initpath):
    
    os.chdir(initpath)
    runcalc = subprocess.Popen(['llsubmit', './lljob'])
    runcalc.communicate()

"""
class Transfer(object):
    def __init__(self, initpath):
        
        #os.chdir("/fshome/tde/test/")
        #scpr = subprocess.Popen(["scp", "-r", "./", "tde@g40cluster:test/"], stdin=subprocess.PIPE)
        #scpr.communicate(input="")
        
        #subprocess.Popen(['ssh','-X','tde@g40cluster'])
        os.chdir(initpath)
        runcalc = subprocess.Popen(['llsubmit', './lljob'])
        
        runcalc.communicate()
"""      
        
#Transfer()
