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


class Satellite:
    def __init__(self):
        """
        Big init routine as the whole board is brought up. 
        """
        self.hardware = {} # initialize a dictionary of hardware available


        # Initialize Neopixel (LED)
        try:
            self.neopixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.5, auto_write=False)
            self.neopixel[0] = (0,0,0)
            self.hardware['Neopixel'] = True
        except Exception as e:
            print('[WARNING][Neopixel]',e)


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