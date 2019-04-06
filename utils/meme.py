import socket
import numpy as np
import struct
import h5py
import time

server_adress = 'localhost'
port = 40000
N = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((server_adress, port))
print("Listening on port {}".format(port))
s.listen()
conn, addr = s.accept()


#for n in range(N):
#    buf = struct.pack('!6000i', *np.random.randint(-1000,1000,6000))
#    conn.send(buf)
#    if(n%10==0):
#        print("Sent {} segments".format(n))

with h5py.File("../recordings/recording5.hdf5", "r") as f:
#    dset = f['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
    dset = f["data"]
#    n_chunks = (int)dset.shape[1]/100
    n_chunks = (int)(dset.shape[1]/100)

    for n in range(n_chunks):
        data = dset[:, n*100:(n+1)*100].reshape(6000)
        buf = struct.pack('<6000i', *data)
        conn.send(buf)
        if(n%10==0):
            print("Sent {} segments".format(n))
        time.sleep(0.1)
        

conn.close()
