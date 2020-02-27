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

# tunable parameters
num_steps = 2000
# L_history = np.zeros(num_steps)
# cmd_history = np.zeros((num_steps,3))


try:
	# loop
	for i in range(num_steps):
	    sensors = simulator.step()
	    
	    cmd = board_communicate(board, sensors.tolist())
	    cmd_history[i,:] = np.array(cmd)
	    # print("Command Received:")
	    # print(cmd)
	    print(i)

except Exception as e:
	print(e)
	pdb.set_trace()

finally:
	board.close()