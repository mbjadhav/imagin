import serial
import io
# import pyvisa

chiller_port = "/dev/ttyUSB0"
print(chiller_port)
## Read version
def read_version(chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 9600, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
    version = ser.write(str.encode('version\r\n'))
    # r_version = ser.read_until(expected='\r\n')
    r_version = ser.readline()

    print (r_version)
    ser.close()
read_version(chiller_port)
# ## Read status
def read_status(chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 9600, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
    status = ser.write(str.encode('status\r\n'))
    # r_status = ser.read_until(expected='\r\n')
    r_status = ser.readline()

    print(r_status)
    ser.close()

# ## Turn on chiller switch_val = 1 for on and 0 for off
def on_off(switch_val, chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 9600, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
    # switch = ser.write('out_mode_05=%f;\r\n'%(switch_val))
    switch = ser.write(str.encode('out_mode_05=%f;\r\n'%(switch_val)))
    # r_switch = ser.read_until(expected='\r\n')
    r_switch = ser.readline()
    
    ser.close()

# on_off(chiller_port,1)
## Setting power
def set_power(power_val, chiller_port = chiller_port ):
    ser = serial.Serial(chiller_port, 9600, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
    power = ser.write(str.encode('OUT_HIL_00=%f;\r\n'%(power_val)))
    # r_power = ser.read_until(expected='\r\n')
    r_power = ser.readline()
    ser.close()


## Set Temperature
def set_temp( temp_val, chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 9600, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
    temp = ser.write(str.encode('out_sp_00= %f;\r\n'%(temp_val)))
    # r_temp = ser.read_until(expected='\r\n')
    r_temp = ser.readline()
    ser.close()

# ## read working temp need to run this before while loop or read_bath function
def read_set_temp(chiller_port = chiller_port):
    ser = serial.Serial(chiller_port, 9600, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
    temp_r = ser.write(str.encode('in_sp_00;\r\n'))
    # r_temp_r = ser.read_until(expected='\r\n')
    r_temp_r = ser.readline()
    print(r_temp_r)
    ser.close()
    return r_temp_r
# ## read current bath temp and while loop starts here
def read_bath(r_temp_r , chiller_port = chiller_port):

    ser = serial.Serial(chiller_port, 9600, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
    bath = ser.write(str.encode('in_pv_00;\r\n'))
    # r_bath = ser.read_until(expected='\r\n')
    r_bath = ser.readline()
    print(r_bath)
    set_temp = False

    while r_bath > r_temp_r:
        ser.close()
        ser = serial.Serial(chiller_port, 9600, bytesize = 8,timeout = 5, parity = serial.PARITY_NONE, xonxoff = 1)
        bath = ser.write(str.encode('in_pv_00;\r\n'))
        # r_bath = ser.read_until(expected='\r\n')
        r_bath = ser.readline()
        ser.close()
    else:
        set_temp = True
        ser.close()

    return set_temp


