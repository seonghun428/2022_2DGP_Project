from pico2d import *

bg = None
chara = None

class BG:
    def __init__(self):
        self.stage = 0
        self.stage01_image = load_image('sprite/bg01.png')
        self.stage02_image = load_image('sprite/bg02.png')
        self.stage03_image = load_image('sprite/bg03.png')
        self.stage04_image = load_image('sprite/bg04.png')

    def draw(self):
        if self.stage == 1:
            self.stage01_image.draw_to_origin(0,0,700, 800)
        elif self.stage == 2:
            self.stage02_image.draw_to_origin(0,0,700, 800)
        elif self.stage == 3:
            self.stage03_image.draw_to_origin(0,0,700, 800)
        elif self.stage == 4:
            self.stage04_image.draw_to_origin(0,0,700, 800)

class Mario:
    def __init__(self):
        self.x = 10
        self.y = 25
        self.frame = 1
        self.state = 0
        self.image = load_image('sprite/mario01.png')
        self.dying_image = load_image('sprite/mario02.png')

    def draw(self):
        if self.state == 0:
            self.image.clip_draw_to_origin(self.frame * 24, 0, 24, 24,  self.x, self.y, 36, 36)
        elif self.state == 1:
            self.dying_image.clip_draw_to_origin(self.frame * 24, 0, 24, 24,  self.x, self.y, 36, 36)

def start():
    global bg, chara
    bg = BG()
    chara = Mario()

def draw():
    bg.draw()
    chara.draw()


open_canvas(700, 800)
start()
for i in range(0, 4):
    bg.stage += 1
    draw()
    update_canvas()
    delay(1.0)
close_canvas()