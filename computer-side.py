"""
A simple module for sending/receiving data via serial (USB) to the PyCubed Mini board.
"""

import json
import serial


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
        board.reset_output_buffer() # clear the current buffer in case previously sent data was not recieved
        board.write(json.dumps(data).encode())
    else:
        raise ValueError("FAIL: data-sent was unserializable via JSON.")


def receive():
    """
    Receives data over serial sent by the board (HITL)

    note that the function will wait until something is received
    """
    while not board.inWaiting():
        pass

    data = board.readline()
    return json.loads(data)



######################### MAIN LOOP ##############################

# initialize serial interface with board
board = serial.Serial()
board.baudrate = 115200
board.port = '/dev/ttyACM0'
board.timeout = .01

board.open()
board.reset_input_buffer()
board.reset_output_buffer()

sensors = [1, 3.3+5.5, 'string', 4.0]

while True:
    cmd = receive()
    print(cmd)
    send(board, sensors)







# # establish initial communications with board
# while not board.inWaiting():
#     pass
# initial = board.readline()
# if not json.loads(initial) == "Hello World!":


# # wait until board mentions something
# while not board.inWaiting():
#     pass




# counter = 0

# while True:
#     if board.inWaiting():
#         counter += 1
#         test = board.readline()
#         x = json.loads(test)
#         print(x)
#         print(counter)
# board.close()



# bytes_to_read = machine.ser.inWaiting()
#         if bytes_to_read:
#             encoded = machine.ser.readline()
#             if encoded:
#                 x = encoded.decode('ascii').strip()

#                 if x == '0':
#                     machine.go_to_state('talking')
#                 elif 'start' in x and 'end' in x:
#                     start = 'start'
#                     end = 'end'
#                     print("here's what i found:")
#                     print(x[x.find(start)+len(start):x.rfind(end)])

# machine.ser = serial.Serial()

#     machine.ser.baudrate = 115200
#     machine.ser.port = '/dev/tty.usbmodem1411'
#     machine.ser.timeout = .01
#     #machine.sim_state = sim_state
#     #machine.state_history = state_history


#     machine.add_state(ListeningState())
#     machine.add_state(TalkingState())

#     machine.go_to_state('listening')
#     machine.ser.open()
#     machine.ser.reset_input_buffer()
#     machine.ser.reset_output_buffer()
#     while True:
#         machine.update()

#     ser.close()
#     print(ser.is_open)
