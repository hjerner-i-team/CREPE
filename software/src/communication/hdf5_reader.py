""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("software/src")+len("software/src")])
""" End import fix """

from stream_service import StreamService, DataModus

import h5py
import numpy as np

# The path to the test_data folder. sys.path[0] is the src folder
path_to_test_data = sys.path[0][0:-1 * len("/software/src")] + "/test_data/"
print(path_to_test_data)

class HDF5Reader(StreamService):

    def __init__(self, _filename="4.h5"):
        StreamService.__init__(self, DataModus.DATA)
        self.filename = _filename

    # Generates a 2d numpy array from a .h5 file to self.stream
    # @dev TODO implement dynamic filesnames or something
    def generate_H5_stream(self): 
        # open the file with h5py
        f = h5py.File(path_to_test_data + self.filename, 'r') 
        # navigate to where the raw data is in the .h5 file
        # Use the program hdfviewer or check our upcomming documentation for full .h5 format
        stream = f['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
        # this will return a h5py object so we convert it to a list
        self.stream = list(stream)

    # Generates a 2d matrice with random numbers to self.stream for testing purposes
    def generate_random_test_stream(self):
        # check that stream is empty
        if self.stream != None: 
            raise RuntimeError("Stream was not empty")

        # generate a 2d numpy matrice of random values between 0 & 1
        rand_data = np.random.rand(59,1000)
        # multiply it by 200 to "simulate" real data
        rand_data = rand_data * 200
        
        # set it as the current stream
        self.stream = rand_data 

if __name__ == "__main__":
    h = HDF5Reader()
    h.generate_H5_stream()
    print(h.stream)
