import os
import argparse
import subprocess
import re
import serial
import sys
import time

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

    def relrd(self, channel):
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

    def gpiord(self, channel):
        command = "ioplus {} gpiord {}".format(self.stack,channel)
        gpioread= subprocess.check_output(command, shell=True)
        gpioread = gpioread.decode('utf-8')
        #relrd = re.findall(r'\d+\.\d+', gpioread)
        return int(gpioread)

    def gpiodirwr(self, channel, value): #direction value 0 - out, 1 - in
        command = "ioplus {} gpiodirwr {} {}".format(self.stack,channel,value)
        os.system(command)

    def gpiodirrd(self, channel):
        command = "ioplus {} gpiodirrd {}".format(self.stack,channel)
        gpiodirread= subprocess.check_output(command, shell=True)
        gpiodirread = gpiodirread.decode('utf-8')
        #relrd = re.findall(r'\d+\.\d+', gpiodirread)
        return int(gpiodirread)

    #ADC input & DAC output voltage commands
    #-------------------------------------------------------------------------------------
    def dacwr(self, channel, value): #Write DAC output voltage value (0 to 10V)
        command = "ioplus {} dacwr {} {}".format(self.stack,channel,value)
        os.system(command)

    def adcrd(self, channel): #Read ADC input voltage value (0 - 3.3V)
        command = "ioplus {} adcrd {}".format(self.stack,channel)
        adcread= subprocess.check_output(command, shell=True)
        adcread = gpioread.decode('utf-8')
        #relrd = re.findall(r'\d+\.\d+', adcread)
        return float(adcread)

    #Optocoupled inputs commands
    #-------------------------------------------------------------------------------------


    #output voltage commands
    #-------------------------------------------------------------------------------------

    #Open drain output commands
    #-------------------------------------------------------------------------------------
