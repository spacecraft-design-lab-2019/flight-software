"""
A simple module for sending/receiving data via serial (USB) to the HITL computer.
"""

import time
import json


def hash(s):
    return sum(bytes(s, 'utf-8'))


def safe_json(data):
    """
    Checks if the input data is serializable via JSON
    """
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
    """
    Sends data over serial to the simulator (HITL)
    """ 
    if not safe_json(data):
        raise ValueError("FAIL: sending data that is unserializable via JSON.")

    msg = json.dumps(data)
    print(json.dumps((msg, hash(msg))))


def receive():
    """
    Receives data from the serial sent by the simulator (HITL)
    """
    encoded = input() # note that this function is blocking until a \r\n character is received.
    try:
        msg = json.loads(encoded)
        assert hash(msg[0]) == msg[1], "checksum failed"
        return json.loads(msg[0])

    except (ValueError, AssertionError):
        send("ERROR: data not well received. Please resend.")
        return False


def sim_communicate(cmd):
    """
    Publishes the latest commanded dipole (based on control law), then polls
    the simulator for spoofed sensor measurements
    """
    send(cmd)

    while True:
        sensors = receive()

        if sensors == False:
            # the sim sent something unreadable
            send("ERROR: data not well received. Please resend.")

        elif sensors == "ERROR: data not well received. Please resend.":
            # the sim did not understand what was last sent
            send(cmd)

        else:
            return sensors

