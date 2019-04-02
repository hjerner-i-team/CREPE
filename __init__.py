""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """

import main

CrepeModus = main.CrepeModus

def CREPE(modus=CrepeModus.LIVE, file_path = None, queue_services = None):
    return main.CREPE(modus=modus, file_path=file_path, queue_services = queue_services)
