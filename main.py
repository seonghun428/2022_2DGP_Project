from pico2d import *

bg = None
chara = None
game_start = False
running = False

move_x = 0

class BG:
    def __init__(self):
        self.stage = 1
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
        self.size = 40
        self.state = 0 # 0 기본 1 점프 2 사다리타기 3 아이템 사용 4 죽음
        self.dir = 0 # 0 오른쪽 1 왼쪽
        self.image = load_image('sprite/mario01.png')
        self.dying_image = load_image('sprite/mario02.png')

    def draw(self):
        match self.state:
            case 0:
                match self.dir:
                    case 0:
                        self.image.clip_draw_to_origin(self.frame * 24, 0, 24, 24,  self.x, self.y, self.size, self.size)
                    case 1:
                        self.image.clip_composite_draw_to_origin(self.frame * 24, 0, 24, 24, 0, 'h', self.x, self.y, self.size, self.size)
            case 4:
                self.dying_image.clip_draw_to_origin(self.frame * 24, 0, 24, 24,  self.x, self.y, self.size, self.size)

def start():
    global bg, chara, game_start
    bg = BG()
    chara = Mario()
    game_start = True

def draw():
    global move_x
    clear_canvas()
    bg.draw()
    chara.x += move_x
    chara.draw()

def handle_events():
    global move_x, running
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            running = True
            if event.key == SDLK_ESCAPE:
                quit()
            elif event.key == SDLK_RIGHT:
                chara.dir = 0
                move_x += 5
            elif event.key == SDLK_LEFT:
                chara.dir = 1
                move_x -= 5
        elif event.type == SDL_KEYUP:
            running = False
            chara.frame = 1
            if event.key == SDLK_RIGHT:
                move_x -= 5
            elif event.key == SDLK_LEFT:
                move_x += 5


open_canvas(700, 800)
start()
while game_start:
    draw()
    update_canvas()
    delay(0.1)
    handle_events()
    if running:
        chara.frame = (chara.frame + 1) % 3

close_canvas()