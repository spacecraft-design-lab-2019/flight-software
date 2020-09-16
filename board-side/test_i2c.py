from pycubedmini import pocketqube as pq
import drv8830
import time

device_list={
    0x6B:'IMU',
    0x29:'Z Panel Sun Sensor',
    0x39:'Y Panel Sun Sensor',
    0x49:'X Panel Sun Sensor',

    0x60:'Z Panel H-Bridge Driver',
    0x62:'Y Panel H-Bridge Driver',
    0x66:'X Panel H-Bridge Driver',
}

for n,i2c in enumerate((pq.i2c1,pq.i2c2,pq.i2c3)):
    print('------ I2C Scan Bus #{}------'.format(n+1))
    while not i2c.try_lock():
        pass
    for _ in range(5):
        dev=i2c.scan()
        print("I2C Bus #{} addresses found: {}".format(n+1,[hex(device_address) for device_address in dev]))
        time.sleep(1)
    i2c.unlock()

