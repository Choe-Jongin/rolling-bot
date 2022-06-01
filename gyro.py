import smbus  # import SMBus module of I2C
import math

#some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

class Gyro:

    def __init__(self):
        # or bus = smbus.SMBus(0) for older version boards
        self.bus = smbus.SMBus(1)
        self.Device_Address = 0x69   # MPU6050 device address

        #write to sample rate register
        self.bus.write_byte_data(self.Device_Address, SMPLRT_DIV, 7)

        #Write to power management register
        self.bus.write_byte_data(self.Device_Address, PWR_MGMT_1, 1)

        #Write to Configuration register
        self.bus.write_byte_data(self.Device_Address, CONFIG, 0)

        #Write to Gyro configuration register
        self.bus.write_byte_data(self.Device_Address, GYRO_CONFIG, 24)

        #Write to interrupt enable register
        self.bus.write_byte_data(self.Device_Address, INT_ENABLE, 1)
        
        self.vels = [0,0,0]
        self.accs = [0,0,0]
        self.degs = [0,0,0]
        
    def read_raw_data(self, addr):
        #Accelero and Gyro value are 16-bit
            high = self.bus.read_byte_data(self.Device_Address, addr)
            low = self.bus.read_byte_data(self.Device_Address, addr+1)

            #concatenate higher and lower value
            value = ((high << 8) | low)

            #to get signed value from mpu6050
            if(value > 32768):
                    value = value - 65536
            return value
    
    #적분용
    def update(self, deltatime):
        delta_degs = self.delta_deg(deltatime)
        self.degs[0] += delta_degs[0]
        self.degs[1] += delta_degs[1]
        self.degs[2] += delta_degs[2]
        #self.degs = [self.degs[0]%360, self.degs[1]%360, self.degs[2]%360]        

    def delta_deg(self, delta):
        #Read Gyroscope raw value
        gyro_x = self.read_raw_data(GYRO_XOUT_H)
        gyro_y = self.read_raw_data(GYRO_YOUT_H)
        gyro_z = self.read_raw_data(GYRO_ZOUT_H)

        gx = gyro_x/131.068*delta
        gy = gyro_y/131.068*delta
        gz = gyro_z/131.068*delta

        return [gx, gy, gz]
            
    def get_acc(self):
    	#Read Accelerometer raw value
        acc_x = self.read_raw_data(ACCEL_XOUT_H)
        acc_y = self.read_raw_data(ACCEL_YOUT_H)
        acc_z = self.read_raw_data(ACCEL_ZOUT_H)
        
        ax = acc_x/16384.0
        ay = acc_y/16384.0
        az = acc_z/16384.0

        return [ax, ay, az]
    
    def get_deg(self):
        
        acc = self.get_acc()
        
        x, y, z = 0, 0, 0
        
        if acc[0] == 0 and acc[2] == 0:
            x = 90
        else :
            x = math.degrees(math.atan(acc[1]/Gyro.dist(acc[0],acc[2])))
            
        if acc[1] == 0 and acc[2] == 0:
            y = 90
        else :
            y = math.degrees(math.atan(acc[0]/Gyro.dist(acc[1],acc[2])))
        
        if acc[0] == 0 and acc[1] == 0:
            z = 90
        else :
            z = math.degrees(math.atan(acc[2]/Gyro.dist(acc[0],acc[1])))
            
        return [x, y, z]
    
    @staticmethod
    def dist(a,b):
        return math.sqrt(a**2+b**2)
