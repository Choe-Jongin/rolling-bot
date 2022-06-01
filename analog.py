import spidev

#mcp3208
spi=spidev.SpiDev()
spi.open(0, 0)    #0번채널 오픈
spi.max_speed_hz=1000000

#analog senser list(pin number)
PRESS=0 #압력센서

def analogread(channel):   #V를 반환하는 함수
    duf=[(1<<2)|(1<<1)|(channel&4)>>2,(channel&3)<<6,0]
    adc=spi.xfer(duf) 
    data=((adc[1]&0xf)<<8)|adc[2]
    return data  

def kpa():     #압력 반환   
    press = analogread(PRESS)
    #print('analogread:', str(press) + 'V:'+str(press/4095) + 'KPa:'+str(25*((press/4095)-0.5)))
    return 25*((press*5/4095)-0.5)

def kpa():     #압력 반환   
    press = analogread(PRESS)
    #print('analogread:', str(press) + 'V:'+str(press/4095) + 'KPa:'+str(25*((press/4095)-0.5)))
    return 25*((press*5/4095)-0.5)