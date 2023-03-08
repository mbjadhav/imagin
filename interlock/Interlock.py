import RPi.GPIO as GPIO
import os
import argparse
import subprocess
import re
import serial
import sys
import time
import math

from relayboard import RelayBoard
from sht85 import SHT85
from steppermotor import StepperMotor

class Interlock():
    def __init__(self, interlock = 0):
        self.Interlock = interlock

    def check_interlock(self):
        print("okay")

    def get_sht85value(self, temp=0, rh=0, dp=0):
        temp, rh = SHT85.read_data()
        dp = SHT85.dew_point(temp, rh)
        sht85values = (temp, rh, dp)    
        return sht85values

    def get_tempchuck(self, tempchuck=0):
        tempchuck = RelayBoard.get_temperature(1)
        return tempchuck

    def get_tempmodule(self, tempmodule=0):
        tempmodule = RelayBoard.get_temperature(2)
        return tempmodule

    def get_lidswitch(self, lidswitch=0):
        lidswitch = RelayBoard.optrd(6)
        return lidswitch
    
    def get_vacuumswitch(self, vacuumswitch=1):
        vacuumswitch = RelayBoard.optrd(7)
        return vacuumswitch

    def get_pressureswitch(self, pressureswitch=1):
        pressureswitch = RelayBoard.optrd(8)
        return pressureswitch
    
    






