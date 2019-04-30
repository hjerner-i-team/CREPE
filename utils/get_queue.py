
""" Import fix - check README for documentation """ 
import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, __currentdir[0:__currentdir.find("/CREPE")+len("/CREPE")])
""" End import fix """

import time

def _get_queue(crep, name_of_service):
    for service in crep.queue_services:
        if name_of_service == service.get_name():
            return service.queue_out
    return False
def get_queue(crep, name_of_service):
    for i in range(100):
        r = _get_queue(crep, name_of_service)
        if r is False:
            time.sleep(0.1)
        else:
            return r

    raise ValueError("[CREPE.utils.get_queue] " ,
            "Could not find a service with name after 10 seconds ", name_of_service)
