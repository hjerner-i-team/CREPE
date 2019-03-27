""" Import fix - check README for documentation """
import os,sys,inspect
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

from communication.stream_service import StreamService, DataModus

import socket
import struct
import numpy as np
import h5py
import os
import json
import time
import requests
from multiprocessing import Process


class MeameListener(StreamService):

    def send_start(self):
        r = requests.get(self.url + '/DAQ/start')
        print(r)

    def send_config(self):
        conf = { 'samplerate' : self.samplerate, 'segmentLength' : self.segmentLength }
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

    def __init__(self, server_adress, port, segmentLength = 100, samplerate = 10000):
        # self.server_adress = '10.20.92.130'
        # self.port = 12340
        StreamService.__init__(self, "STREAM", DataModus.DATA)

        self.server_adress = server_adress
        self.port = port
        self.url = 'http://' + server_adress + ':8888'

        self.samplerate = samplerate
        self.segmentLength = segmentLength

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #Connects to the Meame server and recieves outputstream of DAQ. If record data is true, data recieved is dumped to a HDF5 file
    def listen(self, record_data = False, file_path = ''):
        chunk_dim = (60,self.segmentLength)
        chunk_len = chunk_dim[0] * chunk_dim[1] * 4


        self.send_config()
        self.send_start()
        print("Config sent")
        time.sleep(1)


        self.sock.connect((self.server_adress, self.port))
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
                dset.attrs.__setitem__("Bitrate", self.samplerate)

                while (1):
                    data = self.recvchunk(self.sock, chunk_len)
                    if not data:
                        break

                    data = struct.unpack("<6000i",data)
                    chunk = np.asarray(data, dtype=np.int).reshape(chunk_dim)

                    self.savechunk(dset,chunk)
                    self.append_stream_segment_data(chunk)

                    n_chunks+=1

                print("Connection closed. Recieved {} chunks".format(n_chunks))
        else:
            while (1):
                data = self.recvchunk(self.sock, chunk_len)
                if not data:
                    break

                data = struct.unpack("<6000i", data)
                chunk = np.asarray(data, dtype=np.int).reshape(chunk_dim)

                self.append_stream_segment_data(chunk)
                # print("Appended one chunk to stream")

                n_chunks += 1

            print("Connection closed. Recieved {} chunks".format(n_chunks))

