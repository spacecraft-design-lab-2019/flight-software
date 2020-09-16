from pycubedmini import pocketqube as pq
import time

delay = 1

print('---------- IMU Test ----------')

for _ in range(5):
    # Read acceleration, magnetometer, gyroscope, temperature.
    temp = pq.temperature
    accel_x, accel_y, accel_z = pq.acceleration
    mag_x, mag_y, mag_z       = pq.magnetic
    gyro_x, gyro_y, gyro_z    = pq.gyro

    # Print values.
    print('\tTemperature: {}C'.format(temp))
    print('\tAcc  (m/s^2):   x: {}\ty: {}\tz: {}'.format(accel_x, accel_y, accel_z))
    print('\tMag  (gauss):   x: {}\ty: {}\tz: {}'.format(mag_x, mag_y, mag_z))
    print('\tGyro (deg/sec): x: {}\ty: {}\tz: {}'.format(gyro_x, gyro_y, gyro_z))
    print('')

    # Delay for a second.
    time.sleep(delay)
print('------------------------------')
