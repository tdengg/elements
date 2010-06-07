
import xml.etree.ElementTree as etree
import subprocess
import collect_data

proc1 = subprocess.Popen(['xsltproc ' + execpath + 'parset.xsl ' + rootdir + 'dataconversion_fitcoa.xml > ' + rootdir +  'coadata.xml'], shell=True)
proc1.communicate()