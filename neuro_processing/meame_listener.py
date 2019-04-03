import socket
import struct
import numpy as np
import h5py
import os
import json
import time
import requests
from neuro_processing.stream import Stream


class MeameListener():

    def send_start(self):
        r = requests.get(self.url + '/DAQ/start')
        print(r)

    def send_config(self):
        conf = { 'samplerate' : self.bitrate , 'segmentLength' : self.segment_len }
        r = requests.post(self.url+'/DAQ/connect', data=json.dumps(conf))
        print(r)

    def savechunk(self, dset, chunk):
        N = chunk.shape[1]
        dset.resize(dset.shape[1]+N, axis=1)
        dset[:,-N:] = chunk

    def recvchunk(self, sock, chunklen):
        data = b''
        while(len(data)<chunklen):
            packet = sock.recv(chunklen - len(data))
            if not packet:
                print("Incomplete chunk recieved")
                return None
            data+=packet
        return data

    def __init__(self, stream, server_address, port, bitrate  = 10000, segment_len = 100):
        # self.server_address = '10.20.92.130'
        # self.port = 12340

        self.server_address = server_address
        self.port = port
        self.url = 'http://' + server_address + ':8888'

        self.bitrate  = bitrate 
        self.segment_len = segment_len

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stream = stream


    #Connects to the Meame server and recieves outputstream of DAQ. If record data is true, data recieved is dumped to a HDF5 file
    def listen(self, record_data = False, file_path = ''):
        chunk_dim = (60,self.segment_len)
        chunk_len = chunk_dim[0] * chunk_dim[1] * 4
        print("chunk len: {}".format(chunk_len))

        if self.server_address != "127.0.0.1":
            self.send_config()
            self.send_start()
            print("Config sent")


        self.sock.connect((self.server_address, self.port))
        print("Connected")

        n_chunks = 0
        if record_data == True:
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
                    #TODO add to stream
                    n_chunks+=1

                self.stream.close()
                print("Connection closed. Recieved {} chunks".format(n_chunks))
        else:
            while (1):
                data = self.recvchunk(self.sock, chunk_len)
                if not data:
                    break

                data = struct.unpack("<6000i", data)
                chunk = np.asarray(data, dtype=np.int).reshape(chunk_dim)

                self.stream.append_segment(chunk)
                n_chunks += 1

            self.stream.close()
            print("Connection closed. Recieved {} chunks".format(n_chunks))

