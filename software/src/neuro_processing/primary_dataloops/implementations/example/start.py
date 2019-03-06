""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("software/src")+len("software/src")])
""" End import fix """
from neuro_processing.primary_dataloops.implementations.example import readout_layer

def main():
    readout_layer.main()
