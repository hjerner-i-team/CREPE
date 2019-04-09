from flask import Flask, Response, request
from CREPE.communication.queue_service import QueueService
import queue

# Credits: https://stackoverflow.com/questions/40460846/using-flask-inside-class

class HWAPIWrapper(QueueService):
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
            endpoint='/', 
            endpoint_name='home', 
            handler=self.hello_world
        )
        self.add_endpoint(
            endpoint='/hw-api/input/', 
            endpoint_name='input', 
            handler=self.get_input,
            methods=['GET','POST'],  # Enable post to this endpoint
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
        self.out_valid = False  # Indicates if output value is "stable"
        
    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET']):
        self.app.add_url_rule(
            rule = endpoint, 
            endpoint = endpoint_name, 
            view_func = EndpointAction(handler), 
            methods=methods
        )

    # Test route
    # --------------------------------------------------------------------------
    def hello_world(self):
        return "Hello, World!"

    # Input from sensor
    # --------------------------------------------------------------------------
    # Receive hardware data as a json object. 
    # Should be one accumulated unit, such as a full image matrix, array data read
    # over a period, etc. 
    def get_input(self):
        if request.method == 'GET':
            return 'Send a POST request here to transmit a json'
        elif request.method == 'POST':
            data_json = request.data
            # TODO: Check that json is valid?
            self.put(data_json)
            self.last_input = data_json
            return Response(status=200, headers={})

    # Interpretation output to hardware unit
    # --------------------------------------------------------------------------
    # Return the current best guess of the system
    # Returns a json 
    def get_result(self):
        # Get current interpretation of data (as json)
        # out_json = get_from_readout_current()
        # Return output (as json)
        # return out_json
        try:
            out = self.queue_out.get(block=False)
        except queue.Empty:
            self.out_valid = False
            return self.last_input
        self.out_valid = True
        return out

    # Screen data output
    # --------------------------------------------------------------------------
    # Return the input data which was last submitted by the hardware
    # Intended for external visualization/monitoring 
    # Returns a json
    def get_echo(self):
        # Get the last input submitted by the hardware (as json)
        return self.last_input

    def out_ready(self):
        if self.out_valid:
            return "True"
        else:
            return "False"

class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.default_response = Response(status=200, headers={})

    def __call__(self, *args):
        return self.action()



