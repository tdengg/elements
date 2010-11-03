defaults={
          'exectemplate':'shelcommand.xsl'}

def set (setup):
    
   
    for param in defaults.keys():
        if not(param in setup.keys()):
            setup[param]=defaults[param]