from flask import Flask
from flask import request

application = Flask(__name__)

# Run DEBUG server with:
# FLASK_APP=hw-api.py flask run

# Test route
# ------------------------------------------------------------------------------

@application.route('/')
def hello_world():
	return 'Hello, World!'

# Input from sensor
# ------------------------------------------------------------------------------
# Receive hardware data as a json object. 
# Should be one accumulated unit, such as a full image matrix, array data read
# over a period, etc. 

@application.route('/hw-api/input/', methods=['GET', 'POST'])
# Receive ambiguous json object, send it to pre-processing
def get_input():
	if request.method == 'GET':
		return 'Send a POST request here to transmit a json'
	elif request.method == 'POST':
		data_json = request.get_json()
		print("DEBUG:", data_json)
		# preprocess(data_json)
		return 'OK'


# Interpretation output to hardware unit
# ------------------------------------------------------------------------------
# Return the current best guess of the system
# Returns a json 
@application.route('/hw-api/output/')
def get_result():
	# Get current interpretation of data (as json)
	# out_json = get_from_readout_current()
 
	# Return output (as json)
	# return out_json
	return 'Rock' # TODO: placeholder	


# Screen data output
# -----------------------------------------------------------------------------
# Return the input data which was last submitted by the hardware
# Intended for external visualization/monitoring 
# Returns a json
@application.route('/hw-api/echo/')
def get_echo():
	# Get the last input submitted by the hardware (as json)
	# out_json = get_from_input_current()

	# Return output (as json)
	# return out_json
	return 'Placeholder'
