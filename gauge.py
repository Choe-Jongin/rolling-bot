
from email.mime import image
import math
from color import Colors
import text
from text import dot2
from text import dot4

#추상화 클래스
class Gauge:
    def __init__(self, name, min, max, delay = 1, unit = "U"):
        self.name   = name
        self.min    = min
        self.max    = max
        self.delay  = delay
        self.unit   = unit
        
        self.val    = self.min
        self.valbuff = 0
        
    def get_name(self):
        return self.name
    
    def get_min(self):
        return self.min 
    
    def get_max(self):
        return self.max 
    
    def get_val(self):
        return self.val
    
    def get_per(self):
        return (self.val - self.min) / (self.max - self.min)
    
    def val_update(self):
        self.valbuff += (self.val - self.valbuff)/self.delay
        
    def set_val(self, amount):
        self.val = amount
        if self.val < self.min:
            self.val = self.min
        if self.val > self.max:
            self.val = self.max
    
    def get_per(self):
        return (self.valbuff - self.min) / (self.max - self.min)

#회전 게이지
class DialGauge(Gauge):
    def __init__(self, name, min, max, r, length, rotation = 200, delay = 1):
        super().__init__(name,min,max,delay)
        self.r = r                          #radius
        self.length = length                #length of niddle
        self.rotation = rotation            #max turning rotation
        self.base_r = 270 - self.rotation/2 #게이지가 시작되는 각도
        
        #시작 좌표(바늘의 회전 축)
        self.orix, self.oriy = self.r-1, self.r-1
        
        #각도가 반원이 넘어가게 되면 바늘중심 아래에 추가공간이 필요함
        extra_y = math.ceil(self.length*math.sin(math.radians(self.base_r)))
        if extra_y < 4:
            extra_y = 4
        self.W = int(self.r*2)               #출력할 영역의 너비
        self.H = int(self.r + extra_y)       #출력할 영역의 높이
        
        #데이터가 저장될 영역
        self.idea = [ [0 for _ in range(self.W)] for _ in range(self.H)]    # 본질적인 값
        self.image = [""]                                                   # 본질을 시각화
        
        #detail settings
        self.base_r_offset = 0          #중간값이 가운데에서 돌아가게 적용
        self.show_val   = True          #출력시 값 출력
        self.show_unit  = True          #출력시 단위 출력
        self.show_name  = True          #출력시 이름 출력
        
    #문자열 배열로 반환
    def show(self):
        self.val_update()                       #버퍼적용
        rad = math.radians((self.base_r + self.rotation * self.get_per())) #라디안 각도
        
        #끝 좌표
        desx, desy = self.orix + self.length*math.cos(rad), self.oriy + self.length*math.sin(rad);
    
        #시작 -> 목표까지 점을 기록
        self.idea = [[0 for _ in range(self.W)] for _ in range(self.H)]
        rep = 3
        for i in range(self.length*rep):
            x, y = self.orix + i/rep*math.cos(rad) + 0.5, self.oriy + i/rep*math.sin(rad) + 0.5;
            if x < 0 or y < 0 or x > self.W or y > self.H :
                continue 
            self.idea[int(y)][int(x)] = 1
        
        #본질을 기반으로 눈에 보여질 문자열 생성
        self.image = []
        for i in range(0, self.H, 2):
            self.image.append("")
            for j in range(0, self.W, 1):
                if i+1 == self.H:
                    self.image[i//2] += dot2[self.idea[i][j]]
                else :
                    self.image[i//2] += dot2[self.idea[i][j]*2+self.idea[i+1][j]]
            # self.image +=" \n"
            
        text.replace_str(self.image, [str(int(self.val))], self.r - len(str(int(self.val)))//2 - 1, self.r//2)
        text.replace_str(self.image, [self.name], self.r - len(self.name)//2 - 1, self.r//2+1)
        
        return self.image

    #필수 호출은 아님 필요시 원하는 옵션을 넣어 설정 적용
    def set_detail(self, show_val = None, show_unit = None, show_name = None, base_offset = None, unit = None):
        if show_val != None :
            self.show_val = show_val
        if show_unit != None :
            self.show_unit = show_unit
        if show_name != None :
            self.show_name = show_name
        if unit != None :
            self.unit = unit
        
        #바늘의 시작 위치를 바꿈
        if base_offset != None :
            self.base_r_offset = base_offset
            self.base_r = self.base_r + self.base_r_offset
            
            #시작 좌표(바늘의 회전 축)
            extra_y = math.ceil(self.length*math.sin(math.radians(self.base_r)))  #각도가 반원이 넘어가게 되면 바늘중심 아래로도 공간이 필요함
            if extra_y < math.ceil(self.length*math.sin(math.radians(self.base_r+self.rotation))): #왼쪽보다 오른쪽이 더 아래로 가면 기준이 이 쪽
                extra_y = math.ceil(self.length*math.sin(math.radians(self.base_r+self.rotation)))
            self.W = int(self.r*2)               #출력할 영역의 너비
            self.H = int(self.r + extra_y)       #출력할 영역의 높이
            
            #데이터가 저장될 영역
            self.idea = [ [0 for _ in range(self.W)] for _ in range(self.H)]    # 2r by r int array 본질적인 값
