import serial
import io
# import pyvisa

chiller_port = "/dev/ttyUSB0"
#print(chiller_port)
ser = serial.Serial("/dev/ttyUSB0", 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)


## Read version
def read_version(chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
    ser.write(str.encode('version\r\n'))
#read_version(chiller_port)

# ## Read status
def read_status(c):
    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
    ser.write(str.encode('status\r\n'))

def chiller_on_off(switch_val, chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
    ser.write(str.encode('out_mode_05 {};\r\n'.format(switch_val)))

# ## Turn on chiller switch_val = 1 for on and 0 for off
def chiller_on(chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
    ser.write(str.encode('out_mode_05 1;\r\n'))

def chiller_off(chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
    ser.write(str.encode('out_mode_05 0;\r\n'))

## Setting power
def set_power(power_val, chiller_port = chiller_port ):
    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
    ser.write(str.encode('OUT_HIL_00 {};\r\n'.format(power_val)))

## Set Temperature
def set_temp( temp_val, chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
    ser.write(str.encode('out_sp_00 {};\r\n'.format(temp_val)))

# ## read working temp need to run this before while loop or read_bath function
'''
def read_set_temp(chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
    ser.write(str.encode('in_sp_00;\r\n'))
    return r_temp_r

# ## read current bath temp and while loop starts here
def read_bath(r_temp_r , chiller_port = chiller_port):

    ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
    bath = ser.write(str.encode('in_pv_00;\r\n'))
    #r_bath = ser.read_until(expected='\r\n')
    r_bath = ser.readline()
    set_temp = False

    while r_bath > r_temp_r:
        ser = serial.Serial(chiller_port, 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
        bath = ser.write(str.encode('in_pv_00;\r\n'))
        #r_bath = ser.read_until(expected='\r\n')
        r_bath = ser.readline()
    else:
        set_temp = True

    return set_temp
'''

