import time
import math

from SHT85 import *
mps = 1 # accepted intervals 0.5, 1, 2, 4, 10 seconds
rep = 'HIGH' # Repeatability: HIGH, MEDIUM, LOW

#print ('serial number = ', sht85.sn())
time.sleep(0.5e-3)

periodic(mps,rep)
time.sleep(1)
try:
    while True:
        t,rh = read_data()
        dp = dew_point(t,rh)
        print('Time =', time.strftime("%Y%m%d%H%M%S"))
        print ('Temperature =', t)
        print ('Relative Humidity =', rh)
        print ('Dew Point =', dp)
        time.sleep(mps)

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Killing Thread...")
    time.sleep(0.5e-3)
    stop()

stop()
