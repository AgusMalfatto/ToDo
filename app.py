import os

from todo import configuracion

configuracion.cargar_variables()

import subprocess

def ejecutar_flask_run():
    try:
        subprocess.call(['flask', 'run'])
    except KeyboardInterrupt:
        pass
    
ejecutar_flask_run()

