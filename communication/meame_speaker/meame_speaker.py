""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """

from communication.meame_speaker.config_decimal import *
from communication.meame_speaker.speaker import *
from communication.queue_service import QueueService

class MeameSpeaker(QueueService):
    def __init__(self, periods, name="MEAMESPEAKER", **kwargs):
        QueueService.__init__(self, name, **kwargs)
        
        self.periods = periods

        # Pre-defined stimuli group to work with
        self.stim_group = 0

        # Initialize the MEAME server with desired config
        #do_remote_example()
        template_complete()

    def run(self):
        while True:
            # Send processed data to meame
            data = self.get()
            if data is False:
                return
            self.meame_encoder(data)

    def meame_encoder(self, guess):
        ''' 
        Translates the preprocessed data, in this case the system's current
        guess, into a set of stimuli instructions and transmits them to 
        MEAME
        :param str guess: A string, either "None", "Rock", "Paper", or 
        "Scissors".
        Returns status of transmission
        '''
        

        set_stim(self.stim_group, self.periods[guess])
