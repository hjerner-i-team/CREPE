import numpy as np
from stream import Stream
import time
import matplotlib.pyplot as plt


def moving_avg(N, inputstream, outputstream):
    i = N;
    while(i < inputstream.final_index):
        if(i <= inputstream.size):
            average = np.average(inputstream.data[:,i-N:i],axis = 1)
            assert(average.shape == (60,))
            outputstream.append_collumn(average)
            i +=1
            if(i%100)==0:
                print("Append moving avg on index {}".format(i))
        else:
            time.sleep(0.05)
    outputstream.close()
        
def fft_max(N, T, bitrate,  stream, cutoff = 500):
    i = N
    freqs = []
    while(i < stream.final_index):
        if(i <= stream.size):
            F = np.fft.rfft(stream.data[:, i-N:i], axis = 1)    
            w = np.fft.rfftfreq(N, 1/bitrate)
            top_freq = np.argmax(np.abs(F[:,:cutoff]), axis = 1)
            freqs.append(top_freq)
            print(top_freq)
            if(i == N):
                t = np.arange(N)
                plt.plot(t ,stream.data[0, i-N:i])
                plt.figure()
                plt.plot(w, np.abs(F[0,:]))
                plt.show()
            
            i += bitrate
            if(i%100)==0:
                print("Append fft on index {}".format(i))
        else:
            time.sleep(0.05)
