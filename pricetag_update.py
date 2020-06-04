import socket
import os
from app.models import Good, PriceTagToGood, PriceTag

PORT = 8080

MSG_UPDATE = 0
MSG_RESET = 1
MSG_REBOOT = 2


def send_message(host, serial, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, PORT))
        message = "%s %s" % (serial, message)
        print(message)
        s.sendall(bytes(message, "utf8"))
        data = s.recv(1024)
    print('Received', repr(data))


def upload_data_to_pricetag(serial):
    pricetag = PriceTag.query.filter_by(serial_number=serial).first()
    pricetag_to_goods = [(pr.good_id, pr.index) for pr in PriceTagToGood.query.filter_by(pricetag_id=pricetag.id).all()]
    count = len(pricetag_to_goods)
    print(pricetag_to_goods)
    for good in pricetag_to_goods:
        curr_good = Good.query.filter_by(id=good[0]).first()
        if not curr_good:
            return
        with open('./tmp/count', 'w') as f:
            f.write(str(count))
        cmd = f'/usr/bin/scp ./tmp/count root@{pricetag.current_ip}:/opt/goods/'
        os.system(cmd)
        os.remove('./tmp/count')
        cmd = f'/usr/bin/scp ./goods/{curr_good.uid}/name root@{pricetag.current_ip}:/opt/goods/good{good[1]}/'
        os.system(cmd)
        cmd = f'/usr/bin/scp ./goods/{curr_good.uid}/price root@{pricetag.current_ip}:/opt/goods/good{good[1]}/'
        os.system(cmd)
        cmd = f'/usr/bin/scp ./goods/{curr_good.uid}/specs root@{pricetag.current_ip}:/opt/goods/good{good[1]}/'
        os.system(cmd)
        cmd = f'/usr/bin/scp ./goods/{curr_good.uid}/good.bin root@{pricetag.current_ip}:/opt/goods/good{good[1]}/'
        os.system(cmd)
    send_message(pricetag.current_ip, pricetag.serial_number, MSG_UPDATE)


def update_good(good_uid):
    update_good_name(good_uid)
    update_good_price(good_uid)
    update_good_specs(good_uid)
    update_good_pic(good_uid)


def update_good_name(good_uid):
    good = Good.query.filter_by(uid=good_uid).first()
    if not good:
        return
    pricetag_to_good = PriceTagToGood.query.filter_by(good_id=good.id).first()
    pricetag = PriceTag.query.filter_by(id=pricetag_to_good.pricetag_id).first()
    if not pricetag.current_ip:
        return
    cmd = f'/usr/bin/scp ./goods/{good_uid}/name root@{pricetag.current_ip}:/opt/goods/good{pricetag_to_good.index}/'
    os.system(cmd)
    send_message(pricetag.current_ip, pricetag.serial_number, MSG_UPDATE)


def update_good_price(good_uid):
    good = Good.query.filter_by(uid=good_uid).first()
    if not good:
        return
    pricetag_to_good = PriceTagToGood.query.filter_by(good_id=good.id).first()
    pricetag = PriceTag.query.filter_by(id=pricetag_to_good.pricetag_id).first()
    if not pricetag.current_ip:
        return
    cmd = f'/usr/bin/scp ./goods/{good_uid}/price root@{pricetag.current_ip}:/opt/goods/good{pricetag_to_good.index}/'
    os.system(cmd)
    send_message(pricetag.current_ip, pricetag.serial_number, MSG_UPDATE)


def update_good_pic(good_uid):
    good = Good.query.filter_by(uid=good_uid).first()
    if not good:
        return
    pricetag_to_good = PriceTagToGood.query.filter_by(good_id=good.id).first()
    pricetag = PriceTag.query.filter_by(id=pricetag_to_good.pricetag_id).first()
    if not pricetag.current_ip:
        return
    cmd = f'/usr/bin/scp ./goods/{good_uid}/good.bin root@{pricetag.current_ip}:/opt/goods/good{pricetag_to_good.index}/'
    os.system(cmd)
    send_message(pricetag.current_ip, pricetag.serial_number, MSG_UPDATE)


def update_good_specs(good_uid):
    good = Good.query.filter_by(uid=good_uid).first()
    if not good:
        return
    pricetag_to_good = PriceTagToGood.query.filter_by(good_id=good.id).first()
    pricetag = PriceTag.query.filter_by(id=pricetag_to_good.pricetag_id).first()
    if not pricetag.current_ip:
        return
    cmd = f'/usr/bin/scp ./goods/{good_uid}/specs root@{pricetag.current_ip}:/opt/goods/good{pricetag_to_good.index}/'
    os.system(cmd)
    send_message(pricetag.current_ip, pricetag.serial_number, MSG_UPDATE)

