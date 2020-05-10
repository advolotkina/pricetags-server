import json
import threading
import argparse
import socket
import requests
import os
import shutil
from main_script import app
from main_script import db
from app.models import Good
from tmp.image_preps import prepare_image
from pricetag_update import update_good, update_good_name, update_good_price, update_good_specs, update_good_pic

HOST = '10.42.0.1'
PORT = 8888

events = {1: 'UPDATE_GOOD', 2: 'UPDATE_GOOD_NAME',
          3: 'UPDATE_GOOD_PRICE', 4: 'UPDATE_GOOD_SPECS',
          5: 'UPDATE_GOOD_PIC'}

handlers = {1: update_good, 2: update_good_name,
            3: update_good_price, 4: update_good_specs,
            5: update_good_pic}


def prepare_files(uid):
    with app.app_context():
        good = Good.query.filter_by(uid=uid).first()
        shutil.copyfile(f'./tmp/{uid}/specs', f'./goods/{uid}/specs')
        shutil.copyfile(f'./tmp/{uid}/good.bin', f'./goods/{uid}/good.bin')
        with open(f'./goods/{uid}/name', 'w') as f:
            f.write(good.name)
        with open(f'./goods/{uid}/price', 'w') as f:
            f.write(str(good.price))


def deserialize_message(client_message):
    """
    Метод, десериализующий сообщение клиента.
    :param client_message: Bytearray object, который необходимо десериализовать в список объектов
    :return: None если сообщение клиента не является валидным json. Инача возвращается список объектов словаря.
    """
    try:
        json_message = json.loads(str(client_message, encoding='utf-8'))
    except json.JSONDecodeError:
        return None
    # try:
    #     jsonschema.validate(instance=json_message, schema=message_schema)
    # except jsonschema.exceptions.ValidationError:
    #     return None
    return json_message


def serve_client_connection(conn):
    """
    Метод для обслуживания клиента.
    Считывает данные из сокета и выводит в консоль сообщения клиента.
    :param conn: Объект сокета.
    :return:
    """
    client_message = read_message(conn)
    if not client_message:
        return

    goods = deserialize_message(client_message)
    if goods is None:
        return

    for good in goods[1:]:
        uid = good['uid']
        with app.app_context():
            curr_good = Good.query.filter_by(uid=uid).first()
            os.mkdir(f'./tmp/{uid}/')
            if good['name']:
                curr_good.name = good['name']
            if good['price']:
                curr_good.price = float(good['price'])
            if good['path_to_pic']:
                url = good['path_to_pic']
                r = requests.get(url)
                with open(f'./tmp/{uid}/good.bin', 'wb') as f:
                    f.write(r.content)
                prepare_image(f'./tmp/{uid}/good.bin')
            if good['path_to_specs']:
                url = good['path_to_specs']
                r = requests.get(url)
                with open(f'./tmp/{uid}/specs', 'wb') as f:
                    f.write(r.content)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                return
            else:
                prepare_files(uid)
                os.rmdir(f'./tmp/{uid}/')

    with app.app_context():
        handlers[goods[0]['MSG']]()


def read_message(conn):
    """
    Данный метод считывает данные из сокета.
    """
    request = bytearray()
    try:
        with conn:
            while True:
                chunk = conn.recv(4096)
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
            new_client = threading.Thread(target=serve_client_connection, args=(conn,))
            new_client.start()
