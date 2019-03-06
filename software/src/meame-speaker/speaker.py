import json
import requests

# Methods for sending data to the MEAME server. 
# Used for config and preprocessed data transmission

# TODO: Input validation and exceptions


# Static things and config
# Will need to be changed as MEAME evolves
# ------------------------------------------------------------------------------

MEAME_IP = '10.20.92.130'  # TODO
MEAME_input_port = '8888'
MEAME_output_port = '12340'

urls = {
    'home': '/',			# GET => "hello this is MEAME"
    'DAQ-connect': '/DAQ/connect/', 	# POST => Connect the DAQ with config
    'DAQ-start': '/DAQ/start/',		# GET => Start DAQ server
    'DAQ-stop': '/DAQ/stop/',		# GET => Stop DAQ server
    'status': '/status/',		# GET => Read MEAME status
    'DSP-flash': '/DSP/flash/',		# GET => Upload MEAME Binary
    'DSP-call': '/DSP/call',		# POST => Execute specific DSP function
    'DSP-read': '/DSP/read/',		# POST => Read from DSP
    'DSP-write': '/DSP/write/',		# POST => Write to DSP
    'replay-setup': '/DSP/stim/setup/', # GET => Run example setup sequence
    'replay-start': '/DSP/stim/start/', # GET => Run example start stim sequence
    'replay-stop': '/DSP/stim/stop/',   # GET => Run example stop stim sequence
    'log': '/aux/logmsg/'		# POST => Put message into log
}


# Main methods
# ------------------------------------------------------------------------------

def meame_transmit(destination, json_msg=None):
    '''
    Generic method for transmissions to MEAME

    Example usage: 
    meame_transmit('status') gets current DSP status
    meame_transmit('DAQ-connect', daq_config(1000, 100)) sets up DAQ

    :param str destination: String key of desired MEAME url
    :param json_msg: JSON payload to send
    Returns requests request
    '''
    # The full destination of the request
    full_dest = "http://" + MEAME_IP + ':' +MEAME_input_port + urls[destination]

    # Send request
    if json_msg:
        r = requests.post(full_dest, json=message)
    else:
        # Simply send a GET request to trigger something
        r=requests.get(full_dest)
    return r
     

# Methods producing specific JSON objects
# ------------------------------------------------------------------------------
# All of these should return a specific JSON


def daq_config(samplerate, segmentLength):
    '''
    Configure MEAME's DAQ.

    :param int samplerate: Rate of samling TODO: Better description
    :param int segmentLength: number of 

    When you send a HTTP POST with the JSON object shown below MEAME will listen
    for an incoming TCP connection on port 12340. Since there is only one port 
    for 60 channels the data must be multiplexed. A segment length of 100 means
    that the TCP stream will be segmented, the first 100 integers (400 bytes) will
    be data for 0, the next 100 ints for channel 1 and so forth.
    '''
    daq_conf = {'samplerate': samplerate, 'segmentLength': segmentLength}
    daq_json = json.dumps(daq_conf)
    return daq_json

def dsp_func_call(func, arg_addrs, arg_vals):
    '''
    Call functions on the DSP.

    List of DSP functions:
        1: DUMP
        2: RESET
        3: CONFIGURE ELECTRODE GROUP
        4: SET ELECTRODE GROUP MANUAL
        5: SET ELECTRODE GROUP AUTO
        6: COMMIT CONFIG
        7: START STIM QUEUE
        8: STOP STIM QUEUE
        9: SET ELECTRODE GROUP PERIOD
        10: ENABLE STIME GROUP
        11: DISABLE STIM GROUP
        12: COMMIT CONFIG DEBUG
        13: WRITE SQ DEBUG
        14: SET BLANKING
        15: SET BLANKING PROTECTION

    :param int func: Function number
    :param int[] arg_addrs: Addresses of arguments ???
    :param int[] arg_vals: Values of arguments
    '''
    daq_call = {'func': func, 'argAddrs': arg_addrs, 'argVals': arg_vals}
    daq_call_json = json.dumps(daq_call)
    return daq_call_json
        
def stim_req(electrodes, stim_freqs):
    '''
    Apply electrode stimulation.

    :param int[] electrodes: List of electrodes to stimulate
    :param float[] stim_freq: Frequency to apply TODO: unit?
    Note: Don't use decimals, use float as 'double'
    '''
    stim_req = {'electrodes': electrodes, 'stimFreqs': stim_freqs}
    stim_json = json.dumps(daq_conf)
    return stim_json

def reg_read_req(addrs):
    ''' 
    Read values of specific registers/addresses.
    :param: int[] addrs: List of uint memory addresses
    '''
    reg_red_req = {'addresses': addrs}
    reg_red_json = json.dumps(reg_red_req)
    return reg_red_json

def reg_write_req(addrs, vals):
    '''
    Set the values of specific registers/addresses.
    :param int[] addrs: List of uint memory addresses
    :param int[] vals: List of uint values for registers
    '''
    reg_wrt_req = {'addresses': addrs, 'values': vals}
    reg_wrt_json = json.dumps(reg_wrt_req)
    return reg_set_json

def debug_msg(msg):
    '''
    Send a debug message, is probably logged somewhere
    :param str msg: A descriptive debug message
    '''
    dbg_msg = {'message': msg}
    msg_json = json.dumps(dbg_msg)
    return msg_json


# A main method for debugging
# ------------------------------------------------------------------------------

def main():
    meame_transmit('replay-setup')


if __name__ == '__main__':
    main()



