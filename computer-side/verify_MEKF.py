"""
A simple module for sending/receiving data via serial (USB) to the PyCubed Mini board.
"""
import os, sys
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, dir+'/groundtruth-simulator/Simulator/')

import pdb
import time
import serial
import numpy as np
import sim_config as config
from simulator import Simulator
from board_comms import board_communicate, send
import matplotlib.pyplot as plt
plt.close('all')


######################### MAIN LOOP ##############################

# initialize serial interface with board
board = serial.Serial()
board.baudrate = 115200
board.port = '/dev/ttyACM1'
board.timeout = .1

board.open()
board.reset_input_buffer()
board.reset_output_buffer()


# initialize simulator
simulator = Simulator(config)

# tunable parameters
num_steps = 200
# L_history = np.zeros(num_steps)
xk_history = np.zeros((num_steps, 7))
x_truth_history = np.zeros((num_steps, 4))
Pk_history = np.zeros((num_steps, 6, 6))

# send(board, [0])

try:
    for i in range(num_steps):
        sensors_array = simulator.step()
        sensors = [list(x) for x in sensors_array]
        board_state_estimate = board_communicate(board, sensors)

        # save board results
        xk_history[i, :] = np.array(board_state_estimate[0])
        Pk_history[i, :, :] = np.array(board_state_estimate[1])

        # save sim results
        x_truth_history[i, :] = simulator.debug_output[0]


except Exception as e:
    print(e)
    pdb.set_trace()

finally:
    board.close()

plt.figure()
plt.plot(xk_history[:, 0])
plt.plot(xk_history[:, 1])
plt.plot(xk_history[:, 2])
plt.plot(xk_history[:, 3])
plt.xlabel('time step (.1 sec each)')
plt.ylabel('quaterions - board')
plt.grid()

plt.figure()
plt.plot(x_truth_history[:, 0])
plt.plot(x_truth_history[:, 1])
plt.plot(x_truth_history[:, 2])
plt.plot(x_truth_history[:, 3])
plt.xlabel('time step (.1 sec each)')
plt.ylabel('quaterions - computer')
plt.grid()

plt.show()