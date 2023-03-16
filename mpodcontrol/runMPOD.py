import sys
import serial
import io
import pyvisa
from pyvisa import constants

from MPODControl import MPODControl

sys.path.append('../')
from hmpcontrol.HMPControlTools import *
from chiller.chiller_cf41 import *

#from ControlArduino import *

if __name__ == "__main__":
    mpod = MPODControl()
    channel_LV = 4
    channel_HV = 301

    LV_voltage = 2.4
    LV_current = 6 

    mpod.channel_switch(channel_LV,0)
    mpod.set_voltageCurrent(channel_HV, 0, 0)    
    mpod.channel_switch(channel_HV,0)
    mpod.set_voltageCurrent(channel_LV,LV_voltage,LV_current)

    LV_voltage = mpod.read_senseVoltage(channel_LV) #V
    LV_current = (mpod.read_measCurrent(channel_LV)) #mA

    print(LV_voltage)
    print(LV_current)

    device = connectRohdeS()
    setVoltCurr(device, 2, 2, 4.6)
    peltier_on_off(device,2,0)
    values=measVoltCurr(device, 2)
    #print(values)

    chiller_off()