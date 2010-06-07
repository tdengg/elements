import search_dir
import subprocess


subroot = '/fshome/tde/test/calc9/convergence/Ti/'
root = '/fshome/tde/test/calc9/convergence/'
bin = '/fshome/tde/git/my_calc/gen/elements/'

search = search_dir.SearchDir([], subroot, True)
search.search()

proc = subprocess.Popen(['xsltproc ' + bin + 'examples_status.xsl ' + subroot + 'filelist.xml > ' + root + 'test.html'], stdout = subprocess.PIPE, shell = True)
text, textz = proc.communicate()
print text