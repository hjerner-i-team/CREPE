import rpyc

RPYC_CONFIG = rpyc.core.protocol.DEFAULT_CONFIG
RPYC_CONFIG['allow_pickle'] = True

DEFAULT_STREAM_DIMENSION = 60

class CrepeSettings():
    RPCPORTS = {
            "STREAM": 18861,
    }

    # generates a new RPCPORT and adds it to RPCPORTS
    # @param name is the name of the port
    # @returns new_port 
    def gen_new_RPCPORT(self,name):
        # new port is the last defined RPCPORT + 1
        new_port = max(list(self.RPCPORTS.values())) + 1
        if name not in self.RPCPORTS:
            self.RPCPORTS[name] = new_port
            return new_port
        else:
            raise ValueError("RPCPORT name: ", name, " already taken")



