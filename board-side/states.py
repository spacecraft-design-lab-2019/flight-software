"""
Module for board state machine and generic state

"""
import ulab as np
import detumble_algorithms as detumble


class State():
    """
    generic State class
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
        return True


class IdleState(State):
    """
    Class for remaining idle
    """
    @property
    def name(self):
        return 'idle'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        pass


class LowPowerState(State):
    """
    Class for remaining idle
    """
    @property
    def name(self):
        return 'lowpower'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        pass


class DetumbleState(State):
    """
    Class for detumbling
    """
    @property
    def name(self):
        return 'detumble'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        Bold = np.array(machine.sensors_old[0:3])
        Bnew = np.array(machine.sensors[0:3])
        Bdot = detumble.get_B_dot(Bold, Bnew, .1) # this is a hardcoded tstep (for now)
        machine.cmd = list(detumble.detumble_B_dot(Bnew, Bdot))
