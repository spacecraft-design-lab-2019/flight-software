import serial
import time

data = ['1'] #['6','9','6','9','6','9']

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
            x = machine.ser.read(bytes_to_read).strip().decode('ascii')
            print("received: {}".format(x))
            if x == '0':
                machine.go_to_state('talking')

class TalkingState(object):

    @property
    def name(self):
        return 'talking'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        to_send = package_data(data)
        print('writing to serial')
        machine.ser.write(to_send.encode('ascii'))
        machine.go_to_state('listening')


def package_data(list_of_data):
    '''
    function to turn a list of data into a comma separated string
    '''
    packaged = ','.join(map(str, list_of_data))
    print('packaging: %s' %packaged)
    packaged += '\r\n'
    return packaged

def main():

    machine = StateMachine()
    machine.ser = serial.Serial()
    machine.ser.baudrate = 115200
    machine.ser.port = '/dev/tty.usbmodem1411'
    machine.ser.timeout = .01
    machine.add_state(ListeningState())
    machine.add_state(TalkingState())

    machine.go_to_state('listening')
    machine.ser.open()

    while True:
        machine.update()

    ser.close()
    print(ser.is_open)

if __name__ == "__main__":
    main()
