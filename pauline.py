from pico2d import *
import game_framework

# 상태
class IDLE:
    @staticmethod
    def enter(self,event):
        self.dir = 0

    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        self.frame = 2

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw_to_origin(int(self.frame) * 20, 0, 20, 22,  self.x, self.y, 40, 44)
        elif self.face_dir == -1:
            self.image.clip_composite_draw_to_origin(int(self.frame) * 20, 0, 20, 22, 0, 'h', self.x, self.y, 40, 44)

class Pauline():
    def __init__(self,stagenum):
        if stagenum == 1:
            self.x, self.y = 280, 625
        elif stagenum == 2:
            self.x, self.y = 320, 650
        self.frame = 2
        self.dir = 0
        self.face_dir = 1
        self.image = load_image('sprite/pauline.png')

        self.cur_state = IDLE
        self.cur_state.enter(self,None)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x,self.y,self.x+80,self.y+44

    def handle_collision(self,other,group):
        pass