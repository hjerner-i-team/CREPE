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

from crepe_modus import CrepeModus


# reads from a hdf5 file and puts it unto the queue, or generates a random test stream and outputs it to the queue
class HDF5Reader(QueueService):
    def __init__(self, queue_out=None, file_path=None, mode=CrepeModus.FILE):
        QueueService.__init__(self, name="HDF5READER", queue_out=queue_out)
        self.file_path = file_path
        self.mode = mode

    # Generates a 2d numpy array from a .h5 file to self.stream
    def generate_H5_stream(self): 
        print("\n[CREPE.commnication.hdf5_reader.generate_H5_stream] \n\tusing .h5 file: ",
                self.file_path)
        # open the file with h5py
        f = h5py.File(self.file_path, 'r') 
        # navigate to where the raw data is in the .h5 file
        # Use the program hdfviewer or check our upcomming documentation for full .h5 format
        data = f['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
        #put the data unto the queue 
        for i in range(100, len(data[0]) + 1, 100):
            self.put(data[:, i - 100:i])
        # if the data is not dividable by 100, add the remaning
        remaining = data[:, len(data) - i % 100:len(data)]
        self.put(remaining)
        print("\n[CREPE.communication.hdf5_reader.generate_H5_stream] ", 
                "all hdf5 data pushed to stream")
        # after all data is sent, send poison pill 
        self.end()
        f.close()

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
        if self.mode == CrepeModus.FILE:
            self.generate_H5_stream()
        elif self.mode == CrepeModus.LIVE:
            i = 0
            while True:
                seg = self._generate_random_test_segment_list(100)
                self.put(seg)
                i += 1
                time.sleep(0.005)
                if i == 600:
                    print("\n[CREPE.hdf5_reader.run (LIVE)] finished generated ", 
                            i * 100, " row elements")
                    self.end()
                    return


if __name__ == "__main__":
    #h = HDF5Reader()
    # h.generate_H5_stream()
    file_path = sys.path[0] + "/../test_data/4.h5"
    hdf5 = StartQueueService(HDF5Reader, file_path=file_path, mode=CrepeModus.FILE)
    dummy = QueueService(name="END", queue_in=hdf5.queue_out)
    i = 0
    while True:
        d = dummy.get()
        if d is False:
            hdf5.process.terminate()
            print("\n[HDF5 main] recived ", i, " elements per row")
            print("\n[HDF5 main] terminated processes")
            exit()
        i += len(d[0])

