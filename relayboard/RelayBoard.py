import os
import argparse
import subprocess
import re
import serial
import sys
import time
import math

stack=0

class RelayBoard():
    def __init__(self,  channel=0, value=0, stack=0):
        self.channel=channel
        self.value=value
        #stack=0

    #Relay commands
    #-------------------------------------------------------------------------------------
    def reltest():
        command = "ioplus {} reltest".format(stack)
        os.system(command)

    def relwr(channel, value): #value 0 - off, 1 - on
        command = "ioplus {} relwr {} {}".format(stack,channel,value)
        os.system(command)

    def relrd(channel): #value 0 - off, 1 - on
        command = "ioplus {} relrd {}".format(stack,channel)
        relread= subprocess.check_output(command, shell=True)
        relread = relread.decode('utf-8')
        #relrd = re.findall(r'\d+\.\d+', relread)
        return int(relread)

    #GPIO commands
    #-------------------------------------------------------------------------------------
    def gpiowr(channel, value): #value 0 - off, 1 - on
        command = "ioplus {} gpiowr {} {}".format(stack,channel,value)
        os.system(command)

    def gpiord(channel): #value 0 - off, 1 - on
        command = "ioplus {} gpiord {}".format(stack,channel)
        gpioread= subprocess.check_output(command, shell=True)
        gpioread = gpioread.decode('utf-8')
        #gpiord = re.findall(r'\d+\.\d+', gpioread)
        return int(gpioread)

    def gpiodirwr(channel, value): #direction value 0 - out, 1 - in
        command = "ioplus {} gpiodirwr {} {}".format(stack,channel,value)
        os.system(command)

    def gpiodirrd(channel): #direction value 0 - out, 1 - in
        command = "ioplus {} gpiodirrd {}".format(stack,channel)
        gpiodirread= subprocess.check_output(command, shell=True)
        gpiodirread = gpiodirread.decode('utf-8')
        #gpiodirrd = re.findall(r'\d+\.\d+', gpiodirread)
        return int(gpiodirread)

    #ADC input & DAC output voltage commands
    #-------------------------------------------------------------------------------------
    def dacwr(channel, value): #Write DAC output voltage value (0 to 10V)
        command = "ioplus {} dacwr {} {}".format(stack,channel,value)
        os.system(command)

    def dacrd(channel): #Read DAC output voltage value (0 - 10V)
        command = "ioplus {} dacrd {}".format(stack,channel)
        dacread= subprocess.check_output(command, shell=True)
        dacread = dacread.decode('utf-8')
        #dacrd = re.findall(r'\d+\.\d+', dacread)
        return float(dacread)

    def adcrd(channel): #Read ADC input voltage value (0 - 3.3V)
        command = "ioplus {} adcrd {}".format(stack,channel)
        adcread= subprocess.check_output(command, shell=True)
        adcread = adcread.decode('utf-8')
        #adcrd = re.findall(r'\d+\.\d+', adcread)
        return float(adcread)

    #Optocoupled inputs commands
    #-------------------------------------------------------------------------------------
    def optrd(channel): #Read optocoupled input values (0 - 1)
        command = "ioplus {} optrd {}".format(stack,channel)
        optread= subprocess.check_output(command, shell=True)
        optread = optread.decode('utf-8')
        #optrd = re.findall(r'\d+\.\d+', optread)
        return int(optread)

    #Open drain output commands
    #-------------------------------------------------------------------------------------
    def odwr(channel, value): #Write open drain output pwm value (0% - 100%)
        command = "ioplus {} odwr {} {}".format(stack,channel,value)
        os.system(command)

    def odrd(channel): #Read open drain output pwm value (0% - 100%)
        command = "ioplus {} odrd {}".format(stack,channel)
        odread= subprocess.check_output(command, shell=True)
        odread = odread.decode('utf-8')
        #odrd = re.findall(r'\d+\.\d+', odread)
        return float(odread)

    #Temperature calculation for the chuck (PT102)
    #-------------------------------------------------------------------------------------
    def get_temperature(channel): #Ch1 for chuck PT102 and ch2 for module NTC
        Vin = 3.3
        Rref = 1760
        BetaValue = 3892
        R25 = 1000
        T25 = 298.15
        Tk2c = 275.15
        Vout_ntc = RelayBoard.adcrd(channel)
        Rntc = Rref*(Vout_ntc/(Vin-Vout_ntc))
        Tntc = 1/(math.log10(Rntc/R25)/BetaValue+1/T25)- Tk2c
        return round(Tntc, 2)

