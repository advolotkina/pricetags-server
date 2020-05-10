import socket
import threading
import argparse
from app.models import PriceTag
from main_script import app

HOST = '10.42.0.1'
PORT = 65432


def serve_client_connection(conn, addr):
    """
    Метод для обслуживания клиента.
    """
    client_message = read_message(conn)
    if not client_message:
        return

    serial = client_message.decode('utf-8')
    print(serial, addr[0])
    with app.app_context():
        PriceTag.update(serial, addr[0])


def read_message(conn):
    """
    Данный метод считывает данные из сокета.
    """
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='Определяет IP адрес данного сервера, по умолчанию - 127.0.0.2', default=HOST)
    parser.add_argument('-port', type=int, help='Определяет порт данного сервера, по умолчанию - 8888', default=PORT)
    args = parser.parse_args()
    if args.host:
        HOST = args.host
    if args.port:
        PORT = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            new_client = threading.Thread(target=serve_client_connection, args=(conn, addr))
            new_client.start()
