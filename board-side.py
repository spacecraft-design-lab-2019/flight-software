#screen /dev/tty.usbmodem1411 115200

import board
import digitalio
import time
import supervisor

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

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

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            self.state.exit(self)
        self.state = self.states[state_name]
        self.state.enter(self)

    def update(self):
        if self.state:
            self.state.update(self)

class ReadyState(object):

    @property
    def name(self):
        return 'ready'

    def enter(self, machine):
        State.enter(self, machine)
        led.value = False

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        print('ready\r\n') #read this on comp side using .strip().decode('ascii')
        if supervisor.runtime.serial_bytes_available:
            inText = input().strip()
            if inText == '1':
                machine.go_to_state('payload')
        #time.sleep(.1)

class PayloadState(object):

    @property
    def name(self):
        return 'payload'

    def enter(self, machine):
        State.enter(self, machine)
        led.value = True

    def exit(self, machine):
        State.exit(self, machine)
        #led.value = True

    def update(self, machine):
        print('payload\r\n')
        #time.sleep(.1)

#create machine object of class StateMachine and add two states
machine = StateMachine()
machine.add_state(ReadyState())
machine.add_state(PayloadState())

#start off the StateMachine object in ReadyState
machine.go_to_state('ready')

while True:
    machine.update()
