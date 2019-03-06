# This file represents the main file and entrypoint to this entire project
#   This project is a part of the EiT village NTNU Cyborg
#   In this project we will demonstrate an exepriment with the neurocellculture.
#   This is done by connecting a hardware platform and a software platform to the MEAME
#   interface at St. Olavs.
#
#   Github repo: https://github.com/hjerner-i-team/CREPE

from multiprocessing import Process
from communication.start import main as communication_main
from neuro_processing.start import main as neuro_main

# Function that runs the required shutdown commands before the project is closed 
def shutdown():
    pass

# Main entry point to entire project
def main():
    #Welcome to our main function! Hope you have a happy time

    comm = Process(target=communication_main)
    neuro = Process(target=neuro_main)
    
    comm.start()
    neuro.start()
    
    neuro.join()
    comm.join()
    

    
    shutdown()

if __name__ == "__main__":
    main()
