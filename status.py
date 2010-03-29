import search_dir
import subprocess


subroot = '/fshome/tde/test/calc5/Au/'
root = '/fshome/tde/test/calc5/'
bin = '/fshome/tde/git/my_calc/gen/elements/'

search = search_dir.SearchDir([], subroot, True)
search.search()

proc = subprocess.call(['xsltproc', bin + 'examples_status.xsl', subroot + 'filelist.xml', '>', root + 'test.html'], stdout = subprocess.PIPE)
text, textz = proc.communicate()
print text