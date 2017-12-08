from pico2d import *

import random
import math

class Bison:

    image = None

    DESCENT, RISING, ROTATING, KNOCKOUT = 1, 0, 2, 5

    PIXEL_PER_METER = 108
    FLYING_SPEED_KMPH = 10
    GRAVITIONAL_ACCELERATION = 9.81 #MPS
    ENERGY_LOSS = 9.81
    ELASTIC_ENERGY = 0

    def __init__(self):
        global frame_count
        global time_count
        global DESCENT_SPEED_MPS
        global RISING_SPEED_MPS
        frame_count = 0
        time_count = 0
        DESCENT_SPEED_MPS = 0
        RISING_SPEED_MPS = 0
        self.x, self.y = 0, 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.frame = 0
        self.direction = -1
        self.state = self.DESCENT
        if self.image == None :
            self.image = load_image('./Images/FlyingB_sprite.png')
            pass

    def set_background(self, background):
        self.background = background
        self.x = self.background.w / 4
        self.y = self.background.h

    def update(self, frame_time):
        global frame_count
        global time_count
        global DESCENT_SPEED_MPS
        global RISING_SPEED_MPS

        self.FLYING_SPEED_MPM = ( self.FLYING_SPEED_KMPH * 1000 ) / 60
        self.FLYING_SPEED_MPS = self.FLYING_SPEED_MPM / 60
        self.FLYING_SPEED_PPS = self.FLYING_SPEED_MPS * self.PIXEL_PER_METER
        distance = self.FLYING_SPEED_PPS * frame_time

        self.x += distance

        if self.state == self.DESCENT :
            self.frame = 0
            self.direction = -1
            DESCENT_SPEED_MPS += self.GRAVITIONAL_ACCELERATION * frame_time
            RISING_SPEED_MPS = DESCENT_SPEED_MPS
            self.ELASTIC_ENERGY = DESCENT_SPEED_MPS
            DESCENT_SPEED_PPS = DESCENT_SPEED_MPS * self.PIXEL_PER_METER
            distance = DESCENT_SPEED_PPS * frame_time

            self.y += self.direction * distance

        elif self.state == self.ROTATING :
            frame_count += frame_time
            if frame_count > 0.05 :
                self.frame = ( self.frame + 1 ) % 6
                frame_count = 0
            self.direction = 1
            RISING_SPEED_MPS -= ( self.ENERGY_LOSS + 1.0) * frame_time
            DESCENT_SPEED_MPS = RISING_SPEED_MPS
            RISING_SPEED_PPS = RISING_SPEED_MPS * self.PIXEL_PER_METER
            distance = RISING_SPEED_PPS * frame_time

            self.y += self.direction * distance

            if RISING_SPEED_MPS < 0:
                self.state = self.DESCENT

        elif self.state == self.KNOCKOUT :
            self.image = load_image('./Images/LaunchingB_sprite.png')
            self.FLYING_SPEED_KMPH = 0
            self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 250, self.state * 250, 250, 250,
                             self.x - self.background.q3l,
                             self.y - self.background.q3b)

    def get_bb(self):
        r = 40
        t = 0
        x = self.x - math.cos(t) * r
        y = self.y + math.sin(t) * r
        while True :
            t += 0.25
            return x, y, r