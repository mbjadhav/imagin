from relayboard.RelayBoard import RelayBoard
from sht85 import SHT85
#from steppermotor import StepperMotor

class Interlock():
    def __init__(self, interlock = 0):
        self.interlock = interlock

    def check_interlock():
        allokay = 1
        print("hello")
        return allokay

    def read_sht85value():
        temp, rh = SHT85.read_data()
        dp = SHT85.dew_point(temp, rh)
        sht85values = (temp, rh, dp) 
        return sht85values

    def read_tempchuck():
        tempchuck = RelayBoard.get_temperature(1)
        return tempchuck

    def read_tempmodule():
        tempmodule = RelayBoard.get_temperature(2)
        return tempmodule

    def read_lidswitch():
        lidswitch = RelayBoard.optrd(6)
        lidswitch = abs(lidswitch-1)
        return lidswitch
    
    def read_vacuumswitch():
        vacuumswitch = RelayBoard.optrd(7)
        return vacuumswitch

    def read_pressureswitch():
        pressureswitch = RelayBoard.optrd(8)
        return pressureswitch
    
    def read_switches():
        lidswitch = Interlock.read_lidswitch()
        vacuumswitch = Interlock.read_vacuumswitch()
        pressureswitch = Interlock.read_pressureswitch()
        switches = (lidswitch, vacuumswitch, pressureswitch)
        return switches

    def reset_alarms():
        RelayBoard.relwr(5, 1)
        RelayBoard.relwr(6, 1)
        RelayBoard.relwr(7, 1)
        RelayBoard.relwr(8, 1)
    
    def set_gled(gled=0):  #0 for ON
        RelayBoard.relwr(5, gled)

    def set_yled(yled=0):  #0 for ON
        RelayBoard.relwr(7, yled)

    def set_rled(rled=0):  #0for ON
        RelayBoard.relwr(8, rled)

    def set_alarm(alarm=0):  #0 for ON
        RelayBoard.relwr(6, alarm)
        
    def close_chillervalve(chiller=0):  #1 for OFF
        RelayBoard.relwr(1, chiller)   

    def enable_hv(enhv=0):  #1 for OFF
        RelayBoard.relwr(2, enhv)

    def enable_lv(enlv=0):  #1 for OFF
        RelayBoard.relwr(3, enlv)  

    def switch_pelitier(swpelt=0):  #0 for Positive & 1 for Negative temperature
        RelayBoard.relwr(4, swpelt) 

    def power_pelitier(powerpelt=0):  #1 for ON
        RelayBoard.odwr(1, powerpelt) 





