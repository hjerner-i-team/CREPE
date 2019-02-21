import requests

def input_test():
    test_mat = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20]
    ] 
    # r = requests.get('http://127.0.0.1:5000/hw-api/input/')
    r = requests.post('http://127.0.0.1:5000/hw-api/input/', json=test_mat)

def main():
    input_test()

if __name__ == '__main__':
    main()
