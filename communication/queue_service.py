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

# Inherit from this class to gain access to queues 
class QueueService():
    # @param name is the name of the service/class, only used when printing 
    # @param queue_out is the queue to (out)put data to
    # @param queue_in is the queue to get data from
    def __init__(self, name, queue_out=None, queue_in=None):
        self.name = name
        self.queue_out = queue_out
        self.queue_in = queue_in
        print("[CREPE.stream_service.QueueService] object with name:\t", name, 
                "\tqueue_out:\t", queue_out, "\tqueue_in:\t", queue_in)
        

    # puts an element onto the queue_out
    # @param data is the data to put unto the queue
    def put(self, data):
        self.queue_out.put(data)

    # gets the next element in queudata to put unto the queue
    # @returns whatever elem was in the queue. Most likley a 2d segment
    def get(self):
        return self.queue_in.get()

    # Get at least x number of columns from queue
    # @param x_elems is the minimum number of columns to get
    # @returns a single segment with shape (rows, x_elems or more) 
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
    
    # get x numer of segments / items from queue. 
    # @param x_seg is the number of times to call .get()
    # @returns a single segment concatinaed from x_seg segments/items from queue
    def get_x_seg(self, x_seg):
        data = None
        for i in range(x_seg):
            new_data = self.get()
            if data is None:
                data = new_data
            else:
                data = np.concatenate((data, new_data), axis=1)
        return data

# Starts a new process that creates object and runs the run/loop function
# @param QueueServiceChildClass is a class that inherits from QueueService
# @param **kwargs is the variables that QueueServiceChildClass is called with 
#   As an example: start_and_run_queue_service(ProcessData, queue_in=previous_out_queue,
#   queue_out=a_queue)  kwargs is now {"queue_in": queueobject, "queue_out": anotherqueueobject}
# @returns process, queue_out 
def start_and_run_queue_service(QueueServiceChildClass, **kwargs):
    # creates object and calls run function 
    def _init_and_run(QueueServiceChildClass, kwargs):
        obj = QueueServiceChildClass(**kwargs)
        obj.run() #blocking call
    
    if not "queue_out" in kwargs:
        queue_out = Queue()
        kwargs["queue_out"] = queue_out
    process = Process(target=_init_and_run, args=(QueueServiceChildClass,kwargs,))
    process.start()
    return process, queue_out


""" 

Testing code: 

"""
class GenerateData(QueueService):
    def __init__(self, queue_out):
        QueueService.__init__(self, name="GENDATA", queue_out=queue_out)

    def run(self):
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

    def run(self):
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

def main():
    
    gendata_process, gendata_out = start_and_run_queue_service(GenerateData)
    processdata_process, processdata_out = start_and_run_queue_service(ProcessData, queue_in=gendata_out)
    
    while True:
        pass

if __name__ == "__main__":
    main()


""" Alternative way: 

def generate_data(queue_out):
    gen_data = GenerateData(queue_out)
    gen_data.run()
    print("after gen loop")

def process_data(queue_out, queue_in):
    process_data = ProcessData(queue_out, queue_in)
    process_data.run()
    print("after pro loop")

gen_data_queue = Queue()
gen_data_process = Process(target=generate_data, args=(gen_data_queue,))
gen_data_process.start()

pro_data_queue = Queue()
pro_data_process = Process(target=process_data, args=(pro_data_queue, gen_data_queue))
pro_data_process.start()
"""
