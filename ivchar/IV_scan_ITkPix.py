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
    #arrVoltage = np.zeros(int(nsteps+1))
    #arrCurrent = np.zeros(int(nsteps+1))
    #arrVoltageStd = np.zeros(int(nsteps+1))
    #arrCurrentStd = np.zeros(int(nsteps+1))

    arrVoltage = []
    arrCurrent = []
    arrVoltageStd = []
    arrCurrentStd = []

    #arrVoltage = np.empty(int(nsteps+1), dtype=object)
    #arrCurrent = np.empty(int(nsteps+1), dtype=object)
    #arrVoltageStd = np.empty(int(nsteps+1), dtype=object)
    #arrCurrentStd = np.empty(int(nsteps+1), dtype=object)
    
    #print(Vrate)
    caen = SimpleCaenPowerSupply()
    caen.Set_Compliance(500, 50)
    #mpod.set_voltageRate(channel, Vrate)
    caen.set_current(channel,30)
    caen.channel_switch(channel, "ON")
    #mpod.channel_switch(channel,1)
    caen.set_voltage(channel,Vmin)
    voltage = Vmin

    fig, ax = plt.subplots()
    ax.set_xlabel('Bias Voltage (V)')
    ax.set_ylabel('Leakage Current (nA)')

    for i in range(0, int(nsteps+1)):
        #arrVoltage[i] = voltage
        caen.set_voltage(channel,voltage)
        print("Time (hh/mm/ss) {}".format(time.strftime("%H%M%S")))
        auxVoltage = np.zeros(10)
        auxCurrent = np.zeros(10)
        for j in range(len(auxVoltage)):
            auxVoltage[j] = float(caen.voltage_monitor_value(channel, 0.5))
            auxCurrent[j] = float(caen.current_monitor_value(channel, 0.5))
        #arrVoltage[i] = np.mean(auxVoltage)
        #arrCurrent[i] = np.mean(auxCurrent)
        #arrVoltageStd[i] = np.std(auxVoltage)
        #arrCurrentStd[i] = np.std(auxCurrent)
        
        arrVoltage.append(np.mean(auxVoltage))
        arrCurrent.append(np.mean(auxCurrent))
        arrCurrentStd.append(np.std(auxCurrent))

        #arrVoltage[i] = caen.voltage_monitor_value(channel, delay)
        #arrCurrent[i] = caen.current_monitor_value(channel, delay)
        arrCurrent[i]=arrCurrent[i]*1E3
        if i == 0: current = arrCurrent[i]
        if arrCurrent[i] > current:
            current = arrCurrent[i]
        print("Measured - Voltage: {} V, current: {} nA" .format(arrVoltage[i], arrCurrent[i]))
        voltage=voltage+Vstep
        if arrCurrent[i] > 30E3: #30uA
            print("Current over compliance limit")
            break

        ax.errorbar(arrVoltage, arrCurrent, yerr=arrCurrentStd,fmt='r.')
        plt.pause(0.1)
    caen.close(channel)
    #mpod.set_voltageCurrent(channel, 0, 0)    
    #mpod.channel_switch(channel,0)
    #plt.xlim(Vmin*0.9, Vmax*1.1)
    #plt.ylim(0, 1E3)
    #plt.yscale('log')

    with open('output.txt', 'w') as f:
        f.write("Voltage[V]\tCurrent[nA]\tErrorCurrent[nA]\n")
        for k in range(len(arrVoltage)):
            f.write("{:.2f}\t{:.2f}\t{:.2f}\n".format(arrVoltage[k], arrCurrent[k], arrCurrentStd[k]))
            #f.write(str(arrVoltage[k]) + "\t" + str(arrCurrent[k]) + "\t" + str(arrCurrentStd[k]) + "\n")


    plt.show(block=False)
    plt.savefig('IVcurve.png')
    plt.pause(10)
    #time.sleep(10)
    plt.close()


if __name__ == "__main__":
    plot_IVcurve(0, 0, 200, 5, 1.0)