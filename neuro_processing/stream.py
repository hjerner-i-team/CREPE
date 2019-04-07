import numpy as np
import sys

#Growing numpy array for storing
class Stream():
    def __init__(self,n_rows,n_cols):
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.size = 0
        self.data = np.zeros((self.n_rows,self.n_cols)) 
        self.final_index = sys.maxsize
        
    def append_segment(self, segment):
        if self.size == self.n_cols:
            self.n_cols *= 4
            newdata = np.zeros((self.n_rows, self.n_cols))
            newdata[:,:self.size] = self.data[:,:]
            self.data = newdata 

        assert(segment.shape[0] == self.n_rows)
        segment_len = segment.shape[1] 
        self.data[:, self.size : self.size+segment_len] = segment
        self.size += segment_len
        
    def append_collumn(self, col):
        if self.size == self.n_cols:
            self.n_cols *= 4
            newdata = np.zeros((self.n_rows, self.n_cols))
            newdata[:,:self.size] = self.data[:,:]
            self.data = newdata 

        assert(col.shape[0] == self.n_rows)
        self.data[:, self.size : self.size+1] = col.reshape((60,1))
        self.size += 1

    def close(self):
        self.final_index = self.size
