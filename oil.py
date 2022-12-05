from pico2d import *
import game_framework

class Oil:
    def __init__(self):
        self.x, self.y = 10,25
        self.size = 40
        self.image = None

    def update(self):
        pass

    def draw(self):
        pass

    def get_bb(self):
        pass

    def handle_collision(self,other,group):
        pass