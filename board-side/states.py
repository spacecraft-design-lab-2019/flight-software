"""
Module for board state machine and generic state

"""
import ulab as np
import time
import detumble_algorithms as detumble
from pycubedmini import cubesat


class State():
    """
    generic state class
    """
    def __init__(self):
        pass

    @property
    def name(self):
        return ""

    def enter(self, machine):
        pass

    def exit(self, machine):
        pass

    def update(self, machine):
        pass


class IdleState(State):
    """
    Default state for the satellite. Majority of actions occur via IdleState
    """
    ENTER_VOLT = 0.8 # volt > 0.8 lowpower -> idle
    EXIT_VOLT =  0.3 # 
    @property
    def name(self):
        return 'idle'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        tumbling = False # TODO: need function to detect tumbling
        have_target = False # TODO: need function to detect if have target to reach

        if machine.get_curr_vlot_pct() < self.EXIT_VOLT:
            machine.go_to_state('lowpower')
        elif machine.get_curr_vlot_pct() > machine.states['actuate'].ENTER_VOLT and tumbling:
            machine.go_to_state('actuate')
        # TODO: check if iLQR state is needed 
        # elif machine.get_curr_vlot_pct() > 0.7 and have_target:
        #     machine.go_to_state('iLQR')
        elif machine.get_curr_vlot_pct() > machine.states['payload'].ENTER_VOLT:
            machine.go_to_state('payload') # state which deal with radio and photo
        else:
            pass


            


class LowPowerState(State):
    """
    Low-Power mode to conserve energy
    """
    ENTER_VOLT = 0.3 
    EXIT_VOLT =  0.8  
    @property
    def name(self):
        return 'lowpower'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        while machine.get_curr_vlot_pct() < self.EXIT_VOLT:
            time.sleep(0.5) # check battery voltage every 0.5 second 
        if machine.get_curr_vlot_pct() > self.EXIT_VOLT:
            machine.go_to_state('idle')
        else:
            pass

class ActuateState(State):
    """
    For all actuation purposes (using magnetorquers)
    """
    ENTER_VOLT = 0.7
    EXIT_VOLT = 0.2
    @property
    def name(self):
        return 'actuate'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        Bold = np.array(machine.sensors_old[0:3])
        Bnew = np.array(machine.sensors[0:3])
        Bdot = detumble.get_B_dot(Bold, Bnew, .1) # this is a hardcoded tstep (for now)
        machine.cmd = list(detumble.detumble_B_dot(Bnew, Bdot))
        while machine.get_curr_vlot_pct() > self.EXIT_VOLT:
            # TODO：calculate state estimate, dipole, actuate magnetorquer
            time.sleep(0.1) # update battery information & perform operation in 10 Hz
        if machine.get_curr_vlot_pct() < self.EXIT_VOLT:
            machine.go_to_state('idle')
        else:
            pass

class PayloadState(State):
    """
    For use of camera/radio/etc.
    """
    ENTER_VOLT = 0.7
    EXIT_VOLT = 0.2
    @property
    def name(self):
        return 'payload'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        while machine.get_curr_vlot_pct() > self.EXIT_VOLT:
            #TODO: use radio, take photos
            time.sleep(0.1) # update battery information & perform operation in 10 Hz
        if machine.get_curr_vlot_pct() < self.EXIT_VOLT:
            machine.go_to_state('idle')
        else:
            pass
