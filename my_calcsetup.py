{ 
                'param': { 
                             'scale' : { 
			     		  'azero': 4.319, 
					  'da': 0.05, 
					  'steps': 11},
                             'rmt': [2.85],
                             'rgkmax': [6,7],
                             'ngridk' : [8],
                             'swidth': [0.01],
                             'covera' :{ 
                                          'coverazero': 1.6,  
                                          'dcovera': 1.6/50, 
                                          'steps': 11 } 
                             },
                'species': 'Be', 
                'structure':'hcp',
                'mod': 'simple_conv',
                'speciespath': "http://xml/exciting-code.org/species/",
                'calculate' : 'True',
                'exectemplate':"shelcommand.xsl"
                }
