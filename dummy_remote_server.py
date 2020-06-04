import json
import socket

HOST = '10.42.0.1'
PORT = 8888

# events = {1: 'UPDATE_GOOD', 2: 'UPDATE_GOOD_NAME',
#           3: 'UPDATE_GOOD_PRICE', 4: 'UPDATE_GOOD_SPECS',
#           5: 'UPDATE_GOOD_PIC'}

test_json_message_pic_update = [
    {'MSG': 5,
     'uid': 'good1',
     'path_to_pic': 'http://127.0.0.1:5000/images/test-pic.jpg'}]

# test_json_message_pic_update = [
#     {'MSG': 5,
#      'uid': 'good1',
#      'path_to_pic': 'http://127.0.0.1:5000/images/redmond_rcm_m1507.jpg'}]

test_json_message_names_update = [
    {'MSG': 2, 'uid': 'good1', 'name': 'NEW NAME'},
    {'MSG': 2, 'uid': 'good2', 'name': 'NEW NAME2'},
    {'MSG': 2, 'uid': 'good3', 'name': 'NEW NAME3'}]

test_json_message_prices_update = [
    {'MSG': 3, 'uid': 'good1', 'price': '111'},
    {'MSG': 3, 'uid': 'good2', 'price': '222'},
    {'MSG': 3, 'uid': 'good3', 'price': '333'}]

test_json_message_price_update = [
    {'MSG': 3, 'uid': 'good3', 'price': '4000'}]

test_json_message_names_update = [{'MSG': 2, 'uid': 'good1', 'name': 'Кофеварка REDMOND RCM-CBM1507, эспрессо, бронзовый'},
                     {'MSG': 2, 'uid': 'good2', 'name': 'Кофеварка POLARIS PCM 2001AE, эспрессо, нержавеющая сталь'},
                     {'MSG': 2, 'uid': 'good3', 'name': 'Кофеварка POLARIS PCM 4005A, эспрессо, бежевый'}]

# test_json_message_prices_update = [{'MSG': 3, 'uid': 'good1', 'price': '2000'},
#                                    {'MSG': 3, 'uid': 'good2', 'price': '3000'},
#                                    {'MSG': 3, 'uid': 'good3', 'price': '4000'}]

test_json_message_good_update = [
    {'MSG': 1,
     'uid': 'good3',
     'name': 'TESTESTESTTEST',
     'price': 9999,
     'path_to_pic': 'http://127.0.0.1:5000/images/test-pic.jpg',
     'path_to_specs': 'http://127.0.0.1:5000/images/redmond_rcm_m1507_specs'}]


def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = json.dumps(message)
        print(message)
        s.sendall(bytes(message, "utf8"))


if __name__ == '__main__':
    # send_message(test_json_message_pic_update)
    # send_message(test_json_message_names_update)
    send_message(test_json_message_prices_update)
    # send_message(test_json_message_price_update)
    # send_message(test_json_message_good_update)
