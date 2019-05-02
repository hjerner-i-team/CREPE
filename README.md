# CRÊPE 
## Core Reservoir Experiment Python (Example)
The purpose of this project is to experiment with interaction of real grown neurons as part of the NTNU Cyborg project

Please refer to the project report, or sub-component readme's, for full documention

_This is the work of group 2 - Hjerner i Team - in the EiT village NTNU Cyborg (Course TTK4850)_

## Description
CREPE is a python module that makes communication with MEAME, the program that directly interacts with the neurocultures, easy and fun.
CREPE also alternitavly sets up a multiprocessing framework for data-flow, so that it is easy to process and manage the data that is sent from MEAME. The multiprocessing data-flow framework was made because python is not suitable to process and use large amounts of data, while at the same time running servers and listening for data. 
CREPE also has a hardware api integrated, so that communication with, for example, a raspberry pie is easy to integrate into the data-flow. 

CREPE serves as the main module for this project. The example project (which uses CREPE) can be found on our github page. The goal of this example project is to play a modified Rock, Paper, Scissor game with the neuroculture.

# Installation
##### Clone projects..
```
git clone git@github.com:hjerner-i-team/CREPE.git
cd CREPE
```
##### Install python virtual enviroment 
Make sure you are using python 3 (You can check by using `python -V`). If you have python 2, then install python 3 and use the command `python3` instead of `python` in all following code:
```
python -m venv env
source env/bin/activate
```

You need to use the `source` command on every terminal session.
If using windows then follow the same instructions in this link: https://docs.python.org/3/library/venv.html

##### Install requirements
`pip install -r requirements.txt`

# How to use CREPE
This section will describe how to use CREPE. For examples take a look at out example experiment repo. 
## importing
Import CREPE and requried function and classes 
`from CREPE import CREPE, CrepeModus, QueueService, get_queue` 

_A note on imports: almost every class/function in CREPE is imported, for your convinience, in the `CREPE.__init__.py` file. If the function/class does not exist in `__init__.py`_ you must use the full import path, for example: `from CREPE.communication.meame_speaker.speaker import template_complete`  

CREPE functions / classes in `__init__.py` with description:
TODO

## Settings.py
The settings file is `settings.py`
```
DEFAULT_STREAM_DIMENSION = 60
```
##  Setup crepe
When you initialize a CREPE object it will automaticly set up connection with MEAME and start listening.

### Simple
The easiest way to set up crep is to just initialize it with a modus
`crep = CREPE(modus=CrepeModus.LIVE)`

### CrepeModus
CrepeModus can be any of the different settings found in `crepe_modus.py` 

| Modus  | Description |
|---|---|
| LIVE | Communicate with real MEAME |
| FILE | Read data from a .h5 file |
| OFFLINE | Communicate with an offline MEAME server (for testing) |
| TEST | Generates test data |
| LIVE_RECORD | Communication with real MEAME and record the output from MEAME |

### Definition
CREPE.__init__ is defined as follows
```
def __init__(self, 
    modus=CrepeModus.LIVE, 
    file_path = None,
    queue_services = None
    ):
```
Where file_path is the optional absolute path of a .h5 file. 
queue_services is a optional list of different child classes of `QueueService` with corresponding `kwargs` on the form 
`queue_services = [[ChildQueueService, {"a_variable": 42}], ...]`

### With data-flow
An example of how to setup crepe with data-flow, taken from experiment example repo file `full_examply.py`
We will describe the child classes of QueueService: MovingAvg and ReadoutLayer, later.
```
from CREPE import CREPE, CrepeModus, QueueService
# child classes of QueueService:
from moving_average import MovingAvg
from readout_layer import ReadoutLayer

# Build file path
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
file_path = __currentdir + "/test_data/4.h5"

# Make functions ready to be inserted into the pipeline
queue_services = list()

mov_avg_kwargs = {"mov_avg_size":500}
queue_services.append([MovingAvg, mov_avg_kwargs])

readout_layer_kwargs = {}
queue_services.append([ReadoutLayer, readout_layer_kwargs])

#Create a crepe object and start it
crep = CREPE(modus=CrepeModus.FILE, file_path=file_path, queue_services=queue_services)

# wait untill finnished
crep.wait()
```

## Read output
Whether you are using CREPE just for listening and sending or using the optional data-flow framework (with QueueService) there may be a need to read the output of the last or first element in the data-flow. (As explained in the "# how CREPE works" section). There are three different ways to read the output the last element in the data-flow. 

The following code is inspired from the example experiment repo file `simple_example.py`
### 1. Get data with QueueService helper (Easy and flexibel) (Recomended)
```
from CREPE import QueueService
...
# Create a helper QueueService class, use crep.get_first_queue() if you instead want to get the listeners output
helper = QueueService(name="HELPER", queue_in=crep.get_last_queue())
while True:
    # get the next element
    data = helper.get()
    
    # check if the element was a poisonous pill (aka the last element)
    if data is False:
        crep.shutdown()
        break
        
    # do something with data
    print(data)
```
`CREPE.get_first_queue` gets the first queue in the data-flow, which is the queue that `MeameListener` outputs it's data on.
`CREPE.get_last_queue` gets the last queue in the data-flow, which is the queue that MeameSpeaker outputs it's data on. TODO check that this is correct.

### 2. Get data with CREP helper (Easiest, but not flexible) 
This function works almost like the one above but is implemented in CREPE. It reads from the last element in the data-flow. 
```
# make a function that will do something with the data
def data_func(data):
    # do something with data, for example print it
    print(data)

crep.wait(data_func)
```
or with a lambda function
```
crep.wait(lambda x: print(x))
```

### 3. Get data directly from queue (Harder, but very flexible)
```
from CREPE import is_poison_pill
...
# Alternativly you can get any queue with the function get_queue
queue = crep.get_first_queue()
while True:
    try: 
        # get the next element in the queue
        data = queue.get(timeout=1) #1 seconds timeout
        if is_poison_pill(data):
            break
    except: # .get raises error on timeout
        break
    # do something with data
    print(data)
    
crep.shutdown()
```

## Make a data-flow element => QueueService
QueueService is a class that allows a child access to a queue based data-flow framework, as explained in "How CREPE works".

Please look at the documentation, later in this README, for a detailed look at QueueService, but to summarize: It contains two queues. `self.queue_in` is the input queue it reads from and `self.queue_out` is the output queue it outputs data to. It also has three main functions `put(data)` `get()` `end()` that put data unto the output queue, gets data from the input queue and ends this queue, respectivly. 

To make a child QueueService class, simply inherit and init (with **kwargs):
```
from CREPE import QueueService
class ExampleChild(QueueService):
    def __init__(self, **kwargs):
        QueueService.__init__(self, name="EXAMPLE", **kwargs)
```
The `name` attribute is simply to identify the QueueService in print statements and with the function get_queue.
`**kwargs` is a kwargs varible that should contain `queue_in` and `queue_out` attributes. You don't really have to think about this tho, as you hopefully won't touch it. 

You have to define a `run` main loop function that can look something like this:
```
def run(self):
        while True:
            data = self.get()
            if data is False:
                self.end()
                return
            # do something with data
            print(data)
            # put something on queue
            self.put(random.randint(0,4))
```

## How to start a QueueService object => StartQueueService
Please remark that you should not have to use this helper class, as it is used for you in CREPE. But it migth be usefull for testing purposes. Please refer to `communication/queue_service.py` for an example.

`StartQueueService` is a helper class that starts a new process (using multiprocessing), creates an output queue and runs the `run` loop function inside the new process. 

Use it like this:
```
class GenerateData(QueueService):
...
class ProcessData(QueueService):
...
gendata = StartQueueService(GenerateData)
processdata = StartQueueService(ProcessData, queue_in=gendata.queue_out)
print("name of gendata: ", gendata.get_name()
```

# Development notes 
If you are developing CREPE (not only using it), read this!

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

Thanks https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html and
https://stackoverflow.com/a/11158224 for guiding us towards the solution.

`__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))`
Gets the current directory of the file

`sys.path.insert(0, __currentdir[0:__currentdir.find("CREPE")+len("CREPE")])`
It first finds this projects folders absolute path. And then inserts the new path into the sys.path. This new path overrides the original path. The new path looks something like `/home/user/projects/CREPE/' 

# Documentation

## QueueService
QueueService is a class that helps with the communication between data-flow elements. It gets data from a input queue and outputs data unto a different output queue. It is meant to be inherited by any class who wants to be run as a process in the CREPE data-flow pipeline.

![QueueService flow](https://imgur.com/skMzmk8.png)

### Implementation

QueueService employs two FIFO queues: `queue_out` is the queue that should be pushed to and `queue_in` is the queue that you can get data from. 
Two of QueueService's main functions `get()` and `put(data)` is wrapper functions for the multiproccessing Queue own `get()` and `put(data)` with additional functionality implementing the Poisionus Pill technice (todo explain this). 
We implement this technique by calling the `end()` function. It sends a `PoisionPill` object unto the output queue. The next QueueService's `get()` checks if the next element is such a `PoisionPill` object, and if so, sends the poisiounus pill unto it's own output queue and returns false.

#### Overview

| Category |  Name | Description  | Params | Returns 
|---|---|---|---|---|
| Variable | name | name of this QueueService |   | |
| Variable |  queue_in | Input queue to read from  |   | |
| Variable |  queue_out | Output queue to output data to |   | |
| Function | put | Put data onto the output queue | data = any kind of data | |
| Function | get | Get the next data from the input queue, returns False on queue end (PoisonPill) |   | whatever elem was in the queue. Most likley a 2d segment |
| Function | end | Signals that this QueueService is finnished (no more data will come) and sends a PoisonPill on the output queue |   |  | 
| Helper Function | get_x_elems | Get at least x number of columns from queue |  x_elems = is the minimum number of columns to get | a single segment with shape (rows, x_elems or more) |
| Helper Function | get_x_seg  |  get x numer of segments / items from queue. | x_seg = is the number of times to call .get()  |  a single segment concatinated from x_seg segments/items from queue |
| Helper Function | get_n_col | Same as get_x_elems but without slow concatenations |  N = number of columns, seg_height = heigth of segment, seg_widt = width of segment | A 2d np array with dimension (seg_width, seg_height) |
