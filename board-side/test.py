"""
This is a simple test script to show that the method 
supervisor.runtime.serial_bytes_available does NOT work.

After the first loop iteration, you will notice that on the
PyCubed Mini, the LED stays blue. It never returns to the
blue-red oscillation. In other words, the nested
while loop is never running.
"""

import supervisor
from pycubedmini import cubesat
import time

time.sleep(5)
print(b'board first message')


while True:
    while not supervisor.runtime.serial_bytes_available:
        cubesat.RGB = (255, 0, 0)
        time.sleep(.5)
        cubesat.RGB = (0, 255, 0)
        time.sleep(.5)
        
    cubesat.RGB = (0, 0, 255)
    x = input()
    print(b'I got the following:')
    print(x)
    cubesat.RGB = (255, 255, 0)
    time.sleep(5)