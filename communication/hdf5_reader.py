""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

from communication.queue_service import QueueService, StartQueueService 
from settings import DEFAULT_STREAM_DIMENSION
import time
import random

import h5py
import numpy as np
from enum import Enum
class HDF5Mode(Enum):
    H5 = 0
    TEST = 1

# reads from a hdf5 file and puts it unto the queue, or generates a random test stream and outputs it to the queue
class HDF5Reader(QueueService):

    def __init__(self, queue_out=None, file_path=None, mode=HDF5Mode.H5):
        QueueService.__init__(self, name="HDF5READER", queue_out=queue_out)
        self.file_path = file_path
        self.mode = mode

    # Generates a 2d numpy array from a .h5 file to self.stream
    def generate_H5_stream(self): 
        print("[CREPE.commnication.hdf5_reader] Generating stream from h5 file: ", self.file_path)
        # open the file with h5py
        f = h5py.File(self.file_path, 'r') 
        # navigate to where the raw data is in the .h5 file
        # Use the program hdfviewer or check our upcomming documentation for full .h5 format
        data = f['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
        # this will return a h5py object so we convert it to a list
        print("[CREPE.communication.hdf5_reader] len of a row: ", len(data[0]))
        for i in range(100, len(data[0]) + 1, 100):
            self.put(data[:, i - 100:i])
        remaining = data[:, len(data) - i % 100:len(data)]
        self.put(remaining)
        print("[CREPE.communication.hdf5_reader] data pushed to stream")

    # Generates a 2d matrice with random numbers to self.stream for testing purposes
    def _generate_random_test_segment(self, _range):
        #print("[CREPE.communication.hdf5_reader] Generating random test stream")
        # generate a 2d numpy matrice of random values between 0 & 1
        rand_data = np.random.rand(DEFAULT_STREAM_DIMENSION,_range)
        # multiply it by 200 to "simulate" real data
        rand_data = rand_data * 200
        
        # return new data
        return rand_data

        #self.append_stream_segment_data(rand_data)
    
    def _generate_random_test_segment_list(self, _range):
        rand_data = [[random.random() * 200 for i in range(_range)] for j in range(DEFAULT_STREAM_DIMENSION)]
        return rand_data

    def run(self):
        if self.mode == HDF5Mode.H5:
            self.generate_H5_stream()
        elif self.mode == HDF5Mode.TEST:
            i = 0
            while True:
                seg = self._generate_random_test_segment_list(100)
                self.put(seg)
                i += len(seg[0])
                print(i)
                # sleep for 0.5 seconds
                time.sleep(0.005)
            

if __name__ == "__main__":
    #h = HDF5Reader()
    # h.generate_H5_stream()
    hdf5_process, hdf5_out = StartQueueService(HDF5Reader, 
            file_path="../test_data/4.h5", mode=HDF5Mode.TEST)
    i = 0
    while True:
        i += len(hdf5_out.get()[0])
        print(i)

