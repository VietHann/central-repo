from flask import jsonify
from models import Device, session

def get_devices():
    devices = session.query(Device).all()
    device_list = [{'id': d.id, 'name': d.name, 'type': d.type, 'status': d.status} for d in devices]
    return jsonify(devices=device_list), 200