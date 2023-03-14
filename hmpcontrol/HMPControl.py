import pyvisa
from pyvisa import constants
import serial
import io

from HMPControlTools import *

device = connectRohdeS()
#channel(device, 2)
setVoltCurr(device, 2, 2, 4.6)
peltier_on_off(device,2,0)
values=measVoltCurr(device, 2)
print(values)
#print(whichChannel(device))
#rm = pyvisa.ResourceManager("@py")
#print(rm.list_resources())
#device = rm.open_resource("ASRL/dev/ttyACM0::INSTR",baud_rate=9600, data_bits=8, parity=constants.Parity.none, stop_bits=constants.StopBits.one, write_termination="\n",read_termination="\n")

#ser = serial.Serial("/dev/ttyUSB3", 4800, bytesize = 8,timeout = 5, parity = serial.PARITY_EVEN, xonxoff = 1)
#ser.write(str.encode('out_mode_05 0;\r\n'))