import smbus
import time
import math
import os
import subprocess
import re
import math

bus = smbus.SMBus(1)

SHT85_ADDR       = 0x44 # Device Adress
SHT85_SS         = 0x24 # Single Shot Data Acquisition Mode
SHT85_SS_2       = {'HIGH' : 0x00, 'MEDIUM' : 0x0B, 'LOW' : 0x16} # Repeatability: (HIGH, MEDIUM, LOW)
SHT85_READ       = 0x00 # Read output

rep='HIGH'
bus.write_i2c_block_data(SHT85_ADDR,SHT85_SS,[SHT85_SS_2[rep]])
time.sleep(1)
data   = bus.read_i2c_block_data(SHT85_ADDR,SHT85_READ,6)
print(data)

t_data = data[0] << 8 | data[1]
h_data = data[3] << 8 | data[4]
temp = -45. + 175. * t_data / (2**16-1.)
relh = 100. * h_data / (2**16-1.)

print('Temperature:')
print(temp)
print('Humidity:')
print(relh)

Vin = 3.3
Rref = 1760
BetaValue = 3892
R25 = 1000
T25 = 298.15
Tk2c = 275.15
command ="ioplus 0 adcrd 1"
Vout_str = subprocess.check_output(command, shell=True)
Vout_str = Vout_str.decode('utf-8')
Vout=re.findall(r'\d+\.\d+', Vout_str)
Vout_ntc = float(Vout[0])
Rntc = Rref*(Vout_ntc/(Vin-Vout_ntc))
Tntc = 1/(math.log10(Rntc/R25)/BetaValue+1/T25)- Tk2c
print(Tntc)

#bus.write_byte(0x44, 0xF3)
#data0 = bus.read_byte(0x44)
#wprint(data0)
