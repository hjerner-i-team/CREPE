""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

from multiprocessing import Process, Queue, Array as mpArray
from ctypes import c_char
import numpy as np
import time
from utils.growing_np_array import Array
from enum import Enum

class PoisonPill():
    def __init__(self):
        self.value = "POISON4269"

def is_poison_pill(data):
    if isinstance(data, PoisonPill):
        return True
    # in some instances isinstance will not return true, check therefor value
    try:
        if data.value == "POISON4269":
            return True
    except:
        pass
    return False


# Inherit from this class to gain access to queues 
class QueueService():
    # @param name is the name of the service/class, only used when printing 
    # @param **kwargs is queue arguments
    def __init__(self, name, **kwargs):
        self.name = name
        self.queue_out = None
        self.queue_in = None
        if "queue_out" in kwargs:
            self.queue_out = kwargs["queue_out"]
        if "queue_in" in kwargs:
            self.queue_in = kwargs["queue_in"]
        print("\n[CREPE.communication.QueueService.init] ", 
                "created QueueService object with \n\tname:\t", self.name, 
                "\n\tqueue_out:\t", self.queue_out, "\n\tqueue_in:\t", self.queue_in)
    
    # puts an element onto the queue_out
    # @param data is the data to put unto the queue
    def put(self, data, **kwargs):
        self.queue_out.put(data, **kwargs)

    def end(self, **kwargs):
        print("\n[QueueService.end] ", self.name, " putting PoisonPill on queue")
        self.queue_out.put(PoisonPill(), **kwargs)

    # gets the next element in queudata to put unto the queue
    # @returns whatever elem was in the queue. Most likley a 2d segment
    def get(self, **kwargs):
        data = self.queue_in.get(**kwargs)
        #print(data)
        # print("\n[QueueService.get] ", self.name, " recived PoisonPill, returning False")
        if is_poison_pill(data):
            if self.queue_out is not None:
                self.end()
            return False
        else:
            return data
    
    # empties queue and get last element or false if queue is empty
    def empty_queue_and_get_last(self):
        last_elem = False
        while True:
            try:
                d = self.get(block=False)
                last_elem = d
                if d is False:
                    break
            except queue.Empty:
                break
        return last_elem 
    
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
    # @returns a single segment concatinated from x_seg segments/items from queue
    def get_x_seg(self, x_seg):
        data = None
        for i in range(x_seg):
            new_data = self.get()
            if data is None:
                data = new_data
            else:
                data = np.concatenate((data, new_data), axis=1)
        return data
    
    #Same as get_x_elems but without slow concatenations
    def get_n_col(self, N, seg_height, seg_width):
        assert((N%seg_width) == 0)
        data = np.zeros((seg_height,N))
        for i in range(0, N, seg_width):
            seg = self.get()
            if(seg is False):
                return False
            data[:,i:i+seg_width] = seg
        return data


class StartQueueService():
    # Starts a new process that creates object and runs the run/loop function
    # @param QueueServiceChildClass is a class that inherits from QueueService
    # @param **kwargs is the variables that QueueServiceChildClass is called with 
    #   As an example: start_and_run_queue_service(ProcessData, queue_in=previous_out_queue,
    #   queue_out=a_queue)  kwargs is now {"queue_in": queueobject, "queue_out": anotherqueueobject}
    # @returns process, queue_out 
    def __init__(self, QueueServiceChildClass, **kwargs):
        
        if not "queue_out" in kwargs:
            queue_out = Queue()
            kwargs["queue_out"] = queue_out
        
        # create a shared string to get name of object, not really necesarry tho
        #self.name = Value(ctypes.c_char_p, "notaname")
        self.name = mpArray('c', 20)

        process = Process(target=self._init_and_run, 
                args=(QueueServiceChildClass, self.name, kwargs,))
        process.start()
        self.process = process
        self.queue_out = kwargs["queue_out"]

    # creates object and calls run function 
    def _init_and_run(self, QueueServiceChildClass, name, kwargs):
        obj = QueueServiceChildClass(**kwargs)
        name.value = bytes(obj.name, 'utf-8')
        obj.run() #blocking call

    def get_name(self):
        return self.name.value.decode('utf-8')

""" 

Testing code: 

"""
class GenerateData(QueueService):
    def __init__(self, **kwargs):
        QueueService.__init__(self, name="GENDATA", **kwargs)

    def run(self):
        i = 0
        while True:
            rand_data = np.random.rand(60, 100)
            rand_data = rand_data * 200
            self.put(rand_data)
            time.sleep(0.01)
            i += 1
            if i == 200:
                print("[GenerateData.run] ending")
                self.end()
                return 

class ProcessData(QueueService):
    def __init__(self, **kwargs):
        QueueService.__init__(self, name="PROCESSDATA", **kwargs)
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
                if data is False:
                    print("\n[ProcessData.run] recived poison pill, ending")
                    self.end()
                    return
                self.stream.add(data)
            processed = self.moving_average(i) 
            self.put(processed)
            size_in_bytes = processed.nbytes
            del processed
            i += 1
            #print(self.name, " index ", i, " bytes: ", size_in_bytes )
    
    def moving_average(self, start_index):
        subset = self.stream.data[:,start_index:start_index + self.mov_avg_size]
        avg = np.average(subset, axis=1)
        return avg

def main():
     
    gendata = StartQueueService(GenerateData)
    processdata = StartQueueService(ProcessData, queue_in=gendata.queue_out)
    
    #time.sleep(1)
    #print("name of processs: ", gendata.get_name() , processdata.get_name())
    
    # create a dummy QueueService
    dummy = QueueService(name="END", queue_in = gendata.queue_out)
    while True:
        d = dummy.get()
        if d is False:
            gendata.process.terminate()
            processdata.process.terminate()
            print("\n[main] ended processes, goodbye!")
            return

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
