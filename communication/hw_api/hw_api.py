from flask import Flask, Response, request
from CREPE.communication.queue_service import QueueService
import queue

# Credits: https://stackoverflow.com/questions/40460846/using-flask-inside-class

# A simple Flask-based REST API for the CREPE project. 
# Allows arbitrary sensor systems to interact with a CREPE server, in order to
# integrate their data output with the Cyborg Biological Neural Network for 
# the purpose of experimentation. 
# ------------------------------------------------------------------------------

class HWAPIWrapper(QueueService):
    '''
    A Flask server instance ordinarily operates as an independnt process. 
    The HWAPIWrapper integrates the Flask server with the rest of the project, 
    connecting it to other QueueServices in the core data loop. In doing so,
    other threads can make use of the interface to send and receive data. 
    This comes at the cost of not being able to use the traditional Flask 
    route definition format. Instead routes are defined below. The formatting
    differs slightly, but works essentially like the standard format. 
    '''
    app = None  # Do not make more than one HWAPIWrapper please

    def __init__(self, name="HWAPI", **kwargs):
        # Initialize queue service
        QueueService.__init__(
            self, 
            name=name, 
            **kwargs
        )

        # Initialize flask app
        self.app = Flask(__name__)

        # Add 'routes'/endpoints
        self.add_endpoint(
            endpoint='/',               # URL end for reaching route
            endpoint_name='home',       # Name for internal use
            handler=self.hello_world    # Function which is called upon access
        )
        self.add_endpoint(
            endpoint='/hw-api/input/',
            endpoint_name='input', 
            handler=self.get_input,
            methods=['GET','POST'],     # Enable POST requests to this endpoint
        )
        self.add_endpoint(
            endpoint='/hw-api/output/', 
            endpoint_name='output', 
            handler=self.get_result
        )
        self.add_endpoint(
            endpoint='/hw-api/ready/',
            endpoint_name='ready',
            handler=self.out_ready
        )
        self.add_endpoint(
            endpoint='/hw-api/echo/', 
            endpoint_name='echo', 
            handler=self.get_echo
        )

        self.last_input = "None"  # This is the last json submitted to the api
        self.last_output = "None"
        self.out_valid = False    # Indicates if output value is "stable"
        
    def run(self):
        '''
        Starts the Flask app. 
        Will work as-is for offline testing. 
        Remember to set host if the API is to be accessible on the internet.
        This can be done using:
        self.app.run(host='YOUR_IP')
        '''
        self.app.run()

    def add_endpoint(
            self, 
            endpoint=None, 
            endpoint_name=None, 
            handler=None, methods=['GET']
        ):
        '''
        A helper method for adding new routes to the flask app.
        Remember to do this before calling 'run', as new routes can't be
        added after that point.
        '''
        self.app.add_url_rule(
            rule = endpoint, 
            endpoint = endpoint_name, 
            view_func = EndpointAction(handler), 
            methods=methods
        )

# Routes 
# --------------------------------------------------------------------------
    def hello_world(self):
        '''
        Test route, can be used to check that the API is online.
        '''
        return "Hello, World!"

    def get_input(self):
        '''
        Receive input from hardware. A serialized json object is expected. 
        The json content can for example be an accumulated unit, such as a full 
        image matrix, array of data read over a period etc.
        ''' 
        if request.method == 'GET':
            return 'Send a POST request here to transmit a json'
        elif request.method == 'POST':
            data_json = request.data
            # TODO: Check that json is valid?
            self.put(data_json)
            self.last_input = data_json
            return Response(status=200, headers={})

    def get_result(self):
        '''
        Get the system's current interpretation of data (as json). 
        If there is not valid result available, the last valid output again
        Return final result (as json)
        '''

        latest = self.empty_queue_and_get_last()
        if latest:
            self.out_valid = True
            self.last_output = latest
            return latest
        else:
            self.out_Valid = False
            return self.last_output

    def get_echo(self):
        '''
        Returns the input data which was last submitted by hardware. 
        Intended for external visualization/monitoring. For example if 
        multiple screens are connected to visualize sensor output, it can
        be fetched from here instead of the more resource-constrained hardware.
        Returns a json
        '''
        # Get the last input submitted by the hardware (as json)
        return self.last_input

    def out_ready(self):
        '''
        Indicates whether the last output vas 'fresh' or not. May be useful for
        rapidly polling systems that pull output at a faster rate than what
        the system can produce, or systems with a significant processing 
        period per output.
        '''
        if self.out_valid:
            return "True"
        else:
            return "False"

class EndpointAction(object):
    '''
    A helper class for connection handler functions to their assigned routes.
    These can be modified upon further fine tune the API operation.
    '''

    def __init__(self, action):
        self.action = action
        self.default_response = Response(status=200, headers={})

    def __call__(self, *args):
        return self.action()



