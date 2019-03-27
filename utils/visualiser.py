""" Import fix - check README for documentation """
import os,sys,inspect
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

from CREPE.utils import get_connection
from communication.stream_service import StreamService, DataModus, StreamSegmentIterator

# import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

class Visualiser:
    # filename = "recordings/recording5.hdf5"

    def __init__(self):
        self.N = 100

        self.conn = get_connection("STREAM")

        # Get a row iterator
        self.row_iter = StreamSegmentIterator(_range=100)

        self.fig, self.axs = plt.subplots(20,3, figsize = (10,10))
        self.lines = []
        self.xs = np.arange(N)

        for k,axes in enumerate(axs):
            for j, ax in enumerate(axes):
                i = k*2+j
                # max = dset[i].max()*2
                # ax.set_ylim(-max,max)
                self.line, = ax.plot(self.xs,np.zeros(N))
                self.lines.append(self.line)
                self.ax.set_yticks([])



    def animate(self,i):
        # chunk = dset[:,i*20:i*20+N]
        row = self.row_iter.next_or_wait(self.conn, timeout=1)
        for j,line in enumerate(self.lines):
            line.set_data(self.xs, row[j,:])
        return self.lines

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.animate, fargs=(self,), interval=10, blit=True)
        plt.show()
