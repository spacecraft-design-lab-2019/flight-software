# -*- coding: utf-8 -*-

import time
from pycubedmini import cubesat
from sim_comms import sim_communicate
from states import IdleState

######################## STATE MACHINE ###########################

class StateMachine():
    """
    State Machine class
    """
    def __init__(self):
        self.state = None # the current state
        self.states = {} # dict containing all the states
        self.sensors = [0,0,0,0,0,0,0,0,0] # current sensor measurements
        self.cmd = [0,0,0] # current commanded dipole

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            self.state.exit(self)
        self.state = self.states[state_name]
        self.state.enter(self)

    def update(self,cubesat):
        # publish command input to magnetorquers and poll sensors
        self.sensors = sim_communicate(self.cmd, cubesat)

        if self.state:
            self.state.update(self)


######################### MAIN LOOP ##############################

# create machine object of class StateMachine and add states
machine = StateMachine()
machine.add_state(IdleState())

# start off the StateMachine object in idle
machine.go_to_state('idle')

# wait 5 seconds to allow for running computer-side.py
cubesat.RGB = (255, 0, 0) # set LED to red
time.sleep(5)
cubesat.RGB = (0, 255, 0) # set LED to green


while True:
    machine.update(cubesat)
