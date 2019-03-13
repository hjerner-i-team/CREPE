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

def crepe_start( data_file_path = None ):
    print("Starting CREPE processes")
    comm = Process(target=communication_main, args=[data_file_path])
    neuro = Process(target=neuro_main)
    
    comm.start()
    neuro.start()
    
    #neuro.join()
    #comm.join()

# Function that runs the required shutdown commands before the project is closed 
def shutdown():
    pass

# Main entry point to entire project
def main():
    #Welcome to our main function! Hope you have a happy time
    
    shutdown()

if __name__ == "__main__":
    main()
