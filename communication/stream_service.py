""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

from multiprocessing import Process, Queue
import numpy as np
import time
from utils.growing_np_array import Array
from enum import Enum

"""
class Stream(Array):
    def __init__(self, rows): 
        print("[CREPE.stream_service.StreamService.init] ", self.name, 
                " created array of size (", rows,", 1000)")
        Array.__init__(rows, 1000)

    # TODO add check for equal seg dim
    def append_segment(self, seg):
        self.data.add(seg)
"""

class QueueService():
    def __init__(self, name, queue_out=None, queue_in=None):
        self.name = name
        
        print("[CREPE.stream_service.QueueService] object with name:\t", name, 
                "\tqueue_out:\t", queue_out, "\tqueue_in:\t", queue_in)
        
        self.queue_out = queue_out
        self.queue_in = queue_in

    def put(self, seg):
        self.queue_out.put(seg)

    def get(self):
        return self.queue_in.get()

    def get_x_elems(self, x_elems):
        tmp = 0
        data = None
        while True:
            new_data = self.get()
            if data is None:
                data = new_data
            else:
                data = np.concatenate((data, new_data), axis=1)
            tmp += len(new_data[0])
            if tmp >= x_elems:
                break
        return data
    
    def get_x_seg(self, x_seg):
        data = None
        for i in range(x_seg):
            new_data = self.get()
            if data is None:
                data = new_data
            else:
                data = np.concatenate((data, new_data), axis=1)
        return data

""" 

Testing code: 

"""
class GenerateData(QueueService):
    def __init__(self, queue_out):
        QueueService.__init__(self, name="GENDATA", queue_out=queue_out, queue_in=None)

    def loop(self):
        while True:
            rand_data = np.random.rand(60, 100)
            rand_data = rand_data * 200
            self.put(rand_data)
            time.sleep(0.01)

class ProcessData(QueueService):
    def __init__(self, queue_out, queue_in):
        QueueService.__init__(self, name="PROCESSDATA" , queue_out=queue_out, queue_in=queue_in)
        # we need at least 1000 elems before we can start to preprocess
        self.mov_avg_size = 1000
        
        self.stream = Array(60, self.mov_avg_size * 2)

        data = self.get_x_elems(x_elems=self.mov_avg_size)
        self.stream.add(data)

    def loop(self):
        i = 0
        while True:
            # get next segment if needed
            #print(self.name, " capacity of stream: ", self.stream.capacity, " len: ", len(self.stream))
            if (i + self.mov_avg_size >= len(self.stream)):
                data = self.get()
                self.stream.add(data)
            processed = self.moving_average(i) 
            self.put(processed)
            size_in_bytes = processed.nbytes
            del processed
            i += 1
            print(self.name, " index ", i, " bytes: ", size_in_bytes )
    
    def moving_average(self, start_index):
        subset = self.stream.data[:,start_index:start_index + self.mov_avg_size]
        avg = np.average(subset, axis=1)
        return avg
def generate_data(queue_out):
    gen_data = GenerateData(queue_out)
    gen_data.loop()
    print("after gen loop")

def process_data(queue_out, queue_in):
    process_data = ProcessData(queue_out, queue_in)
    process_data.loop()
    print("after pro loop")

def main():
    gen_data_queue = Queue()
    gen_data_process = Process(target=generate_data, args=(gen_data_queue,))
    gen_data_process.start()

    pro_data_queue = Queue()
    pro_data_process = Process(target=process_data, args=(pro_data_queue, gen_data_queue))
    pro_data_process.start()

    while True:
        pass
        #data = pro_data_queue.get()
        #print("Average: ", data)
if __name__ == "__main__":
    main()
