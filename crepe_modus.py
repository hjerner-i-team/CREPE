from enum import Enum

# Enum to represet which modus crepe can be in
# LIVE - live connection with meame
# FILE - get data from an h5 file
class CrepeModus(Enum):
    LIVE = 0
    FILE = 1
    OFFLINE = 2
    TEST = 3
