import os
import argparse
import subprocess
import re
import serial
import sys
import time
import math

class RelayBoard():
    def __init__(self,  channel=0, value=0, stack=0):
        self.channel=channel
        self.value=value
        self.stack=0

    #Relay commands
    #-------------------------------------------------------------------------------------
    def reltest(self):
        command = "ioplus {} reltest".format(self.stack)
        os.system(command)

    def relwr(self, channel, value): #value 0 - off, 1 - on
        command = "ioplus {} relwr {} {}".format(self.stack,channel,value)
        os.system(command)

    def relrd(self, channel): #value 0 - off, 1 - on
        command = "ioplus {} relrd {}".format(self.stack,channel)
        relread= subprocess.check_output(command, shell=True)
        relread = relread.decode('utf-8')
        #relrd = re.findall(r'\d+\.\d+', relread)
        return int(relread)

    #GPIO commands
    #-------------------------------------------------------------------------------------
    def gpiowr(self, channel, value): #value 0 - off, 1 - on
        command = "ioplus {} gpiowr {} {}".format(self.stack,channel,value)
        os.system(command)

    def gpiord(self, channel): #value 0 - off, 1 - on
        command = "ioplus {} gpiord {}".format(self.stack,channel)
        gpioread= subprocess.check_output(command, shell=True)
        gpioread = gpioread.decode('utf-8')
        #gpiord = re.findall(r'\d+\.\d+', gpioread)
        return int(gpioread)

    def gpiodirwr(self, channel, value): #direction value 0 - out, 1 - in
        command = "ioplus {} gpiodirwr {} {}".format(self.stack,channel,value)
        os.system(command)

    def gpiodirrd(self, channel): #direction value 0 - out, 1 - in
        command = "ioplus {} gpiodirrd {}".format(self.stack,channel)
        gpiodirread= subprocess.check_output(command, shell=True)
        gpiodirread = gpiodirread.decode('utf-8')
        #gpiodirrd = re.findall(r'\d+\.\d+', gpiodirread)
        return int(gpiodirread)

    #ADC input & DAC output voltage commands
    #-------------------------------------------------------------------------------------
    def dacwr(self, channel, value): #Write DAC output voltage value (0 to 10V)
        command = "ioplus {} dacwr {} {}".format(self.stack,channel,value)
        os.system(command)

    def dacrd(self, channel): #Read DAC output voltage value (0 - 10V)
        command = "ioplus {} dacrd {}".format(self.stack,channel)
        dacread= subprocess.check_output(command, shell=True)
        dacread = dacread.decode('utf-8')
        #dacrd = re.findall(r'\d+\.\d+', dacread)
        return float(dacread)

    def adcrd(self, channel): #Read ADC input voltage value (0 - 3.3V)
        command = "ioplus {} adcrd {}".format(self.stack,channel)
        adcread= subprocess.check_output(command, shell=True)
        adcread = adcread.decode('utf-8')
        #adcrd = re.findall(r'\d+\.\d+', adcread)
        return float(adcread)

    #Optocoupled inputs commands
    #-------------------------------------------------------------------------------------
    def optrd(self, channel): #Read optocoupled input values (0 - 1)
        command = "ioplus {} optrd {}".format(self.stack,channel)
        optread= subprocess.check_output(command, shell=True)
        optread = optread.decode('utf-8')
        #optrd = re.findall(r'\d+\.\d+', optread)
        return int(optread)

    #Open drain output commands
    #-------------------------------------------------------------------------------------
    def odwr(self, channel, value): #Write open drain output pwm value (0% - 100%)
        command = "ioplus {} odwr {} {}".format(self.stack,channel,value)
        os.system(command)

    def odrd(self, channel): #Read open drain output pwm value (0% - 100%)
        command = "ioplus {} odrd {}".format(self.stack,channel)
        odread= subprocess.check_output(command, shell=True)
        odread = odread.decode('utf-8')
        #odrd = re.findall(r'\d+\.\d+', odread)
        return float(odread)

    #Temperature calculation for the chuck (PT102)
    #-------------------------------------------------------------------------------------
    def getTemperature(self, channel): #Ch1 for chuck PT102 and ch2 for module NTC
        Vin = 3.3
        Rref = 1760
        BetaValue = 3892
        R25 = 1000
        T25 = 298.15
        Tk2c = 275.15
        Vout_ntc = self.adcrd(channel)
        Rntc = Rref*(Vout_ntc/(Vin-Vout_ntc))
        Tntc = 1/(math.log10(Rntc/R25)/BetaValue+1/T25)- Tk2c
        return Tntc

