import json
import socket

HOST = '10.42.0.1'
PORT = 8888

# events = {1: 'UPDATE_GOOD', 2: 'UPDATE_GOOD_NAME',
#           3: 'UPDATE_GOOD_PRICE', 4: 'UPDATE_GOOD_SPECS',
#           5: 'UPDATE_GOOD_PIC'}

# test_json_message = [{'MSG': 5, 'uid': 'good1', 'path_to_pic': 'http://127.0.0.1:5000/images/coffee.jpg'}]
# test_json_message = [{'MSG': 2, 'uid': 'good1', 'name': 'Кофеварка REDMOND RCM-CBM1514, эспрессо, бронзовый'},
#                      {'MSG': 2, 'uid': 'good2', 'name': 'Кофеварка POLARIS PCM 2001AE, эспрессо, нержавеющая сталь'},
#                      {'MSG': 2, 'uid': 'good3', 'name': 'Кофеварка POLARIS PCM 4005A, эспрессо, бежевый'}]

# test_json_message = [{'ffdfdsfds':3232, 'fdsfsdfds':434, 'sdfsdfsdfsd': 'dsfdsfdsfds'}, {'dsfsd':32}]

test_json_message = [{'MSG': 1, 'uid': 'good1', 'name': 'Кофеварка REDMOND RCM-M1507, капельная, черный/серебристый',
                      'price': 2000, 'path_to_pic': 'http://127.0.0.1:5000/images/redmond_rcm_m1507.jpg',
                      'path_to_specs': 'http://127.0.0.1:5000/images/redmond_rcm_m1507_specs'}]


def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = json.dumps(message)
        print(message)
        s.sendall(bytes(message, "utf8"))


if __name__ == '__main__':
    send_message(test_json_message)
