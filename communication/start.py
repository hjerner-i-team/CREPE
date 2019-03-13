""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

from rpyc.utils.server import ThreadedServer
from communication.hdf5_reader import HDF5Reader 
from settings import RPCPORTS, RPYC_CONFIG

def main(data_file_path=None):
    if data_file_path == None:
        print("Starting stream")
        print("Error, stream is not implemented yet")
    else:
        print("Starting hdf5 reader server on file: ", data_file_path)
        h5 = HDF5Reader( data_file_path )
        if data_file_path == "__TESTING":
            h5.generate_random_test_stream()

        t = ThreadedServer(h5, port=RPCPORTS["STREAM"], protocol_config=RPYC_CONFIG)
        t.start()
        print("After thread start")

if __name__ == "__main__":
    main()
