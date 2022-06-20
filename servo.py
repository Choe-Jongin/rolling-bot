import RPi.GPIO as GPIO
import time

class Servo:
    
    def __init__(self, pin):
        self.pin = pin
        self.duty_min = 1.5
        self.duty_max = 12.5
        self.max = 120
        self.deg = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start( self.duty_min+(self.duty_max-self.duty_min)/2)
        
    def close(self):
        self.pwm.stop();
        
    def set_degree(self, degree):
      
        if degree > self.max:
            degree = self.max
        if degree < 0:
            degree = 0
        
        duty = self.duty_min+((self.duty_max-self.duty_min)*degree/self.max)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.003*abs(self.deg - degree))
        self.deg = degree

#프로그램 시작
if __name__ == "__main__":           
    s = Servo(18)
    
    for i in range(2,30):
        
        print(i/2)
        s.pwm.ChangeDutyCycle(i/2)
        time.sleep(0.5)
        
    GPIO.cleanup()