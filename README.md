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
The import system in python is literally garbage in semi-large projects. You can't import 
modules above package directory and import paths will differ when you run the file directly and
when the file is imported elsewhere. The fix for this is to root all imports in the root folder.
In our case `CREPE/software/src/`. Meaning that all python files can import as if they lived in
the root folder. 

**Include this at the start of every file that imports files/modules within this project**
```
""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("software/src")+len("software/src")])
""" End import fix """
```

### Documentation
Thanks to https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html and
https://stackoverflow.com/a/11158224 to guide us to the solution

`__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))`
Gets the current directory of the file

`sys.path.insert(0, __currentdir[0:__currentdir.find("software/src")+len("software/src")])`
It first finds this projects folders absolute path. (/CREPE/) and then adds "software/src" to it
And then inserts the new path into the sys.path. This new path overrides the original path.
The new path looks something like `/home/user/projects/CREPE/software/src' 




