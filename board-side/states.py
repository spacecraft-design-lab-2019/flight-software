"""
Module for board state machine and generic state

"""
import ulab as np
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
        full_voltage = 3.7 # TODO: need verify the hard code value
        curr_volt_pct = cubesat.battery_voltage()/full_voltage
        if curr_volt_pct < self.EXIT_VOLT:
            machine.go_to_state('lowpower')
        elif curr_volt_pct > machine.states['actuate'].ENTER_VOLT and tumbling:
            machine.go_to_state('actuate')
        # TODO: check if iLQR state is needed 
        # elif curr_volt_pct > 0.7 and have_target:
        #     machine.go_to_state('iLQR')
        elif curr_volt_pct > machine.states['payload'].ENTER_VOLT:
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
        pass
