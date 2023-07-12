import pyvisa as visa
import time
import sys
import signal
import os
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import pandas as pd
import argparse

sys.path.insert(1, '/home/astropixadmin/imagin')

from CAEN_PS import *
from hmpcontrol.HMPControlTools import *

delay = 0.2

def plot_IVcurve(channel, Vmin=0, Vmax=10, Vstep=1, Vrate=1.0):

    # plot arguments
    if args.liveplot: plt.ion() #enable interactive mode
    nsteps = (Vmax-Vmin)/Vstep
    arrVoltage = np.empty(int(nsteps+1), dtype=object)
    arrCurrent = np.empty(int(nsteps+1), dtype=object)
    time_values = []
    voltage_values = []
    current_values = []

    fig, ax = plt.subplots()
    ax.set_ylim(0,0.04)
    ax.set_xlabel('time')
    ax.set_ylabel('I Current (nA)')

    # csv file arguments
    header = ['Module_ID', 'time', 'I_HV', 'V_HV']
    filename = f'{args.outdir}/{args.name}_{time.strftime("%Y%m%d-%H%M%S")}.csv'
    file = open(filename,'w')
    writer=csv.writer(file, delimiter=',',quotechar='"')
    writer.writerow(header)
    file.flush

    caen = SimpleCaenPowerSupply()
    caen.channel_switch(channel, "ON")
    caen.set_RampUp(channel, rate)
    caen.set_current(channel, 31) #compliance 310 uA
    caen.set_voltage(channel,Vmin)
    voltage = Vmin
        
    try:
        while True:
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
            current = caen.current_monitor_value(channel, delay)
            voltage = caen.voltage_monitor_value(channel, delay)

            timestamp=time.strftime("%m%d%Y-%H%M%S")
            time_values.append(timestamp)   
            current_values.append(current)         
            # Clear the plot and plot updated data
  
            if args.liveplot:
                plt.clf()
                plt.plot(time_values, current_values, 'b-')
                plt.draw()
                plt.pause(args.waittime-1)

            # Print values
            strgout = time.strftime("%m%d%Y-%H%M%S") + " : I = " + str(current*1E3) + " nA." 
            print(strgout)
            
            # Write to CSV file
            chip_ID=args.name
            row=[chip_ID,timestamp,current*1E3,voltage]
            row_str=[str(value) for value in row]
            writer.writerow(row_str)
            file.flush()
            time.sleep(args.waittime)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
       print("Killing Thread...")
       file.close()
       caen.close(channel)

       # Disable interactive mode
       if args.liveplot: 
           plt.ioff()
       else:
           plt.plot(time_values, current_values, 'b-')
           plt.draw()
       # Display final plot
       plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IV measurement Code')
    parser.add_argument('-n', '--name', default='ModuleID', required=False,
                    help='Option to give additional name to output files upon running')
    parser.add_argument('-o', '--outdir', default='.', required=False,
                    help='Output Directory for all datafiles')
    parser.add_argument('-p', '--liveplot', action='store_true', 
                    default=False, required=False, 
                    help='Set to see the live plot refreshing after every point')
    parser.add_argument('-t','--waittime', action='store', default = 2, type=float,
                    help = 'Specify wait time between points')

    args = parser.parse_args()

    plot_IVcurve(0, 10.0, 1)

    

    
