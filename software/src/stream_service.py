"""
 This file is meant to be inherited such that a class can expose a stream trough RPC
 to other components in this project
"""

import h5py
import rpyc
from enum import Enum
import numpy as np

# The path to the test_data folder
path_to_test_data = "../../test_data/"

# WARNING The following enum is not currently usefull. 
# Enum to represent which mode the DataProxy should be in
class DataModus(Enum):
    DATA = 1
    RESULT = 2
    TESTING = 3

# A class that stores a stream of data, implements data gathering functions and exposes it to RPC
# @dev Should be inherited by processes who wish to share data. 
# @dev Currently it generates a random "stream" with the dimensions 59,1000 for testing purposes
# @dev Data is exposed trough a "pull" scheme. Call the exposed functions to get data
class StreamService(rpyc.Service): 
    def __init__(self, _dataModus=DataModus.TESTING):
        # Check if the enum atribute is an enum of type DataModus
        if not isinstance(_dataModus, DataModus):
            raise ValueError("Did not recive an DataModus enum")
        self.modus = _dataModus
        
        self.stream = None 
        
        # If the modus is set to testing then generate test data
        if _dataModus == DataModus.TESTING:
            self.generate_random_test_stream()

    # Raises error if self.stream is empty / not initialized
    def _raiseErrorOnNullStream(self):
        if self.stream is None:
            raise RuntimeError("stream was not generated")
    
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

    # Generates a 2d numpy array from a .h5 file to self.stream
    # @dev TODO implement dynamic filesnames or something
    def generate_H5_stream(self): 
        _filename = "4.h5"
        # open the file with h5py
        f = h5py.File(path_to_test_data + _filename, 'r') 
        # navigate to where the raw data is in the .h5 file
        # Use the program hdfviewer or check our upcomming documentation for full .h5 format
        stream = f['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
        # this will return a h5py object so we convert it to a list
        self.stream = list(stream)
    
    # Function to check attribute values and calculate the rigth end index
    # @param _row One of channels in self.stream
    # @param _amount The range we wish to read
    # @param _startIndex The starting index to begin reading from on the channel
    # @returns endIndex Either False or _startIndex < endIndex < length of channel 
    def _safe_row_data_range(self, _row, _amount, _startIndex):
        # check if you called a channel that exists
        if(_row >= len(self.stream)): 
            raise AttributeError("_row was out of range with regards to the stream")
        
        # check if we can read from stream and if so, how much
        if _startIndex >= len(self.stream[_row]):
            # There is no more data to return
            return False
        elif _startIndex + _amount >= len(self.stream[_row]):
            # There is more data, but not the full amount. 
            # Return the index at the end of the stream
            return len(self.stream[_row])
        else:
            # Normal case, return the end index with maximum range
            return _startIndex + _amount
    
    # Get a subset of a channels data
    # @notice Exposed to RPC
    # @param _row One of channels in self.stream
    # @param _amount The range we wish to read
    # @param _startIndex The starting index to begin reading from on the channel
    def exposed_get_row_data(self, _row, _amount, _startIndex):
        self._raiseErrorOnNullStream()
        endIndex = self._safe_row_data_range(_row, _amount, _startIndex)
        if not endIndex:
            return False
        data = self.stream[_row][_startIndex:endIndex]
        return data

    # Get the dimensions of self.stream
    # @notice Exposed to RPC
    def exposed_get_stream_dimensions(self):
        self._raiseErrorOnNullStream()
        return len(self.stream), len(self.stream[0])
    
    # Get a segment of the stream (all channels)
    # @notice Exposed to RPC 
    # @param _amount The range we wish to read
    # @param _startIndex The starting index to begin reading from
    def exposed_get_stream_segment(self, _amount, _startIndex):
        self._raiseErrorOnNullStream()

        """ Example: 
        Original stream: 
        [
            [ 66, 77, 88, 99],
            [ 44, 33, 22, 11]
        ]
        Segmented with for examle _amount=2, and _startIndex=1
        [
            [ 77, 88],
            [ 33, 22]
        ]

        """
        
        # Generate a new array, where each row is a subset of the corresponding channel
        seg = [self.exposed_get_row_data(x, _amount, _startIndex)
                for x in range(len(self.stream))]

        return seg


"""

DEBUG CODE:

"""


# A small test to check and debug DataProxyService 
# @dev Raises RuntimeError if test does not pass
def dataProxyTester(dp):
    # check _safe_row_data_range
    # Normal case:
    endIndex = dp._safe_row_data_range(0,100,0)
    if endIndex != 100:
        raise RuntimeError()
    # not the full amount of data
    endIndex = dp._safe_row_data_range(0,100,930)
    if endIndex != 1000:
        raise RuntimeError()
    # no data left
    endIndex = dp._safe_row_data_range(0,100,1000)
    if endIndex != False:
        raise RuntimeError()

if __name__ == "__main__":
    d = DataProxyService()
    dataProxyTester(d)
