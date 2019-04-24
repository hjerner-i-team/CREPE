# MEAME Speaker
## - A Python wrapper for application --> MEAME communication

## Purpose
The neural cell cultures sitting inside the MEA are connected to a server called MEAME. The MEA applies stimuli and reads the resulting cell activity, and MEAME in turn is responsible for controlling and gathering data from the MEA. An application seeking to interface with the cell cultures therefore must know how to communicate with MEAME. The knowledge of how to speak to MEAME (not listen to it) is supplied by MEAME Speaker. 

## What does it do?
Communication to MEAME is performed using its HTTPS REST API. MEAME features a set of URLs, each of which can be accessed using GET or POST requests. GET-enabled URLs trigger either a predefined course of action, or a simple response. POST-enabled URLs expect to receive a serialized JSON object with data detailing which actions are to be performed. The set of these URLs and their function can be found in speaker.py. 

While a single pre-defined setup sequence can applied using the replay-URLs, more complex configurations must be defined manually for most experiemnts. This process involves sending a larger set of JSONs containing both function calls as well as writes to specific memory locations. 

MEAME Speaker abstracts this process by wrapping the creation and transmission of those JSON objects, which absolves the user from memorizing specific memory locations and unexpected quirks. JSONs are filled with desired values, transmitted and automatically routed to their correct destination. After a desired configuration is applied, MEAME Speaker can be used to apply dynamic stimuli. While the provided methods can be used by themselves by any project, a QueueService-based class has been included. MEAME Speaker can therefore be seamlessly integrated into CREPE projects by inserting the class into the core QueueService loop.  

## Contents 
* **speaker.py** - The collection of wrapping functions. All one needs for python-friendly communication with the MEAME server. 
* **meame\_speaker.py** - The QueueService class. Use this as last node before the MEAME server in your core data loop. 
* **config\_decimal.py** - The set of memory addresses and other constants which are derived from MEAME, SHODAN, and the MEA documentation. 
  
speaker.py is separated into several categories. The *Example functions* section provides an example of what a configuration of MEAME can look like. It is intended as a starting point for new users and can be used for basic debuggin purposes. *Core methods* contains the functions which are primarily inteded to be used when creating new projects with CREPE. If these do not satisfy your needs, consider expanding their functionality for the benefit of others. *Communication methods* houses the methods responsible for the HTTPS communication. If routing fails this would be the first place to look. The remaining sections contain methods related to lower-level operations. These should ordinarily not be invoced directly by the user. 

## Use
MEAME Speaker functionality should be utilized in the core data loop, between the input pre-processor and the MEAME server. Functions can be imported and called from the pre-processor directly, or by inserting the MeameSpeaker QueueService. In the latter case some tweaking of the QueueService may be required in order for it to work with the logic of your program. The idea is that MeameSpeaker.meame\_encoder() should map data from the queue to a group of electrodes and a stimuli frequency, then transmit it. 

For en example of MEAME Speaker in action, please refer to the SSP project. 

## Further work
At this time MeameSpeaker assumes the following: 
* That the user knows exactly what they are doing
* That MEAME works predictably and as intended, always
Exception handling, diagnostics and feedback are therefore sorely needed. 

Furthermore not all work related to the abstraction process was finished in time. For instance, electrode and group management has not been implemented in a user friendly fashion, due to lacking documentation. 
