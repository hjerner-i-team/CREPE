import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """
import socket
import struct
import numpy as np
import h5py
import os
import json
import time
import requests
from neuro_processing.stream import Stream
from communication.queue_service import QueueService


class MeameListener(QueueService):

    def send_start(self):
        r = requests.get(self.url + '/DAQ/start')
        print(r)

    def send_config(self):
        print("Sending config to {}".format(self.url))
        conf = { 'samplerate' : self.bitrate , 'segmentLength' : self.segment_len }
        r = 0
        try:
            r = requests.post(self.url+'/DAQ/connect', data=json.dumps(conf)).status_code
        except:
            pass 

        return r

    def savechunk(self, dset, chunk):
        N = chunk.shape[1]
        dset.resize(dset.shape[1]+N, axis=1)
        dset[:,-N:] = chunk

    def recvchunk(self, sock, chunklen):
        data = b''
        while(len(data)<chunklen):
            packet = sock.recv(chunklen - len(data))
            if not packet:
                if(len(data) > 0):
                    print("Incomplete segment recieved")
                return None
            data+=packet
        return data

    def __init__(self, server_address, port, bitrate  = 10000, segment_len = 100, record = False, **kwargs ):
        QueueService.__init__(self, name="MEAMELISTENER" , **kwargs)

        self.record_data = record
        self.file_path = ''
        
        self.server_address = server_address
        self.port = port
        self.url = 'http://' + server_address + ':8888'

        self.bitrate  = bitrate 
        self.segment_len = segment_len

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #Connects to the Meame server and recieves outputstream of DAQ. If record data is true, data recieved is dumped to a HDF5 file
    def run(self):
        chunk_dim = (60,self.segment_len)
        chunk_len = chunk_dim[0] * chunk_dim[1] * 4
        print("segment len: {}".format(chunk_len))

#        if(self.server_address != "127.0.0.1"):
#            r = self.send_config()
#            if(r != 200):
#                print("Meame server not online")
#                self.end()
#                return
#            self.send_start()
#            print("Config sent")
#            time.sleep(1)


        self.sock.connect((self.server_address, self.port))
        print("Connected")

        n_chunks = 0
        if self.record_data == False:
            while (1):
                data = self.recvchunk(self.sock, chunk_len)
                if not data:
                    break

                data = struct.unpack("<6000i", data)
                chunk = np.asarray(data, dtype=np.int).reshape(chunk_dim)

                self.put(chunk)
                n_chunks += 1
                #print("Segments recieved: {}".format(n_chunks))
    
            self.end()
            print("Connection closed. Recieved {} chunks".format(n_chunks))

        else:
            i = 0

            if file_path == '':
                filename = "recordings/recording{}.hdf5".format(i)
                while (os.path.exists(filename)):
                    i += 1
                    filename = "recordings/recording{}.hdf5".format(i)
            else:
                filename = file_path

            with h5py.File(filename, "w") as f:
                print("Recording to file {}".format(filename))
                dset = f.create_dataset("data", (chunk_dim[0], 0), dtype='i', maxshape=(60, None), chunks=chunk_dim)
                dset.attrs.__setitem__("Starttime", time.localtime())
                dset.attrs.__setitem__("Bitrate", self.bitrate )

                while (1):
                    data = self.recvchunk(self.sock, chunk_len)
                    if not data:
                        break

                    data = struct.unpack("<6000i",data)
                    chunk = np.asarray(data, dtype=np.int).reshape(chunk_dim)

                    self.savechunk(dset,chunk)
                    self.put(chunk)
                    n_chunks+=1

                self.end()
                print("Connection closed. Recieved {} chunks".format(n_chunks))

