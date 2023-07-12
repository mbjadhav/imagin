import pyvisa as visa
import time
import sys
import signal
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from CAEN_PSDesk import *

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
    voltage = Vmin

    for i in range(0, int(nsteps+1)):
        arrVoltage[i] = voltage
        caen.set_voltage(channel,arrVoltage[i])
        print("Time (hh/mm/ss) {}".format(time.strftime("%H%M%S")))
        arrVoltage[i] = caen.voltage_monitor_value(channel, delay)
        arrCurrent[i] = caen.current_monitor_value(channel, delay)
        arrCurrent[i]=arrCurrent[i]*1E3
        if i == 0: current = arrCurrent[i]
        if arrCurrent[i] > current:
            current = arrCurrent[i]
        print("Measured - Voltage: {} V, current: {} nA" .format(arrVoltage[i], arrCurrent[i]))
        voltage=voltage+Vstep
        if arrCurrent[i] > 30E3: #30uA
            print("Current over compliance limit")
            break
    caen.close(channel)
    #mpod.set_voltageCurrent(channel, 0, 0)    
    #mpod.channel_switch(channel,0)
    plt.plot(arrVoltage, arrCurrent)
    plt.xlabel('Bias Voltage (V)')
    plt.ylabel('Leakage Current (nA)')
    plt.xlim(Vmin*0.9, Vmax*1.1)
    plt.ylim(0, 1E3)
    #plt.yscale('log')
    plt.show(block=False)
    plt.savefig('IVcurve.png')
    plt.pause(10)
    #time.sleep(10)
    plt.close()


if __name__ == "__main__":
    plot_IVcurve(0, 0, 10, 1, 1.0)
