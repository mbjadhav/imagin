import pyvisa as visa
import time
import sys
import signal
import os

#from Color_Printing import ColorFormat
import general

xx="00"

class SimpleCaenPowerSupply(object):

    def __init__(self):
        global xx
        rm = visa.ResourceManager("@py")
        resources = rm.list_resources()
        print(resources)
        self.inst = rm.open_resource("ASRL/dev/ttyACM0::INSTR")
        #self.inst.write_termination("\r\n")
        #self.inst.read_termination("\r\n")
        idn = self.inst.query("$BD:"+xx+",CMD:MON,PAR:BDNAME")
        print(idn)
        remote_status = self.check_remote_status()
        print(remote_status)
        if "DT1471ET" or "DT5519E" in idn:
          print("\nConnected to CAEN Power Supply.\n")
        else:
          print("Power supply is not available.")
        print("Checking remote status...")
        if "LOCAL" in remote_status:
            print( "Remote access is closed.")
        else:
            print("Remote access is opened.")

        self.compliance = 300.0 #uA
        self.delta_I = 0.5 #uA
        self.I_value = 0.0 #uA
        self.initial_I = 1
        self.timeout = 100000
        
        self.progress = general.progress(2)


    def simple_query(self, comm, channel=-1, delay=0.5):
        time.sleep(delay)
        command = ''
        output = ''
        if channel == -1:
          command = "$BD:"+xx+",CMD:MON,PAR:{}".format(comm)
        else:
          command = "$BD:"+xx+",CMD:MON,CH:{},PAR:{}".format(channel, comm)
        output = self.inst.query(command)
       # print(output)
        output = output.split(",")
        #print(output)
        #if channel == -1:
        output = output[2].split(":")
        #else:
        #    output = output[2].split(":")
        output = output[1]
        return output

    def simple_set(self, channel, par, value):
        command = "$BD:"+xx+",CMD:SET,CH:{},PAR:{},VAL:{}".format(channel,par,value)
        self.inst.query(command)

    def check_remote_status(self):
        return self.simple_query("BDCTR")

    def channel_switch(self, channel, status):
        self.inst.query("$BD:"+xx+",CMD:SET,CH:{},PAR:{}".format(channel, status))

    def simple_reset(self, channel):
        self.channel_switch(channel, "OFF")
        VMON = self.simple_query("VMON", channel)
        #print(VMON)
        while float(VMON) > 0.1:
            VMON = self.simple_query("VMON", channel)
            print("Voltage : {}".format(VMON))

    def set_voltage(self, channel, value):
        print("\n")
        print("Set channel {} voltage to {}".format(channel, value))
        #self.simple_set(channel, "VSET", value)
        VMON = self.simple_query("VMON", channel)
        self.simple_set(channel, "VSET", value)
        print("VMON: {}".format(VMON))
        #print(self.simple_query("VMON", channel))
        while abs(float(VMON)- value)>0.35:
           #time.sleep(5)
            self.progress("Ramping voltage... {}".format(VMON.split()[0]), "Set Voltage:{}".format(value))
            VMON = self.simple_query("VMON", channel)
            #time.sleep(3)
        print("Finished, the voltage now is {}".format(self.simple_query("VMON", channel)))
        print("\n")

    def set_current(self, channel, value):
        print("\n")
        print("Set channel {} current to {} uA".format(channel, value))
        #self.simple_set(channel, "VSET", value)
        self.simple_set(channel, "ISET", value)
        IMON = self.simple_query("IMON", channel)
        print("IMON: {}".format(IMON))
        print("\n")

    def set_RampUp(self, channel, value):
        print("\n")
        print("Set channel {} RampUp to {} V/s".format(channel, value))
        self.simple_set(channel, "RUP", value)

    def set_voltage_Q(self, channel, value):
        VMON = self.simple_query("VMON", channel)
        self.simple_set(channel, "VSET", value)
        timeout_counter = 5000
        counter = 0
        while abs(float(VMON)- value)>1.0:
            VMON = self.simple_query("VMON", channel)
            counter += 1
            if( counter == timeout_counter ):
                print("Timeout: Maximum counter reached {}".format(timeout_counter))
                break

    def voltage_monitor(self, channel, delay):
        local_VMON = 999
        local_VMON = self.simple_query("VMON", channel, delay)
        print("Monitoring Voltage: {}".format(local_VMON))
        return local_VMON

    def voltage_monitor_value(self, channel, delay):
        local_VMON = self.simple_query("VMON", channel, delay)
        return float(local_VMON)

    def current_monitor(self, channel, delay):
        local_IMON = self.simple_query("IMON", channel, delay)
        print("Monitoring Current: {}".format(local_IMON))
        return local_IMON

    def current_monitor_value(self, channel, delay):
        local_IMON = self.simple_query("IMON", channel, delay)
        return float(local_IMON)

    def confirm_voltage(self, channel, TargetVoltage, delay=5):
        voltage = self.simple_query("VMON", channel, delay)
        if abs(float(voltage) - TargetVoltage) < 1.5:
            return True
        else:
            return False

    def reset_channel(self, channel):
        print("\n")
        print("Resetting channel {}. Power off".format(channel))
        VMON = self.simple_query("VMON", channel)
        self.channel_switch(channel, "OFF")
        while abs(float(VMON)-0.0)>1.0:
            VMON = self.simple_query("VMON", channel, 2)
            print("Monitoring Voltage: {}".format(VMON))
        print("Finished. You need to re-power the channel")
        print("\n")

    def Get_Voltage_Current_Pair(self, channel):
        '''
        param channel := reading channel
        return the voltage and current as a 2D list.
        '''
        VMON = self.voltage_monitor_value(channel,0)
        IMON = self.current_monitor_value(channel,0)

        return [VMON, IMON]

    def Set_Compliance(self, compliance, rate_of_change):
        self.compliance = compliance #uA
        self.delta_I = rate_of_change #uA\

    def Check_Compliacne(self, channel, iValue):
        if self.initial_I == 1:
            self.I_value = iValue
            self.initial_I = 0
        else:
            pass
        if iValue <= self.compliance:
            self.I_value = iValue
        else:
            dI = iValue - self.I_value
            if dI >= self.delta_I:
                #print(self.I_value)
                print("Current Warning: Rapid Increase")
                print( "Shutdown Channel: {}".format(channel))
                self.close(channel)
                return 1
        return 0

    def read_channel_status_bit(self, channel ):
        stat = self.simple_query( "STAT", channel )
        stat = stat.split("\r")[0]
        return stat

    def decodeStatusBit( self, status, bit):
        '''
        decoding the channel status bit

        param status := is the raw input bit,
        param bit := the bit you want to check against.
        '''
        status_bits = format(int(status), "#016b")
        if bit > 15:
            print("bit > max bit(15)")
        else:
            if status_bits[15-bit] == "1":
                print("WARNING: %s"%self.__status_bit_meaning[bit][1])
                return 1
            else:
                return 0


    def checkTripped(self, ch, voltage):
        #check to see if the channel is tripped
        status_bit = self.read_channel_status_bit(ch)
        tripped = self.decodeStatusBit( status_bit, 7)
        if tripped:
            self.channel_switch(ch, "ON")
            self.set_voltage_Q(ch, voltage)


    def close(self, channel):
        print("\n")
        print("object calls close(). {} channels are turning off".format(channel))
        if channel == "ALL":
          self.channel_switch(0, "OFF")
          self.channel_switch(1, "OFF")
          self.channel_switch(2, "OFF")
          self.channel_switch(3, "OFF")
        elif channel == 0:
          self.channel_switch(0, "OFF")
        elif channel == 1:
          self.channel_switch(1, "OFF")
        elif channel == 2:
          self.channel_switch(2, "OFF")
        elif channel == 3:
          self.channel_switch(3, "OFF")
        print("\n")

