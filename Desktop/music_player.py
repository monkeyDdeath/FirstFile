

import pygame
from pygame.locals import *
import sys
import time
import os


# 颜色
white = (255, 255, 255)
red = (255, 0 ,0)
gree = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
yellow = (255, 255, 128)
high_green = (128, 255, 0)
paint_blue = (64, 231, 244)
grey = (192, 192, 192)

bg_color = white

# 绘制面板
def drawboard():
    displayURF.fill(bg_color)
    split_line1 = pygame.draw.rect(displayURF, paint_blue, (80,0,5,500))
    split_line2 = pygame.draw.rect(displayURF, paint_blue, (900,0,5,500))
    draw_right_button()
    draw_songs()

# 右边控制按钮文本
def right_button():
    text_list = ['开始', '暂停/播放', '下一首歌', '上一首歌', '随机播放', '顺序播放']
    init_top_ori = 150
    init_left_ori = 950
    init_top_high = 150
    init_left_high = 950
    text_store_ori = list()
    text_store_high = list()
    for text in text_list:
        text_surf = fontObj1.render(text, True, grey, white)
        text_rect = text_surf.get_rect()
        text_rect.center = (init_left_ori, init_top_ori)
        text_store_ori.append((text_surf, text_rect))
        init_top_ori += 40
    for text in text_list:
        text_surf = fontObj1.render(text, True, high_green, blue)
        text_rect = text_surf.get_rect()
        text_rect.center = (init_left_high, init_top_high)
        text_store_high.append((text_surf, text_rect))
        init_top_high += 40
    return (text_store_ori, text_store_high)

# 绘制右边控制按钮
def draw_right_button():
    # 两种方案存储的值
    text_store_ori, text_store_high = right_button()
    # 新的位置列表
    text_last = list()
    '''
    变色的思路就是，先提供两个方案的存储值，鼠标移动到哪里就向新的位置列表里添加
    那个的高亮方案
    '''
    for i, element in enumerate(text_store_ori):
        if element[1].collidepoint(spotx, spoty):
            text_last.append(text_store_high[i])
        else:
            text_last.append(element)
    for surf, rect in text_last:
        displayURF.blit(surf, rect)
   
# ----------播放选项---------------
def start():
    # 该功能实际上是全部重新开始
    song_name_last, song_path_list = load_songs()
    pygame.mixer.music.load(song_path_list[0].encode('utf-8'))
    pygame.mixer.music.play(-1)

def pause():
    if pygame.mixer.music.get_busy():
        time1 = pygame.mixer.music.get_pos()
        time.sleep(0.001)
        time2 = pygame.mixer.music.get_pos()
        if time1 == time2:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

def next_song():
    print('next')

def front_song():
    print('front')

def loop_play():
    print('loop')

def random_play():
    print('random')
# ----------播放选项---------------

# 响应鼠标按下事件
def func_execute():
    text_store_ori, text_store_high = right_button()
    for i, element in enumerate(text_store_ori):
        if element[1].collidepoint(spotx, spoty):
            if i == 0:
                start()
            elif i == 1:
                pause()
            elif i == 2:
                next_song()
            elif i == 3:
                front_song()
            elif i == 4:
                random_play()
            elif i == 5:
                loop_play()
               
# 读取存储的歌名
def load_songs():
    songs_list = os.listdir(r'.\music')
    song_name_list = list()
    song_path_list = list()
    for song in songs_list:
        song_name = song.split('.')
        song_name_list.append(song_name[0])
        song_path = os.path.join('.\music', song)
        song_path_list.append(song_path)
    return (song_name_list, song_path_list)
    
# 转化为待传歌名
def songs_to_blit():
    title = '歌单列表'
    title_surf = fontObj1.render(title, True, white, blue)
    title_rect = title_surf.get_rect()
    title_rect.center = (40, 10)
    title_store = (title_surf, title_rect)
    
    # 显示全部歌名和部分歌名列表
    song_name_list_ori, song_path_list = load_songs()
    song_name_list_high = list()
    for name in song_name_list_ori:
        highname = name[0:8]
        song_name_list_high.append(highname)
    
    init_top_ori = 45
    init_left_ori = 40
    init_top_high = 45
    init_left_high = 40
    
    name_store_ori = list()
    name_store_high = list()
    for name in song_name_list_ori:
        name_surf = fontObj2.render(name, True, red, white)
        name_rect = name_surf.get_rect()
        name_rect.center = (init_left_ori, init_top_ori)
        name_store_ori.append((name_surf, name_rect))
        init_top_ori += 20
    for name in song_name_list_high:
        name_surf = fontObj2.render(name, True, black, white)
        name_rect = name_surf.get_rect()
        name_rect.center = (init_left_high, init_top_high)
        name_store_high.append((name_surf, name_rect))
        init_top_high += 20
    return (title_store, name_store_ori, name_store_high)

def draw_songs():
    title, oriname, highname = songs_to_blit()
    title_surf, title_rect = title
    displayURF.blit(title_surf, title_rect)
    
    song_name_last = list()
    for i, element in enumerate(oriname):
        if element[1].collidepoint(spotx, spoty):
            song_name_last.append(element)
        else:
            song_name_last.append(highname[i])
    
    for surf, rect in song_name_last:
        displayURF.blit(surf, rect)

def player():
    global displayURF, fontObj1, spotx, spoty, fontObj2
    pygame.init()
    pygame.mixer.init()
    displayURF = pygame.display.set_mode((1000, 500))
    fps = pygame.time.Clock()
    
    # 字体设置
    fontObj1 = pygame.font.SysFont('kaiti', 20)
    fontObj2 = pygame.font.SysFont('fangsong', 10)
    
    # 鼠标位置
    spotx = 0
    spoty = 0
    
    while True:
        drawboard()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEMOTION:
                spotx, spoty = event.pos[0], event.pos[1]
                
            elif event.type == MOUSEBUTTONUP:
                func_execute()
        
        pygame.display.update()
        fps.tick(50)
        

if __name__ == '__main__':
    player()
