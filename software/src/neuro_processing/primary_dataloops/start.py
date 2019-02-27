""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("software/src")+len("software/src")])
""" End import fix """

# This file will keep track of which start the primary dataloop.

from neuro_processing.primary_dataloops.modus import PrimaryDataLoopModus, PrimaryDataLoopModusEnum
from neuro_processing.primary_dataloops.implementations.example import start as example

modus = PrimaryDataLoopModus()

def main():
    print(modus)
    example.main()

if __name__ == "__main__":
    main()
