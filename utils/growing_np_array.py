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
    def grow(self):
        print("growing", self.size, self.capacity)
        if self.size == self.capacity:
            self.capacity *= 4
            print("new capacity: ", self.capacity) 
            new_data = np.zeros((self.rows, self.capacity))
            print("new array: ", new_data)
            new_data[:,:self.size] = self.data
            print("after copying")
            self.data = new_data

    # add a 2d segment to the end of the array
    # @param seg is the 2d segment to add, it must have clean dimensions (all rows must have equal length)
    def add(self, seg):
        self.grow()   
        for i, row in enumerate(seg):
            for j, elem in enumerate(row):
                self.data[i][self.size + j] = elem
        
        self.size += len(seg[0])
    
    # when using len(stream_object) this will be called
    def __len__(self):
        return self.size
