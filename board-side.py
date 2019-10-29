
#screen /dev/tty.usbmodem1411 115200


import board
import digitalio
import time
import supervisor
import busio

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

while True:
    if supervisor.runtime.serial_bytes_available:
        inText = input().strip()
        print("hello")
        # Sometimes Windows sends an extra (or missing) newline - ignore them
        if inText == "":
            continue
        else:
            print(inText)
            led.value = True
            time.sleep(5)
            led.value = False
        #print("received")
