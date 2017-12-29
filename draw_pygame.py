#coding:utf-8
import pygame,sys,math
from pygame.color import THECOLORS
from datetime import *  
'''
Author: Gao Mengru<mgao@microstrategy.com>
Date: Dec 26,2017
Functionality: receive a specialized data structure and draw graph to visualize the relations
'''

def visualize(data):
    GRAPH_SIZE=0


    #for links between funcs
    func_links=[]
    funcs_list=[]
    for k,v in data.items():
        funcs_list.extend(v.keys())


    #print len(data.items())
    for k,v in data.items():
        #print k,v
        item_func_num=len(v.keys())
        tmp=set()
        for kk,vv in v.items():
            for vvv in vv:
                if vvv not in funcs_list:
                    tmp.add(vvv)
                else:
                    func_links.append((kk,vvv))    
        # 获取当前 cluster 中 variables 的个数            
        item_var_num=len(tmp)
        GRAPH_SIZE+=max(item_func_num,item_var_num)
        #print "func_num:",item_func_num,'var_num',item_var_num
    #print(len(func_links))
    #print 'graph_size:',GRAPH_SIZE
    #定义 矩形和椭圆形 单元 的 长和宽
    #print("手动count——func的数量:",len(funcs_list))
    RECT_SIZE_WIDTH=50
    RECT_SIZE_HEIGHT=30

    # 单元与单元之间的间隔
    SPARE=5

    # 画布的长和宽
    CANVAS_WIDTH=(RECT_SIZE_WIDTH+2*SPARE)*GRAPH_SIZE-3*SPARE
    CANVAS_HEIGHT=600


    #模块初始化，任何pygame程序均需要执行此句
    pygame.init()
    #定义窗口的标题为'MSTR_Hackathon2017'
    screencaption=pygame.display.set_caption('MSTR Hackathon2017')
    #定义窗口大小为
    screen=pygame.display.set_mode([CANVAS_WIDTH,CANVAS_HEIGHT])
    #用白色填充窗口
    screen.fill([255,255,255])
    #设置字体
    my_font = pygame.font.SysFont("arial", 10)

    #把变量myimage赋给导入的图片
    myimage=pygame.image.load('floppy-icon.jpg') 
    screen.blit(myimage,[20,20])

    # 全局变量
    # 矩形的定位
    rect_top=150
    rect_left=0
    # 椭圆的定位
    ellipse_top=CANVAS_HEIGHT-150
    ellipse_left=0

    # 连线的高度定位
    LINE_START_HEIGHT=rect_top+RECT_SIZE_HEIGHT
    LINE_END_HEIGHT=ellipse_top



    memo=0
    total_v_for_key=[]
    for k,v in data.items():
        # 获取当前 cluster 中 func 的个数
        item_func_num=len(v.keys())

        tmp=[]
        for kk,vv in v.items():
            for vvv in vv:
                if (vvv not in tmp) and (vvv not in funcs_list):
                    tmp.append(vvv)

          
        item_var_num=len(tmp)

        '''
        比较 func部分的画布长度 和 variable部分的画布长度
        选择较大的那个作为subfigure的width
        同时 rect_left 和 ellipse_left 定位 也可以确定
        memo: 用于记录当前已经使用的画布的长度
        一旦剩余画布长度不够画，我们必须另起一行
        '''
        sub_rect_width=(RECT_SIZE_WIDTH+SPARE)*item_func_num+SPARE
        sub_ellipse_width=(RECT_SIZE_WIDTH+SPARE)*item_var_num+SPARE
        if sub_rect_width>sub_ellipse_width:
            rect_left+=SPARE
            ellipse_left+=(sub_rect_width-2*SPARE)/(item_var_num+1)-RECT_SIZE_WIDTH/2
            memo+=sub_rect_width
        else:
            ellipse_left+=SPARE
            rect_left+=(sub_ellipse_width-2*SPARE)/(item_func_num+1)-RECT_SIZE_WIDTH/2
            memo+=sub_ellipse_width

        '''
        v1 用于保存当前 cluster 所有的 func 的 矩形的下边的中点x坐标
        v1: rect_left+RECT_SIZE_WIDTH/2
        v2 用于保存当前 cluster 所有的 var 的 椭圆的上边的中点x坐标
        v2: ellipse_left+RECT_SIZE_WIDTH/2
        用于后续绘制连线用
        text_surface 用于填充标签
        '''
        v1=[]
        for kk in v.keys():
            pygame.draw.rect(screen,[255,0,0],[rect_left,rect_top,RECT_SIZE_WIDTH,RECT_SIZE_HEIGHT],2)
            v1.append(rect_left+RECT_SIZE_WIDTH/2)
            text_surface = my_font.render(kk, True, (0,0,0), (255, 255, 255))
            textRectObj = text_surface.get_rect()  # 获得要显示的对象的rect
            textRectObj.center = (rect_left+RECT_SIZE_WIDTH/2, rect_top+RECT_SIZE_HEIGHT/2)  # 设置显示对象的坐标
            screen.blit(text_surface, textRectObj) 
            rect_left+=(RECT_SIZE_WIDTH+SPARE)
        #print v1
        total_v_for_key.extend(v1)
        v2=[]
        for i in range(item_var_num):
            pygame.draw.ellipse(screen, [255,0,255], [ellipse_left, ellipse_top, RECT_SIZE_WIDTH,RECT_SIZE_HEIGHT], 2)
            v2.append(ellipse_left+RECT_SIZE_WIDTH/2)
            text_surface = my_font.render(tmp[i], True, (0,0,0), (255, 255, 255))
            textRectObj = text_surface.get_rect()  # 获得要显示的对象的rect
            textRectObj.center = (ellipse_left+RECT_SIZE_WIDTH/2, ellipse_top+RECT_SIZE_HEIGHT/2)  # 设置显示对象的坐标
            screen.blit(text_surface, textRectObj)    
            ellipse_left+=(RECT_SIZE_WIDTH+SPARE) 
        #print v2
        '''
        画连接线
        因为使用了OrderDict，所以可以再次迭代一遍
        tmp3: 记录当前 keys() 迭代到第几个了，用于遍历 v1
        tmp2: 记录当前 keys() 下的 dict对象的 value 迭代到第几个了
        '''
        tmp3=0
        tmp2=[]
        for kk,vv in v.items():
            #print kk,vv
            x=v1[tmp3] 
            for vvv in vv:
                if vvv in funcs_list:
                    continue
                #print kk,vvv,tmp2
                if vvv in tmp2:
                    idx=tmp2.index(vvv)
                else:
                    idx=len(tmp2)
                    tmp2.append(vvv)
                y=v2[idx]
                #print kk,vvv,tmp3,idx
                pygame.draw.aaline(screen, (0, 0, 0), (x, LINE_START_HEIGHT), (y,LINE_END_HEIGHT))
            tmp3+=1  
        #print len(v1),len(v2)              
        rect_left=memo
        ellipse_left=rect_left
    #print(funcs_list)
    #print(total_v_for_key)
    #print(len(total_v_for_key),len(funcs_list),len(data.keys()))  #54个func
    for tup in func_links:
        x1=total_v_for_key[funcs_list.index(tup[0])]
        x2=total_v_for_key[funcs_list.index(tup[1])]
        #print(x1,x2,tup[0],tup[1])
        hhh=rect_top-RECT_SIZE_HEIGHT if (x2-x1)/10>rect_top-RECT_SIZE_HEIGHT else (x2-x1)/10
        #pygame.draw.arc( screen, (0,0,0), ( 150, 150, 100, 100 ), 0, math.pi, 2 )  #(x轴，y轴，横跨的长度，高度)
        if x1<x2:
            pygame.draw.arc( screen, (0,0,0), ( x1, rect_top-RECT_SIZE_HEIGHT, x2-x1, 60), 0, math.pi, 1 )
        elif x1>x2:
            pygame.draw.arc( screen, (0,0,0), ( x2, rect_top-RECT_SIZE_HEIGHT, x1-x2, 60 ), 0, math.pi, 1 ) 
        else: 
            #print(x1,x2,tup[0],tup[1])
            continue    


    pygame.display.flip()


    while True:
        for event in pygame.event.get():
            #判断鼠标位置以及是否摁了下去
            if (event.type==pygame.MOUSEBUTTONDOWN) and (20<=event.pos[0]<=84) and (20<=event.pos[1]<=84):
                myimage2=pygame.image.load('floppy-icon-2.jpg') 
                screen.blit(myimage2,[20,20])
                pygame.display.flip()
                myimage2=pygame.image.load('white.jpg') 
                screen.blit(myimage2,[20,20])
                pygame.display.flip()
                #pygame.time.delay(500)
                fname=str(datetime.now().strftime("%Y%m%d%H%M%S"))+'.png'
                pygame.image.save(screen, fname)
                screen.blit(myimage,[20,20])
                pygame.display.flip()
            if event.type==pygame.QUIT:
                sys.exit()    

#draw_fig(data)

