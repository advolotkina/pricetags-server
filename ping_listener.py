import socket
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import PriceTag

HOST = '10.42.0.1'  
PORT = 65432        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if not data:
                break
            conn.sendall(data)
            #найти pricetag по серийнику и сравнить старый и новый айпи, если старый отличается, то обновить

            PriceTag.update(data.decode("utf8"), addr[0])
            cmd = "./scp-config.sh %s" % addr[0]
            os.system(cmd)