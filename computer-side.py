"""
A simple module for sending/receiving data via serial (USB) to the PyCubed Mini board.
"""
import os, sys
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir+'/groundtruth-simulator/Simulator/')

import pdb
import time
import serial
import numpy as np
import sim_config as config
from simulator import Simulator
from board_comms import board_communicate
import matplotlib.pyplot as plt
plt.close('all')


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
cmd = [0,0,0] # start off first iteration with zero command

num_steps = 2000
w_history = np.zeros(num_steps)

for i in range(num_steps):
    sensors = simulator.step(np.array(cmd))
    w_history[i] = np.linalg.norm(sensors[3:6])
    cmd = board_communicate(board, sensors.tolist())
    print(i)

board.close()

plt.figure()
plt.plot(w_history)
plt.xlabel('time step (.1 sec each)')
plt.ylabel('angular velocity magnitude')
plt.grid()
plt.show()