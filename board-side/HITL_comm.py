"""
A simple module for sending/receiving data via serial (USB) to the HITL computer.
"""

import json
import supervisor

def safe_json(data):
    if data is None:
        return True
    elif isinstance(data, (str, bool, int, float)):
        return True
    elif isinstance(data, (tuple, list)):
        return all(safe_json(x) for x in data)
    elif isinstance(data, dict):
        return all(isinstance(k, str) and safe_json(v) for k, v in data.items())
    return False

def send(data):
    if safe_json(data):
        print(json.dumps(data))
    else:
        print(json.dumps("FAIL: data-sent was unserializable via JSON."))

def receive():
    if supervisor.runtime.serial_bytes_available:
        encoded = input()
        try:
            data = json.loads(encoded)
        except Exception as e:
            return None
        else:
            return data
    else:
        return None