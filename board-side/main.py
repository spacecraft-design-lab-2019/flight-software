import time
import board
import busio
import adafruit_tsl2561
import sensor_reads as sensor
# Create the I2C bus
i2c = busio.I2C(board.SCL1, board.SDA1)
i1c = busio.I2C(board.SCL2, board.SDA2)
# Create the TSL2561 instance, passing in the I2C bus
zplus = adafruit_tsl2561.TSL2561(i2c,0x29)
yplus = adafruit_tsl2561.TSL2561(i2c,0x39)
xminus = adafruit_tsl2561.TSL2561(i2c,0x49)
zminus = adafruit_tsl2561.TSL2561(i1c,0x29)
xplus = adafruit_tsl2561.TSL2561(i1c,0x49)

# Print chip info
#print("Chip ID = {}".format(tsl1.chip_id))
#print("Enabled = {}".format(tsl1.enabled))
#print("Gain = {}".format(zplus.gain))
#print("Integration time = {}".format(zplus.integration_time))
print("Configuring TSL2561...")
while True:
    # Enable the light sensor
    zplus.enabled = True
    yplus.enabled = True
    xminus.enabled = True
    zminus.enabled = True
    xplus.enabled = True
    time.sleep(1)
    # Set gain 0=1x, 1=16x
    zplus.gain = 0
    yplus.gain = 0
    xminus.gain = 0
    zminus.gain = 0
    xplus.gain = 0
    # Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
    zplus.integration_time = 1
    yplus.integration_time = 1
    xminus.integration_time = 1
    zminus.integration_time = 1
    xplus.integration_time = 1
    print("Getting readings...")
    # Get raw (luminosity) readings individually
    zplus_broad = zplus.broadband
    yplus_broad = yplus.broadband
    xminus_broad = xminus.broadband
    zminus_broad = zminus.broadband
    xplus_broad = xplus.broadband

    print(zplus_broad)
    print(yplus_broad)
    print(xminus_broad)
    print(zminus_broad)
    print(xplus_broad)

    r_sat = [1000,1000,30000]
    q_eci2body = [.8,.2,.4,.3]
    sunvec = sensor.sense2vector([xplus_broad, xminus_broad,yplus_broad,0,zplus_broad,zminus_broad], r_sat, q_eci2body, albedo = True)
    print(sunvec)

    time.sleep(1)
    # Disble the light sensor (to save power)
#     tsl.enabled = False