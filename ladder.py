from pico2d import *

class Ladder:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.stage = 1

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x, self.y, self.x + 25, self.y + 25

    def handle_collision(self,other,group):
        pass