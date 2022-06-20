#GUI
from text import PRND
from text import gauge

#module
from bot import Bot
from gauge import DialGauge, VerGauge, Gauge
from kbmanager import KM
from text import replace_str

#program
import os
import time
import threading
import RPi.GPIO as GPIO


FPS = 10

class Main:
    
    #프로그램 구성 요소 
    name="ROLLING BOT"     #프로그램 이름
    state = 0           #메인루프 동작 상태(0:정상, -1:종료)
    start = 0           #프로그램 시작시간
    time = 0            #프로그램 동작시간
    
    #UI
    lines = 24
    __cleanline = " "*80
    back_buff = [ " "*80 for _ in range(lines)]
    
    #로봇 관련
    bot = Bot("TEAM 3 BOT")

    #프로그램 시작 지점
    @staticmethod
    def entry():
        
        #setting
        KM.set_key_list(['up','down','left','right','esc','q', 'shift', 'esc'])
        t1 = threading.Thread(target=Main.UI)
        t2 = threading.Thread(target=KM.detect)
        
        try:
            print('start raspi')
            
            #start monitorig UI
            t1.start()
            
            #keyboard input
            t2.start()
                
            #start main loop
            Main.loop()
            Main.state = -1
            KM.running = False
        except KeyboardInterrupt:   #키보드로 강제 종료시 진입(ctrl + C)
            print("exit")
        finally:                    #정상/비정상 프로그램 종료 시 처리
            KM.running = False
            t1.join()
            print('system off success')
            print('press esc')
            t2.join()
            Main.bot.close()
            Main.state = -1
            GPIO.cleanup()
            Main.clear()
            print("clean main")
    
    #메인루프
    @staticmethod
    def loop():
        
        #임시 UI 테스트 코드
        run = 1
        
        while run == 1:
            # KM.update()
            Main.bot.update()
            if KM.is_press('up'):
                Main.bot.acc += 0.1
            else :
                if Main.bot.acc > -Main.bot.get_vel():
                    Main.bot.acc = -Main.bot.get_vel()/20
                
            if(KM.is_press('left')):
                Main.bot.set_ver()
                
            if(KM.is_press('up')):
                Main.bot.set_neu()
                
            if(KM.is_press('right')):
                Main.bot.set_hor()
                # Main.bot.set_hor_buffered()
                
            if(KM.is_press('q')):
                break;
            
            time.sleep(0.03)
            
    #**********    UI    *************
    
    #화면 지우기
    @staticmethod
    def clear():
        if os.name.split()[0] == "nt":
            os.system('cls')                #윈도우
        else :
            os.system('clear')              #리눅스/유닉스
    
    #커서이동         
    @staticmethod
    def goto00():
        print("\033[0;0H", end='')
    
    #UI의 메인루프
    @staticmethod
    def UI():
        
        Main.clear()
        Main.start = time.time()
        elaps = Main.start
        Main.time = 0
        curr = 0
        
        veldial = DialGauge("velocity",0,135,20,18)
        accdial = DialGauge("acc",-2,8,20,18,150,5)
        veldial.set_detail(unit="cm/s")
        accdial.set_detail(base_offset=-32, unit="cm/s^2")
        
        tiltgauge = VerGauge("tile",0,120,30,2)
        
        #메인루프
        while Main.state != -1:
            #흐르는 시간 측정
            now = time.time()
            delta = now - elaps
            Main.time += delta
            curr += now - elaps
            elaps = now
            
            Main.bot.gyro.update(delta)
            
            #FPS 적용(1프레임 마다 진입)
            if curr >= 1/FPS:
                curr -= 1/FPS
                Main.goto00()

                tiltgauge.set_val(Main.bot.get_deg())
                tiltgauge.val_update()
                                
                replace_str(Main.back_buff,[
        '┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓',
        '┃'+Main.name.center(70)+'┃',
        '┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫',
        '┃                                                                      ┃',
        '┃                                                           ╭────────╮ ┃',
        '┃                                                           │'+PRND[Main.bot.gear][0]+'│ ┃',
        '┃                                                           │'+PRND[Main.bot.gear][1]+'│ ┃',
        '┃                                                           │'+PRND[Main.bot.gear][2]+'│ ┃',
        '┃                                                           │'+PRND[Main.bot.gear][3]+'│ ┃',
        '┃                                                           │'+PRND[Main.bot.gear][4]+'│ ┃',
        '┃                                                           │'+PRND[Main.bot.gear][5]+'│ ┃',
        '┃                                                           ╰────────╯ ┃',
        '┃                                                              V N H   ┃',
        '┃                                                                      ┃',
        '┃                                                                      ┃',
        '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'],0,0)
                
                replace_str(Main.back_buff, tiltgauge.show(), 2,10)
                
                print('\n'.join(Main.back_buff))
                Main.back_buff = [ Main.__cleanline for _ in range(Main.lines)]
    
#프로그램 시작
if __name__ == "__main__":           
    Main.entry()

#████████
#██    ██
#██    ██
#████████
#██    ██
#██    ██
#████████
