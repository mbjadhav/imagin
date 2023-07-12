import pyvisa
from pyvisa import constants
import re

def channel(device, channel):
    device.write("INST:NSEL {}".format (channel))

def whichChannel(device):
    channel = device.query("INST:NSEL?")
    return(channel)

def peltier_on_off(device, Nch, on_off):
    channel(device, Nch)
    device.write("OUTP {}".format(on_off))

def hmp_on_off(device, Nch, on_off):
    channel(device, Nch)
    device.write("OUTP {}".format(on_off))

def setVolt(device, voltage):
    device.write("APPL {}".format(voltage))

def setVoltCurr(device, Nch, voltage, current):
    channel(device, Nch)
    device.write("APPL {}, {}".format(voltage, current))

def getVoltCurr(device, Nch):
    channel(device, Nch)
    voltcurr = device.query("APPL?")
    getvoltcurr = re.findall(r'\d+\.\d+', voltcurr)
    return(getvoltcurr)

def measVolt(device, Nch):
    channel(device, Nch)
    measvolt = device.query("MEAS:VOLT?")
    return(measvolt)

def measCurr(device, Nch):
    channel(device, Nch)
    meascurr = device.query("MEAS:CURR?")
    return(meascurr)

def measVoltCurr(device, Nch):
    channel(device, Nch)
    #measvoltcurr = device.query("MEAS?")
    measvoltcurr = (device.query("MEAS:VOLT?"), device.query("MEAS:CURR?"))
    return(measvoltcurr)

def connectRohdeS():
    rm = pyvisa.ResourceManager("@py")
    #print(rm.list_resources())
    device = rm.open_resource("ASRL/dev/ttyACM1::INSTR",baud_rate=9600, data_bits=8, parity=constants.Parity.none, stop_bits=constants.StopBits.one, write_termination="\n",read_termination="\n")
    return(device)
