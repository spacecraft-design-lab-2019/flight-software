
from earth import *
from dynamics import *
from ekf_step import *
# from downlink_scheduler import *

import gc
import time
from pycubedmini import cubesat
from sim_comms import sim_communicate, passthrough_msg
from states import *

import ulab as np

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
        passthrough_msg("debug")
        self.sensors = sim_communicate(self.cmd)

        if self.state:
            self.state.update(self)

        passthrough_msg("free heap space: {}".format(gc.mem_free()))
        # if gc.mem_free() < 10000:
        #     gc.collect()

        # passthrough_msg(self.sensors)



######################### MAIN LOOP ##############################


# create machine object of class StateMachine and add states
machine = StateMachine()
machine.add_state(DetumbleState())
machine.add_state(SchedulerState())

# start off the StateMachine object in the scheduler
machine.go_to_state('detumble')
print(machine.state)
# print(machine.state.sched.act_list.centers)
# print(machine.state.sched.act_list.windows)
# print(machine.state.sched.act_list.gs_numbers)


# wait until an input from the computer before continuing
cubesat.RGB = (255, 0, 0) # set LED to red
step = 0
input()
#cubesat.RGB = (0, 255, 0) # set LED to green
while True:
    print("Step: {}".format(step))
    step += 1
    machine.update()

