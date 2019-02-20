# This file/class keeps track of the primary dataloop modus
from enum import Enum

# Enum variable to keep track of which modus the primary dataloop should be in
# LIVE = 1          Data will only go trough the chosen readoutlayer once before output 
# TRAINING = 2      Data will go trough the primary data loop before output
# LIVETRAINING =3   Same as LIVE but after output it will also go trough primary dataloop
class PrimaryDataLoopModusEnum(Enum):
    LIVE = 1                    
    TRAINING = 2            
    LIVETRAINING = 3        

# Class to hold and manage the primary dataloop modus
class PrimaryDataLoopModus():

    # Defaults the class to LIVE modus
    # @param _modus check setModus for definition
    def __init__(self, _modus=PrimaryDataLoopModusEnum.LIVE):
       self.setModus(_modus)

    # @return PrimaryDataLoopModusEnum 
    def getModus(self):
        return self.modus

    # @return str
    def getModusName(self):
        return self.modus.name

    # @return int
    def getModusValue(self):
        return self.modus.value
    
    # @param _modus is an Enum of type PrimaryDataLoop or either a string or int to represent
    # a name/value in the enum
    def setModus(self, _modus):
        if isinstance(_modus, PrimaryDataLoopModusEnum):
            self.modus = _modus
        elif isinstance(_modus, str):
            self.modus = PrimaryDataLoopModusEnum[_modus]
        elif isinstance(_modus, int):
            self.modus = PrimaryDataLoopModusEnum(_modus)
        else:
            raise AttributeError("No correct modus was given")

    def __str__(self):
        return str(self.modus)
