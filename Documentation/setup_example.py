{'autoconv':{	'start': {'ngridk': 2, 'rgkmax': 6, 'swidth': 0.10000000000000001}, 			#Starting parameters for convergence
		'end': {'ngridk': 16, 'rgkmax': 9, 'swidth': 0.01}, 					#Maximum values of convergence parameters
		'order': {'1': 'rgkmax', '2': 'swidth', '3':'ngridk'}, 					#Order of convergence steps
		'stepsize': {'ngridk': 1, 'rgkmax': 0.5, 'swidth': -0.01}, 				#Convergence stepsize
		'err':{'energy':1,'B':10,'V':1,'err':1}							#Creterion for convergence					
		},
'isautoconv': True,  											#
'calculate': 'True', 											#
'structure': 'fcc', 											#Lattice type
'exectemplate': 'shelcommand.xsl', 
'speciespath': '/home/tom/git/exciting/species', 							#
'species': 'Al', 											#Define species
'param': {	'scale': {'azero': 7.4287197647957877, 'steps': 11, 'da': 0.050000000000000003}, 	#Set azero as starting lattice parameter
		'rmt': [2.0], 'rgkmax': [6.0, 6.5, 7.0], 
		'swidth': [0.10000000000000001], 
		'covera': {'dcovera': 0.032000000000000001, 'steps': 11, 'coverazero': 1.6000000000000001}, 
		'ngridk': [2]}, 
'mod': 'eos'
}
