# CRÊPE 
## Core Reservoir Experiment Python Example
Interaction experiment with real grown neurons as part of the NTNU Cyborg project
 
_This is the work of group 2 - Hjerner i Team - in the EiT village NTNU Cyborg (Course TTK4850)_

## Description
CREPE is an example experiment for the interaction with NTNU Cyborgs architechture for interacting with grown neurocultures.
Our goal in the end is to play a modified Rock, Paper, Scissori game with the neuroculture.

# Installation
 - Clone project

`git clone git@github.com:hjerner-i-team/CREPE.git && cd CREPE`

- Install python virtual enviroment 

Make sure you are using python 3 (You can check by using `python -V`). If you have python 2, then install python 3 and use the command `python3` instead of `python` in all following code:

`python -m venv env`

`source env/bin/activate`

You need to use the `source` command on every terminal session.

If using windows then follow the same instructions in this link: https://docs.python.org/3/library/venv.html

- Install requirements

`pip install -r requirements.txt`

# Development notes
## Imports 
#### Include this at the start of every file that imports files/modules within this project
```
""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])
""" End import fix """
```


#### Import fix documentation

The import system in python is literally garbage in semi-large projects. You can't import 
modules above package directory and import paths will differ when you run the file directly and
when the file is imported elsewhere. The fix for this is to root all imports in the root folder.
In our case `CREPE`. Meaning that all python files can import as if they lived in
the root folder. 

Thanks to https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html and
https://stackoverflow.com/a/11158224 to guide us to the solution

`__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))`
Gets the current directory of the file

`sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])`
It first finds this projects folders absolute path. And then inserts the new path into the sys.path. This new path overrides the original path. The new path looks something like `/home/user/projects/CREPE/' 

# Documentation

## CREPE - main.py
```
class CREPE():
    # start all the processe 
    # @param data_file_path is the file path to an optional .h5 file
    def __init__(self, data_file_path = None ):
    
    # Function that runs the required shutdown commands before the project is closed 
    def shutdown(self):
```
### \_\_init\_\_.py
To make things easy we have also included an easy import of the CREPE class
```
# import CREPE.main and start it 
import main
def CREPE( path_to_file = None ):
    return main.CREPE(path_to_file)
```
You can use this in any file like this
```
from CREPE import CREPE
crep = CREPE(path_to_file)
```

## Settings.py
The settings file is located `software/src/settings.py`
It currently holds two variables
```
RPCPORTS
STREAM_DIMENSION
```

## StreamService
StreamService is a class that exposes a stream (a two dimensional array) containing neuro data trough RPC.

### Theory

StreamService employs a push-pull pattern. Data is "pushed" to StreamService, and anyone can "pull" the data trough RPC. If the data is not yet ready, an
optional callback argument can be supplied. StreamService will then call that callback once data is available. 

#### Problem

Since this project cannot live in a single process we have to spawn several processes that have a need to communicate with eachother.  

#### Prestudy

We looked at multiproccessing/threading and tcp as alternative ways for communication between processes.
A Tcp connection would be more complex and time consuming to implement.
Mulitprocessing was better than threading for our purpose. 
Multiprocessing with shared memory or pipes would have been a good solution. But it would be a bit more complex, harder to implement and not as expandable as RPC.

##### RPyC - Python RPC
We chose to go for RPyC. A RPC module for python. https://rpyc.readthedocs.io/en/latest/ 
It is very easy to use and provides us with all the functionality we need. It is also exelent for symetric computing, which makes this solution easier to use. 

This documentation will only cover this project. Check out RPyC's documentation to learn how it works.

### How to use:
For an example, look at the SSP repo

#### Expose self (push data)

To expose data, inherit from StreamService
```
from stream_service import StreamService, DataModus

class thisisclass(StreamService):
```

You have to init the StreamService with one of this moduses:

```
class DataModus(Enum):     
    DATA = 1               
    RESULT = 2
    TESTING = 3

class thisisclass(StreamService):
    def __init__(self):
        StreamService.__init__(self, DataModus.DATA)
```

To add data to the stream use one of these two functions

```
# Appends new data to row
# @param _row is one of the channels in self.stream
# @param _new_data is either an array containing new data or a single value
def append_stream_row_data(self, _row, _new_data):

# Appends segment to stream
# @param _new_data is either a 1D array with new values for each channel, or a 2d array
#   with a list of new values for each channel. To not append to a channel send None or an
#   empty list for that particular channel.
def append_stream_segment_data(self, _new_data):
```

Add the name of the service with a random free port to `software/src/settings.py`
`
RPCPORTS = {
    "STREAM": 18861,
}
`

This piece of code will start the RPC server, in this project we place this code in the `start.py` file in each module that is exposed with StreamService.

```
from rpyc.utils.server import ThreadedServer
from settings import RPCPORTS, RPYC_CONFIG

...

t = ThreadedServer= ThreadedServer(h5, port=RPCPORTS["HDF5Reader"], protocol_config=RPYC_CONFIG)
t.start()
```

### Call data (pull data)

StreamService exposes these two functions trough RPC. Please note that only functions that starts with the `exposed_` name is exposed trough RPC, and the
`exposed_`name is omitted when calling those functions. 

```
# Get a subset of a channels data
# @notice Exposed to RPC
# @param _row One of channels in self.stream
# @param _range The range we wish to read
# @param _startIndex The starting index to begin reading from on the channel
# @param _callback is the func to call when data is ready, if it is not ready now.  
# @returns a segmented 1d array or False
def exposed_get_row_segment(self, _row, _range, _startIndex, _callback=None):

# Get a segment of the stream (all channels)
# @notice Exposed to RPC 
# @param _range The range we wish to read
# @param _startIndex The starting index to begin reading from
# @param _callback is the func to call when data is ready, if it is not ready now.  
# @returns a segmented 2d array where each row has equal dimensions or False
def exposed_get_stream_segment(self, _range, _startIndex, _callback=None):
```

To call these functions then use this piece of code in the "client"
```
import rpyc
from settings import RPCPORTS, RPYC_CONFIG

c = rpyc.connect("localhost", RPCPORTS["<WHATEVERSERVICEYOURCALLING>"], config=RPYC_CONFIG)     
data = c.root.get_stream_segment(_range=10, _startIndex=0, _callback=callback_function)

```

#### Stream Iterator
There is some helper classes that will help you iterate over the entire stream so you don't have to keep track of indexes and so on. 

```
# Iterates over a row in the stream.
class StreamRowIterator():    
    # @param _channel is the row id. 
    # @param _range is the number of elements to return on each iteration
    def __init__(self, _channel=0, _range = 100):
        ...

    # gets the next set of data from the stream
    # @param _conn is the rpc connection object
    def next(self, _conn): 
        ...
    
    # gets the next set of data from the stream or waints for the the next set
    # @param _conn is the rpc connection object
    # @param sleep is the amount of seconds between calls
    # @param timeout is the amount of x * sleep seconds with no data we can recive before returning False.
    def next_or_wait(self, conn, sleep = 0.1, timeout = None):
        ...


# Iterates over segments in the stream
class StreamSegmentIterator(): 
    # @param _range is the number of elements to return on each iteration
    def __init__(self, _range = 100):
        ...

    # gets the next set of data from the stream
    # @param _conn is the rpc connection object
    # @returns 2D stream segment with row length 1 < x < self.range or False
    def next(self, _conn): 
        ...
        
    # gets the next set of data from the stream or waints for the the next set
    # @param _conn is the rpc connection object
    # @param sleep is the amount of seconds between calls
    # @param timeout is the amount of x * sleep seconds with no data we can recive before returning False.
    def next_or_wait(self, conn, sleep = 0.1, timeout = None):
        ...
```

Use these iterators like this
```
from stream_service import StreamSegmentIterator, StreamRowIterator

...
rowIter = StreamRowIterator(_channel=0, _range=100)
while True:
    # c is the rpyc connection
    data = rowIter.next_or_wait(c, timeout=1)
    if data is False:
        break

    # do stuff with data 
```

## utils.py
This file will include nice-to-have functions

```   
   # Waints for and returns a rpyc connection  
   # @param port is a port defined in RPCPORT  
   # @returns an rpyc connection object        
   def get_connection(port): 
``` 
