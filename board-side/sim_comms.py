"""
A simple module for sending/receiving data via serial (USB) to the HITL computer.
"""

import json
import time
import supervisor


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
    if safe_json(data):
        print(json.dumps(data))
    else:
        raise ValueError("FAIL: data-sent was unserializable via JSON.")


def receive():
    """
    Receives data from the serial sent by the simulator (HITL)
    """
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


def sim_communicate(cmd, cubesat):
    """
    Publishes the latest commanded dipole (based on control law), then polls
    the simulator for spoofed sensor measurements
    """
    send(cmd)


    # PROBABLY ADD A TIME.SLEEP() HERE SO THAT THE COMPUTER SIDE HAS TIME TO TAKE SENT COMMAND OUT OF BUFFER. THAT WAY
    # SUPERVISOR.RUNTIME.SERIAL_BYTES_AVAILABLE WILL NOT ONLY RETURN TRUE

    # wait until the simulator sends back sensor inputs. (hopefully not long)
    #  -- could potentially add timeout function here to ensure we don't block
    #     the on-board code for too long
    while not supervisor.runtime.serial_bytes_available:
        cubesat.RGB = (0, 0, 255)
        pass

    # IMPORTANT NOTE:
    # -- the command input() that is called in the method receive() is blocking until a \r\n character is received.
    # -- for some reason, after the first loop, supervisor.runtime.serial_bytes_available ALWAYS returns true, and the
    #    code is held up at input()

    cubesat.RGB = (255, 255, 0)
    sensors = receive()
    cubesat.RGB = (0, 255, 255)
    return sensors