# CREPE Hardware API
## - A connection between sensor systems and the CREPE server

## Purpose
The CREPE is not bound to a single type of sensor. Ideally it should be possible to connect sensors of any shape or form to the system, as the sensor choise depends on the goal of the chosen experiment. The API must therefore provide a method of communication which is both flexible and as simple as possible, as devices have different capabilities and limiting factors. 

## What does it do? 
The Hardware API is a Flask instance, providing a general HTTP REST API for sensor-server bidirectional interaction. It operates using a push-pull model, where the sensor system can push data as it is recorded, and pull results as it needs them. Data is transmitted as serialized JSON objects, so that data of any shape or form in principle can be transmitted. The API imposes minimal requirements upon the sensor system, which only requires the ability to use JSONs, HTTP and a network connection. Since that connection can be wireless, the solution allows mobile sensor systems. Multiple sensors can be connected simultaneously, given that they know how to coordinate with each other. The API is implemented as a QueueService in the primary data-loop, so that inbound and outbound data is efficiently communicated to/from other CREPE components. 

The current implementation comes with five pre-defined routes for general operation, however more can easily be added if desired. These five routes are: 

* / - The default route for testing. It simply displays a "Hello World". 
* /hw-api/input/ - Where the sensor can send JSON objects. Data sent here is transmittet through the CREPE data-loop and results in stimuli. 
* /hw-api/output/ - Where a sensor system, or an entirely separate system, can get the current finished output of the system as JSON. If the system for instance is supposed to perform some sort of object recognition, this is the place where the system's current best estimate is sent from.
* /hw-api/ready/ - Which is used to indicate if the current data sent from /output/ is valid. Systems which require a significant processing period before the output data is ready are encouraged to use this feature.
* /hw-api/echo/ - Where the most recent input submitted to /input/ is returned "as is". This feature is intended for cases such as input visualization, where the sensor system might be too limited in output-capacity to support multiple receivers. With /echo/, separate systems like screens can fetch the data from the CREPE server instead. 

## Contents 
* hw\_api.py - The Flask API implemented as a CREPE QueueService. 

## Use 
If the API is to be used on the internet (instead of locally for testing), remember to update the host IP address **before deployment**. Instructions can be found in hw\api.py. 

Add new methods to the API by writing a handler function that processes input, then add a matching endpoint in the \_\_init\_\_ method similarly to the existing ones.

> Why is the hw\api.py file different from the usual Flask route definition file?
An ordinary Flask server exists as an independent process. In CREPE it must instead exist as a thread, sharing the same process as the other components. The route definitions therefore use the alternate method, which involves creating a wrapper class that can be manipulated manually. This wrapper class can then inherit from the QueueService, making it launchable as a thread. Although the syntax is a bit different, it operates just like a normal Flask instance. 

## Further work 
The current API implementation suffers from two security concerns:
* The built-in Flask debug server is used. This acceptable for small experiments, but not for production-level projects. Instead a more mature WSGI server such as Gunicorn should be used. At the time of writing this was not implemented due to time constraints.
* Data is transmitted in plaintext as HTTP. Ideally HTTPS should be used, in case the data sent is of a sensitive nature. 

Furthermore the API could benefit from central config-file, which would remove the need to manually edit values such as the host's IP for each re-deployment. 
