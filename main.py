# This file represents the main file and entrypoint to this entire project
#   This project is a part of the EiT village NTNU Cyborg
#   In this project we will demonstrate an exepriment with the neurocellculture.
#   This is done by connecting a hardware platform and a software platform to the MEAME
#   interface at St. Olavs.
#
#   Github repo: https://github.com/hjerner-i-team/CREPE

""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """

from multiprocessing import Process
from communication.start import main as communication_main
from neuro_processing.start import main as neuro_main

class CREPE():
    # start all the processe 
    # @param data_file_path is the file path to an optional .h5 file
    def __init__(self, data_file_path = None ):
        print("[CREPE] Starting CREPE processes")
        self.comm = Process(target=communication_main, args=[data_file_path])
        self.neuro = Process(target=neuro_main)
        
        self.comm.start()
        self.neuro.start()
        
        #self.neuro.join()
        #self.comm.join()

    # Function that runs the required shutdown commands before the project is closed 
    def shutdown(self):
        self.comm.terminate()
        self.neuro.terminate()
        print("Terminated CREPE processes")

if __name__ == "__main__":
    crep = CREPE()
    crep.start("__TESTING")
