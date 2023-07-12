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

delay = 2

def plot_IVcurve(channel, Vset, rate):

    # plot arguments
    if args.liveplot: plt.ion() #enable interactive mode
    time_values = []
    I2_values = []

    fig, ax = plt.subplots()
    ax.set_ylim(0,0.04)
    ax.set_xlabel('time')
    ax.set_ylabel('I2')

    # csv file arguments
    header = ['chip_ID', 'time', 'I_HV', 'V_HV', 'I1_LV', 'V1_LV', 'I2_LV', 'V2_LV', 'I3_LV', 'V3_LV', 'I4_LV', 'V4_LV' ]
    filename = f'{args.outdir}/{args.name}_{time.strftime("%Y%m%d-%H%M%S")}.csv'
    file = open(filename,'w')
    writer=csv.writer(file, delimiter=',',quotechar='"')
    writer.writerow(header)
    file.flush

    device = connectRohdeS()
    setVoltCurr(device, 1, 1.8, 0.01)
    setVoltCurr(device, 2, 1.8, 0.1)
    setVoltCurr(device, 3, 2.7, 1)
    setVoltCurr(device, 4, 1.2, 0.01)

    hmp_on_off(device, 1, 1)
    hmp_on_off(device, 2, 1)
    hmp_on_off(device, 3, 1)
    hmp_on_off(device, 4, 1)

    caen = SimpleCaenPowerSupply()
    caen.channel_switch(channel, "ON")
    caen.set_RampUp(channel, rate)
    caen.set_current(channel, 310) #compliance 310 uA
    caen.set_voltage(channel,Vset)
        
    try:
        while True:
            current = caen.current_monitor_value(channel, delay)
            voltage = caen.voltage_monitor_value(channel, delay)

            IV_LV1=measVoltCurr(device, 1)
            IV_LV2=measVoltCurr(device, 2)
            IV_LV3=measVoltCurr(device, 3)
            IV_LV4=measVoltCurr(device, 4)
            
            V1, I1 = IV_LV1
            V2, I2 = IV_LV2
            V3, I3 = IV_LV3
            V4, I4 = IV_LV4

            timestamp=time.strftime("%m%d%Y-%H%M%S")
            time_values.append(timestamp)
            I2_values.append(I2)
            
            # Clear the plot and plot updated data
  
            if args.liveplot:
                plt.clf()
                plt.plot(time_values, I2_values, 'b-')
                plt.draw()
                plt.pause(args.waittime-1)

            # Print values
            strgout = time.strftime("%m%d%Y-%H%M%S") + " : I = " + str(current*1E3) + " nA." 
            print(strgout)
            strgout1 = time.strftime("%m%d%Y-%H%M%S") + " : LV1 = " + str(IV_LV1) + " LV2" + str(IV_LV2) + " LV3"  + str(IV_LV3) + " LV4" + str(IV_LV4) + " mA."
            print(strgout1)
            
            # Write to CSV file
            chip_ID=args.name
            row=[chip_ID,timestamp,current*1E3,voltage, I1, V1, I2, V2, I3, V3, I4, V4]
            row_str=[str(value) for value in row]
            writer.writerow(row_str)
            file.flush()
            time.sleep(args.waittime)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
       print("Killing Thread...")
       file.close()
       caen.close(channel)
       hmp_on_off(device, 1, 0)
       hmp_on_off(device, 2, 0)
       hmp_on_off(device, 3, 0)
       hmp_on_off(device, 4, 0)

       # Disable interactive mode
       if args.liveplot: 
           plt.ioff()
       else:
           plt.plot(time_values, I2_values, 'b-')
           plt.draw()
       # Display final plot
       plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Astropix Driver Code')
    parser.add_argument('-n', '--name', default='mycsvfile', required=False,
                    help='Option to give additional name to output files upon running')
    parser.add_argument('-o', '--outdir', default='.', required=False,
                    help='Output Directory for all datafiles')
    parser.add_argument('-p', '--liveplot', action='store_true', 
                    default=False, required=False, 
                    help='Set to see the live plot refreshing after every point')
    parser.add_argument('-t','--waittime', action='store', default = 59, type=float,
                    help = 'Specify wait time between points')

    args = parser.parse_args()

    plot_IVcurve(0, 0.0, 1)

    

    
