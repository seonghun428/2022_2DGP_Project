from pico2d import *
import game_framework

#oil action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

# 상태 정의
class IDLE:
    @staticmethod
    def enter(self,event):
        pass
    
    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(self):
        self.image.clip_draw_to_origin(int(self.frame) * 20, 0, 20, 32,  self.x, self.y, 40, 62)

class Oil:
    def __init__(self):
        self.x, self.y = 60,25
        self.size = 40
        self.frame = 0
        self.image = load_image('sprite/oil.png')

        self.cur_state = IDLE
        self.cur_state.enter(self,None)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x,self.y,self.x + 40,self.y + 62

    def handle_collision(self,other,group):
        pass