#GUI
from color import Colors
from text import dot2
from text import dot4
from text import PRND

#module
from bot import Bot

#program
import os
import time
import math
import threading
FPS = 20

class Main:
    name="ROLLING  BOT"     #프로그램 이름(*짝수길이)
    state = 0           #메인루프 동작 상태(0:정상, -1:종료)
    start = 0           #프로그램 시작시간
    time = 0            #프로그램 동작시간
    
    bot = Bot("TEAM 3 BOT")
    
    velo = 0
    velobuff = 0

    #프로그램 시작 지점
    def entry():
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
    def loop():
        
        time.sleep(600)
    
    #**********    UI    *************
    
    #화면 지우기
    def clear():
        if os.name.split()[0] == "nt":
            os.system('cls')                #윈두우
        else :
            os.system('clear')              #리눅스/유닉스
    
    #UI의 메인루프
    def update():
        print('start ui')
        Main.start = time.time()
        elaps = Main.start
        Main.time = 0
        curr = 0
        gear = 0
        
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
                
                if Main.velobuff < 5:
                    Main.velo = 150
                if Main.velobuff > 149 :
                    Main.velo = 0
                    Main.bot.gear_select("down")
                    
                Main.velobuff += (Main.velo - Main.velobuff)/9
                Main.niddle_gauge(160+Main.velobuff, 30, 20, 15)
                
                #velocity
                print(Main.buff)
                print(' '*12, int(Main.velobuff),"cm/s")
            
                
    #UI표시
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

        #안티 앨리어싱
        # for i in range(2, H-2, 2):
        #     for j in range(1, W-1, 1):
        #         if Main.idea[i][j] == 0 and Main.idea[i+1][j] == 0:
        #             if Main.idea[i-2][j] == 1 and Main.idea[i-1][j] == 1 and Main.idea[i][j-1] == 1 and Main.idea[i+1][j-1] == 1:
        #                 Main.idea[i][j] = 1
        #             if Main.idea[i+2][j] == 1 and Main.idea[i+3][j] == 1 and Main.idea[i][j+1] == 1 and Main.idea[i+1][j+1] == 1:
        #                 Main.idea[i+1][j] = 1
                        
        Main.buff = ""
        for i in range(0, H, 2):
            for j in range(0, W, 1):
                if i == oriy and j == orix :
                    Main.buff += Colors.RED+ '▀' +Colors.DEF
                    continue
                Main.buff += dot2[Main.idea[i][j]*2+Main.idea[i+1][j]]
            Main.buff +=" \n"
            
        # for i in range(0, H, 4):
        #     for j in range(0, W, 2):
        #         a = Main.idea[i][j] | Main.idea[i+1][j]
        #         b = Main.idea[i][j+1] | Main.idea[i+1][j+1]
        #         c = Main.idea[i+2][j] | Main.idea[i+3][j]
        #         d = Main.idea[i+2][j+1] | Main.idea[i+3][j+1]
        #         Main.buff += dot4[a*8 + b*4 + c*2 + d*1]
        #     Main.buff +=" \n"   
            
        # for t in range(15):
        #     for l in range(15):
        #         count = 0
        #         count += 1 if Main.dist_point_to_line(l, t, orix, oriy, desx, desy) else -1
        #         count += 1 if Main.dist_point_to_line(l+1, t, orix, oriy, desx, desy) else -1
        #         count += 1 if Main.dist_point_to_line(l, t+1, orix, oriy, desx, desy) else -1
        #         count += 1 if Main.dist_point_to_line(l+1, t+1, orix, oriy, desx, desy) else -1
                    
        #         # if count == 4 or count == -4:
        #         #     Main.buff[t][l] = 0
        #         # else :
        #         #     Main.buff[t][l] = 1
                
        #         if l == int(orix) and t == int(oriy):
        #             Main.buff[t][l] = 1
        #         elif l == int(desx) and t == int(desy):
        #             Main.buff[t][l] = 1
        #         else :
        #             Main.buff[t][l] = 0
                    
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