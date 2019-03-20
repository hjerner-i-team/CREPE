RPCPORTS = {
        "STREAM": 18861,
}

# generates a new RPCPORT and adds it to RPCPORTS
# @param name is the name of the port
# @returns new_port 
def gen_new_RPCPORT(name):
    # new port is the last defined RPCPORT + 1
    new_port = RPCPORTS.values()[-1] + 1
    if not RPCPORTS[name]:
        RPCPORTS[name] = new_port
        return new_port
    else:
        raise ValueError("RPCPORT name: ", name, " already taken")

import rpyc

RPYC_CONFIG = rpyc.core.protocol.DEFAULT_CONFIG
RPYC_CONFIG['allow_pickle'] = True

STREAM_DIMENSION = 60 
