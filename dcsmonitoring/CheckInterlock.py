import datetime
import time
import serial
import os
import re
import subprocess

#subprocess.call('python3 ControlArduino.py', creationflags=subprocess.CREATE_NEW_CONSOLE) #windows
#subprocess.Popen("python3 ControlArduino.py", shell=True)
subprocess.run("python3 ControlArduino.py&", shell=True)
print("it worked")

'''
AllOkay = 2;

while True:
    ser = serial.Serial('/dev/ttyACM0',9600)
    b = ser.readline()
    string_n = b.decode()
    string = string_n.rstrip()
    try:
        temperature, air_humid, temperature_moduleN, dew_pt, IsPressure, IsVac, IsLidClosed, IsOkay = string.split()
        AllOkay = int(IsOkay)
    except ValueError:
        print("Oooops! Arduino issue, not getting four numbers. Try again ...")
    print(AllOkay)
    time.sleep(3)
    
'''
