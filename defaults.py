defaults={
          'autoconv' : 'False',
          'mod': 'eos', 
          'exectemplate':'shelcommand.xsl',
          'calculate':"True",
          'speciespath':"http://xml.exciting-code.org/species/"
          }

def set (setup):
    
   
    for param in defaults.keys():
        if not(param in setup.keys()):
            setup[param]=defaults[param]