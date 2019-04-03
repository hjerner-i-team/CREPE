import numpy as np
from neuro_processing.stream import Stream
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
#            if(i%100)==0:
#                print("Append moving avg on index {}".format(i))
        else:
            time.sleep(0.05)
    outputstream.close()
        
def fft_max(N, T, bitrate,  inputstream, outputstream, cutoff = 500):
    i = N
    while(i < inputstream.final_index):
        if(i <= inputstream.size):
            F = np.fft.rfft(inputstream.data[:, i-N:i], axis = 1)    
            w = np.fft.rfftfreq(N, 1/bitrate)
            top_freq = np.argmax(np.abs(F[:,:cutoff]), axis = 1)
#            print("FFT appending to stream:")
#            print(top_freq)
            outputstream.append_collumn(top_freq)
            
            i += bitrate
#            if(i%100)==0:
#                print("Append fft on index {}".format(i))
        else:
            time.sleep(0.05)
    outputstream.close()
