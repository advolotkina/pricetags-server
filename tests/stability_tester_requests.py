import socket
import time
from matplotlib import pyplot as plt

HOST = '10.42.0.125'
PORT = 8080
SERIAL = 'serial1'
MSG_UPDATE = 0
PERIOD_OF_TIME = 86400

reference_response_message_count = 3600
real_response_message_count = 0


def send_message():
    global real_response_message_count
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = "%s %s" % (SERIAL, MSG_UPDATE)
        s.sendall(bytes(message, "utf8"))
        data = s.recv(1024)
        if data.decode('utf-8') == 'OK':
            real_response_message_count += 1


if __name__ == '__main__':
    start = time.time()
    while True:
        send_message()
        time.sleep(60)
        if time.time() > start + PERIOD_OF_TIME:
            break

    left = [1, 2]
    height = [reference_response_message_count, real_response_message_count]
    tick_label = ['запросов', 'ответов']
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['blue', 'black'])
    plt.ylabel('кол-во сообщений')
    plt.title('График кол-ва запросов на ценник и ответов, полученных от ценника')
    plt.savefig('Result2.png')
