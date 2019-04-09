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

import time 

from communication.hdf5_reader import HDF5Reader
from neuro_processing.neuro_processing import NeuroProcessor
from communication.queue_service import QueueService, StartQueueService
#from communication.meame_listener import MeameListener
from multiprocessing import Process, Queue
from crepe_modus import CrepeModus
import signal

class CREPE():

    # starts the required communication services and inits crepe
    # @param modus is a CrepeModus enum
    # @param data_file_path is the file path to an optional .h5 file
    def __init__(self, modus=CrepeModus.LIVE, file_path = None, queue_services = None):
        self.modus = modus
        self.queue_services = []
        
        print("\n[CREPE.init] init crepe with args:\n\tmodus_\t",modus,"\n\tfile_path:\t", 
                file_path,"\n\tqueue_services:\t",queue_services)

        if modus == CrepeModus.LIVE:
            
            neuro = StartQueueService(NeuroProcessor)
            self.queue_services.append(neuro)

        elif modus == CrepeModus.FILE:
            # initates a h5 reader and start the service
            hdf5 = StartQueueService(HDF5Reader, file_path=file_path)
            self.queue_services.append(hdf5)

        elif modus == CrepeModus.OFFLINE:
            neuro = StartQueueService(NeuroProcessor, meame_address = "127.0.0.1", meame_port = 40000, bitrate=1000)
            self.queue_services.append(neuro)
        elif modus == CrepeModus.TEST:
            hdf5 = StartQueueService(HDF5Reader, mode=self.modus)
            self.queue_services.append(hdf5)

        else:
            raise ValueError("Wrong crepe modus supplied")


        if queue_services is not None:
            for i, service in enumerate(queue_services):
                queue_in = self.queue_services[-1].queue_out
                service[1]["queue_in"] = queue_in
                qs = StartQueueService(service[0], **service[1])
                self.queue_services.append(qs)
            if len(self.queue_services) > 1:
                print("\n[CREPE.init] started ", len(self.queue_services) - 1 ," extra services")

        # connect meame speaker here
        signal.signal(signal.SIGINT, lambda signal, frame: self._shutdown())
    
    def get_first_queue(self):
        return self.queue_services[0].queue_out

    def get_last_queue(self):
        return self.queue_services[-1].queue_out

    def wait(self, data_func=None):
        last_queue = self.get_last_queue()
        dummy = QueueService(name="END", queue_in=last_queue)
        while True:
            data = dummy.get()
            if data is False:
                self.shutdown()
                return
            if data_func is not None:
                data_func(data)

    def _shutdown(self):
        print("\n[CREPE._shutdown] sigint intercepted, shutting down")
        self.shutdown()
        sys.exit(0)

    # Function that runs the required shutdown commands before the project is closed 
    def shutdown(self):
        # print("[CREPE] queue_services ", [x.get_name() for x in self.queue_services] )
        for x in self.queue_services:
           print("[CREPE.shutdown] Terminating ", x.get_name())
           x.process.terminate()
        self.queue_service = None
        print("[CREPE.shutdown] Terminated all CREPE processes")

if __name__ == "__main__":
    #crep = CREPE(modus=CrepeModus.FILE, file_path="../test_data/4.h5")
    crep = CREPE()
    time.sleep(3)
    crep.shutdown()
