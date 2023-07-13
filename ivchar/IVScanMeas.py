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

def plot_IVcurve():

    # plot arguments
    caen = SimpleCaenPowerSupply()

    if args.liveplot: plt.ion() #enable interactive mode

    nsteps = (args.Vmax-args.Vmin)/args.voltagestep
    print("Number steps it will take are {}".format(nsteps+1))

    arrVoltage = []
    arrCurrentMean = []
    time_values = []
    arrCurrentStd = []

    arrCurrent = np.zeros((int(nsteps+1), args.naveraging))

    fig, ax = plt.subplots()
    #ax.set_ylim(0,0.04)
    ax.set_xlabel('Bias Voltage V_{bias} (V)')
    ax.set_ylabel('Leakage Current, I (nA)')

    # csv file arguments
    userName = ['User', args.username]
    logSN = ['Module_SN', args.modulesn, 'FE_Chip', args.fechip]
    logEnv = ['RoomTemp (C)', args.roomtemp, 'RelHumidity [%]', args.humidity]
    logConditions = ['CurrentCompliance (uA)', args.compliance, 'VoltageStep (V)', args.voltagestep]
    logAveraging = ['WaitTime (s)', args.waittime, 'Naveraging', args.naveraging]
    header = ['Start Time', 'V_Bias (V)', 'I_leakage (nA)', 'I_Uncertainty (nA)', 'I_readAvg (nA)']

    filename = f'{args.outdir}/{args.modulesn}_{args.fechip}_{time.strftime("%Y%m%d-%H%M%S")}.csv'
    file = open(filename,'w')
    writer=csv.writer(file, delimiter=',',quotechar='"')
    writer.writerow(userName)
    writer.writerow(logSN)
    writer.writerow(logEnv)
    writer.writerow(logConditions)
    writer.writerow(logAveraging)
    file.flush

    caen.channel_switch(args.channel, "ON")
    caen.set_RampUp(args.channel, args.vramp)
    caen.set_current(args.channel, args.compliance) #compliance 310 uA
    caen.set_voltage(args.channel,args.Vmin)
    voltage = args.Vmin
        
    try:
        start_time = time.strftime("%m%d%Y-%H%M%S")
        print("Start Measurement Time (mdY-HMS) {}".format(start_time))

        for i in range(0, int(nsteps+1)):
            timestamp=time.strftime("%m%d%Y-%H%M%S")
            time_values.append(timestamp)
                
            caen.set_voltage(args.channel,voltage)
            VoltageMon = float(caen.voltage_monitor_value(args.channel, args.waittime))
            auxCurrent = np.zeros(args.naveraging)
            for j in range (0, int(args.naveraging)):
                auxCurrent[j] = float(caen.current_monitor_value(args.channel, args.waittime))*1E3
                arrCurrent[i][j] = auxCurrent[j]
                if auxCurrent[j] > 30E3: #30uA
                    print("Current over compliance limit")
                    break
            
            arrVoltage.append(VoltageMon)
            arrCurrentMean.append(np.mean(auxCurrent))
            arrCurrentStd.append(np.std(auxCurrent))
            
            print(arrCurrent[i])

            # Clear the plot and plot updated data
            if args.liveplot:
                #plt.clf()
                #plt.plot(arrVoltageMean, arrCurrentMean, 'b-')
                #plt.draw()
                ax.errorbar(arrVoltage, arrCurrentMean, yerr=arrCurrentStd,fmt='r.')
                plt.pause(args.waittime)

            voltage=voltage+args.voltagestep

        caen.close(args.channel)
        
        stop_time = time.strftime("%m%d%Y-%H%M%S")
        print("Stop Measurement Time (mdY-HMS) {}".format(stop_time))

        logRunTime = ['StartTime', start_time, 'StopTime', stop_time]
        writer.writerow(logRunTime)
        writer.writerow(header)
        file.flush
        # Write to CSV file
        for k in range (len(arrVoltage)):
            row=[time_values[k], arrVoltage[k], arrCurrentMean[k], arrCurrentStd[k], arrCurrent[k]]
            row_str=[str(value) for value in row]            
            writer.writerow(row_str)
            file.flush()
            time.sleep(args.waittime)
            
        plt.show(block=False)
        plotname = f'{args.outdir}/{args.modulesn}_{args.fechip}_{time.strftime("%Y%m%d-%H%M%S")}.png'
        plt.savefig(plotname)
        plt.pause(2)
        plt.close()

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
       print("Killing Thread...")
       file.close()
       caen.close(args.channel)

       # Disable interactive mode
       if args.liveplot: 
           plt.ioff()
       else:
           plt.plot(arrVoltageMean, arrCurrentMean, 'b-')
           plt.draw()
       # Display final plot
       plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IV measurement Code')
    parser.add_argument('-u', '--username', default=None, required=True,
                    help='User working on IV measurements')
    parser.add_argument('-sn', '--modulesn', default='ModuleSN', required=True,
                    help='Module S/N')
    parser.add_argument('-fe', '--fechip', default='FEchip', required=True,
                    help='FE Chip ID for record (SQ requirement)')
    parser.add_argument('-c', '--compliance', default=100, type=float, required=True,
                    help='Current Comliance (SQ requirement 100 uA)')
    parser.add_argument('-rt', '--roomtemp', default = 20, type=float, required=True,
                    help='Room temperature in Celcius (SQ requirement)')
    parser.add_argument('-rh', '--humidity', default=None, required=True,
                    help='Relative Humidity (SQ requirement)')
    parser.add_argument('-ch', '--channel', default=0, type=int, required=True,
                    help='Channel power Supply')
    parser.add_argument('-vmin', '--Vmin', default=0, type=float, required=True,
                    help='Set minimum voltage in Volts')
    parser.add_argument('-vmax', '--Vmax', default=200, type=float, required=True,
                    help='Set maximum voltage in Volts')
    parser.add_argument('-vstp', '--voltagestep', default=2, type=float, required=True,
                    help='Voltage step in Volts (SQ requirement)')
    parser.add_argument('-vramp', '--vramp', default=5, type=float, required=False,
                    help='Voltage ramping rate in Volts')
    parser.add_argument('-d','--waittime', action='store', default = 2, type=float, required=True,
                    help = 'Specify wait time between points')
    parser.add_argument('-navg', '--naveraging', default=10, type=int, required=True,
                    help='How many readings are averaged')
    parser.add_argument('-o', '--outdir', default='../../ITkPix_Preproduction/IV_SQ', required=False,
                    help='Output Directory for all datafiles')
    parser.add_argument('-p', '--liveplot', action='store_true', 
                    default=False, required=False, 
                    help='Set to see the live plot refreshing after every point')

    args = parser.parse_args()

    plot_IVcurve()

    
#python3 IVScanMeas.py -u "MJadhav" -sn "20UPGB4200007" -fe "14BA2" -c 100 -vstp 5 -d 2 -navg 10 -rt 20.8 -rh 43.4 -o "../../ITkPix_Preproduction/IV_SQ" -p
    
