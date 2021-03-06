from pico2d import *

import math
import FlyingState

import game_framework

from BisonInLaunchState import Bison
from Monster import Monster
from Gauge import *
from LaunchStateBackgrounds import *

name = "LaunchState"

bison = None
monster = None
gaugebar = None
gaugepoint = None
background = None
grass = None
bgm = None
PIXEL_PER_METER = 108

hittingsound = None
successsound = None

LAUNCHING = None

def play_bgm():
    global bgm
    bgm = load_wav('./Sounds/LaunchBGM.wav')
    bgm.set_volume(80)
    bgm.play()

def load_HittingSound():
    global hittingsound
    hittingsound = load_wav('./Sounds/Launch_normal.wav')
    hittingsound.set_volume(80)

def load_SuccessSound():
    global successsound
    successsound = load_wav('./Sounds/Launch_success.wav')
    successsound.set_volume(80)

def play_HittingSound():
    hittingsound.play()

def play_SuccessSound():
    successsound.play()



def create_LaunchingStage():
    global bison, monster, gaugebar, gaugepoint, background, ground, grass
    bison = Bison()
    monster = Monster()
    gaugebar = GaugeBar()
    gaugepoint = GaugePoint()
    background = Background()
    grass = Grass()
    ground = Ground()
    load_HittingSound()
    load_SuccessSound()
    pass

def destroy_LaunchingStage():
    global bison, monster, gaugebar, gaugepoint, background, ground, grass, bgm
    del(bison)
    del(monster)
    del(gaugebar)
    del(gaugepoint)
    del(background)
    del(grass)
    del(ground)
    del(bgm)

def enter():
    global LAUNCHING
    #open_canvas(1080,600,sync=60)
    hide_lattice()
    game_framework.reset_time()
    create_LaunchingStage()
    play_bgm()
    LAUNCHING = True

def exit():
    global LAUNCHING
    destroy_LaunchingStage()
    LAUNCHING = False

def collide(a,b):
    BisonX, BisonY, BisonR = a.get_bb()
    MonsterX, MonsterY, MonsterR = b.get_bb()

    if math.sqrt(
            math.pow((BisonX - MonsterX),2)
            + math.pow((BisonY - MonsterY),2)
                ) \
            > (BisonR + MonsterR ):
        return False
    return True
    # 주인공 개체의 X1,Y1 좌표값과 충돌판정될 반지름
    # 몬스터 개체의 X2,Y2 좌표값과 반지름을 get_bb로 반환시켜
    # 루트 ( (X1 - X2)^2 + (Y1 - Y2)^2 )가
    # 각 반지름의 합보다 클경우는
    # 두 개체가 접하지 않은것으로 판정 -> False 반환 !

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
                game_framework.change_state(FlyingState)
            else :
                bison.handle_event(event)


def update(frame_time):
    if LAUNCHING == True :
        monster.update(frame_time)
        bison.update(frame_time)
        if collide(bison, monster) :
            if bison.state == bison.ATTACKING :
                play_HittingSound()
                bison.state = bison.HITTING
                monster.state = monster.NORMAL_DRAGGING
            elif bison.state == bison.BOOSTERED:
                play_HittingSound()
                play_SuccessSound()
                bison.state = bison.HITTING
                monster.state = monster.SUCCESS_DRAGGING
            elif bison.state == bison.FAILED :
                bison.state = bison.REFLECTING
                monster.state = monster.FAIL_DRAGGING
        background.update(frame_time)
        gaugebar.update(frame_time, bison)
        gaugepoint.update(frame_time, bison)

    elif LAUNCHING == False :
        game_framework.change_state(FlyingState)

def draw(frame_time):
    clear_canvas()
    background.draw()
    ground.draw()
    monster.draw()
    bison.draw()
    grass.draw()
    gaugebar.draw()
    gaugepoint.draw()
    update_canvas()
    pass

if __name__ == '__main__' :
    enter()