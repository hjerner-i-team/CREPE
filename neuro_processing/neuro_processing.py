""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

import numpy as np
import _thread 
import time
from threading import Event
from pre_processing.stream import Stream
from pre_processing.meame_listener import MeameListener
from pre_processing.neuro_processing import *
from communication.queue_service import QueueService

class neuroProcessor(meame_address = "127.0.0.1", meame_port = 4000, bitrate = 10000):
    def __init__():
        #Initialize streams
        meamestream = Stream(60, 10000)
        avgstream = Stream(60, 10000)

        #Initialize meame listener. Needs an output stream
        meamelistener = MeameListener(meame_address, meame_port, meamestream)
        
    def run():
        print("Starting meame listener")
        _thread.start_new_thread(meamelistener.listen,())
        print("Starting moving avg")
        _thread.start_new_thread(moving_avg, (100, meamestream, avgstream,))
        print("Starting FFT")
        #_thread.start_new_thread(moving_avg, (segment_dim[1], stream,))
        fft_max(1000,1,1000, avgstream)

            

    
