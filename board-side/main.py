import time
import board
import busio
import adafruit_tsl2561
import sensor_reads as sensor
# Create the I2C bus
i2c = busio.I2C(board.SCL1, board.SDA1)
i1c = busio.I2C(board.SCL2, board.SDA2)
# Create the TSL2561 instance, passing in the I2C bus
tsl1 = adafruit_tsl2561.TSL2561(i2c,0x39)
tsl2 = adafruit_tsl2561.TSL2561(i2c,0x49)
tsl3 = adafruit_tsl2561.TSL2561(i1c,0x29)
# Print chip info
#print("Chip ID = {}".format(tsl1.chip_id))
#print("Enabled = {}".format(tsl1.enabled))
#print("Gain = {}".format(tsl1.gain))
#print("Integration time = {}".format(tsl1.integration_time))
print("Configuring TSL2561...")
while True:
    # Enable the light sensor
    tsl1.enabled = True
    tsl2.enabled = True
    tsl3.enabled = True
    time.sleep(1)
    # Set gain 0=1x, 1=16x
    tsl1.gain = 0
    tsl2.gain = 0
    tsl3.gain = 0
    # Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
    tsl1.integration_time = 1
    tsl2.integration_time = 1
    tsl3.integration_time = 1
    print("Getting readings...")
    # Get raw (luminosity) readings individually
    broadband1 = tsl1.broadband
    broadband2 = tsl2.broadband
    broadband3 = tsl3.broadband
    
    r_sat = [1000,1000,30000]
    q_eci2body = [.8,.2,.4,.3]
    sunvec = sensor.sense2vector([broadband1, 0,broadband2,0,broadband3,0], r_sat, q_eci2body, albedo = True)
    print(sunvec)

    time.sleep(1)
    # Disble the light sensor (to save power)
#     tsl.enabled = False