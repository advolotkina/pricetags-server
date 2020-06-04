import socket
import threading
import time
from app.models import PriceTag
from main_script import app
from matplotlib import pyplot as plt

HOST = '10.42.0.1'
PORT = 65432

reference_ping_message_count = 288
real_ping_message_count = 0
PERIOD_OF_TIME = 86400


def serve_client_connection(conn, addr):
    global real_ping_message_count
    client_message = read_message(conn)
    if not client_message:
        return

    serial = client_message.decode('utf-8')
    serial = serial.replace('\n', '')
    real_ping_message_count += 1
    with app.app_context():
        PriceTag.update(serial, addr[0])


def read_message(conn):
    request = bytearray()
    try:
        with conn:
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    return request
                request += chunk
    except ConnectionResetError:
        return None


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        start = time.time()
        while True:
            conn, addr = s.accept()
            new_client = threading.Thread(target=serve_client_connection, args=(conn, addr))
            new_client.start()
            if time.time() > start + PERIOD_OF_TIME:
                break

    left = [1, 2]
    height = [reference_ping_message_count, real_ping_message_count]
    tick_label = ['реальное', 'эталонное']
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['red', 'green'])
    plt.ylabel('кол-во полученных сообщений')
    plt.title('График кол-ва полученных сообщений за 24 часа')
    plt.savefig('Result1.png')
