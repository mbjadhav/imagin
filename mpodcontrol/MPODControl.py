import os
import argparse
import subprocess
import re

parser = argparse.ArgumentParser(description="Script to control Weiner MPod")
parser.add_argument("-ch","--channel",dest="channel",required=True,type=str)
parser.add_argument("-v","--voltage",dest="voltage",required=True,type=float)

#parser = argparse.ArgumentParser(description="Script to control Weiner MPod")
#parser.add_argument("-ch","--channel",dest="channel",required=True,type=str)
#parser.add_argument("-v","--voltage",dest="voltage",required=True,type=float)

#opt = parser.parse_args()
#channel = opt.channel
#voltage = opt.voltage

class MPODControl():
    def __init__(self,  channel=0, value=0, voltage=0, current=0):
        self.channel=channel
        self.value=value
        self.voltage=voltage
        self.current=current

    def channel_switch(self, channel, value):
        #os.system("snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru 192.168.200.50 outputVoltage.u{} F 0".format(channel))
        command = "snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru 192.168.200.50 outputSwitch.u{} i {}".format(channel,value)
        os.system(command)

    def read_voltageRate(self, channel):
        command = "snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public 192.168.200.50 outputVoltageRiseRate.u{}".format(channel)
        vratestr= subprocess.check_output(command, shell=True)
        vratestr = vratestr.decode('utf-8')
        vrate = re.findall(r'\d+\.\d+', vratestr)
        return float(vrate[0])
         
    def read_voltage(self, channel):
        command = "snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public 192.168.200.50 outputVoltage.u{}".format(channel)
        vstr= subprocess.check_output(command, shell=True)
        vstr = vstr.decode('utf-8')
        vbias = re.findall(r'\d+\.\d+', vstr)
        return float(vbias[0])
        
    def read_senseVoltage(self, channel):
        command = "snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public 192.168.200.50 outputMeasurementSenseVoltage.u{}".format(channel)
        vstr= subprocess.check_output(command, shell=True)
        vstr = vstr.decode('utf-8')
        vbias = re.findall(r'\d+\.\d+', vstr)
        return float(vbias[0])

    def read_current(self, channel):
        command = "snmpget -Oqv -v 2c -m +WIENER-CRATE-MIB -c public 192.168.200.50 outputCurrent.u{}".format(channel)
        #ileakage = os.system(command) 
        istr= subprocess.check_output(command, shell=True)
        istr = istr.decode('utf-8')
        ileakage = re.findall(r'\d+\.\d+', istr)
        return float(ileakage[0])

    def read_measCurrent(self, channel):
        command = "snmpget -Op +2.9 -Oqv -v 2c -m +WIENER-CRATE-MIB -c public 192.168.200.50 outputMeasurementCurrent.u{}".format(channel)
        #ileakage = os.system(command) 
        istr= subprocess.check_output(command, shell=True)
        istr = istr.decode('utf-8')
        ileakage = re.findall(r'\d+\.\d+', istr)
        return float(ileakage[0])

    def set_voltageRate(self, channel, rate):
        command = "snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru 192.168.200.50 outputVoltageRiseRate.u{} F {}".format(channel,rate)
        os.system(command)    
        return

    def set_voltage(self, channel, voltage):
        command = "snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru 192.168.200.50 outputVoltage.u{} F {}".format(channel,voltage)    
        os.system(command)

    def set_current(self, channel, current):
        command = "snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru 192.168.200.50 outputCurrent.u{} F {}".format(channel,current)    
        os.system(command)

    def set_voltageCurrent(self, channel, voltage, current):
        command1 = "snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru 192.168.200.50 outputVoltage.u{} F {}".format(channel,voltage)
        command2 = "snmpset -Oqv -v 2c -m +WIENER-CRATE-MIB -c guru 192.168.200.50 outputCurrent.u{} F {}".format(channel,current)    
        os.system(command1)        
        os.system(command2)

# #Read voltage on that channel
# channel_read(channel)
# #Change voltage of that channel
# channel_changeVoltage(channel,voltage)
# #Read voltage on that channel
# channel_read(channel)
# #Change voltage of that channel to 0
# channel_changeVoltage(channel,0)
# #Read voltage of that channel
# channel_read(channel)
# #Turn off channel
# channel_switch(channel,0)
