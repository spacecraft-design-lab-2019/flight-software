import serial
import time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/tty.usbmodem1411'
ser.timeout = .01 #why this specific timeout value?
print(ser)
ser.open()
print(ser.is_open)

while True:
    bytes_to_read = ser.inWaiting()
    #print('number of bytes to read: %s' %bytes_to_read)
    if bytes_to_read:
        x = ser.read(bytes_to_read).strip().decode('ascii')
        print("received: {}".format(x))
        if x == 'ready':
            to_send = '1\r\n'
            print('writing to serial: %s' %to_send)
            ser.write(to_send.encode('ascii'))

ser.close()
print(ser.is_open)
