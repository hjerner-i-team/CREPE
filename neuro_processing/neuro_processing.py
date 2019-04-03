""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

import numpy as np
import _thread 
import time
from threading import Event
from neuro_processing.stream import Stream
from neuro_processing.meame_listener import MeameListener
from neuro_processing.processing import *
from communication.queue_service import QueueService

class NeuroProcessor(QueueService):
    def __init__(self, meame_address = "10.20.92.130", meame_port = 12340, bitrate = 10000, segment_length = 100,queue_out=None, queue_in=None):
        QueueService.__init__(self, name="NEUROPROCESSOR" , queue_out=queue_out, queue_in=queue_in)

        #Initialize streams
        self.meamestream = Stream(60, 10000)
        self.avgstream = Stream(60, 10000)
        self.fftstream = Stream(60, 100)

        #Initialize meame listener. Needs an output stream
        self.meamelistener = MeameListener(self.meamestream,meame_address, meame_port, bitrate, segment_length)
        
    def run(self):
        print("Starting meame listener")
        _thread.start_new_thread(self.meamelistener.listen,())
#        print("Starting moving avg")
#        _thread.start_new_thread(moving_avg, (100, self.meamestream, self.avgstream,))
        print("Starting FFT")
        _thread.start_new_thread(fft_max, (1000,1,1000, self.meamestream,self.fftstream,))
        
        #put final output stream to queue    
        i = 1
        while(i < self.fftstream.final_index):
            if(i <= self.fftstream.size):
                self.put(self.fftstream.data[:,i-1:i].reshape(60))
#                print("Neuro putting to outputstream:")
#                print(self.fftstream.data[:,i-1:i].reshape(60))
                i += 1
            else:
                time.sleep(0.05)
        print("Neuro processor finished")
    
