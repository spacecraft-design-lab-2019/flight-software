#things the satellite ALWAYS needs to be doing
#keeping time
#accepting comms
#broadcasting comms (?)
#determining attitude: we can't detumble if we don't know we need to
#   reading sensor data
#reading battery
#other?

## QUESTION:
# how are we going to implement power saving?
#   use time.sleep?
#   physically turn off the flight computer and use some sort of counter?

# Set to false to disable testing/tracing code

## QUESTION:
# is this trinket specific?
import board
import digitalio
import time
import supervisor

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
#############################################


TESTING = True

def log(s):
    """Print the argument if testing/tracing is enabled."""
    if TESTING:
        print(s)

def read_magnetometer():
    log("magnetometer reading is:")
    return

def read_sun_sensor():
    log("sun sensor reading is:")
    return

def read_imu():
    log("imu reading is:")
    return

def read_sensors(machine,time):
    read_magnetometer()
    read_sun_sensor()
    read_imu()

    return True

def determine_attitude(machine,time):
    return

def control_attitude():
    return

def read_battery(machine):
    if machine.battery < 20: #if battery is below 20%
        return True
    else: return False

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
        # if switch.fell:
        #     machine.paused_state = machine.state.name
        #     machine.pause()
        #     return False
        return True

class StateMachine(object):

    def __init__(self):
        self.state = None
        self.states = {}
        self.I = [[17,0,0],[0,18,0],[0,0,22]]
        self.r = [6712880.93e-3,1038555.54e-3,-132667.04e-3]
        self.q = [1, 0, 0, 0]
        self.v = [-831.937369e-3,4688.525767e-3,-6004.570270e-3]
        self.w = [0, 0, 0]
        self.t = 0
        self.battery = 19 #initialize battery at 100% charge (?)

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            log('Exiting %s' % (self.state.name))
            self.state.exit(self)
        self.state = self.states[state_name]
        log('Entering %s' % (self.state.name))
        self.state.enter(self)

    def update(self):
        if self.state:
            log('Updating %s' % (self.state.name))
            self.state.update(self)

class IdleState(object):

    @property
    def name(self):
        return 'idle'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        if read_battery(machine):
            machine.go_to_state('lowpp')
        else:
            read_sensors(machine, 0)

class LowPowerState(object):

    @property
    def name(self):
        return 'lowpp'

    def enter(self, machine):
        State.enter(self, machine)
        led.value = True

    def exit(self, machine):
        State.exit(self, machine)
        led.value = False

    def update(self, machine):
        if not read_battery(machine):
            machine.go_to_state('idle')

machine = StateMachine()
machine.add_state(IdleState())
machine.add_state(LowPowerState())

machine.go_to_state('idle')

while True:
    if supervisor.runtime.serial_bytes_available:
        inText = input().strip()
        # Sometimes Windows sends an extra (or missing) newline - ignore them
        if inText == "":
            continue
        else:
            machine.battery = int(inText)
        print("received: %s" %inText)
    machine.update()
    time.sleep(5)
