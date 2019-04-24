""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """

from main import CREPE
from crepe_modus import CrepeModus


# communication
from communication.queue_service import QueueService, PoisonPill, is_poison_pill, StartQueueService
from communication.hdf5_reader import HDF5Reader
from communication.hw_api.hw_api import HWAPIWrapper, EndpointAction

# neuro_processing
from neuro_processing.meame_listener import MeameListener

# utils
from utils.get_queue import get_queue
from utils.growing_np_array import Array as GrowingArray
from utils.visualiser import Visualiser






