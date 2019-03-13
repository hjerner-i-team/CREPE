""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """

import rpyc
from settings import RPCPORTS, RPYC_CONFIG
import time

# Waints for and returns a rpyc connection 
# @param port is a port defined in RPCPORT
# @returns an rpyc connection object
def get_connection(port):
    t = 0.5
    i = 0
    while True:
        if i != 1 and i % 10 == 1:
            print("... still wainting for ", port, " connection")
        try:
            conn = rpyc.connect("localhost", RPCPORTS[port], config=RPYC_CONFIG)
            print("Got the ", port, " connection! :)")
            return conn
        except:
            if i == 0:
                print("Waiting for a connection to the ", port, " server") 
            time.sleep(t)
        i += 1

