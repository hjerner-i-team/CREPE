""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """


# import CREPE.main and start it 
import main
def CREPE(modus=main.CrepeModus.LIVE, path_to_file = None ):
    return main.CREPE(modus=modus, path_to_file=path_to_file)

CrepeModus = main.CrepeModus
