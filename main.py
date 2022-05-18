#GUI
from color import Colors
from text import dot2
from text import dot4
from text import PRND

#module
from bot import Bot
from kbmanager import KM
import keyboard

#program
import os
import time
import math
import threading

FPS = 20

class Main:
    
    #프로그램 구성 요소 
    name="ROLLING  BOT"     #프로그램 이름(*짝수길이)
    state = 0           #메인루프 동작 상태(0:정상, -1:종료)
    start = 0           #프로그램 시작시간
    time = 0            #프로그램 동작시간
    
    #로봇 관련
    bot = Bot("TEAM 3 BOT")
    
    velo = 0
    velobuff = 0

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
            if KM.is_down('up'):
                Main.bot.up_acc(0.5)
            else :
                Main.bot.up_acc(-3)
                
            if KM.is_press('shift'):
                Main.bot.gear_select('down')
                
            if KM.is_down('esc'):
                run = 0
            time.sleep(0.1)
                    
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
                    
                Main.velobuff += (Main.bot.get_vel() - Main.velobuff)/3
                Main.niddle_gauge(160+Main.velobuff, 30, 20, 15)
                
                #velocity
                print(Main.buff)
                print(' '*12, int(Main.velobuff),"cm/s")
            
    #UI표시
    @staticmethod
    def show_window():
        W = 70
        T = str(int(Main.time))+'s'+' '*(5-len(str(int(Main.time))))
        gear = Main.bot.gear
        print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
        print('┃'+' '*((W-len(Main.name))//2)+Main.name+' '*((W-len(Main.name))//2)+'┃')
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
        print('┃                                                                      ┃')
        print('┃                                                                      ┃')
        print('┃                                                                      ┃')
        print('┃                                                                      ┃')
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
        return Main.gauge_v(30,0,150,Main.velobuff)
    
    vel_buff = 0
    def gauge_vel():
        Main.vel_buff = Main.tilevel_buffbuff + (Main.time+5-Main.vel_buff)/5
        return Main.gauge_v(30,0,10,Main.vel_buff)
    
    def niddle_gauge(deg, W, H, length):
        deg = deg%360
        rad = math.radians(deg)
        orix, oriy = W/2, H*4/5;
        desx, desy = orix + length*math.cos(rad) + 0.5, oriy + length*math.sin(rad) + 0.5;
                 
        Main.idea = [[0 for _ in range(W+1)] for _ in range(H+1)]
        rep = 2
        for i in range(length*rep):
            x, y = orix + i/rep*math.cos(rad) + 0.5, oriy + i/rep*math.sin(rad) + 0.1;
            if x < 0 or y < 0 or x > W or y > H :
                continue 
            Main.idea[int(y)][int(x)] = 1
                        
        Main.buff = ""
        for i in range(0, H, 2):
            for j in range(0, W, 1):
                if i == oriy and j == orix :
                    Main.buff += Colors.RED+ '▀' +Colors.DEF
                    continue
                Main.buff += dot2[Main.idea[i][j]*2+Main.idea[i+1][j]]
            Main.buff +=" \n"
            
    def dist_point_to_line(x, y, x1, y1, x2, y2):
        distance = (y1-y2)*x + (x2-x1)*y + (x1*y2- x2*y1) / math.sqrt((y2-y1)**2 + (x2-x1)**2);
        return distance

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