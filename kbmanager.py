import keyboard
from enum import Enum


class key_state(Enum):
    NO      = 0
    UP      = 1
    PRESS   = 2
    DOWN    = 3
    RELESE  = 4

class KM:
    
    keylist = {}    #인식할 키 목록
    
    @staticmethod
    def set_key_list(list):
        for key in list:
            KM.keylist[key] = key_state.UP
        if KM.keylist[key] == [] :
            KM.keylist['esc'] = key_state.UP
            
    @staticmethod
    def update():
        
        for key in KM.keylist:
            #안눌린 상태에서
            if  KM.keylist[key] == key_state.UP :
                # 누름
                if keyboard.is_pressed(key) == True:
                    KM.keylist[key]= key_state.PRESS
            
            #눌린 상태에서
            elif  KM.keylist[key] == key_state.PRESS or KM.keylist[key] == key_state.DOWN :
                # 계속 누름
                if keyboard.is_pressed(key) == True:
                    KM.keylist[key] = key_state.DOWN
                # 땜
                elif keyboard.is_pressed(key) == False:
                    KM.keylist[key] = key_state.RELESE
            
            #눌럿다 땐 상태에서
            elif  KM.keylist[key] == key_state.RELESE :
                # 다시 누름
                if keyboard.is_pressed(key) == True:
                    KM.keylist[key] = key_state.PRESS
                # 안 눌름 
                else :
                    KM.keylist[key] = key_state.UP
                    
    @staticmethod      
    def get_key_state(key):
        if key in KM.keylist == False:
            return key_state.NO
        return KM.keylist[key]    
    
    @staticmethod
    def is_press(key):
        if key in KM.keylist == False:
            return False
        if KM.get_key_state(key) == key_state.PRESS:
            return True
        return False
    
    @staticmethod
    def is_down(key):
        if key in KM.keylist == False:
            return False
        if KM.get_key_state(key) == key_state.PRESS or KM.get_key_state(key) == key_state.DOWN:
            return True
        return False
    
    @staticmethod
    def is_relese(key):
        if key in KM.keylist == False:
            return False
        if KM.get_key_state(key) == key_state.RELESE:
            return True
        return False
    