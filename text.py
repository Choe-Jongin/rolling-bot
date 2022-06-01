
dot2 = [' ','▄','▀','█']
dot4 = [' ','▗','▖','▄','▝','▐','▞','▟','▘','▚','▌','▙','▀','▜','▛','█']
gauge = [' ','▏','▎','▍','▌','▋','▊','▉','█']

PRND = [["███████ ",
         "██    ██",
         "██    ██",
         "███████ ",
         "██      ",
         "██      ",
         "██      "],
        
        ["███████ ",
         "██    ██",
         "██    ██",
         "███████ ",
         "██  ██  ",
         "██   ██ ",
         "██    ██"],
        
        ["██████  ",
         "██   ██ ",
         "██    ██",
         "██    ██",
         "██    ██",
         "██   ██ ",
         "██████  "]]

def replace_str(ori:list , new:list , x:int, y:int):
    if ori == [] :
        return
    if new == [] :
        return
    
    ori_h = len(ori)        #원래 줄수
    if y >= ori_h:
        return 
    if x >= len(ori[0]):
        return
    
    insert_h = len(new)
    if insert_h > ori_h - y:
        insert_h = ori_h - y
    
    for i in range(0, insert_h):
        insert_w = len(new[i])
        if insert_w >= len(ori[y+i]) - x:
            insert_w = len(ori[y+i]) - x
        ori[y+i] = ori[y+i][:x] + new[i][0:insert_w] + ori[y+i][x+insert_w:]