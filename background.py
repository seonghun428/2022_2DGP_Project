from pico2d import *

class BG:
    def __init__(self):
        self.stage = 1
        self.stage01_image = load_image('sprite/bg01.png')
        self.stage02_image = load_image('sprite/bg04.png')
        # self.stage02_image = load_image('sprite/bg02.png')
        # self.stage03_image = load_image('sprite/bg03.png')
        # self.stage04_image = load_image('sprite/bg04.png')

    def change_stage(self):
        self.stage += 1

    def update(self):
        pass

    def draw(self):
        if self.stage == 1:
            self.stage01_image.draw_to_origin(0,0,700, 800)
        elif self.stage == 2:
            self.stage02_image.draw_to_origin(0,0,700, 800)
        # elif self.stage == 3:
        #     self.stage03_image.draw_to_origin(0,0,700, 800)
        # elif self.stage == 4:
        #     self.stage04_image.draw_to_origin(0,0,700, 800)

class Land:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.stage = 1

    def update(self):
        if self.stage == 1:
            pass
        elif self.stage == 2:
            pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x,self.y,self.x+25,self.y+25

    def handle_collision(self,other,group):
        pass