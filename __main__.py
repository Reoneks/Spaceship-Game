import sys,pygame
import random
import math
import Bot
###########################################################
def StartPause(screen,f1):
    time=pygame.time.get_ticks()
    while(1):
        if(pygame.time.get_ticks()-time>=1000 and pygame.time.get_ticks()-time<2000):
            text3=f1.render('3',1,(180,0,0))
            screen.blit(text3,(450,400))
        elif(pygame.time.get_ticks()-time>=2000 and pygame.time.get_ticks()-time<3000):
            text3=f1.render('2',1,(180,0,0))
            screen.blit(text3,(500,400))
        elif(pygame.time.get_ticks()-time>=3000 and pygame.time.get_ticks()-time<4000):
            text3=f1.render('1',1,(180,0,0))
            screen.blit(text3,(550,400))
        elif(pygame.time.get_ticks()-time>=4000):
            break
        pygame.display.flip()
###########################################################
def RandomVisibility(meteorsvisibility):
    for i in range(0,10):
        meteorsvisibility[i]=1
    rand=random.randint(2,5)
    for i in range(0,rand):
        true=1
        while(true):
            rand1=random.randint(0,9)
            if(meteorsvisibility[rand1]!=0):
                meteorsvisibility[rand1]=0
                true=0
    return meteorsvisibility
###########################################################
def GameOver(screen):
    Bot.StopBot()
    pygame.mixer.music.stop()
    pygame.mixer.music.load("src/Music/detonate.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.4)
    pygame.time.delay(500)
    endgame=pygame.image.load("src/Images/explosive.png")
    endgamerect=endgame.get_rect(center=(x,y))
    screen.blit(endgame,endgamerect)
    time=pygame.time.get_ticks()
    pygame.display.flip()
    while(1):
        if(pygame.time.get_ticks()-time>=2000):
            break
    pygame.mixer.music.stop()
    pygame.display.quit()
    print("Game Over")
    print("Score: ",Score)
    sys.exit()
###########################################################
def Keys(Mod,speed,pause,key,BotActivated):
    if(key[pygame.K_SPACE]):
        if(pause==0):
            pause=1
            pygame.mixer.music.pause()
            pygame.time.delay(200)
        else:
            pause=0
            pygame.mixer.music.unpause()
            pygame.time.delay(200)
    if(key[pygame.K_d] or key[pygame.K_RIGHT]):
        speed[0]=Mod
    if(key[pygame.K_a] or key[pygame.K_LEFT]):
        speed[0]=-Mod
    if(key[pygame.K_w] or key[pygame.K_UP]):
        speed[1]=-Mod
    if(key[pygame.K_s] or key[pygame.K_DOWN]):
        speed[1]=Mod
    if(key[pygame.K_b]):
        if(BotActivated==0):
            BotActivated=1
        else:
            BotActivated=0
            Bot.StopBot()
    return speed,pause,BotActivated
###########################################################
def CheckEvents():
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            GameOver(screen)
###########################################################
def CheckBorders(ballrect,meteorsy,width,key,height,speed,x,y,meteorrect,meteors,ScoreLine,Score,meteorsvisibility):
    meteoritricthend=0
    if(ballrect.right>width and (key[pygame.K_d] or key[pygame.K_RIGHT]) or ballrect.left<0 and (key[pygame.K_a] or key[pygame.K_LEFT])):
        speed[0]=0
    else:
        x+=speed[0]
    if(ballrect.top<0 and (key[pygame.K_w] or key[pygame.K_UP]) or ballrect.bottom>height and (key[pygame.K_s] or key[pygame.K_DOWN])):
        speed[1]=0
    else:
        y+=speed[1]
    for i in range(0,10):
        if(meteorrect[i].bottom>height):
            meteorsy=-154
            meteoritricthend=1
            meteorrect[i]=meteors.get_rect(center=(50+i*100,meteorsy))
    if(meteoritricthend==1):
        ScoreLine+=1
        Score+=1
        meteorsvisibility=RandomVisibility(meteorsvisibility)
    return speed,x,y,meteorsy,meteorrect,ScoreLine,Score,meteorsvisibility
###########################################################
def DrawScreen(pause,screen,text2,background,ball,ballrect,meteorsvisibility,meteors,meteorrect,f1,Score):
    if(pause==1):
        screen.blit(text2,(500,400))
        pygame.display.flip()
    screen.blit(background,(0,0))
    screen.blit(ball,ballrect)
    for i in range(0,10):
        if(meteorsvisibility[i]!=0):screen.blit(meteors,meteorrect[i])
    text1=f1.render('Score: '+str(Score),1,(180,0,0))
    screen.blit(text1,(880,10))
    if(pause==0):pygame.display.flip()
    return screen
###########################################################
pygame.init()
Mod=2
ButtonPushed=0
BotActivated=0
ScoreLine=0
size=width,height=1000,800
Score=0
pause=0
startpause=1
speed=[0,0]
meteorspeed=[0,1]
screen=pygame.display.set_mode(size)
ball=pygame.image.load("src/Sprites/spaceship.png")
meteors=pygame.image.load("src/Sprites/meteor.png")
meteorsy=(-154)
meteorsvisibility=[]
for i in range(10):
    meteorsvisibility.append(1)
x=500
y=400
background=pygame.image.load("src/Images/sky.jpg").convert()
ballrect=ball.get_rect(center=(x,y))
meteorrect=[]
f1=pygame.font.SysFont('timesnewroman',29)
text2=f1.render('Pause',1,(180,0,0))
pygame.mixer.music.load("src/Music/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)
meteorsvisibility=RandomVisibility(meteorsvisibility)
for i in range(0,10):
    meteorrect.append(meteors.get_rect(center=(50+i*100,meteorsy)))
while(1):
    if(ScoreLine>=10):
        ScoreLine=0
        Mod+=1
        meteorspeed=[0,Mod-1]
    key=pygame.key.get_pressed()
    speed,pause,BotActivated=Keys(Mod,speed,pause,key,BotActivated)
    if(BotActivated==1):
        temp=[]
        for i in range(10):
            if(meteorsvisibility[i]==0):
                temp.append(50+i*100)
        minimum=999999
        for i in temp:
            if(math.fabs(x-i)<math.fabs(x-minimum)):
                minimum=i
        ButtonPushed=Bot.MoveShip(x,minimum,ButtonPushed)
    CheckEvents()
    if(pause==0 and startpause==0):
        speed,x,y,meteorsy,meteorrect,ScoreLine,Score,meteorsvisibility=CheckBorders(ballrect,meteorsy,width,key,height,speed,x,y,meteorrect,meteors,ScoreLine,Score,meteorsvisibility)
        meteorsy+=meteorspeed[1]
        for i in range(0,10):
            if(((meteorsy+35)>=(y-39)) and ((50+i*100+35)>=(x-39)) and ((50+i*100-35)<=(x+39)) and ((meteorsy-35)<=(y+39)) and (meteorsvisibility[i]!=0)):
                GameOver(screen)
        ballrect=ballrect.move(speed)
        for i in range(0,10):
            meteorrect[i]=meteorrect[i].move(meteorspeed)
    screen=DrawScreen(pause,screen,text2,background,ball,ballrect,meteorsvisibility,meteors,meteorrect,f1,Score)
    speed[0]=0
    speed[1]=0
    if(startpause==1):
        startpause=0
        StartPause(screen,f1)
