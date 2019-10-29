import serial
import time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/tty.usbmodem1411'
ser.timeout = 0.01
print(ser)
ser.open()
print(ser.is_open)
ser.write(b'100\r\n')
x = ser.read(5)
# x = ser.readlines()
print("received: {}".format(x))
# out = ''
# time.sleep(1)
# while ser.inWaiting() > 0:
#     print("here 1")
#     out += ser.readline().decode().strip()
#     #out += o.decode('utf-8')
#     print(out)
# if out != '':
#     print(">>" + out)
time.sleep(1)
ser.close()
print(ser.is_open)
