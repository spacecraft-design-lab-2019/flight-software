"""
Module for board state machine and generic state

"""

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
        super().exit(machine)

    def update(self, machine):
        pass
