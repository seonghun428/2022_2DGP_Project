from pico2d import *
import game_framework

# 상태
class IDLE:
    @staticmethod
    def enter(self,event):
        pass

    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        pass

class Pauline():
    def __init__(self):
        self.x = 200
        self.y = 650
        self.frame = 3
        self.image = load_image('sprite/pauline.png')

        self.cur_state = IDLE
        self.cur_state.enter(self,None)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x,self.y,self.x+40,self.y+44

    def handle_collision(self,other,group):
        pass