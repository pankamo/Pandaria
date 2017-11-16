from pico2d import *
import random
import os
import sys
sys.path.append("E:\Pytemp\Burrito\Pandaria\Data")
import Bison_Launch

name = "Launch_State"

Launching = True
shivering = 0
Shooting = False
MonsterHit = 0
Direction = None

# 화면 내의 너비 : 10 METER로 설정
# 미터당 픽셀 : 108 px
PIXEL_PER_METER = 108

class LaunchBackground :
    def __init__(self):
        os.chdir('E:\Pytemp\Burrito\Pandaria\Images')
        self.image = load_image('TempMAP.png')

    def draw(self):
        self.image.draw(540, 300)

class Monster:
    def __init__(self):
        os.chdir('E:\Pytemp\Burrito\Pandaria\Images')
        self.image = load_image('TempM.png')
        self.x, self.y = (800, 280)

    def update(self, frame_time):
        DRAG_SPEED_MPS = 0.4
        DRAG_SPEED_MPM = (DRAG_SPEED_MPS * 60.0)
        DRAG_SPEED_KMPH = (DRAG_SPEED_MPM * 60.0 / 1000.0)
        DRAG_SPEED_PPS = (DRAG_SPEED_MPS * PIXEL_PER_METER)
        distance = DRAG_SPEED_PPS * frame_time
        # 시속 1.44 Km / 초당 43.2 픽셀이동

        if Shooting == True:
            global MonsterHit
            # 몬스터가 부딪힌 후 3초간 밀려나는 모습을 구현합니다.
            if MonsterHit >= 1 and MonsterHit < 3 :
                self.image = load_image('TempMHit.png')
                self.x += distance
                MonsterHit = MonsterHit + frame_time
            if MonsterHit == 3 :
                pass
        elif Shooting == False:
            pass

    def draw(self):
        self.image.draw(self.x, self.y)

class Rope:
    def __init__(self):
        os.chdir('E:\Pytemp\Burrito\Pandaria\Images')
        self.image = load_image('TempR.png')
        self.x, self.y = ( 250, 250 )

    def update(self, frame_time):
        RECOV_SPEED_MPS = 15
        RECOV_SPEED_MPM = (RECOV_SPEED_MPS * 60.0)
        RECOV_SPEED_KMPH = (RECOV_SPEED_MPM * 60.0 / 1000.0)
        RECOV_SPEED_PPS = (RECOV_SPEED_MPS * PIXEL_PER_METER)
        distance = RECOV_SPEED_PPS * frame_time
        # 로프복구속도는 Bison과 똑같이
        # 시속 54 Km / 초당 1620 픽셀이동

        global Shooting
        if Shooting == False :
            global shivering
            if ( shivering + 1 ) % 2 == 1 :
                self.x = self.x - 2
            else :
                self.x = self.x + 2
        if Shooting == True :
            if self.x < 300:
                self.x += distance
            if self.x >= 300:
                pass

    def draw(self):
        self.image.draw(self.x, self.y)

class Guagebar:
    def __init__(self):
        os.chdir('E:\Pytemp\Burrito\Pandaria\Images')
        self.image = load_image('TempGuage.png')
        self.x, self.y = (540, 550)

    def update(self,frame_time):
        if MonsterHit < 1:
            pass
        if MonsterHit >= 1:
            self.y = self.y + 1
        # 몬스터와 부딪히면 게이지바가 사라집니다

    def draw(self):
        self.image.draw(self.x, self.y)

class Guagepoint:
    def __init__(self):
        os.chdir('E:\Pytemp\Burrito\Pandaria\Images')
        self.image = load_image('TempGuagePoint.png')
        self.x, self.y = (random.randint(200,880), 450)
        global direction
        direction = [-1,1]
        direction = random.choice(direction)

    def update(self, frame_time):
        global ShootingFail
        global ShootingNormal
        global ShootingBoost

        # 게이지포인트가 좌우반복운동하도록 합니다.
        if Shooting == False:
            global direction
            if direction == 1:
                self.x = min(880, self.x + (direction * 3))
                if self.x == 880:
                    direction = -1
            if direction == -1:
                self.x = max(200, self.x + (direction * 3))
                if self.x == 200:
                    direction = 1

        if Shooting == True:
            if ( GP.x >= 370 and GP.x < 490 ) \
                or ( GP.x > 590 and GP.x <= 710) :
                ShootingNormal = True
            if GP.x < 370 or GP.x > 710:
                ShootingFail = True
            if GP.x >= 490 and GP.x <= 590:
                ShootingBoost = True

    def draw(self):
        if MonsterHit < 1:
            self.image.draw(self.x, self.y)
        if MonsterHit >= 1:
            self.image.draw(self.x, self.y)
            self.y = self.y + 1

def handle_events(frame_time):
    global Launching
    global Shooting
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Launching = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            Launching = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            Shooting = True
            pass


current_time = 0.0
def get_frame_time():
    global current_time
    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time

open_canvas(1080,600)

LB = LaunchBackground()
MS = Monster()
RP = Rope()
GB = Guagebar()
GP = Guagepoint()

def updates():
    Bison_Launch.update(frame_time)
    MS.update(frame_time)
    RP.update(frame_time)
    GB.update(frame_time)
    GP.update(frame_time)

def drawings():
    LB.draw()
    MS.draw()
    Bison_Launch.draw()
    RP.draw()
    GB.draw()
    GP.draw()

def MakeAll():
    updates()
    drawings()

while Launching :

    frame_time = get_frame_time()
    handle_events(frame_time)
    clear_canvas()
    MakeAll()
    update_canvas()

close_canvas()
