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

    def read_sensors(sensors):
        print("sensor readings are:")
        return sensor_readings

    def determine_attitude(sensor_readings):
        print("attitude is:")
        return attitude




machine = StateMachine()
machine.add_state(IdleState())

machine.go_to_state('idle')

while True:
    machine.update()
