import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from MPODControl import MPODControl

def plot_IVcurve(channel, Vmin=0, Vmax=10, Vstep=1, Vrate=1.0):
    
    nsteps = (Vmax-Vmin)/Vstep
    arrVoltage = np.empty(int(nsteps+1), dtype=object)
    arrCurrent = np.empty(int(nsteps+1), dtype=object)
    mpod = MPODControl()
    print(Vrate)
    mpod.set_voltageRate(channel, Vrate)
    mpod.channel_switch(channel,1)
    mpod.set_voltage(channel,Vmin)
    voltage = mpod.read_voltage(channel)

    for i in range(0, int(nsteps+1)):
        arrVoltage[i] = voltage
        mpod.set_voltage(channel,arrVoltage[i])
        #print(time.strftime("%H%M%S"))
        while True:
            Vcheck = mpod.read_senseVoltage(channel)
            if abs(Vcheck-arrVoltage[i]) <0.3:
                break
        #print(time.strftime("%H%M%S"))
        time.sleep(1)
        arrCurrent[i] = mpod.read_measCurrent(channel)
        arrCurrent[i]=arrCurrent[i]*1E9
        print(arrCurrent[i])
        voltage=voltage+Vstep
    #mpod.set_voltageCurrent(channel, 0, 0)    
    #mpod.channel_switch(channel,0)
    plt.plot(arrVoltage, arrCurrent)
    plt.xlabel('Bias Voltage (V)')
    plt.ylabel('Leakage Current (nA)')
    plt.xlim(Vmin*0.9, Vmax*1.1)
    plt.ylim(0, 2000)
    #plt.yscale('log')
    plt.show(block=False)
    plt.savefig('IVcurve.png')
    plt.pause(10)
    #time.sleep(10)
    plt.close()


if __name__ == "__main__":
    plot_IVcurve(311, 0, 60, 2, 1.0)