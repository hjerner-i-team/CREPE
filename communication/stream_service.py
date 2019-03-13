"""
 This file is meant to be inherited such that a class can expose a stream trough RPC
 to other components in this project
"""

import rpyc
from enum import Enum
import numpy as np
from settings import STREAM_DIMENSION
import time

# WARNING The following enum is not currently usefull. 
# Enum to represent which mode the DataProxy should be in
class DataModus(Enum):
    DATA = 1
    RESULT = 2
    TESTING = 3

class Callback():
    def __init__(self, _streamService, _callback, _range, _startIndex, _row=None):
        self.streamService = _streamService
        self.callback = _callback
        self.range = _range
        self.startIndex = _startIndex
        self.row = _row

    def __call__(self):
        # if row is None then call stream_segment if not then call row_segment
        if self.row == None:
            data = self.streamService.get_stream_segment(self.range, self.startIndex)
            self.callback(data)
        else:
            data = self.streamService.get_row_segment(self.row, self.range, self.startIndex)
            self.callback(data)


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
        
        # The stream array that will contain the data
        # If DataModus.DATA it will be 2d
        # Else if DataModus.RESULT it will be 1d
        # TODO add settings for dimensions
        self.stream = [[] for x in range(0, STREAM_DIMENSION)]

        # Callback functions array
        self._row_segment_callbacks = []
        self._streams_segment_callbacks = []

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
        if all([ len(x) != 0 for x in self.stream ]):
            raise RuntimeError("Stream was not empty")

        # generate a 2d numpy matrice of random values between 0 & 1
        rand_data = np.random.rand(59,1000)
        # multiply it by 200 to "simulate" real data
        rand_data = rand_data * 200
        
        # set it as the current stream
        self.append_stream_segment_data(rand_data) 

    def _call_all(self, _arrayOfFunctions):
        for i in range(len(_arrayOfFunctions)):
            _arrayOfFunctions[i]()

    def _update_callbacks(self, _row=None):
        # If row is None then this is a segment updating callback
        if _row == None:
            # Call all wainting callbacks
            self._call_all(self._streams_segment_callbacks)
            # Reset the callback array
            self._streams_segment_callbacks = []
        else:
            # find the callbacks who corespond to _row
            rowcallbacks = [ x for x in self._row_segment_callbacks if x.row == _row ] 
            # call all
            self._call_all(rowcallbacks) 
            # Delete all rowcallbacks elements from self._row_segment_callbacks
            self._row_segment_callbacks =list(set(self._row_segment_callbacks) - set(rowcallbacks))

    # An extension of append_stream_row_data
    def _append_stream_row_data_without_updating_callbacks(self, _row, _new_data):
        # check if variable is single value, array or a numpy object
        if isinstance(_new_data, list): 
            self.stream[_row] += _new_data
        elif isinstance(_new_data, np.ndarray):
            self.stream[_row] = np.append(self.stream[_row], _new_data)
        else:
            self.stream[_row].append(_new_data)

    # Appends new data to row
    # @param _row is one of the channels in self.stream
    # @param _new_data is either an array containing new data or a single value
    def append_stream_row_data(self, _row, _new_data):
        self._append_stream_row_data_without_updating_callbacks(_row, _new_data) 
        self._update_callbacks(_row)

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
            if len(_new_data[i]) > 0:
                self._append_stream_row_data_without_updating_callbacks(i, _new_data[i])
        self._update_callbacks()

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
    # @notice will be called by exposed function
    # @param _row One of channels in self.stream
    # @param _range The range we wish to read
    # @param _startIndex The starting index to begin reading from on the channel
    def get_row_segment(self, _row, _range, _startIndex):
        self._raiseErrorOnNullStream()
        endIndex = self._safe_row_segment_range(_row, _range, _startIndex)
        if not endIndex:
            return False
        data = self.stream[_row][_startIndex:endIndex]
        return data

    
    # Get a segment of the stream (all channels)
    # @notice will be called by exposed functions
    # @param _range The range we wish to read
    # @param _startIndex The starting index to begin reading from
    # @returns a segmented 2d array where each row has equal dimensions or False
    def get_stream_segment(self, _range, _startIndex):
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
        seg = [self.get_row_segment(x, _range, _startIndex)
                for x in range(len(self.stream))]
        
        # make sure that the segment is complete by checking that none is false
        if not all(x is not False for x in seg):
            return False

        # check if dimensions are correct/clean
        lens = [len(row) for row in seg]
        if not all(l == lens[0] for l in lens):
            # now we must find the shortest dimension and cut the entire segment to that length
            smallest = min(lens)
            seg = [row[0:smallest] for row in seg]
        return seg

    # Get a subset of a channels data
    # @notice Exposed to RPC
    # @param _row One of channels in self.stream
    # @param _range The range we wish to read
    # @param _startIndex The starting index to begin reading from on the channel
    # @param _callback is the func to call when data is ready, if it is not ready now.  
    # @returns a segmented 1d array or False
    def exposed_get_row_segment(self, _row, _range, _startIndex, _callback=None):
        data = self.get_row_segment(_row, _range, _startIndex)
        # check if we got a false value
        if data is False:
            if _callback == None:
                return False
            # Make a callback object
            cb = Callback(self, _callback, _range, _startIndex, _row)
            # Append to callbacks array to send data later
            self._row_segment_callbacks.append(cb)
            return False

        return data


    # Get a segment of the stream (all channels)
    # @notice Exposed to RPC 
    # @param _range The range we wish to read
    # @param _startIndex The starting index to begin reading from
    # @param _callback is the func to call when data is ready, if it is not ready now.  
    # @returns a segmented 2d array where each row has equal dimensions or False
    def exposed_get_stream_segment(self, _range, _startIndex, _callback=None):
        data = self.get_stream_segment(_range, _startIndex)
        
        # check if we got a false value
        if data is False:
            if _callback == None:
                return False
            # Make a callback object
            cb = Callback(self, _callback, _range, _startIndex)
            # Append to callbacks array to send data later
            self._streams_segment_callbacks.append(cb)
            return False

        return data

    def testgetstream(self,_range, _startIndex, _callback):
        return self.exposed_get_stream_segment(_range, _startIndex, _callback)

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
        if row_segment is False:
            return False

        # Increase the iteration index
        self.index += len(row_segment)

        return row_segment
    
    # gets the next set of data from the stream or waints for the the next set
    # @param _conn is the rpc connection object
    # @param sleep is the amount of seconds between calls
    # @param timeout is the amount of x * sleep seconds with no data we can recive before returning False.
    def next_or_wait(self, conn, sleep = 0.1, timeout = None):
        i = 0
        while True:
            i += 1
            row = self.next(conn)
            if row is not False:
                return row
            else:
                time.sleep(sleep)
                if timeout != None and i > timeout:
                    break
        return False

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
        stream_segment = _conn.root.get_stream_segment(self.range, self.index)
        
        # Check that we got data
        if stream_segment is False:
            return False

        # Increase the iteration index
        self.index += len(stream_segment[0])

        return stream_segment

    # gets the next set of data from the stream or waints for the the next set
    # @param _conn is the rpc connection object
    # @param sleep is the amount of seconds between calls
    # @param timeout is the amount of x * sleep seconds with no data we can recive before returning False.
    def next_or_wait(self, conn, sleep = 0.1, timeout = None):
        i = 0
        while True:
            i += 1
            seg = self.next(conn)
            if seg is not False:
                return seg
            else:
                time.sleep(sleep)
                if timeout != None and i > timeout:
                    break
        return False
"""

DEBUG CODE:

"""

def callbacktester(self, data):
    print("in callbacktester: \n", self, "\n", data)

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

    # Check callback things
    streamService = StreamService(DataModus.DATA)
    
    res = streamService.testgetstream(2, 0, callbacktester)
    print(res)
    if res != False:
        raise RuntimeError()


    print("If not \"in callbacktester:\" was printed then error")




if __name__ == "__main__":
    d = StreamService()
    dataProxyTester(d)
