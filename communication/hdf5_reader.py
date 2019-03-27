""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

from communication.stream_service import StreamService, DataModus
from settings import DEFAULT_STREAM_DIMENSION
import time
import random

import h5py
import numpy as np

# The path to the test_data folder. sys.path[0] is the src folder
path_to_test_data = sys.path[0][0:-1 * len("/CREPE")] + "/test_data/"

class HDF5Reader(StreamService):

    def __init__(self, name, port, file_path="4.h5"):
        StreamService.__init__(self, name, port, DataModus.DATA)
        self.file_path = file_path

    # Generates a 2d numpy array from a .h5 file to self.stream
    def generate_H5_stream(self): 
        print("[CREPE.commnication.hdf5_reader] Generating stream from h5 file: ", self.file_path)
        # open the file with h5py
        f = h5py.File(self.file_path, 'r') 
        # navigate to where the raw data is in the .h5 file
        # Use the program hdfviewer or check our upcomming documentation for full .h5 format
        data = f['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
        # this will return a h5py object so we convert it to a list
        self.append_stream_segment_data(list(data))
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
        print(rand_data)
        return rand_data
        

    def start(self):
        #print("DebugPre ", self)
        self.start_loop(self.loop)

    def loop(self):
        while True:
            seg = self._generate_random_test_segment_list(100)
            self.append_stream_segment_data(seg)
            # sleep for 0.5 seconds
            #time.sleep(0.5)
    




if __name__ == "__main__":
    h = HDF5Reader()
    h.generate_H5_stream()
    print(h.stream)
