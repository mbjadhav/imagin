import pyvisa as visa
import time
import sys
import signal
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from CAEN_PS import *

delay = 2

def plot_IVcurve(channel, Vmin=0, Vmax=10, Vstep=1, Vrate=1.0):
    
    nsteps = (Vmax-Vmin)/Vstep
    arrVoltage = np.empty(int(nsteps+1), dtype=object)
    arrCurrent = np.empty(int(nsteps+1), dtype=object)
    #print(Vrate)
    caen = SimpleCaenPowerSupply()
    caen.Set_Compliance(500, 50)
    #mpod.set_voltageRate(channel, Vrate)
    caen.channel_switch(channel, "ON")
    #mpod.channel_switch(channel,1)
    caen.set_voltage(channel,Vmin)
    voltage = caen.voltage_monitor_value(channel, delay)

    for i in range(0, int(nsteps+1)):
        arrVoltage[i] = voltage
        caen.set_voltage(channel,arrVoltage[i])
        #print(time.strftime("%H%M%S"))
        while True:
            Vcheck = caen.voltage_monitor_value(channel, delay)
            print("still here")
            if abs(Vcheck-arrVoltage[i])<=0.5:
                break
        #print(time.strftime("%H%M%S"))
        time.sleep(2)
        arrCurrent[i] = caen.current_monitor_value(channel, delay)
        arrCurrent[i]=arrCurrent[i]
        print(arrCurrent[i])
        voltage=voltage+Vstep
        if arrCurrent[i] > 499:
        	break
    #mpod.set_voltageCurrent(channel, 0, 0)    
    #mpod.channel_switch(channel,0)
    plt.plot(arrVoltage, arrCurrent)
    plt.xlabel('Bias Voltage (V)')
    plt.ylabel('Leakage Current (nA)')
    plt.xlim(Vmin*0.9, Vmax*1.1)
    plt.ylim(0, 10)
    #plt.yscale('log')
    plt.show(block=False)
    plt.savefig('IVcurve.png')
    plt.pause(10)
    #time.sleep(10)
    plt.close()


if __name__ == "__main__":
    plot_IVcurve(0, 0, 100, 1, 1.0)
