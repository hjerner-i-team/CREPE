"""
 This file is meant to be inherited such that a class can expose a stream trough RPC
 to other components in this project
"""

import rpyc
from enum import Enum
import numpy as np

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

    # Appends new data to row
    # @param _row is one of the channels in self.stream
    # @param _new_data is either an array containing new data or a single value
    def append_stream_row_data(self, _row, _new_data):
        # check if variable is single value or array
        if isinstance(_new_data, list): 
            self.stream[_row] += _new_data
        else:
            self.stream[_row].append(_new_data)

    # Appends segment to stream
    # @param _new_data is either a 1D array with new values for each channel, or a 2d array
    #   with a list of new values for each channel. To not append to a channel send None or an
    #   empty list for that particular channel.
    def append_stream_segment_data(self, _new_data):
        # check that _new_data matches the stream
        if not (len(self.stream) == len(_new_data)):
            raise ValueError("New data was not of correct dimensions")
        # Add the new data to stream
        for i in range(len(_new_data)):
            if not (_new_data[i] == None or not _new_data[i]):
                self.append_stream_row_data(i, _new_data[i])

    # Function to check attribute values and calculate the rigth end index
    # @param _row One of channels in self.stream
    # @param _range The range we wish to read
    # @param _startIndex The starting index to begin reading from on the channel
    # @returns endIndex Either False or _startIndex < endIndex < length of channel 
    def _safe_row_segment_range(self, _row, _range, _startIndex):
        # check if you called a channel that exists
        if(_row >= len(self.stream)): 
            raise AttributeError("_row was out of range with regards to the stream")
        
        # check if we can read from stream and if so, how much
        if _startIndex >= len(self.stream[_row]):
            # There is no more data to return
            return False
        elif _startIndex + _range >= len(self.stream[_row]):
            # There is more data, but not the full range. 
            # Return the index at the end of the stream
            return len(self.stream[_row])
        else:
            # Normal case, return the end index with maximum range
            return _startIndex + _range
    
    # Get a subset of a channels data
    # @notice Exposed to RPC
    # @param _row One of channels in self.stream
    # @param _range The range we wish to read
    # @param _startIndex The starting index to begin reading from on the channel
    def exposed_get_row_segment(self, _row, _range, _startIndex):
        self._raiseErrorOnNullStream()
        endIndex = self._safe_row_segment_range(_row, _range, _startIndex)
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
    # @param _range The range we wish to read
    # @param _startIndex The starting index to begin reading from
    # @returns a segmented 2d array where each row has equal dimensions or False
    def exposed_get_stream_segment(self, _range, _startIndex):
        self._raiseErrorOnNullStream()

        """ Example: 
        Original stream: 
        [
            [ 66, 77, 88, 99],
            [ 44, 33, 22, 11]
        ]
        Segmented with for examle _range=2, and _startIndex=1
        [
            [ 77, 88],
            [ 33, 22]
        ]

        """
        
        # Generate a new array, where each row is a subset of the corresponding channel
        seg = [self.exposed_get_row_segment(x, _range, _startIndex)
                for x in range(len(self.stream))]
        
        # make sure that the segment is complete by checking that none is false
        if not all(x != False for x in seg):
            return False

        # check if dimensions are correct/clean
        lens = [len(row) for row in seg]
        if not all(l == lens[0] for l in lens):
            # now we must find the shortest dimension and cut the entire segment to that length
            smallest = min(lens)
            seg = [row[0:smallest] for row in seg]

        return seg

# Iterates over a row in the stream.
class StreamRowIterator():
    
    # @param _channel is the row id. 
    # @param _range is the number of elements to return on each iteration
    def __init__(self, _channel=0, _range = 100):
        self.index = 0
        self.channel = _channel
        self.range = _range

    # gets the next set of data from the stream
    # @param _conn is the rpc connection object
    def next(self, _conn): 
        # Get data from rpc
        row_segment = _conn.root.get_row_segment(self.channel, self.range, self.index)
        
        # Check that we got data
        if not row_segment:
            return False

        # Increase the iteration index
        self.index += len(row_segment)

        return row_segment

# Iterates over segments in the stream
class StreamSegmentIterator(): 

    # @param _range is the number of elements to return on each iteration
    def __init__(self, _range = 100):
        self.index = 0
        self.range = _range

    # gets the next set of data from the stream
    # @param _conn is the rpc connection object
    # @returns 2D stream segment with row length 1 < x < self.range or False
    def next(self, _conn): 
        # Get data from rpc
        stream_segment = _conn.root.get_stream_segment(self.channel, self.range, self.index)
        
        # Check that we got data
        if not stream_segment:
            return False

        # Increase the iteration index
        self.index += len(stream_segment[0])

        return stream_segment

"""

DEBUG CODE:

"""


# A small test to check and debug DataProxyService 
# @dev Raises RuntimeError if test does not pass
def dataProxyTester(dp):
    # check _safe_row_segment_range
    # Normal case:
    endIndex = dp._safe_row_segment_range(0,100,0)
    if endIndex != 100:
        raise RuntimeError()
    # not the full range of data
    endIndex = dp._safe_row_segment_range(0,100,930)
    if endIndex != 1000:
        raise RuntimeError()
    # no data left
    endIndex = dp._safe_row_segment_range(0,100,1000)
    if endIndex != False:
        raise RuntimeError()

if __name__ == "__main__":
    d = StreamService()
    dataProxyTester(d)
