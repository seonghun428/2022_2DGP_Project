from pico2d import *

bg = None

class BG:
    def __init__(self):
        self.stage = 0
        self.stage01_image = load_image('sprite/bg01.png')
        self.stage02_image = load_image('sprite/bg02.png')
        self.stage03_image = load_image('sprite/bg03.png')
        self.stage04_image = load_image('sprite/bg04.png')

    def draw(self):
        if self.stage == 1:
            self.stage01_image.draw(111, 128)
        elif self.stage == 2:
            self.stage02_image.draw(111, 128)
        elif self.stage == 3:
            self.stage03_image.draw(111, 128)
        elif self.stage == 4:
            self.stage04_image.draw(111, 128)

def start():
    global bg
    bg = BG()


open_canvas(223, 256)
start()
for i in range(0, 4):
    bg.stage += 1
    bg.draw()
    update_canvas()
    delay(1.0)
close_canvas()