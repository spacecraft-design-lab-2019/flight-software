import board
#import digitalio
import time
import supervisor
import os
import sys
import busio
import storage
import adafruit_sdcard
from digitalio import DigitalInOut, Direction, Pull
from adafruit_bus_device.spi_device import SPIDevice

'''
### Feather M4 Express Main Module
## Allan Shtofenmakher
# Spacecraft Design Lab

# AKA main.py
# Reads SD card file names and communicates with OpenMV camera
# and SD card breakout board over SPI
# Features NeoPixel rainbow_cycle to indicate proper operation

# Project Start Date: 21 October 2019
# Last Updated: 31 October 2019

'''


# define helper function to print the contents of the SD
def print_directory(path, tabs=0):
    for file in os.listdir(path):
        try:
            stats = os.stat(path + "/" + file)  # changed from statvfs()
            filesize = stats[6]
            isdir = stats[0] & 0x4000

            if filesize < 1000:
                sizestr = str(filesize) + " by"
            elif filesize < 1000000:
                sizestr = "%0.1f KB" % (filesize / 1000)
            else:
                sizestr = "%0.1f MB" % (filesize / 1000000)

            prettyprintname = ""
            for _ in range(tabs):
                prettyprintname += "   "
            prettyprintname += file
            if isdir:
                prettyprintname += "/"
            print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

            #recursively print directory contents
            if isdir:
                print_directory(path + "/" + file, tabs + 1)
        except:
            print('error')
            pass

def snap_a_pic():
    # initialize loop index i
    i = 0
    while True:

        # increment loop_index, divide by 10, and redefine loop index as remainder
        i = (i+1) % 10  # run from 0 to 9

        # run SPI communication once every ten loops  # CHANGED TO 2
        if (i % 2) == 0:

          # initialize/reset save_to_SD_flag to disable saving
          save_to_SD_flag = 0

          # communicate with camera over SPI
          with camera as spi:

              # prepare hello_buffer
              hello_buffer = bytearray(5)
              spi.write_readinto(b'hello', hello_buffer)
              # spi.write(b'hello')  # for writing only
              # spi.readinto(hello_buffer)  # for reading only

              # convert hello_buffer into string using strange workaround
              hello_buffer_string = ''.join(chr(b) for b in hello_buffer)

              # print message received from camera
              print('buffer string: ' + hello_buffer_string)

              # continue if the proper hello_buffer_string has been received
              if hello_buffer_string == 'ready':

                  # prepare new size_buffer
                  size_buffer = bytearray(5)

                  # receive image size from camera
                  spi.write_readinto(b'<OwO>', size_buffer)

                  # convert bytearray to string
                  image_size_string = ''.join(chr(b) for b in size_buffer)

                  # try to convert image_size_string to integer and continue onwards
                  try:

                      # convert string to number
                      image_size = int(image_size_string)

                      # print size of image to terminal
                      print('number of bytes in photo: ' + image_size_string)

                      # prepare buffer to receive image from camera
                      image_buffer = bytearray(image_size)

                      # indicate start of image transmission
                      print("Receiving image . . . ")

                      # send dummy bytearray; receive image
                      spi.write_readinto(image_buffer, image_buffer)

                      if image_buffer:

                          # indicate completion of image transmission
                          print("Image received!")

                          # print converted image for troubleshooting
                          #print(image_buffer)

                          # change save_to_SD_flag to save image at end of loop
                          save_to_SD_flag = 1

                      else:

                          # indicate failure of image transmission
                          print('')
                          print('Failed to receive message.  File not saved to SD card.')
                          print('')

                  # if not possible, print error message
                  except:

                      # print error message if image_size_string is not numeric
                      print('')
                      print("Message received from camera: " + image_size_string)
                      print("cannot be converted to integer.")
                      print('')

              # strange workaround to enable printing bytearray buf (for troubleshooting)
              # print(''.join(chr(b) for b in hello_buffer))

              # slow down the process
              time.sleep(0.1)

          # if image was received, save image to SD
          if save_to_SD_flag:

              # indicate start of save
              print("Saving data . . . ")

              # write image to file
              with open('/sd/picture1.jpg', 'wb') as f:
                  f.write(image_buffer)

              '''
              ### Run this section to test SD card's read/write abilities
              # read image from file
              with open('/sd/picture1.jpg', 'rb') as f:
                  image_data = f.read()

              # save image under different name
              with open('/sd/picture2.jpg', 'wb') as f:
                  f.write(image_data)
              '''

              # print success message
              print('Save completed!')
              break
