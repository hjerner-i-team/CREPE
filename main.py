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

from enum import Enum
from communication.hdf5_reader import HDF5Reader
from communication.stream_service import StreamService
from settings import CrepeSettings
from utils import RpycHelper
from communication.meame_listener import MeameListener
from multiprocessing import Process

# Enum to represet which modus crepe can be in
# LIVE - live connection with meame
# FILE - get data from an h5 file
class CrepeModus(Enum):
    LIVE = 0
    FILE = 1

class CREPE(CrepeSettings, RpycHelper):

    # starts the required communication services and inits crepe
    # @param modus is a CrepeModus enum
    # @param data_file_path is the file path to an optional .h5 file
    def __init__(self, modus=CrepeModus.LIVE, path_to_file= None ):
        self.modus = modus
        self.stream_services = []

        if modus == CrepeModus.LIVE:
            loop_process = Process(target=StreamService.init_and_run, args=[HDF5Reader, "STREAM", self.RPCPORTS["STREAM"]])
            loop_process.start()
            self.stream_services.append(loop_process)
            # TODO - since live is not yet implemented we generate a test stream

            #listener = MeameListener("10.20.92.130", 12340)
            # test.generate_random_test_stream()

            #listener.start_loop("STREAM", listener.listen, [])
            # self.stream_services.append(test)


        elif modus == CrepeModus.FILE:
            # initates a h5 reader and start the service
            h5 = HDF5Reader("STREAM", self.RPCPORTS["STREAM"], path_to_file)
            h5.generate_H5_stream()
            h5._start_rpc_server("STREAM")
            self.stream_services.append(h5)
        else:
            raise ValueError("Wrong crepe modus supplied")
    # Function that runs the required shutdown commands before the project is closed 
    def shutdown(self):
        for x in self.stream_services:
           print("[CREPE] Terminating ", x.name)
           x.terminate_service()
        print("[CREPE] Terminated all CREPE processes")

if __name__ == "__main__":
    crep = CREPE()
    crep.shutdown()
