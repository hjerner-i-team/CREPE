""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

from rpyc.utils.server import ThreadedServer
from communication.hdf5_reader import HDF5Reader 
from settings import RPCPORTS, RPYC_CONFIG


def main():
    print("Startin hdf5 reader")
    h5 = HDF5Reader()
    h5.generate_random_test_stream()
    
    print("Starting threaded hdf5reader server")
    t = ThreadedServer(h5, port=RPCPORTS["HDF5Reader"], protocol_config=RPYC_CONFIG)
    t.start()
    print("After thread start")

if __name__ == "__main__":
    main()
