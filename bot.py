from servo import Servo
from battery import Battery
from gyro import Gyro
from servo import Servo
#import analog

class Bot:
    
    def __init__(self, name):
        self.name = name
        
        self.battery = Battery()
        self.gyro = Gyro()
        self.servo1 = Servo(18)
        
        self.vel = 0
        self.acc = 0
        self.gear = 0
        
        self.set_neu()
        
        
    def close(self):
        self.servo1.close() 
        
    def set_ver(self):
        self.servo1.set_degree(0)
        
    def set_hor(self):
        self.servo1.set_degree(180)
        
    def set_neu(self):
        self.gear = 2;
        self.servo1.set_degree(90)
        
    def update(self):
        self.up_speed(self.acc)
        
    def up_speed(self, amount):
        self.vel += amount
        if self.vel < 0 :
            self.vel = 0
            self.acc = 0

    def up_acc(self, amount):
        self.acc += amount
    
    #getter
    def get_vel(self):
        return self.vel
    
    def get_acc(self):
        return self.acc
        
    def get_battery_per(self):
        return self.battery.per()
        
    def get_battery_capa(self):
        return self.battery.capa()
    
    def gear_select(self, dir):
        if dir == 'up':
            self.gear = (self.gear-1)%3
        if dir == 'down':
            self.gear = (self.gear+1)%3