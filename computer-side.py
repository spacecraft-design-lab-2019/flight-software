import serial
import time
import os
import sys

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir+'/groundtruth-simulator/Simulator/')

from simulation_step import *

import numpy as np
import sim_config as config
import conversions as conv
from constants import *
from propagate_step import *
import sensors as sense


class State(object):
    def __init__(self):
        pass

    @property
    def name(self):
        return ''

    def enter(self, machine):
        pass

    def exit(self, machine):
        pass

    def update(self, machine):
        return True

class StateMachine():
    def __init__(self):
        self.state = None
        self.states = {}
        self.sensors = None
        self.sim_state = None
        self.state_history = None
        self.i = 0

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            print('Exiting %s' % (self.state.name))
            self.state.exit(self)
        self.state = self.states[state_name]
        print('Entering %s' % (self.state.name))
        self.state.enter(self)

    def update(self):
        if self.state:
            self.state.update(self)

class ListeningState(object):

    @property
    def name(self):
        return 'listening'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        bytes_to_read = machine.ser.inWaiting()
        if bytes_to_read:
            encoded = machine.ser.readline()
            if encoded:
                x = encoded.decode('ascii').strip()

                if x == '0':
                    machine.go_to_state('talking')
                elif 'start' in x and 'end' in x:
                    start = 'start'
                    end = 'end'
                    print("here's what i found:")
                    print(x[x.find(start)+len(start):x.rfind(end)])

class TalkingState(object):

    @property
    def name(self):
        return 'talking'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        # Simulator
        machine.sensors, machine.sim_state = simulation_step(np.zeros(3), machine.sim_state)
        machine.state_history[machine.i+1, :] = machine.sim_state['state']
        to_send = package_data(list(machine.sim_state['state']))
        print('writing to serial')
        machine.ser.write(to_send.encode('ascii'))
        machine.go_to_state('listening')

def package_data(list_of_data):
    '''
    function to turn a list of data into a comma separated string
    '''
    packaged = ','.join(map(str, list_of_data))
    print('packaging: %s' %packaged)
    #print(len(list_of_data))
    packaged += '\r\n'
    return packaged

def main():
    #----------------Initialize / Setup Workspace------------------
    tspan = np.array([0, 86400])    # [sec]
    T = np.arange(0, tspan[1]+tstep, tstep)


    #---------------------Initial State Vector---------------------
    r_i, v_i = sgp4_step(line1, line2, tstart)
    # pdb.set_trace()
    state_i = np.r_[r_i, q_i, v_i, w_i]
    state_history = np.zeros((np.shape(T)[0], np.shape(state_i)[0]))
    state_history_sgp4 = np.zeros((np.shape(T)[0], 6))
    state_history[0, :] = state_i
    state_history_sgp4[0, :] = np.r_[r_i, v_i]
    sim_state = {'state': state_i, 't': tstart}

    machine = StateMachine()
    machine.ser = serial.Serial()

    machine.ser.baudrate = 115200
    machine.ser.port = '/dev/tty.usbmodem1411'
    machine.ser.timeout = .01
    machine.sim_state = sim_state
    machine.state_history = state_history


    machine.add_state(ListeningState())
    machine.add_state(TalkingState())

    machine.go_to_state('listening')
    machine.ser.open()
    machine.ser.reset_input_buffer()
    machine.ser.reset_output_buffer()
    while True:
        machine.update()

    ser.close()
    print(ser.is_open)

if __name__ == "__main__":
    main()
