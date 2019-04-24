import requests, json
from CREPE.communication.meame_speaker.config_decimal import *
from CREPE.communication.meame_speaker.speaker import *

def input_test():
    test_mat = [
        [20, 20, 20, 20, 20, 20, 20, 20],
        [20, 20, 20, 26, 26, 20, 20, 20],
        [20, 20, 26, 26, 26, 26, 20, 20],
        [20, 26, 26, 26, 26, 26, 26, 20],
        [20, 26, 26, 26, 26, 26, 26, 20],
        [20, 20, 26, 26, 26, 26, 20, 20],
        [20, 20, 20, 26, 26, 20, 20, 20],
        [20, 20, 20, 20, 20, 20, 20, 20],
        [20, 20, 20, 20, 20, 20, 20, 20], 
    ] 
    # r = requests.get('http://127.0.0.1:5000/hw-api/input/')
    json_mat = json.dumps(test_mat)
    print(json_mat)
    r = requests.post('http://129.241.209.138:5000/hw-api/input/', data=json_mat)
    print(r.status_code)

def output_test():
    r = requests.get('http://129.241.209.138:5000/hw-api/output/')
    print(r.status_code)
    print(r.text)

def apply_stim(freq):
    set_stim(0, freq)

def main():
    input_test()
    output_test()
    apply_stim(5000)

if __name__ == '__main__':
    main()
