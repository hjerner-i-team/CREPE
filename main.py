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
import time 

from communication.hdf5_reader import HDF5Reader, HDF5Mode
from neuro_processing.neuro_processing import NeuroProcessor
from communication.queue_service import QueueService, StartQueueService
#from communication.meame_listener import MeameListener
from multiprocessing import Process, Queue
import signal

# Enum to represet which modus crepe can be in
# LIVE - live connection with meame
# FILE - get data from an h5 file
class CrepeModus(Enum):
    LIVE = 0
    FILE = 1
    OFFLINE = 2

class CREPE():

    # starts the required communication services and inits crepe
    # @param modus is a CrepeModus enum
    # @param data_file_path is the file path to an optional .h5 file
    def __init__(self, modus=CrepeModus.LIVE, file_path = None, queue_services = None):
        self.modus = modus
        self.queue_services = []

        hdf5 = None
        if modus == CrepeModus.LIVE:
            # TODO - since live is not yet implemented we generate a test stream
            hdf5 = StartQueueService(HDF5Reader, mode=HDF5Mode.TEST)
            
            #listener = MeameListener("10.20.92.130", 12340)

            #listener.start_loop("STREAM", listener.listen, [])
            # self.stream_services.append(test)

        elif modus == CrepeModus.FILE:
            # initates a h5 reader and start the service
            hdf5 = StartQueueService(HDF5Reader, file_path=file_path)

        elif modus == CrepeModus.OFFLINE:
            neuro = StartQueueService(NeuroProcessor, meame_address = "127.0.0.1", meame_port = 40000, bitrate=1000)
        else:
            raise ValueError("Wrong crepe modus supplied")

#        self.queue_services.append(hdf5)
        self.queue_services.append(neuro)
 
        signal.signal(signal.SIGINT, self._shutdown)
        
        if queue_services is not None:
            for i, service in enumerate(queue_services):
                queue_in = self.queue_services[-1].queue_out
                service[1]["queue_in"] = queue_in
                qs = StartQueueService(service[0], **service[1])
                self.queue_services.append(qs)
            if len(self.queue_services) > 1:
                print("[CREPE] started ", len(self.queue_services) - 1 ," extra services")

        # connect meame speaker here
    
    def _shutdown(self, sig, frame):
        print("[CREPE] signal: ", sig, " with frame: ", frame, " intercepted, shutting down")
        self.shutdown()
        sys.exit(0)

    # Function that runs the required shutdown commands before the project is closed 
    def shutdown(self):
        for x in self.queue_services:
           print("[CREPE] Terminating ", x.get_name())
           x.process.terminate()
        print("[CREPE] Terminated all CREPE processes")

if __name__ == "__main__":
    #crep = CREPE(modus=CrepeModus.FILE, file_path="../test_data/4.h5")
    crep = CREPE()
    time.sleep(3)
    crep.shutdown()
