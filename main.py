#GUI
from text import PRND

#module
from bot import Bot
from gauge import DialGauge
from kbmanager import KM
from text import replace_str

#program
import os
import time
import threading

FPS = 20

class Main:
    
    #프로그램 구성 요소 
    name="ROLLING BOT"     #프로그램 이름
    state = 0           #메인루프 동작 상태(0:정상, -1:종료)
    start = 0           #프로그램 시작시간
    time = 0            #프로그램 동작시간
    
    #로봇 관련
    bot = Bot("TEAM 3 BOT")

    #프로그램 시작 지점
    @staticmethod
    def entry():
        
        #setting
        KM.set_key_list(['up','down','left','right','esc','q', 'shift'])
        
        try:
            print('start raspi')
            
            #start monitorig UI
            t = threading.Thread(target=Main.update)
            t.start()
            
            #start main loop
            Main.loop()
            Main.state = -1
        except KeyboardInterrupt:   #키보드로 강제 종료시 진입(ctrl + C)
            print("exit")
        finally:                    #정상/비정상 프로그램 종료 시 처리
            Main.state = -1
            print("clean main")
    
    #메인루프
    @staticmethod
    def loop():
        
        run = 1
        while run == 1:
            KM.update()
            Main.bot.update()
            if KM.is_press('up'):
                Main.bot.acc = 8
            elif KM.is_down('up'):
                Main.bot.up_acc(-0.3)
                if Main.bot.acc < 0.5:
                    Main.bot.acc = 0.5
            elif KM.is_relese('up'):
                Main.bot.acc = -2
            else :
                if Main.bot.acc > -Main.bot.get_vel():
                    Main.bot.acc = -Main.bot.get_vel()/20
                
            if KM.is_press('shift'):
                Main.bot.gear_select('down')
                
            if KM.is_down('esc'):
                run = 0
            time.sleep(0.03)
            
    #**********    UI    *************
    
    #화면 지우기
    @staticmethod
    def clear():
        if os.name.split()[0] == "nt":
            os.system('cls')                #윈도우
        else :
            os.system('clear')              #리눅스/유닉스
    
    #UI의 메인루프
    @staticmethod
    def update():
        Main.start = time.time()
        elaps = Main.start
        Main.time = 0
        curr = 0
        
        dial = DialGauge("velocity",0,135,20,18)
        accdial = DialGauge("acc",-2,8,20,18,150,5)
        dial.set_detail(unit="cm/s")
        accdial.set_detail(base_offset=-32, unit="cm/s^2")
        
        while Main.state != -1:
            #흐르는 시간 측정
            now = time.time()
            Main.time += now - elaps
            curr += now - elaps
            elaps = now
            
            #FPS 적용(1프레임 마다 진입)
            if curr >= 1/FPS:
                curr -= 1/FPS
                Main.clear()
                Main.show_window()
                
                dial.set_val(Main.bot.get_vel())
                accdial.set_val(Main.bot.get_acc())
                
                temp_back_buff = [ " "*80 for _ in range(20)]
                replace_str(temp_back_buff, dial.show(),0,0)
                replace_str(temp_back_buff, accdial.show(),40,0)
                print('\n'.join(temp_back_buff))
                print("battery 80%")
                print("▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁")
                print("█████████████   ▕")
                print("▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")
                    
                
    #UI표시
    @staticmethod
    def show_window():
        W = 70
        gear = Main.bot.gear
        print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
        print('┃'+Main.name.center(W)+'┃')
        print('┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫')
        print('┃                                                                      ┃')
        print('┃                                                       ','╭──────────╮',' ┃')
        print('┃                                                       ','│',PRND[gear][0],'│',' ┃')
        print('┃                                                       ','│',PRND[gear][1],'│',' ┃')
        print('┃                                                       ','│',PRND[gear][2],'│',' ┃')
        print('┃                                                       ','│',PRND[gear][3],'│',' ┃')
        print('┃                                                       ','│',PRND[gear][4],'│',' ┃')
        print('┃                                                       ','│',PRND[gear][5],'│',' ┃')
        print('┃                                                       ','│',PRND[gear][6],'│',' ┃')
        print('┃                                                       ','╰──────────╯',' ┃')
        print('┃                                                            P R D     ┃')
        print('┃                                                                      ┃')
        print('┃  Tilt    0 '+Main.gauge_tilt()+' 150                        ┃')
        print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

    def gauge_v(length, start, end, val):
        mid = int(length*((val-start)/(end-start)))
        if mid < 0 :
            mid = 0
        if mid >= length:
            mid = length-1
        return "─"*(mid)+"●"+"─"*(length-mid-1)
    
    def gauge_tilt():
        return Main.gauge_v(30,0,150,Main.bot.get_vel())
    
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