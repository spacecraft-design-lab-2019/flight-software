"""
A simple module for sending/receiving data via serial (USB) to the board.
"""

import json
import time, pdb

## Note:
#   The following article can be referenced to help JSON serialize a custom class:
#   https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041

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
    if not safe_json(data):
        raise ValueError("FAIL: sending data that is unserializable via JSON.")

    board.reset_output_buffer() # clear the current buffer in case previously sent data was not recieved
    msg = json.dumps(data)
    to_send = json.dumps((msg, hash(msg))) + '\r\n'
    board.write(to_send.encode())
    board.read_until() # here because for some reason the sent sensors are clogging up the buffer


def receive(board):
    """
    Receives data over serial sent by the board (HITL)

    note that the function will wait for 1 seconds max
    """
    start = time.time()
    while board.in_waiting == 0:
        if (time.time() - start) > 1.0:
            return None

    try:
        encoded = board.read_until()
        msg = json.loads(encoded)
        # assert hash(msg[0]) == msg[1], "checksum failed"
        return json.loads(msg[0])

    except (json.decoder.JSONDecodeError, AssertionError):
        if encoded == b"Traceback (most recent call last):\r\n":
            # the board code has errored out
            print("ERROR: board code has errored out:\n")
            while board.in_waiting > 0:
                print(board.read_until())
            quit()

        else:
            return False


def board_communicate(board, sensors):
    """
    Publishes the latest sensor measurements, then polls the board for the
    latest commanded dipole.
    """
    send(board, sensors)

    for i in range(3):
        data = receive(board)

        if data == False:
            # the board sent something unreadable
            send(board, "ERROR: data not well received. Please resend.")
            print("data was false") # for debugging
            
        elif data == None:
            # the board did not send anything - is likely stuck on input()
            send(board, sensors)
            print("data was none") # for debugging

        elif data == "ERROR: data not well received. Please resend.":
            # the board did not understand what was last sent
            send(board, sensors)
            print("board didn't understand") # for debugging

        else:
            return data

    raise RuntimeError("could not communicate with board in 3 attempts.")