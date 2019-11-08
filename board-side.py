#screen /dev/tty.usbmodem1411 115200

import board
import digitalio
import time
import supervisor
# import relevant libraries
import os
import sys
import busio
#import storage
#import adafruit_sdcard
#from digitalio import DigitalInOut, Direction, Pull
#from adafruit_bus_device.spi_device import SPIDevice
import random

from fake_sensors import * #from camera import *
from gnc import *

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

import neopixel
colorful_led = neopixel.NeoPixel(board.NEOPIXEL, 1)
colorful_led.brightness = 0.01

### UNCOMMENT WHEN CAMERA IS SET UP ####
# set up SPI communication
# spi = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# cs_cam = DigitalInOut(board.D4)  # use pin 4 for camera
# cs_sd = DigitalInOut(board.D5)  # use pin 5 for SD card
# camera = SPIDevice(spi, cs_cam, baudrate=115200, polarity=0, phase=0)
# sdcard = adafruit_sdcard.SDCard(spi, cs_sd)

# Use the filesystem as normal! Our files are under /sd
# vfs = storage.VfsFat(sdcard)
# storage.mount(vfs, "/sd")
# sys.path.append("/sd")

# print SD card file names and stats
# print('Files on filesystem:')
# print('--------------------')
# print_directory("/sd")
# print('')


def package_data(list_of_data):
    '''
    function to turn a list of data into a comma separated string
    '''
    packaged = ','.join(map(str, list_of_data))
    packaged += '\r\n'
    return packaged

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
        self.I = [[17,0,0],[0,18,0],[0,0,22]]
        self.sensors = [0,0,0,0,0,0]
        self.vector = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.t = 0
        self.battery = 100

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

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        print('0\r\n') #read this on comp side using .strip().decode('ascii')
        if supervisor.runtime.serial_bytes_available:
            machine.go_to_state('listening')
            # inText = input().strip()
            # if inText == '1':
            #     machine.go_to_state('payload')

class ListeningState(object):

    @property
    def name(self):
        return 'listening'

    def enter(self, machine):
        State.enter(self, machine)
        colorful_led[0] = (0, 0, 255) #blue

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        if supervisor.runtime.serial_bytes_available:
            inText = input().strip()
            if len(inText) == 11:
                machine.sensors = inText.split(",")
                machine.go_to_state('idle')

class TalkingState(object):

    @property
    def name(self):
        return 'talking'

    def enter(self, machine):
        State.enter(self, machine)
        print(package_data(machine.vector))

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        machine.go_to_state('listening')

class PayloadState(object):

    @property
    def name(self):
        return 'payload'

    def enter(self, machine):
        State.enter(self, machine)
        snap_a_pic()

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        print('payload\r\n')

class IdleState(object):

    @property
    def name(self):
        return 'idle'

    def enter(self, machine):
        State.enter(self, machine)
        colorful_led[0] = (255, 0, 0) #red

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        machine.vector = gnc_main(machine.sensors)
        #also we want to be sending/receiving comms via radio
        machine.go_to_state('talking')


class AttitudeControl(object):

    @property
    def name(self):
        return 'attitude'

    def enter(self, machine):
        State.enter(self, machine)
        led.value = True

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        return
        #if abs(machine.vector - measurements) <= threshold
            #then go to idle state

#create machine object of class StateMachine and add two states
machine = StateMachine()
machine.add_state(ReadyState())
machine.add_state(PayloadState())
machine.add_state(IdleState())
machine.add_state(ListeningState())
machine.add_state(TalkingState())
machine.add_state(AttitudeControl())

#start off the StateMachine object in ReadyState
machine.go_to_state('ready')

while True:
    machine.update()
