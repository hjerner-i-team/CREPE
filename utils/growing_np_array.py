""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

import numpy as np

# A dynamicly growing np array
class Array():
    # creates a zeroed 2d np array with dim (rows, maxsize)
    # @param rows is the number of rows
    # @param max_size is the initial collum size. 
    def __init__(self, rows, max_size):
        self.rows = rows
        self.data = np.zeros((rows, max_size))
        self.capacity = max_size
        self.size = 0

    # if the current array is full, then it creates a new one with 4 times the capacity and copies all the elements.
    def grow(self, new_data_size=0):
        if self.size + new_data_size >= self.capacity:
            new_data = np.zeros((self.rows, self.capacity * 3))
            self.capacity *= 4
            print("\n[CREPE.utils.growing_np_array] growing, current size:\t", self.size, 
                    "\tnew capacity:\t", self.capacity)
   
            #new_data[:,:self.size] = self.data
            #np.copyto(new_data, self.data)
            #multiple ways to create a new array with old data was researched and we found out that hstack works best
            self.data = np.hstack((self.data, new_data))

    # add a 2d segment to the end of the array
    # @param seg is the 2d segment to add, it must have clean dimensions (all rows must have equal length)
    def add(self, seg):
        self.grow(new_data_size=len(seg[0]))   
        for i, row in enumerate(seg):
            for j, elem in enumerate(row):
                self.data[i][self.size + j] = elem
        
        self.size += len(seg[0])
    
    # when using len(stream_object) this will be called
    def __len__(self):
        return self.size
