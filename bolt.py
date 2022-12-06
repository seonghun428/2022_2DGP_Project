from pico2d import *

class Bolt():
    cnt = 8
    def __init__(self,x,y):
        self.x, self.y = x,y
        self.image = load_image('sprite/bolt.png')
        self.can_draw = True
    
    def update(self):
        pass

    def draw(self):
        if self.can_draw:
            self.image.draw_to_origin(self.x,self.y,25,28)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x,self.y,self.x + 25, self.y + 28

    def handle_collision(self,other,group):
        if group == 'chara:bolt':
            if self.can_draw:
                Bolt.cnt -= 1
            self.can_draw = False