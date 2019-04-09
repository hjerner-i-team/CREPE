""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """

import main
from crepe_modus import CrepeModus

def CREPE(modus=CrepeModus.LIVE, file_path = None, queue_services = None):
    return main.CREPE(modus=modus, file_path=file_path, queue_services = queue_services)

# communication
from communication.queue_service import QueueService, PoisonPill, is_poison_pill, StartQueueService
from communication.hdf5_reader import HDF5Reader
from communication.hw_api.hw_api import HWAPIWrapper, EndpointAction

# neuro_processing
from neuro_processing.neuro_processing import NeuroProcessor
from neuro_processing.meame_listener import MeameListener
from neuro_processing.processing import moving_avg, fft_max
from neuro_processing.stream import Stream

# utils
from utils.get_queue import get_queue
from utils.growing_np_array import Array as GrowingArray
from utils.visualiser import Visualiser






