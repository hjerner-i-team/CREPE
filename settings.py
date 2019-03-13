RPCPORTS = {
        "STREAM": 18861,
}

import rpyc

RPYC_CONFIG = rpyc.core.protocol.DEFAULT_CONFIG
RPYC_CONFIG['allow_pickle'] = True

STREAM_DIMENSION = 60 
