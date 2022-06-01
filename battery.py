import smbus
from ina219 import INA219
from ina219 import DeviceRangeError
SHUNT_OHMS = 0.05

# addr=0x40 #ups i2c address

class Battery:
    def __init__(self):
        self.max = 4000
        self.ina = INA219(SHUNT_OHMS)
        self.ina.configure()

    def capa(self):
        capacity=2000
        return capacity
    
    def power(self):
        return self.ina.power()

    def per(self):
        v = self.ina.voltage()

        electricity= (v-5)/1.2
        return electricity

        
# ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
#▕ █████████████  ▕ 
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
