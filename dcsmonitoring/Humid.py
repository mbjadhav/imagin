from influxdb import InfluxDBClient
import datetime
import time
import serial
import os
import re
import subprocess

def read_info(temperature, air_humid, temperature_moduleN, dew_pt):
    data_list = [{
        'measurement': 'RD53A-001-RealModule',
        'tags': {'cpu': 'felix'},
        'fields':{
            'time': datetime.datetime.now().strftime("%H:%M:%S"),
            'temperature': float(temperature),
            #'air_temp': float(air_temp),
            'air_humid': float(air_humid),
            'temperature_moduleN' : float(temperature_moduleN),
            'dew_pt': float(dew_pt)
        }
    }]
    return data_list

def IV_info(LV_voltage, LV_current, HV_voltage, HV_current):
    data_list = [{
        'measurement': 'RD53A-001-RealModule',
        'tags': {'cpu': 'felix'},
        'fields':{
            'time': datetime.datetime.now().strftime("%H:%M:%S"),
            'LV_voltage': float(LV_voltage),
            'LV_current': float(LV_current),
            'HV_voltage': float(HV_voltage),
            'HV_current': float(HV_current)
        }
    }]
    return data_list

client = InfluxDBClient(host='localhost',port=8086)
client.switch_database('humidDB')
print('Please set threshold for interlock in the Arduino program!')

while True:
    ser = serial.Serial('/dev/ttyACM1',9600)
    b = ser.readline()
    string_n = b.decode()
    string = string_n.rstrip()
    print(string)
    with open ("temp_vals.txt" ,"w") as myFile:

        temperature, air_humid, temperature_moduleN, dew_pt = string.split()
        
        myFile.write(temperature_moduleN)
        myFile.write("\n")
        myFile.flush()
        myFile.close()

    try:
        temperature, air_humid, temperature_moduleN, dew_pt = string.split()
        client.write_points(read_info(temperature, air_humid, temperature_moduleN, dew_pt))
    except ValueError:
        print("Oooops! Arduino issue, not getting four numbers. Try again ...")
    time.sleep(3)
    

