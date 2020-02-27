# -*- coding: utf-8 -*-

import gc
import time
from pycubedmini import cubesat
from sim_comms import sim_communicate, passthrough_msg
from states import IdleState, DetumbleState

######################## STATE MACHINE ###########################

class StateMachine():
    """
    State Machine class
    """
    def __init__(self):
        self.state = None # the current state
        self.states = {} # dict containing all the states
        self.sensors_old = [0,0,0,0,0,0,0,0,0] # previous sensor measurements
        self.sensors = self.sensors_old # current sensor measurements
        self.cmd = [0,0,0] # current commanded dipole

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            self.state.exit(self)
        self.state = self.states[state_name]
        self.state.enter(self)

    def update(self):
        # publish command input to magnetorquers and poll sensors
        self.sensors_old = self.sensors
        self.sensors = sim_communicate(self.cmd)

        if self.state:
            self.state.update(self)

        passthrough_msg("free heap space: {}".format(gc.mem_free()))
        # if gc.mem_free() < 10000:
        #     gc.collect()


######################### MAIN LOOP ##############################

# create machine object of class StateMachine and add states
machine = StateMachine()
# machine.add_state(IdleState())
machine.add_state(DetumbleState())
machine.cubesat = cubesat

# start off the StateMachine object in idle
machine.go_to_state('detumble')

# wait until an input from the computer before continuing
machine.cubesat.RGB = (255, 0, 0) # set LED to red
input()
machine.cubesat.RGB = (0, 255, 0) # set LED to green

while True:
    machine.update()
    