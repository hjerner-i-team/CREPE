import json
import requests
from config_decimal import *

# Methods for sending data to the MEAME server. 
# Used for config and preprocessed data transmission

# TODO: Input validation and exceptions

# Static things and config
# ------------------------------------------------------------------------------
# Will need to be changed as MEAME evolves

MEAME_IP = '10.20.92.130' 
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


# Example functions
# ------------------------------------------------------------------------------
# These are intended as examples to help you get going.

def template_complete():
    '''
    Performs a complete example setup of MEAME from local values.
    '''
    meame_transmit('DSP-flash')
    template_setup()
    template_stim()
    template_setup()

def template_setup():
    '''
    Perform a setup procedure for the MEAME server. This is one of many possible
    configurations. 
    In this one in particular, we will set up: 

    This is a replica of the procedure found in the MEAME-DSP repository, and
    at the time of writing also callable at /DSP/stim/setup/.
    '''

    # TODO: Decode mystery
    commands = [  # A list of commands to run 
        dsp_write_sq_dbg(),  # Write SQ debug
        dsp_set_elec_grp_auto(),  # Set electrode group auto
        dsp_stop_stim_queue(),  # Stop stim queue
        dsp_reset(),  # Reset
        reg_write_req([37388], [0]),
        dsp_stop_stim_queue(),  # Stop stim queue
        reg_write_req(
            [STG_MWRITE1, STG_MWRITE1], 
            [32593, 1671343]
        ),
        reg_write_req([37420], [0]),
        reg_write_req([STG_MWRITE2, STG_MWRITE2], [32211289, 655385]),
        reg_write_req([37452], [0]),
        dsp_stop_stim_queue(),  # Stop stim queue
        reg_write_req([STG_MWRITE3, STG_MWRITE3], [32593, 1671343]),
        reg_write_req([37484], [0]),
        reg_write_req([STG_MWRITE4, STG_MWRITE4], [3211289, 655385]),
        reg_write_req([37516], [0]), 
        dsp_stop_stim_queue(),  # Stop stim queue
        reg_write_req([STG_MWRITE5, STG_MWRITE5], [32593, 1671343]), 
        reg_write_req([37548], [0]),
        reg_write_req([STG_MWRITE6, STG_MWRITE6], [3211289, 655385]),  
        dsp_reset(),  # Reset
        # Set blanking protection
        dsp_set_blanking_prot([4268, 4272], [311724626, 310378578]),
        # Config electrode group 0
        dsp_conf_elec_grp(
            [STIM_QUEUE_GROUP, STIM_QUEUE_ELEC0, STIM_QUEUE_ELEC1], 
            [ELEC_GRP_0, 82, 310378496]
        ), 
        # Config electrode group 1
        dsp_conf_elec_grp(
            [STIM_QUEUE_GROUP, STIM_QUEUE_ELEC0, STIM_QUEUE_ELEC1], 
            [ELEC_GRP_1, 310378496, 82]
        ),
        # Config electrode group 2
        dsp_conf_elec_grp(
            [STIM_QUEUE_GROUP, STIM_QUEUE_ELEC0, STIM_QUEUE_ELEC1], 
            [ELEC_GRP_2, 1346048, 0]
        ),
        # Set electrode group manual
        dsp_set_elec_grp_manual(
            [4284, 4288, 4292, 4296], 
            [13382412, 204672195, 13068, 204668928]
        ),
        dsp_commit_conf(),  # Commit config
        dsp_start_stim_queue(),  # Start stim queue
        # Set electrode group period
        dsp_set_elec_grp_period( 
            [STIM_QUEUE_GROUP, STIM_QUEUE_PERIOD], 
            [0, 5000]
        ) 
    ]  
    
    # Send commands in order to execute them
    for command in commands:
        auto_transmit(command)
        
def template_stim():
    command = dsp_func_call(10, [STIM_QUEUE_GROUP], [0]) 
    auto_transmit(command)

def do_remote_example():
    ''' 
    Use the remote GET urls to set up an example experiment.
    This uses the setups located on the MEAME server. 
    Returns requests requests touple
    '''
    request_flash = meame_transmit('DSP-flash')
    request_t_1 = meame_transmit('replay-setup')
    request_start = meame_transmit('replay-start')
    request_t_2 = meame_transmit('replay-setup')

    # Manual method with raw requests
    #requests.get('http://10.20.92.130:8888/DSP/flash')
    #requests.get('http://10.20.92.130:8888/DSP/stim/setup/')
    #requests.get('http://10.20.92.130:8888/DSP/stim/start/')
    #requests.get('http://10.20.92.130:8888/DSP/stim/setup/')

    return (request_flash, request_t_1, request_start, request_t_2)


# Core methods
# ------------------------------------------------------------------------------

def auto_transmit(json_msg):
    ''' 
    Send messages to the right destinations based on their json content.

    :param json_msg: JSON payload to send
    Returns requests request
    '''
    json_obj = json.loads(json_msg)
    # Attempt to get different identifying fields 
    if 'func' in json_obj:
        request = meame_transmit('DSP-call', json_msg)
    elif 'samplerate' in json_obj:
        request = meame_transmit('DSP-write', json_msg)
    elif 'electrodes' in json_obj:
        request = meame_transmit('DSP-write', json_msg)
    elif 'values' in json_obj:
        request = meame_transmit('DSP-write', json_msg)
    elif 'addresses' in json_obj:
        request = meame_transmit('DSP-read', json_msg)
    elif 'message' in json_obj: 
        request = meame_transmit('log', json_msg)
    else: 
        # If no messages match throw exception
        pass # TODO
    
    return  request

def meame_transmit(destination, json_msg=None):
    '''
    Generic method for transmissions to MEAME

    Example usage: 
    meame_transmit('status') gets current DSP status
    meame_transmit('DAQ-connect', daq_config(1000, 100)) sets up DAQ

    :param str destination: String key of desired MEAME url
    :param json_msg: JSON payload to send
    Returns request
    '''
    # The full destination of the request
    full_dest = "http://" + MEAME_IP + ':' + MEAME_input_port + urls[destination]

    # Send request
    if json_msg:
        #r = requests.post(full_dest, json=json_msg)
        r = requests.post(full_dest, data=json_msg)
    else:
        # Simply send a GET request to trigger something
        r=requests.get(full_dest)
    return r

def get_dsp_status(do_print=False): 
    '''
    Display the DSP's current state of well-being. 
    
    :param bool do_print: Set true to print to stdout. 
    Returns a json in the format:
        TODO
    '''
    response_json = meame_transmit('status')
    response_string = json.loads(response.text)
    if do_print:
        # TODO: formatting
        print(response_string)
    return response_string

def meame_set_stim(group_num, period):
    '''
    Apply stimulation to a stim group 
    :param
    '''
    # 9: SET ELECTRODE GROUP PERIOD
    # 10: ENABLE STIME GROUP
    
    #commands = [
    #    dsp_func_call
    pass
     

# DSP function wrappers
# ------------------------------------------------------------------------------
# The DSP (Digital Signal Processor) features 15 separate functions. 
# These can be called with the corresponding number, or these readable 
# wrapper methods. 

def dsp_dump():
    '''
    TODO: description
    Returns a serialized json object string
    '''
    return dsp_func_call(1)

def dsp_reset():
    '''
    TODO
    Returns a serialized json object string
    '''
    return dsp_func_call(2)
 
def dsp_conf_elec_grp(arg_addrs=[], arg_vals=[]):
    '''
    TODO
    :param int[] arg_addrs: Memory addresses of arguments
    :param int[] arg_vals: Values of arguments
    Returns a serialized json object string
    '''
    return dsp_func_call(3, arg_addrs, arg_vals)

def dsp_set_elec_grp_manual(arg_addrs=[], arg_vals=[]):
    '''
    In manual mode, each electrode will be configured only by the stimulus 
    select and enable registers.
    :param int[] arg_addrs: Memory addresses of arguments
    :param int[] arg_vals: Values of arguments
    Returns a serialized json object string
    '''
    return dsp_func_call(4, arg_addrs, arg_vals)

def dsp_set_elec_grp_auto():
    '''
    In auto mode, the stimulus and enable mux are additionally controlled
    by its assigned sideband.
    Returns a serialized json object string
    '''
    return dsp_func_call(5)
 
def dsp_commit_conf():
    '''
    TODO
    Returns a serialized json object string
    '''
    return dsp_func_call(6)

def dsp_start_stim_queue():
    '''
    TODO
    Returns a serialized json object string
    '''
    return dsp_func_call(7)

def dsp_stop_stim_queue():
    '''
    TODO
    Returns a serialized json object string
    '''
    return dsp_func_call(8)

def dsp_set_elec_grp_period(arg_addrs=[], arg_vals=[]):
    '''
    TODO
    :param int[] arg_addrs: Memory addresses of arguments
    :param int[] arg_vals: Values of arguments
    Returns a serialized json object string
    '''
    return dsp_func_call(9, arg_addrs, arg_vals)

def dsp_enable_stim_grp():
    '''
    TODO
    Returns a serialized json object string
    '''
    return dsp_func_call(10)

def dsp_disable_stim_grp():
    '''
    TODO
    Returns a serialized json object string
    '''
    return dsp_func_call(11)

def dsp_commit_conf_dbg():
    '''
    TODO
    Returns a serialized json object string
    '''
    return dsp_func_call(12)

def dsp_write_sq_dbg():
    '''
    TODO
    Returns a serialized json object string
    '''
    return dsp_func_call(13)

def dsp_set_blanking():
    '''
    Blanking disconnects all electrodes for a short period of time during the 
    stimulation pulse, to reduce stimulation artefacts.
    Returns a serialized json object string
    '''
    return dsp_func_call(14)

def dsp_set_blanking_prot(arg_addrs=[], arg_vals=[]):
    '''
    TODO
    :param int[] arg_addrs: Addresses of arguments ???
    :param int[] arg_vals: Values of arguments
    Returns a serialized json object string
    '''
    return dsp_func_call(15, arg_addrs, arg_vals)


# Methods producing specific JSON objects
# ------------------------------------------------------------------------------
# These correspond to 'low-level' DSP functions. You *should* use the provided
# wrappers instead.
# All of these should return a specific JSON.


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
    Returns a serialized json object string
    '''
    daq_conf = {'samplerate': samplerate, 'segmentLength': segmentLength}
    daq_json = json.dumps(daq_conf)
    return daq_json

def dsp_func_call(func, arg_addrs=[], arg_vals=[]):
    '''
    Call functions on the DSP. 
    Originally defined in MEAME2/DSPexecutor.cs
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
    Returns a serialized json object string
    '''
    daq_call = {"func": func, "argAddrs": arg_addrs, "argVals": arg_vals}
    daq_call_json = json.dumps(daq_call)
    return daq_call_json
        
def stim_req(electrodes, stim_freqs):
    '''
    Apply electrode stimulation.

    :param int[] electrodes: List of electrodes to stimulate
    :param float[] stim_freq: Frequency to apply TODO: unit?
    Note: Don't use decimals, use float as 'double'
    Returns a serialized json object string
    '''
    stim_req = {'electrodes': electrodes, 'stimFreqs': stim_freqs}
    stim_json = json.dumps(daq_conf)
    return stim_json

def reg_read_req(addrs):
    ''' 
    Read values of specific registers/addresses.
    :param: int[] addrs: List of uint memory addresses
    Returns a serialized json object string
    '''
    reg_red_req = {'addresses': addrs}
    reg_red_json = json.dumps(reg_red_req)
    return reg_red_json

def reg_write_req(addrs, vals):
    '''
    Set the values of specific registers/addresses.
    :param int[] addrs: List of uint memory addresses
    :param int[] vals: List of uint values for registers
    Returns a serialized json object string
    '''
    reg_wrt_req = {"addresses": addrs, "values": vals}
    reg_wrt_json = json.dumps(reg_wrt_req)
    return reg_wrt_json

def debug_msg(msg):
    '''
    Send a debug message, is probably logged somewhere
    :param str msg: A descriptive debug message
    Returns a serialized json object string
    '''
    dbg_msg = {'message': msg}
    msg_json = json.dumps(dbg_msg)
    return msg_json


# A main method for debugging
# ------------------------------------------------------------------------------

def main():
    template_complete()


if __name__ == '__main__':
    main()



