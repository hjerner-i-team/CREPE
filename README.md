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
    
# LIVE - live connection with meame
# FILE - get data from an h5 file
class CrepeModus(Enum):
    LIVE = 0
    FILE = 1
```
### \_\_init\_\_.py
To make things easy we have also included an easy import of the CREPE class that you can use like this
```
from CREPE import CREPE, CrepeModus
crep = CREPE(modus=CrepeModus.LIVE, file_path="../test_data/4.h5")
```

## Settings.py
The settings file is located `software/src/settings.py`
```
STREAM_DIMENSION
```

## QueueService
QueueService is a class that helps with the communication between two processes with two queues. It is meant to be inherited by any class who wants to be run as a process in the CREPE pipeline.

### Theory

QueueService employs two FIFO queues: `queue_out` is the queue that should be pushed to and `queue_in` is the queue that you can get data from.

We also implemented the same pattern with RPC, because of ease-of-use but it introduced too much performance overhead making the program too slow to be usefull. We therefor opted for a multiprocessing Queue based pattern. Queues are fast and efficient. The only downside is that there is a sligth performance loss because it has to pickle and unpickle numpy arrays.

#### Problem

Since this project cannot live in a single process we have to spawn several processes that have a need to communicate with eachother.  

#### Prestudy

We looked at RPC, multiproccessing/threading and tcp as alternative ways for communication between processes.
A Tcp connection would be more complex and time consuming to implement.
Mulitprocessing was better than threading for our purpose. 
Multiprocessing with shared memory or pipes is a good solution. Tough it would be a bit more complex, harder to implement and not as expandable as RPC.
RPC would be a very good solution, since it was easy to setup and use. But since we require that our processes run a main loop it was too much overhead to both run the main loop and a rpc server on the same process.

### How to use:
For an example, look at the SSP repo

#### QueueService class
The queues are stored in `self.queue_out` and `self.queue_in` but you should never have to directly interact with them.
They can be used by calling `self.put(data)` and `self.get()`. 

```
class QueueService():
    # @param name is the name of the service/class, only used when printing 
    # @param queue_out is the queue to (out)put data to
    # @param queue_in is the queue to get data from
    def __init__(self, name, queue_out=None, queue_in=None):
    
    # puts an element onto the queue_out
    # @param data is the data to put unto the queue
    def put(self, data):
    
    # gets the next element in queudata to put unto the queue
    # @returns whatever elem was in the queue. Most likley a 2d segment
    def get(self):

    # Get at least x number of columns from queue
    # @param x_elems is the minimum number of columns to get
    # @returns a single segment with shape (rows, x_elems or more) 
    def get_x_elems(self, x_elems):

    # get x numer of segments / items from queue. 
    # @param x_seg is the number of times to call .get()
    # @returns a single segment concatinaed from x_seg segments/items from queue
    def get_x_seg(self, x_seg):
```
For a detailed example look at the SSP repo.

For a simple example take a look at the `communication/queue_service.py` file.

An extremely simple example:
```
class GenerateData(QueueService):
    def __init__(self, queue_out):
        QueueService.__init__(self, name="GENDATA", queue_out=queue_out)

    def run(self):
        while True:
            rand_data = np.random.rand(60, 100)
            rand_data = rand_data * 200
            self.put(rand_data)
            time.sleep(0.01)
```

#### StartQueueService - a helper class
This class starts a new process that creates object and runs the run/loop function
```
class StartQueueService():
    # Starts a new process that creates object and runs the run/loop function
    # @param QueueServiceChildClass is a class that inherits from QueueService
    # @param **kwargs is the variables that QueueServiceChildClass is called with 
    #   As an example: start_and_run_queue_service(ProcessData, queue_in=previous_out_queue,
    #   queue_out=a_queue)  kwargs is now {"queue_in": queueobject, "queue_out": anotherqueueobject}
    # @returns process, queue_out 
    def __init__(self, QueueServiceChildClass, **kwargs):
    
    # get the name of the process
    def get_name(self):
```
How to Use:
```
class GenerateData(QueueService):
...
class ProcessData(QueueService):
....
processdata = StartQueueService(ProcessData, queue_in=gendata.queue_out)
gendata = StartQueueService(GenerateData)
processdata = StartQueueService(ProcessData, queue_in=gendata.queue_out)
```
