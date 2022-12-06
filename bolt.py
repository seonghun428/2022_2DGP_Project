from pico2d import *
import game_framework

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

    def get_bb(self):
        return self.x,self.y,self.x + 25, self.y + 28

    def handle_collision(self,other,group):
        if group == 'chara:bolt':
            if self.can_draw:
                Bolt.cnt -= 1
                if Bolt.cnt == 0:
                    import ending
                    game_framework.change_state(ending)
            self.can_draw = False