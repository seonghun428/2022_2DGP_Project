from pico2d import *

class BG:
    def __init__(self, stage_num):
        self.stage = stage_num
        self.start_image = load_image('sprite/start.png')
        self.stage01_image = load_image('sprite/bg01.png')
        self.stage02_image = load_image('sprite/bg04.png')
        self.end_image = load_image('sprite/end.png')
        self.font = load_font('font/ARCADE.TTF', 50)
        self.start_sound = load_music('sound/05.mp3')
        self.start_sound.set_volume(32)
        self.end_sound = load_music('sound/14.mp3')
        self.end_sound.set_volume(32)
        match self.stage:
            case 0:
                self.start_sound.play(1)
            case 1:
                pass
            case 2:
                pass
            case 3:
                self.end_sound.play(1)

    def update(self):
        pass

    def draw(self):
        match self.stage:
            case 0:
                self.start_image.draw_to_origin(0,0,700,800)
            case 1:
                self.stage01_image.draw_to_origin(0,0,700,800)
            case 2:
                self.stage02_image.draw_to_origin(0,0,700,800)
            case 3:
                self.end_image.draw_to_origin(0,0,700,800)
                self.font.draw(110, 300,'Press Enter to Restart',(255,255,255))
                self.font.draw(110, 200,'Press Escape to Exit',(255,255,255))

class Land:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x,self.y,self.x+25,self.y+5

    def handle_collision(self,other,group):
        pass