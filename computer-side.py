"""
A simple module for sending/receiving data via serial (USB) to the PyCubed Mini board.
"""
import os, sys, pdb
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir+'/groundtruth-simulator/Simulator/')

import json
import serial, time
import numpy as np
import sim_config as config
from simulator import Simulator


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


def send(board, data):
    """
    Sends data over serial to the board (HITL)
    """
    if safe_json(data):
        # board.reset_output_buffer() # clear the current buffer in case previously sent data was not recieved
        to_send = json.dumps(data) + '\r\n'
        board.write(to_send.encode())
    else:
        raise ValueError("FAIL: data-sent was unserializable via JSON.")


def receive():
    """
    Receives data over serial sent by the board (HITL)

    note that the function will wait until something is received
    """
    while board.in_waiting == 0:
        pass

    data = board.read_until()
    return json.loads(data)



######################### MAIN LOOP ##############################

# initialize serial interface with board
board = serial.Serial()
board.baudrate = 115200
board.port = '/dev/ttyACM0'
board.timeout = .1

board.open()
board.reset_input_buffer()
board.reset_output_buffer()

# initialize simulator
simulator = Simulator(config)

for i in range(100):

    board.read_until() # this statement is here because for some reason the previously sent sensors are clogging up the buffer
    cmd = receive()

    print("Command:")
    print(cmd)

    # sensors = simulator.step(np.array(cmd))
    sensors = np.random.rand(4)
    print("Sensors:")
    print(sensors)

    pdb.set_trace()
    send(board, sensors.tolist())
    print()

board.close()