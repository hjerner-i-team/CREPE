""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("software/src")+len("software/src")])
""" End import fix """

from stream_service import StreamService, DataModus 
import rpyc
from settings import RPCPORTS, RPYC_CONFIG
import numpy

class ReadoutLayer(StreamService):
    
    def __init__(self):
        StreamService.__init__(self, DataModus.RESULT)
        self.conn = None

    def make_connection(self):
        c = rpyc.connect("localhost", RPCPORTS["HDF5Reader"], config=RPYC_CONFIG)     
        self.conn = c
        print("Connection made: ", c)
        self.pull_1_segment()
    
    def callback_print(self, data):
        print("In callback print: ", data)

    def pull_1_segment(self):
        data = self.conn.root.get_stream_segment(1, 0, self.callback_print)
        print("In pull_1_segment: ", len(data))
        self.append_stream_segment_data(data)
        print(self.stream)

def main():
    print("Readoutlayer example start")
    r = ReadoutLayer()
    r.make_connection()

