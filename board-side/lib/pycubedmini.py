"""
CircuitPython driver for PyCubed Mini satellite board

PyCubed Mini

* Author(s): Max Holliday, Hridu Jain


REFERENCE:
use Max's driver file as reference for building this one:
https://www.notion.so/pycubed-py-b80aabda74284488bfd9b8ef46a0eba2#183edc9a066a43a5a78705566592221f
https://github.com/pycubed/software/blob/master/default%20libraries/mainboard-v04/pycubed.py

"""
import time
import board
import neopixel
import busio
import adafruit_sdcard
from digitalio import DigitalInOut
import bmx160


# logger = computerlogger
# logger = locallogger

class Satellite:
    def __init__(self):
        """
        Big init routine as the whole board is brought up.
        """

         # initialize a dictionary of hardware available
        self.hardware = {
                         'Neopixel': False,
                         'IMU': False,
                         'SDCard': False
                         }


        self.i2c = busio.I2C(board.SCL1, board.SDA1)
        self.spi = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # Initialize Neopixel (LED)
        try:
            self.neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.5, auto_write=False)
            self.neopixel[0] = (0,0,0)
            self.hardware['Neopixel'] = True
        except Exception as e:
            print('[WARNING][Neopixel]', e)

        # Initialize the BMX160:
        try:
            self.imu = bmx160.BMX160_I2C(i2c)
            self.hardware['IMU'] = True
        except Exception as e:
            print('[WARNING][IMU]', e)

        # Initialize the SDCard
        try:
            cs_sd = DigitalInOut(board.CS_SD)
            self.sdcard = adafruit_sdcard.SDCard(spi, cs_sd)

            # Use the filesystem as normal. Files are under "/sd"
            vfs = storage.VfsFat(self.sdcard)
            storage.mount(vfs, "/sd")
            sys.path.append("/sd")
            self.hardware['SDCard'] = True
        except Exception as e:
            print('[WARNING][SDCard]', e)





    # query/set color of Neopixel (LED)
    @property
    def RGB(self):
        return self.neopixel[0]
    @RGB.setter
    def RGB(self,value):
        if self.hardware['Neopixel']:
            try:
                self.neopixel[0] = value
                self.neopixel.show()
            except Exception as e:
                print('[WARNING]',e)


cubesat = Satellite()