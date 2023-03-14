from influxdb import InfluxDBClient
import datetime
import time
import serial
import os
import re
import subprocess
import sys
import sht85

from mpodcontrol.MPODControl import MPODControl
from hmpcontrol.HMPControlTools import * 
from chiller.chiller_cf41 import *

from sht85 import SHT85
from interlock.Interlock import Interlock
from relayboard.RelayBoard import RelayBoard
mps = 1 # accepted intervals 0.5, 1, 2, 4, 10 seconds
rep = 'HIGH' # Repeatability: HIGH, MEDIUM, LOW

SHT85.periodic(mps,rep)

#print ('serial number = ', sht85.sn())
time.sleep(0.5e-3)

def read_info(temperature, air_humid, temperature_moduleN, dew_pt, IsPressure, IsVac, IsLidClosed, IsOkay):
    data_list = [{
        'measurement': 'RD53A-001-RealModule',
        'tags': {'cpu': 'felix'},
        'fields':{
            'time': datetime.datetime.now().strftime("%H:%M:%S"),
            'temperature': float(temperature),
            #'air_temp': float(air_temp),
            'air_humid': float(air_humid),
            'temperature_moduleN' : float(temperature_moduleN),
            'dew_pt': float(dew_pt),
            'is_presOK': int(IsPressure),
            'is_vacOK': int(IsVac),
            'is_lidClosed' : int(IsLidClosed),
            'is_okay' : int(IsOkay)
        }
    }]
    return data_list

def read_IV_info(HV_voltage, HV_current, LV_voltage, LV_current, PL_voltage, PL_current):
    
    data_list = [{
        'measurement': 'RD53A-001-RealModule',
        'tags': {'cpu': 'felix'},
        'fields':{
            'time': datetime.datetime.now().strftime("%H:%M:%S"),
            'HV_voltage': float(HV_voltage),
            'HV_current': float(HV_current),
            'LV_voltage': float(LV_voltage),
            'LV_current': float(LV_current),
            'PL_voltage': float(PL_voltage),
            'PL_current': float(PL_current)
        }                                                          
    }]
    return data_list

client = InfluxDBClient(host='localhost',port=8086)
client.switch_database('dcsDB')
print('Please set threshold for interlock in the Arduino program!')

powerSwitch = 0  #set to 1 if want to switch on chiller and Power Supplyies
inst_start_count = 0
run_once = 1
temp_value = 15
set_temp(temp_value)

ps_peltier = connectRohdeS()    
Nch_pltr = 3
Pltr_voltage = 2
Pltr_current = 4.6
setVoltCurr(ps_peltier, Nch_pltr, Pltr_voltage, Pltr_current)  #device, channel no, voltage, current
    
mpod = MPODControl()
channel_LV = 4
LV_voltage = 2.4
LV_current = 6
channel_HV = 301
HV_voltage = 0
HV_current = 0
mpod.set_voltageCurrent(channel_LV,LV_voltage,LV_current)
mpod.set_voltageCurrent(channel_HV,HV_voltage,HV_current)

time.sleep(1)

while True:
    t,rh, dp = Interlock.read_sht85value()
    tchuck = Interlock.read_tempchuck()
    #tmodule = Interlock.read_tempmodule()
    tmodule=0
    slid, svacuum, spressure = Interlock.read_switches()
    tevent = time.strftime("%Y%m%d%H%M%S")
    ser = serial.Serial('/dev/ttyACM0',9600)
    
    print(f"{tevent}\t{t}\t{rh}\t{dp}\t{tchuck}\t{tmodule}\t{slid}\t{svacuum}\t{spressure}\n")

    LV_voltage = mpod.read_senseVoltage(channel_LV) #V
    LV_current = (mpod.read_measCurrent(channel_LV)) #mA
    HV_voltage = mpod.read_senseVoltage(channel_HV) #V
    HV_current = (mpod.read_measCurrent(channel_HV))*1E6 #uA

    values=measVoltCurr(ps_peltier, Nch_pltr) #measure voltage and current of channel Nch
    PL_voltage = values[0] #V
    PL_current = values[1] #A
    print(HV_voltage, HV_current, LV_voltage, LV_current, PL_voltage, PL_current)
    '''        
    with open ("temp_vals.txt" ,"w") as myFile:

        temperature, air_humid, temperature_moduleN, dew_pt, IsPressure, IsVac, IsLidClosed, IsOkay = string.split()
        myFile.write(temperature_moduleN)
        myFile.write("\n")
        myFile.flush()
        myFile.close()
    '''
    temperature = t
    air_humid = rh
    temperature_moduleN = tchuck #for now added it as chuck need module temp
    dew_pt = dp
    IsPressure = spressure 
    IsVac = svacuum 
    IsLidClosed = slid 
    IsOkay = 1

    delta_ModuleTemp = abs(float(temperature_moduleN)-temp_value)
    if inst_start_count < 5:
        print(inst_start_count)
        print(delta_ModuleTemp)
    if run_once == 1:    
        if powerSwitch == 1:
            chiller_on() #switch Chiller ON = 1

        if inst_start_count < 5 and delta_ModuleTemp > 5:   #change to 1 fro actual program
            print("Module temperature not reached desired value at {} degC" .format(temp_value))
            time.sleep(10)
        if delta_ModuleTemp < 5:   #change to 1 fro actual program
            inst_start_count += 1
            if inst_start_count == 5:
                if powerSwitch == 1: # need to be set to 1 in the begining of code
                    peltier_on_off(ps_peltier,Nch_pltr,1) #switch peltier ON = 1
                    mpod.channel_switch(channel_LV,1)   #switch LV MPOD ON = 1
                    mpod.channel_switch(channel_HV,0)   #switch HV MPOD ON = 1
                run_once = 0
            '''
            if inst_start_count > 145 and inst_start_count < 301:
                print(inst_start_count)
                if inst_start_count >150 and inst_start_count < 161:
                    Pltr_voltage += 0.1
                    print(Pltr_voltage)
                    setVoltCurr(ps_peltier, Nch_pltr, Pltr_voltage, Pltr_current)
                if inst_start_count >200 and inst_start_count < 211:
                    Pltr_voltage -= 0.2
                    print(Pltr_voltage)
                    setVoltCurr(ps_peltier, Nch_pltr, Pltr_voltage, Pltr_current)
                if inst_start_count >250 and inst_start_count < 261:
                    Pltr_voltage += 0.1
                    print(Pltr_voltage)
                    setVoltCurr(ps_peltier, Nch_pltr, Pltr_voltage, Pltr_current)
            if inst_start_count == 300:
                Pltr_voltage = 2
                setVoltCurr(ps_peltier, Nch_pltr, Pltr_voltage, Pltr_current)
                run_once = 0
            '''    
    AllOkay = int(IsOkay)            
    if AllOkay == 0:
        mpod.channel_switch(channel_HV,0)   #switch HV MPOD OFF = 0
        mpod.channel_switch(channel_LV,0)   #switch LV MPOD OFF = 0
        peltier_on_off(ps_peltier,Nch_pltr,0) #switch peltier OFF = 0
        chiller_off()
    try:
        client.write_points(read_info(temperature, air_humid, temperature_moduleN, dew_pt, IsPressure, IsVac, IsLidClosed, IsOkay))
        client.write_points(read_IV_info(HV_voltage, HV_current, LV_voltage, LV_current, PL_voltage, PL_current))
    except ValueError:
        print("Oooops! Arduino issue, not getting four numbers. Try again ...")
    time.sleep(1)
    

