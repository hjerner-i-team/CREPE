""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """

import rpyc
from settings import RPCPORTS, RPYC_CONFIG
import time


def get_stream_connection():
    t = 0.1
    i = 0
    while True:
        print("trying")
        try:
            return rpyc.connect("localhost", RPCPORTS["STREAM"], config=RPYC_CONFIG)
        except:
            time.sleep(t)
            if i > 100:
                raise ValueError("Connection could not be esthablised")
        i += 1
