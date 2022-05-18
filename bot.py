from servo import Servo
from battery import Battery
#import analog

class Bot:
    
    def __init__(self, name):
        self.name = name
        
        self.servo = Servo()
        self.battery = Servo()
        self.gear = 0
    
    def get_vel(self):
        return 40
    
    def get_acc(self):
        return 30
        
    def get_bat(self):
        return 40
    
    def gear_select(self, dir):
        if dir == 'up':
            self.gear = (self.gear-1)%3
        if dir == 'down':
            self.gear = (self.gear+1)%3