# This class is to enable other classes (preprocessing) to pull experiment data
# It can either get data directly from the live tcp connection class, or gather data from a
# experiment file .h5
import h5py
from enum import Enum

# The path to the test_data folder
path_to_test_data = "../../../test_data/"

# Enum to represent which mode the DataProxy should be in
class DataModus(Enum):
    LIVE = 1
    H5DATA = 2

# TODO: Add a way to set filename dynamicly
class DataProxy():
    def __init__(self):
        self.modus = DataModus.H5DATA
        self.stream = None
        
    def _generate_H5_stream(self): 
        _filename = "4.h5"
        f = h5py.File(path_to_test_data + _filename, 'r') 
        stream = f['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
        self.stream = list(stream)
    
    def _get_channel_data(self, _channel, _amount, _startIndex):
        if self.stream == None:
            raise ValueError("stream was not generated")
        data = self.stream[_channel][_startIndex:_startIndex + _amount]
        return data
    
    def _get_stream_dim(self):
        if self.stream == None:
            raise ValueError("stream was not generated")
        return len(self.stream), len(self.stream[0])
    
    def _get_stream_segment(self, _amount, _startIndex):
        if self.stream == None: 
            raise ValueError("stream was not generated")
        seg = [self._get_channel_data(x, _amount, _startIndex) for x in range(len(self.stream))]
        return seg
        

if __name__ == "__main__":
    d = DataProxy()
    d._generate_H5_stream()
    #    d._get_channel_data(0,100,0)
    print(d._get_stream_segment(100,0))

