from servo import Servo
from battery import Battery

#import analog

class Bot:
    
    def __init__(self, name):
        self.name = name
        
        self.servo = Servo()
        self.battery = Servo()
        
        self.vel = 0
        self.acc = 0
        self.gear = 0
        
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
        
    def get_bat(self):
        return 40
    
    def gear_select(self, dir):
        if dir == 'up':
            self.gear = (self.gear-1)%3
        if dir == 'down':
            self.gear = (self.gear+1)%3