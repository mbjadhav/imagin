from relayboard import RelayBoard
from sht85 import SHT85
#from steppermotor import StepperMotor

class Interlock():
    def __init__(self, interlock = 0):
        self.Interlock = interlock

    def check_interlock(self):
        print("okay")

    def get_sht85value(self, temp=0, rh=0, dp=0):
        temp, rh = SHT85.read_data()
        dp = SHT85.dew_point(temp, rh)
        sht85values = (temp, rh, dp)    
        return sht85values

    def get_tempchuck(self, tempchuck=0):
        tempchuck = RelayBoard.get_temperature(1)
        return tempchuck

    def get_tempmodule(self, tempmodule=0):
        tempmodule = RelayBoard.get_temperature(2)
        return tempmodule

    def get_lidswitch(self, lidswitch=0):
        lidswitch = RelayBoard.optrd(6)
        return lidswitch
    
    def get_vacuumswitch(self, vacuumswitch=1):
        vacuumswitch = RelayBoard.optrd(7)
        return vacuumswitch

    def get_pressureswitch(self, pressureswitch=1):
        pressureswitch = RelayBoard.optrd(8)
        return pressureswitch
    
    def set_gled(self, gled=0):  #1 for ON
        RelayBoard.relwr(5, gled)

    def set_yled(self, yled=0):  #1 for ON
        RelayBoard.relwr(7, yled)

    def set_rled(self, rled=0):  #1 for ON
        RelayBoard.relwr(8, rled)

    def set_alarm(self, alarm=0):  #1 for ON
        RelayBoard.relwr(6, alarm)
        
    def close_chillervalve(self, chiller=0):  #1 for OFF
        RelayBoard.relwr(1, chiller)   

    def enable_hv(self, enhv=0):  #1 for OFF
        RelayBoard.relwr(2, enhv)

    def enable_lv(self, enlv=0):  #1 for OFF
        RelayBoard.relwr(3, enlv)  

    def switch_pelitier(self, swpelt=0):  #0 for Positive & 1 for Negative temperature
        RelayBoard.relwr(4, swpelt) 

    def power_pelitier(self, powerpelt=0):  #1 for ON
        RelayBoard.odwr(1, powerpelt) 





