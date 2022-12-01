from pico2d import *

class Ladder:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.stage = 1

    def update(self):
        pass

    def draw(self):
        pass

    def get_bb(self):
        return self.x, self.y, self.x + 50, self.y + 100

    def handle_collision(self,other,group):
        pass