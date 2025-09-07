'''
打包最终文件
'''
import pygame
import sys
import time
import random
SCREEN_WIDTH=1600
SCREEN_HEIGHT=1000
BG_COLOR=pygame.Color(255,255,255,255)
TEXT_COLOR=pygame.Color(0,0,0)
#定义一个基类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
       pygame.sprite.Sprite.__init__(self)
class MainGame():
    window = None
    my_tank = None
    his_tank = None
    red_bar = None
    blud_bar = None
    cokespeed = None
    pepsispeed = None
    red_long = 0
    blue_long = 0
    coke_win = None
    pepsi_win = None
    begin = None
    genshin = True
    pass1 = False
    pass2 = False
    pass3 = False
    genshin_again = False
    score_box = True
    score1 = 0
    score2 = 0
    count = 0
    coke_death = 0
    pepsi_death = 0
    #按钮列表
    buttonDict = {}
    #存储人机可乐的列表
    enemyColaList = []
    #定义人机可乐的数量
    enemyColaCount = 0
    #存储玩家子弹的列表
    myBulletList = []
    hisBulletList = []
    #存储爆炸效果的列表
    explodeList = []
    #存储墙壁的列表
    wallList = []
    #创建领域
    area = None
    def __init__(self):
        pass
    #开始界面
    def beginGame(self):
        #加载主窗口
        #初始化窗口
        pygame.display.init()
        #设置窗口的大小以及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        #设置窗口的标题
        pygame.display.set_caption('Coke vs Pepsi')
        #初始化开始画面
        self.createBegin()
        #初始化按钮
        self.createButton()
        #设置游戏图标
        icon = pygame.image.load('img/icon.ico')
        pygame.display.set_icon(icon)
        while True:
            MainGame.window.fill(BG_COLOR)
            #绘制正常的开始游戏
            if MainGame.genshin:
                self.blitBegin()
                self.blitButton('begin1')
                if MainGame.buttonDict['begin1'].rect.collidepoint(pygame.mouse.get_pos()):
                    #展示激活的按钮
                    self.blitButton('begin2')
            self.getEvent()
            pygame.display.update()
    #开始游戏，关卡3
    def start_game(self):
        #初始化玩家可乐
        MainGame.my_tank = Cola(0.1*SCREEN_WIDTH,0.5*SCREEN_HEIGHT,10)
        MainGame.his_tank = MyTank(0.9*SCREEN_WIDTH,0.5*SCREEN_HEIGHT,10)
        #初始化领域
        self.createArea()
        while MainGame.pass1:
            #清屏
            MainGame.window.fill(BG_COLOR)
            #清理墙壁
            MainGame.wallList.clear()
            #设置循环一次的用时,为了降低可乐移速
            time.sleep(0.003)  #暂停程序运行的时间
            if MainGame.score_box:
                MainGame.window.blit(self.getTextSurface(f'Coke vs Pepsi = {MainGame.score1}:{MainGame.score2}'),(10,20))
                MainGame.window.blit(self.getTextSurface(f'CokeDeaths:{MainGame.coke_death}'),(10,80))
                MainGame.window.blit(self.getTextSurface(f'PepsiDeaths:{MainGame.pepsi_death}'),(10,140))
                MainGame.window.blit(self.getTextSurface(f'战绩可以按下Tab隐藏'),(10,200))
            MainGame.window.blit(self.getTextSurface('关卡3:全区域内移速增加'),(550,80))
            self.getEvent()
            #展示领域
            self.blitArea()
            MainGame.my_tank.displayTank()
            MainGame.his_tank.displayTank()
            #画进度条
            #初始化进度条
            self.createBar()
            self.blitBar()
            if MainGame.red_long <= SCREEN_WIDTH:
                self.my_tank.inArea()
            if MainGame.blue_long <= SCREEN_WIDTH:
                self.his_tank.inArea()
            #循环遍历我方子弹列表，展示我方子弹
            self.blitMyBullet()      #试过了
            self.blitHisBullet()
            #循环遍历爆炸列表，展示爆炸效果
            self.blitExplode()
            #循环遍历墙壁列表，展示墙壁
            self.biltWall()
            #调用相撞的方法
            self.bullet_hit_wall()
            #胜利加分
            if MainGame.red_long >= SCREEN_WIDTH:
                MainGame.score1 += 1
                MainGame.red_long = 0
                MainGame.blue_long = 0
                MainGame.pass1 = False
                if MainGame.score1 == 2:
                    self.displayfinal('coke')
                    break
            if MainGame.blue_long >= SCREEN_WIDTH:
                MainGame.score2 += 1
                MainGame.red_long = 0
                MainGame.blue_long = 0
                MainGame.pass1 = False
                if MainGame.score2 == 2:
                    self.displayfinal('pepsi')
                    break
            #玩家控制可乐移动
            #player1
            if MainGame.my_tank.button_left:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_right==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_down==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_up==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            if MainGame.my_tank.live:
                MainGame.my_tank.cola_hit()
            #player2
            if MainGame.his_tank.button_left:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_right==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_down==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_up==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            if MainGame.his_tank.live:
                MainGame.his_tank.cola_hit()
            pygame.display.update()
    #关卡2
    def start_game2(self):
        #初始化玩家可乐
        MainGame.my_tank = Cola(0.1*SCREEN_WIDTH,0.5*SCREEN_HEIGHT,3)
        MainGame.his_tank = MyTank(0.9*SCREEN_WIDTH,0.5*SCREEN_HEIGHT,3)
        #初始化墙壁
        self.createWall('pass2')
        #初始化领域
        self.createArea()
        #初始化加速带图像
        self.createSpeedBar()
        while MainGame.pass2:
            #清屏
            MainGame.window.fill(BG_COLOR)
            #设置循环一次的用时,为了降低可乐移速
            time.sleep(0.003)  #暂停程序运行的时间
            #画加速带
            self.blitSpeedBar()
            if MainGame.score_box:
                MainGame.window.blit(self.getTextSurface(f'Coke vs Pepsi = {MainGame.score1}:{MainGame.score2}'),(10,20))
                MainGame.window.blit(self.getTextSurface(f'CokeDeaths:{MainGame.coke_death}'),(10,80))
                MainGame.window.blit(self.getTextSurface(f'PepsiDeaths:{MainGame.pepsi_death}'),(10,140))
                MainGame.window.blit(self.getTextSurface(f'战绩可以按下Tab隐藏'),(10,200))
            MainGame.window.blit(self.getTextSurface('关卡2:加速带内移速增加'),(575,80))
            self.getEvent()
            #展示领域
            self.blitArea()
            MainGame.my_tank.displayTank()
            MainGame.his_tank.displayTank()
            #画进度条
            #初始化进度条
            self.createBar()
            self.blitBar()
            if MainGame.red_long <= SCREEN_WIDTH:
                self.my_tank.inArea()
            if MainGame.blue_long <= SCREEN_WIDTH:
                self.his_tank.inArea()
            #循环遍历我方子弹列表，展示我方子弹
            self.blitMyBullet()      #试过了
            self.blitHisBullet()
            #泉水内移速增加
            if MainGame.my_tank.rect.left > 400:
                MainGame.my_tank.speed = 5
            elif MainGame.my_tank.rect.left <= 400:
                MainGame.my_tank.speed = 20
            if MainGame.his_tank.rect.left < 1200:
                MainGame.his_tank.speed = 5
            elif MainGame.his_tank.rect.left >= 1200:
                MainGame.his_tank.speed = 20
            #循环遍历爆炸列表，展示爆炸效果
            self.blitExplode()
            #循环遍历墙壁列表，展示墙壁
            self.biltWall()
            #调用相撞的方法
            self.bullet_hit_wall()
            #胜利结算画面
            if MainGame.red_long >= SCREEN_WIDTH:
                MainGame.score1 += 1
                MainGame.red_long = 0
                MainGame.blue_long = 0
                MainGame.pass2 = False
                if MainGame.score1 == 2:
                    self.displayfinal('coke')
                    break
                MainGame.pass1 = True
                MainGame().start_game()
            if MainGame.blue_long >= SCREEN_WIDTH:
                MainGame.score2 += 1
                MainGame.pass2 = False
                MainGame.red_long = 0
                MainGame.blue_long = 0
                if MainGame.score2 == 2:
                    self.displayfinal('pepsi')
                    break
                MainGame.pass1 = True
                MainGame().start_game()
            #玩家控制可乐移动
            #player1
            if MainGame.my_tank.button_left:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_right==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_down==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_up==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            if MainGame.my_tank.live:
                MainGame.my_tank.cola_hit()
            #player2
            if MainGame.his_tank.button_left:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_right==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_down==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_up==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            if MainGame.his_tank.live:
                MainGame.his_tank.cola_hit()
            pygame.display.update()
    #关卡1
    def start_game3(self):
        #初始化玩家可乐
        MainGame.my_tank = Cola(0.1*SCREEN_WIDTH,0.5*SCREEN_HEIGHT,3)
        MainGame.his_tank = MyTank(0.9*SCREEN_WIDTH,0.5*SCREEN_HEIGHT,3)
        #初始化墙壁
        self.createWall('pass3')
        #初始化领域
        self.createArea()
        while MainGame.pass3:
            #清屏
            MainGame.window.fill(BG_COLOR)
            #设置循环一次的用时,为了降低可乐移速
            time.sleep(0.003)  #暂停程序运行的时间
            if MainGame.score_box:
                MainGame.window.blit(self.getTextSurface(f'Coke vs Pepsi = {MainGame.score1}:{MainGame.score2}'),(10,20))
                MainGame.window.blit(self.getTextSurface(f'CokeDeaths:{MainGame.coke_death}'),(10,80))
                MainGame.window.blit(self.getTextSurface(f'PepsiDeaths:{MainGame.pepsi_death}'),(10,140))
                MainGame.window.blit(self.getTextSurface(f'战绩可以按下Tab隐藏'),(10,200))
            MainGame.window.blit(self.getTextSurface('关卡1:墙可以被打破'),(575,80))
            self.getEvent()
            #展示领域
            self.blitArea()
            MainGame.my_tank.displayTank()
            MainGame.his_tank.displayTank()
            #画进度条
            #初始化进度条
            self.createBar()
            self.blitBar()
            if MainGame.red_long <= SCREEN_WIDTH:
                self.my_tank.inArea()
            if MainGame.blue_long <= SCREEN_WIDTH:
                self.his_tank.inArea()
            #循环遍历我方子弹列表，展示我方子弹
            self.blitMyBullet()      #试过了
            self.blitHisBullet()
            #循环遍历爆炸列表，展示爆炸效果
            self.blitExplode()
            #循环遍历墙壁列表，展示墙壁
            self.biltWall()
            #调用相撞的方法
            self.bullet_hit_wall()
            #胜利结算画面
            if MainGame.red_long >= SCREEN_WIDTH:
                MainGame.score1 += 1
                MainGame.pass1 = False
                MainGame.pass2 = True
                MainGame.red_long = 0
                MainGame.blue_long = 0
                MainGame().start_game2()
                # MainGame.score1 += 1
                # MainGame.red_long = 0
                # MainGame.blue_long = 0
                # MainGame.pass3 = False
                # if MainGame.score1 == 2:
                #     self.displayfinal('coke')
                #     break
            if MainGame.blue_long >= SCREEN_WIDTH:
                MainGame.score2 += 1
                MainGame.pass1 = False
                MainGame.pass2 = True
                MainGame.red_long = 0
                MainGame.blue_long = 0
                MainGame().start_game2()
                # MainGame.score2 += 1
                # MainGame.red_long = 0
                # MainGame.blue_long = 0
                # MainGame.pass3 = False
                # if MainGame.score1 == 2:
                #     self.displayfinal('pepsi')
                #     break
            #玩家控制可乐移动
            #player1
            if MainGame.my_tank.button_left:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_right==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_down==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            elif MainGame.my_tank.button_up==True:
                MainGame.my_tank.move()
                MainGame.my_tank.hitWall()
            if MainGame.my_tank.live:
                MainGame.my_tank.cola_hit()
            #player2
            if MainGame.his_tank.button_left:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_right==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_down==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            elif MainGame.his_tank.button_up==True:
                MainGame.his_tank.move()
                MainGame.his_tank.hitWall()
            if MainGame.his_tank.live:
                MainGame.his_tank.cola_hit()
            pygame.display.update()
    def blitEnemyCola(self):
        for enemy in MainGame.enemyColaList:
            if enemy.live:
                enemy.displayTank()
                enemy.randMove()
            else:
                MainGame.enemyColaList.remove(enemy)
    #创建结算动画
    def createWin(self):
        MainGame.coke_win = Win(0.25*SCREEN_WIDTH,0.1*SCREEN_HEIGHT,'coke')
        MainGame.pepsi_win = Win(0.25*SCREEN_WIDTH,0.1*SCREEN_HEIGHT,'pepsi')
    #创建按钮
    def createButton(self):
        button1 = Button(680,850,'begin1')
        button2 = Button(680,850,'begin2')
        again = Button(1500,0,'again')
        MainGame.buttonDict['begin1'] = button1
        MainGame.buttonDict['begin2'] = button2
        MainGame.buttonDict['again'] = again
    def blitButton(self,which):
        if which == 'begin1':
            MainGame.buttonDict['begin1'].displayButton()
        elif which == 'begin2':
            MainGame.buttonDict['begin2'].displayButton()
        elif which == 'again':
            MainGame.buttonDict['again'].displayButton()
    def displayfinal(self,who):
        self.createWin()
        if who == 'coke':
            while True:
                #清屏
                MainGame.window.fill(BG_COLOR)
                self.getEvent()
                MainGame.coke_win.displayWin()
                MainGame.window.blit(self.getTextSurface(f'Coke Win！！！'),(400,50))
                MainGame.window.blit(self.getTextSurface(f'Coke vs Pepsi = {MainGame.score1}:{MainGame.score2}'),(400,900))
                self.blitButton('again')
                if MainGame.genshin_again:
                    break
                pygame.display.update()
        if who == 'pepsi':
            while True:
                #清屏
                MainGame.window.fill(BG_COLOR)
                self.getEvent()
                MainGame.pepsi_win.displayWin()
                MainGame.window.blit(self.getTextSurface(f'Pepsi Win！！！'),(400,50))
                MainGame.window.blit(self.getTextSurface(f'Coke vs Pepsi = {MainGame.score1}:{MainGame.score2}'),(400,900))
                self.blitButton('again')
                if MainGame.genshin_again:
                    break
                pygame.display.update()
    #重玩的方法
    def again(self):
        MainGame.score1 = 0
        MainGame.score2 = 0
        MainGame.red_long = 0
        MainGame.blue_long = 0
        MainGame.genshin_again = False
        MainGame.pass3 = True
        self.start_game3()
        print(f'{MainGame.pass2}')
    #创建进度条的方法
    def createBar(self):
        MainGame.red_bar = ProgressBar(0,0,MainGame.red_long,'red')
        MainGame.blud_bar = ProgressBar(0,SCREEN_HEIGHT+5,MainGame.blue_long,'blue')
    def blitBar(self):
        MainGame.red_bar.displayBar()
        MainGame.blud_bar.displayBar()
    #创建领域的方法
    def createArea(self):
        MainGame.area = Area(0.5*SCREEN_WIDTH-175,0.5*SCREEN_HEIGHT-125)
    def blitArea(self):
        MainGame.area.displayArea()
    #创建墙壁的方法
    def createWall(self,pass_type):
        MainGame.wallList.clear()
        if pass_type == 'pass2':
            wall11 = Wall(0.25*SCREEN_WIDTH,0.1*SCREEN_HEIGHT,20,800,1000)
            wall12 = Wall(0.75*SCREEN_WIDTH-20,0.1*SCREEN_HEIGHT,20,800,1000)
            MainGame.wallList.append(wall11)
            MainGame.wallList.append(wall12)
        if pass_type == 'pass3':
            wall1 = Wall(0.25*SCREEN_WIDTH-20,0.1*SCREEN_HEIGHT,90,90,6)
            wall2 = Wall(0.75*SCREEN_WIDTH-40,0,90,90,6)
            wall3 = Wall(0.25*SCREEN_WIDTH-20,300,90,90,6)
            wall4 = Wall(0.25*SCREEN_WIDTH-20,500,90,90,6)
            wall5 = Wall(0.25*SCREEN_WIDTH-20,700,90,90,6)
            wall6 = Wall(0.25*SCREEN_WIDTH-20,900,90,90,6)
            wall7 = Wall(0.75*SCREEN_WIDTH-40,200,90,90,6)
            wall8 = Wall(0.75*SCREEN_WIDTH-40,400,90,90,6)
            wall9 = Wall(0.75*SCREEN_WIDTH-40,600,90,90,6)
            wall10 = Wall(0.75*SCREEN_WIDTH-40,800,90,90,6)
            MainGame.wallList.append(wall1)
            MainGame.wallList.append(wall2)
            MainGame.wallList.append(wall3)
            MainGame.wallList.append(wall4)
            MainGame.wallList.append(wall5)
            MainGame.wallList.append(wall6)
            MainGame.wallList.append(wall7)
            MainGame.wallList.append(wall8)
            MainGame.wallList.append(wall9)
            MainGame.wallList.append(wall10)
    def biltWall(self):
        for wall in MainGame.wallList:
            wall.displayWall()
    #子弹与墙壁相撞消失的方法
    def bullet_hit_wall(self):
        for bullet in MainGame.myBulletList:
            if bullet.live:
                for wall in MainGame.wallList:
                    if pygame.sprite.collide_rect(bullet,wall):
                        wall.hp -= 1
                        bullet.live = False
                        if wall.hp <= 0:
                            MainGame.wallList.remove(wall)
        for bullet in MainGame.hisBulletList:
            if bullet.live:
                for wall in MainGame.wallList:
                    if pygame.sprite.collide_rect(bullet,wall):
                        wall.hp -= 1
                        bullet.live = False
                        if wall.hp <= 0:
                            MainGame.wallList.remove(wall)
    #player1的子弹
    def blitMyBullet(self):
        for bullet in MainGame.myBulletList:
            if bullet.live:
                if MainGame.my_tank.live:
                    bullet.displayBullet()
                    bullet.move()
                    bullet.myBullet_hit_enemy()
                    bullet.myBullet_hit_hisBullet()
            else:
                MainGame.myBulletList.remove(bullet)
    #player2的子弹
    def blitHisBullet(self):
        for bullet in MainGame.hisBulletList:
            if bullet.live:
                if MainGame.his_tank.live:
                    bullet.displayBullet()
                    bullet.move()
                    bullet.hisBullet_hit_enemy()
                    bullet.hisBullet_hit_myBullet()
            else:
                MainGame.hisBulletList.remove(bullet)
    def blitExplode(self):
        for explode in MainGame.explodeList:
            #判断是否活着
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.explodeList.remove(explode)
    #创建加速带图片
    def createSpeedBar(self):
        MainGame.cokespeed = Img(0,0,400,1050,'cokespeed')
        MainGame.pepsispeed = Img(1200,0,400,1050,'pepsispeed')
    def blitSpeedBar(self):
        MainGame.cokespeed.displayImg()
        MainGame.pepsispeed.displayImg()
    #结束游戏
    def end_game(self):
        print('感谢游玩捏，byebye~')

    #左上角文字的绘制
    def getTextSurface(self,text):
        pygame.font.init()   #字体初始化
        font = pygame.font.SysFont('kaiti',50)   #创建字体
        textSurface = font.render(text,True,TEXT_COLOR)
        return textSurface
    #获取事件
    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type==pygame.QUIT:
                self.end_game()
                pygame.quit()   #用于终止pygame模块的程序
                sys.exit()   #结束整个python程序
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MainGame.buttonDict['begin1'].rect.collidepoint(pygame.mouse.get_pos()):
                    MainGame.pass3 = True
                    MainGame.genshin = False
                    MainGame().start_game3()
                if MainGame.buttonDict['again'].rect.collidepoint(pygame.mouse.get_pos()):
                    self.again()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key==pygame.K_TAB:
                    if not MainGame.score_box:
                        MainGame.score_box = True
                    elif MainGame.score_box:
                        MainGame.score_box = False
            if not MainGame.genshin:
                #player1
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_a:
                        MainGame.my_tank.direction = 'L'
                        MainGame.my_tank.button_left = True
                        # MainGame.my_tank.move()
                        print('←')
                    elif event.key==pygame.K_d:
                        MainGame.my_tank.direction = 'R'
                        MainGame.my_tank.button_right = True
                        # MainGame.my_tank.move()
                        print('→')
                    elif event.key==pygame.K_w:
                        MainGame.my_tank.direction = 'U'
                        MainGame.my_tank.button_up = True
                        # MainGame.my_tank.move()
                        print('↑')
                    elif event.key==pygame.K_s:
                        MainGame.my_tank.direction = 'D'
                        MainGame.my_tank.button_down = True
                        print('↓')
                    elif event.key == pygame.K_r:
                        MainGame.my_tank.revive_cola()
                    elif event.key==pygame.K_SPACE:
                        #创建我方子弹
                        if len(MainGame.myBulletList) < 3 and MainGame.my_tank.live:
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)
                #player2
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        MainGame.his_tank.direction = 'L'
                        MainGame.his_tank.button_left = True
                        # MainGame.my_tank.move()
                        print('←')
                    elif event.key==pygame.K_RIGHT:
                        MainGame.his_tank.direction = 'R'
                        MainGame.his_tank.button_right = True
                        # MainGame.my_tank.move()
                        print('→')
                    elif event.key==pygame.K_UP:
                        MainGame.his_tank.direction = 'U'
                        MainGame.his_tank.button_up = True
                        # MainGame.my_tank.move()
                        print('↑')
                    elif event.key==pygame.K_DOWN:
                        MainGame.his_tank.direction = 'D'
                        MainGame.his_tank.button_down = True
                        # MainGame.my_tank.move()
                        print('↓')
                    elif event.key==pygame.K_KP_0:
                        #创建对方子弹
                        if len(MainGame.hisBulletList) < 3 and MainGame.his_tank.live:
                            hisBullet = HisBullet(MainGame.his_tank)
                            MainGame.hisBulletList.append(hisBullet)
                            for wall in MainGame.wallList:
                                print(f"Wall HP after hit: {wall.hp}")
                    elif event.key==pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_KP_PERIOD:
                        MainGame.his_tank.revive_cola()
                if event.type==pygame.KEYUP:
                    #player1
                    if event.key==pygame.K_a:
                        MainGame.my_tank.button_left = False
                    elif event.key==pygame.K_d:
                        MainGame.my_tank.button_right = False
                    elif event.key==pygame.K_w:
                        MainGame.my_tank.button_up = False
                    elif event.key==pygame.K_s:
                        MainGame.my_tank.button_down = False
                    #player2
                    if event.key==pygame.K_LEFT:
                        MainGame.his_tank.button_left = False
                    elif event.key==pygame.K_RIGHT:
                        MainGame.his_tank.button_right = False
                    elif event.key==pygame.K_UP:
                        MainGame.his_tank.button_up = False
                    elif event.key==pygame.K_DOWN:
                        MainGame.his_tank.button_down = False
        for bullet in MainGame.myBulletList:
            if bullet.rect.left <= 0:
                bullet.live = False
                MainGame.myBulletList.remove(bullet)
            elif bullet.rect.left >= SCREEN_WIDTH:
                bullet.live = False
                MainGame.myBulletList.remove(bullet)
            elif bullet.rect.top <= 0:
                bullet.live = False
                MainGame.myBulletList.remove(bullet)
            elif bullet.rect.top >= SCREEN_HEIGHT:
                bullet.live = False
                MainGame.myBulletList.remove(bullet)
        for bullet in MainGame.hisBulletList:
            if bullet.rect.left <= 0:
                bullet.live = False
                MainGame.hisBulletList.remove(bullet)
            elif bullet.rect.left >= SCREEN_WIDTH:
                bullet.live = False
                MainGame.hisBulletList.remove(bullet)
            elif bullet.rect.top <= 0:
                bullet.live = False
                MainGame.hisBulletList.remove(bullet)
            elif bullet.rect.top >= SCREEN_HEIGHT:
                bullet.live = False
                MainGame.hisBulletList.remove(bullet)
    def createEnemyCola(self):
        top = 100  #固定这个可乐生成时的y坐标
        #循环生成敌方可乐
        for i in range(MainGame.enemyColaCount):
            left = random.randint(0,600)
            speed = random.randint(20,50)
            enemy = EnemyTank(left,top,speed)
            MainGame.enemyColaList.append(enemy)
    def createBegin(self):
        MainGame.begin = BeginWindow(50,50)
    def blitBegin(self):
        MainGame.begin.displayBegin()
#可乐类,player1类
class Cola(BaseItem):
    def __init__(self,left,top,speed):
        #保存可乐的图片,获取图片的同时更改图片尺寸
        self.images = {
            'U':pygame.transform.scale(pygame.image.load('img/coke_up.png'),(62,100)),
            'L':pygame.transform.scale(pygame.image.load('img/coke_left.png'),(100,62)),
            'R':pygame.transform.scale(pygame.image.load('img/coke_right_new.png'),(100,62)),
            'D':pygame.transform.scale(pygame.image.load('img/coke_down.png'),(62,100))
        }
        self.direction = 'L'  #初始方向
        self.picture=self.images[self.direction]  #获取当前方向的对应图片,这个图片是初始的方向
        self.rect=self.picture.get_rect()   #根据图片获取一个矩形区域
        #设置矩形区域的left和top
        self.rect.left = left
        self.rect.top = top
        #可乐移动的速度
        self.speed = speed
        #可乐移动的开关
        self.button_left=False
        self.button_right=False
        self.button_up=False
        self.button_down=False
        #可乐的存活与否
        self.live = True
        #复活次数
        self.num = 0
        #坦克原坐标
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
    #在领域内的留存检测方法
    def inArea(self):
        if self.live:
            if pygame.sprite.collide_rect(self,MainGame.area) and not pygame.sprite.collide_rect(MainGame.his_tank,MainGame.area):
                MainGame.red_long += 1
    #移动
    def move(self):
        #每次移动都记录这个坐标,如果碰撞了就恢复到这个位置，不继续进行移动指令
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        if not self.live:return
        #判断坦克的朝向，并进行移动
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'R':
            if self.rect.left+self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'D':
            if self.rect.top+self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
    #射击
    def shot(self):
        pass
    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                self.stay()
    #展示可乐
    def displayTank(self):
        #更改可乐的朝向
        if not self.live:return
        self.picture = self.images[self.direction]
        #调用blit方法展示
        MainGame.window.blit(self.picture,self.rect)
    #敌方可乐与我方可乐相撞的方法
    def cola_hit(self):
        if not self.live:return
        for enemy in MainGame.enemyColaList:
            if pygame.sprite.collide_rect(enemy,self):
                #修改敌方可乐和我方子弹的状态
                enemy.live = False
                self.live = False
                #创建爆炸对象
                explode = Explode(enemy)
                #将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
        if MainGame.his_tank.live and pygame.sprite.collide_rect(MainGame.his_tank,self):
            MainGame.his_tank.live = False
            self.live = False
            explode = Explode(MainGame.his_tank)
            MainGame.explodeList.append(explode)
            MainGame.coke_death += 1
            MainGame.pepsi_death += 1
            if not MainGame.my_tank.live:
                MainGame.my_tank.rect.left = 0.1*SCREEN_WIDTH
                MainGame.my_tank.rect.top = 0.5*SCREEN_HEIGHT
            if not MainGame.his_tank.live:
                MainGame.his_tank.rect.left = 0.9*SCREEN_WIDTH
                MainGame.his_tank.rect.top = 0.5*SCREEN_HEIGHT

    #可乐复活的方法
    def revive_cola(self):
        if self.live == False:
            self.live = True
            self.num += 1
            self.rect.left = 0.1*SCREEN_WIDTH
            self.rect.top = 0.5*SCREEN_HEIGHT
#第二玩家可乐
class MyTank(BaseItem): 
    def __init__(self,left,top,speed):
        #保存可乐的图片,获取图片的同时更改图片尺寸
        self.images = {
            'U':pygame.transform.scale(pygame.image.load('img/pepsi_up.png'),(62,100)),
            'L':pygame.transform.scale(pygame.image.load('img/pepsi_left.png'),(100,62)),
            'R':pygame.transform.scale(pygame.image.load('img/pepsi_right.png'),(100,62)),
            'D':pygame.transform.scale(pygame.image.load('img/pepsi_down.png'),(62,100))
        }
        self.direction = 'L'  #初始方向
        self.picture=self.images[self.direction]  #获取当前方向的对应图片,这个图片是初始的方向
        self.rect=self.picture.get_rect()   #根据图片获取一个矩形区域
        #设置矩形区域的left和top
        self.rect.left = left
        self.rect.top = top
        #可乐移动的速度
        self.speed=speed
        #可乐移动的开关
        self.button_left=False
        self.button_right=False
        self.button_up=False
        self.button_down=False
        #可乐的存活与否
        self.live = True
        #复活次数
        self.num = 0
        #坦克原坐标
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
    #移动
    def move(self):
        #每次移动都记录这个坐标,如果碰撞了就恢复到这个位置，不继续进行移动指令
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        if not self.live:return
        #判断坦克的朝向，并进行移动
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'R':
            if self.rect.left+self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'D':
            if self.rect.top+self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
    #射击
    def shot(self):
        pass
    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self,wall):
                self.stay()
    #展示可乐
    def displayTank(self):
        #更改可乐的朝向
        if not self.live:return
        self.picture = self.images[self.direction]
        #调用blit方法展示
        MainGame.window.blit(self.picture,self.rect)
    #敌方可乐与我方可乐相撞的方法
    def cola_hit(self):
        if not self.live:return
        for enemy in MainGame.enemyColaList:
            if pygame.sprite.collide_rect(enemy,self):
                #修改敌方可乐和我方子弹的状态
                enemy.live = False
                self.live = False
                #创建爆炸对象
                explode = Explode(enemy)
                #将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
        if MainGame.my_tank.live and pygame.sprite.collide_rect(MainGame.my_tank,self):
            MainGame.my_tank.live = False
            self.live = False
            explode = Explode(MainGame.my_tank)
            MainGame.explodeList.append(explode)
            MainGame.coke_death += 1
            MainGame.pepsi_death += 1
            if not MainGame.my_tank.live:
                MainGame.my_tank.rect.left = 0.1*SCREEN_WIDTH
                MainGame.my_tank.rect.top = 0.5*SCREEN_HEIGHT
            if not MainGame.his_tank.live:
                MainGame.his_tank.rect.left = 0.9*SCREEN_WIDTH
                MainGame.his_tank.rect.top = 0.5*SCREEN_HEIGHT
    #在领域内的留存检测方法
    def inArea(self):
        if self.live:
            if pygame.sprite.collide_rect(self,MainGame.area) and not pygame.sprite.collide_rect(MainGame.my_tank,MainGame.area):
                MainGame.blue_long += 1

    #可乐复活的方法
    def revive_cola(self):
        if self.live == False:
            self.live = True
            self.num += 1
            self.rect.left = 0.9*SCREEN_WIDTH
            self.rect.top = 0.5*SCREEN_HEIGHT
#人机可乐
class EnemyTank(Cola):
    def __init__(self,left,top,speed):
        #调用父类的初始化(init)方法
        super(EnemyTank,self).__init__(left,top)
        #加载图片集
        self.images = {
            'U':pygame.transform.scale(pygame.image.load('img/horse_up.png'),(100,100)),
            'L':pygame.transform.scale(pygame.image.load('img/horse_left.png'),(100,100)),
            'R':pygame.transform.scale(pygame.image.load('img/horse_right.png'),(100,100)),
            'D':pygame.transform.scale(pygame.image.load('img/horse_down.png'),(100,100))
        }
        #方向,随机生成敌方可乐的方向
        self.direction = self.randDirection()
        #获得随机方向的图片
        self.picture = self.images[self.direction]
        #占地区域
        self.rect = self.picture.get_rect()
        #对left和top进行赋值
        self.rect.left = left
        self.rect.top = top
        #速度
        self.speed = speed
        #移动开关
        self.flag = True
        #初始时步数
        self.step = 60
    #可乐初始式随机方向的方法
    def randDirection(self):
        direction = random.randint(1,4)
        if direction == 1:
            return 'U'
        if direction == 2:
            return 'D'
        if direction == 3:
            return 'L'
        if direction == 4:
            return 'R'
    
    #可乐随机移动的方法
    def randMove(self):
        if self.step<=0:
            self.direction = self.randDirection()
            self.step = 60
        else:
            self.move()
            self.step -= 1
#player1子弹类
class Bullet(BaseItem):
    def __init__(self,cola):
        #加载图片
        self.images = {
            'U':pygame.transform.scale(pygame.image.load('img/water_up.png'),(50,50)),
            'L':pygame.transform.scale(pygame.image.load('img/water_left.png'),(50,50)),
            'R':pygame.transform.scale(pygame.image.load('img/water_right.png'),(50,50)),
            'D':pygame.transform.scale(pygame.image.load('img/water_down.png'),(50,50))
        }
        #坦克的方向决定了子弹的方向
        self.direction = cola.direction
        #获取子弹的区域
        self.rect = self.images[self.direction].get_rect()
        #子弹的left与top和方向有关
        if self.direction == 'U':
            self.rect.left = cola.rect.left + cola.rect.width/2 - self.rect.width/2
            self.rect.top = cola.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = cola.rect.left + cola.rect.width/2 - self.rect.width/2
            self.rect.top = cola.rect.top + cola.rect.height
        elif self.direction == 'L':
            self.rect.left = cola.rect.left - self.rect.width/2 - self.rect.width/2
            self.rect.top = cola.rect.top + cola.rect.width/2 - self.rect.width/2
        elif self.direction == 'R':
            self.rect.left = cola.rect.left + cola.rect.width
            self.rect.top = cola.rect.top + cola.rect.width/2 - self.rect.width/2
        #子弹的速度
        self.speed = 15
        #子弹是否存活
        self.live = True
    #子弹移动的方法
    def move(self):
        if self.direction == 'U':
            self.rect.top -= self.speed
        elif self.direction == 'D':
            self.rect.top += self.speed
        elif self.direction == 'R':
            self.rect.left += self.speed
        elif self.direction == 'L':
            self.rect.left -= self.speed
    #展示子弹的方法
    def displayBullet(self):
        MainGame.window.blit(self.images[self.direction],self.rect)
    #子弹击中敌方可乐的方法
    def myBullet_hit_enemy(self):
        #循环遍历敌方可乐列表，判断是否发生碰撞
        for enemy in MainGame.enemyColaList:
            if pygame.sprite.collide_rect(enemy,self) == True:
                #修改敌方可乐和我方子弹的状态
                enemy.live = False
                self.live = False
                #创建爆炸对象
                explode = Explode(enemy)
                #将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
    #子弹击中玩家的方法
    def myBullet_hit_enemy(self):
        if MainGame.his_tank.live:
            if pygame.sprite.collide_rect(MainGame.his_tank,self) == True:
                #修改敌方可乐和我方子弹的状态
                MainGame.his_tank.live = False
                self.live = False
                #创建爆炸对象
                explode = Explode(self)
                #将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
                MainGame.pepsi_death += 1
                if not MainGame.my_tank.live:
                    MainGame.my_tank.rect.left = 0.1*SCREEN_WIDTH
                    MainGame.my_tank.rect.top = 0.5*SCREEN_HEIGHT
                if not MainGame.his_tank.live:
                    MainGame.his_tank.rect.left = 0.9*SCREEN_WIDTH
                    MainGame.his_tank.rect.top = 0.5*SCREEN_HEIGHT    
    #击中对方子弹的方法
    def myBullet_hit_hisBullet(self):
        for bullet in MainGame.hisBulletList:
            if pygame.sprite.collide_rect(bullet,self):
                bullet.live = False
                self.live = False
                explode = Explode(bullet)
                MainGame.explodeList.append(explode)
#player2子弹类
class HisBullet(BaseItem):
    def __init__(self,cola):
        #加载图片
        self.images = {
            'U':pygame.transform.scale(pygame.image.load('img/water_up.png'),(50,50)),
            'L':pygame.transform.scale(pygame.image.load('img/water_left.png'),(50,50)),
            'R':pygame.transform.scale(pygame.image.load('img/water_right.png'),(50,50)),
            'D':pygame.transform.scale(pygame.image.load('img/water_down.png'),(50,50))
        }
        #坦克的方向决定了子弹的方向
        self.direction = cola.direction
        #获取子弹的区域
        self.rect = self.images[self.direction].get_rect()
        #子弹的left与top和方向有关
        if self.direction == 'U':
            self.rect.left = cola.rect.left + cola.rect.width/2 - self.rect.width/2
            self.rect.top = cola.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = cola.rect.left + cola.rect.width/2 - self.rect.width/2
            self.rect.top = cola.rect.top + cola.rect.height
        elif self.direction == 'L':
            self.rect.left = cola.rect.left - self.rect.width/2 - self.rect.width/2
            self.rect.top = cola.rect.top + cola.rect.width/2 - self.rect.width/2
        elif self.direction == 'R':
            self.rect.left = cola.rect.left + cola.rect.width
            self.rect.top = cola.rect.top + cola.rect.width/2 - self.rect.width/2
        #子弹的速度
        self.speed = 15
        #子弹是否存活
        self.live = True
    #子弹移动的方法
    def move(self):
        if self.direction == 'U':
            self.rect.top -= self.speed
        elif self.direction == 'D':
            self.rect.top += self.speed
        elif self.direction == 'R':
            self.rect.left += self.speed
        elif self.direction == 'L':
            self.rect.left -= self.speed
    #展示子弹的方法
    def displayBullet(self):
        MainGame.window.blit(self.images[self.direction],self.rect)
    #子弹击中敌方可乐的方法
    def hisBullet_hit_enemy(self):
        #循环遍历敌方可乐列表，判断是否发生碰撞
        for enemy in MainGame.enemyColaList:
            if pygame.sprite.collide_rect(enemy,self) == True:
                #修改敌方可乐和我方子弹的状态
                enemy.live = False
                self.live = False
                #创建爆炸对象
                explode = Explode(enemy)
                #将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
    #子弹击中玩家的方法
    def hisBullet_hit_enemy(self):
        if MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank,self) == True:
                #修改敌方可乐和我方子弹的状态
                MainGame.my_tank.live = False
                self.live = False
                #创建爆炸对象
                explode = Explode(self)
                #将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
                MainGame.coke_death += 1
                if not MainGame.my_tank.live:
                    MainGame.my_tank.rect.left = 0.1*SCREEN_WIDTH
                    MainGame.my_tank.rect.top = 0.5*SCREEN_HEIGHT
                if not MainGame.his_tank.live:
                    MainGame.his_tank.rect.left = 0.9*SCREEN_WIDTH
                    MainGame.his_tank.rect.top = 0.5*SCREEN_HEIGHT
    #击中对方子弹的方法
    def hisBullet_hit_myBullet(self):
        for bullet in MainGame.myBulletList:
            if pygame.sprite.collide_rect(bullet,self):
                bullet.live = False
                self.live = False
                explode = Explode(bullet)
                MainGame.explodeList.append(explode)
#图片类
class Img():
    def __init__(self,left,top,length,width,name):
        self.image = {'coke_speed':pygame.transform.scale(pygame.image.load('img/cokespeed.png'),(length,width)),
                      'pepsi_speed':pygame.transform.scale(pygame.image.load('img/pepsispeed.png'),(length,width))}
        if name == 'cokespeed':
            self.image = self.image['coke_speed']
            self.rect = self.image.get_rect()
            self.rect.left = left
            self.rect.top = top
        if name == 'pepsispeed':
            self.image = self.image['pepsi_speed']
            self.rect = self.image.get_rect()
            self.rect.left = left
            self.rect.top = top
    def displayImg(self):
        MainGame.window.blit(self.image,self.rect)
        
#墙壁类
class Wall():
    def __init__(self,left,top,length,width,hp):
        self.image = pygame.image.load('img/wall.png')
        self.image = pygame.transform.scale(self.image,(length,width))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.hp = hp
    #展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image,self.rect)
#领域类
class Area():
    def __init__(self,left,top):
        self.image = pygame.image.load('img/area_new.png')
        self.image = pygame.transform.scale(self.image,(350,250))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    #展示领域的方法
    def displayArea(self):
        MainGame.window.blit(self.image,self.rect)
#进度条类
class ProgressBar():
    def __init__(self,left,top,long,color):
        self.image = {'red':pygame.transform.scale(pygame.image.load('img/CokeRed.png'),(long,20)),
                      'blue':pygame.transform.scale(pygame.image.load('img/PepsiBlue.png'),(long,20))}
        if color == 'red':
            self.rect = self.image['red'].get_rect()
            self.rect.left = left
        if color == 'blue':
            self.rect = self.image['blue'].get_rect()
            #self.rect.left = SCREEN_WIDTH - left
            self.rect.left = left
        self.rect.top = top
        self.long = long
        self.color = color
    #展示进度条的方法
    def displayBar(self):
        if self.color == 'red':
            MainGame.window.blit(self.image['red'],self.rect)
        if self.color == 'blue':
            MainGame.window.blit(self.image['blue'],self.rect)
#爆炸类
class Explode():
    def __init__(self,button):
        #爆炸的位置由当前子弹打中的坦克位置决定
        self.rect = button.rect
        self.rect.left = self.rect.left - 80
        self.rect.top = self.rect.top - 40
        self.picture = pygame.image.load('img/cola_dead_new.png')
        self.live = True
        self.step = 0
    #展示爆炸效果的方法
    def displayExplode(self):
        #根据索引获取爆炸对象
        if self.step<10:
            self.step+=1
            #添加到主窗口
            MainGame.window.blit(pygame.transform.scale(self.picture,(75,75)),self.rect)
        else:
            self.live = False
            self.step = 0
#结算画面类
class Win():
    def __init__(self,left,top,cola):
    #存储结算动画的字典
        self.win_image = {'coke':pygame.transform.scale(pygame.image.load('img/coke_win.png'),(800,800)),
                    'pepsi':pygame.transform.scale(pygame.image.load('img/pepsi_win.png'),(800,800))}
        if cola == 'coke':
            self.rect = self.win_image['coke'].get_rect()
            self.rect.left = left
            self.rect.top = top
        if cola == 'pepsi':
            self.rect = self.win_image['pepsi'].get_rect()
            self.rect.left = left
            self.rect.top = top
        self.cola = cola
    #展示结算画面的方法
    def displayWin(self):
        if self.cola == 'coke':
            MainGame.window.blit(self.win_image['coke'],self.rect)
        if self.cola == 'pepsi':
            MainGame.window.blit(self.win_image['pepsi'],self.rect)
#开始画面类
class BeginWindow():
    def __init__(self,left,top):
        self.image = pygame.transform.scale(pygame.image.load('img/loading.png'),(1500,800))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    #展示开始画面的方法
    def displayBegin(self):
        MainGame.window.blit(self.image,self.rect)
#按钮类
class Button():
    def __init__(self,left,top,button):
        self.image = {'begin1':pygame.transform.scale(pygame.image.load('img/start1.png'),(241,84)),
                      'begin2':pygame.transform.scale(pygame.image.load('img/start2.png'),(241,84)),
                      'again':pygame.transform.scale(pygame.image.load('img/again.png'),(100,100))}
        self.button = button
        if button == 'begin1':
            self.rect = self.image['begin1'].get_rect()
            self.rect.left = left
            self.rect.top = top
        if button == 'begin2':
            self.rect = self.image['begin2'].get_rect()
            self.rect.left = left
            self.rect.top = top
        if button == 'again':
            self.rect = self.image['again'].get_rect()
            self.rect.left = left
            self.rect.top = top
    #展示按钮的方法
    def displayButton(self):
        MainGame.window.blit(self.image[self.button],self.rect)
#音乐类
class Music():
    def __init__(self):
        pass
    #播放音乐的方法
    def play(self):
        pass

if __name__=='__main__':
    MainGame().beginGame()




