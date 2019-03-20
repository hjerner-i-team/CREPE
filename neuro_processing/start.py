""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """

#from neuro_processing.primary_dataloops import start as primary

def main():
    #primary.main()
    pass

if __name__ == "__main__":
    main()
