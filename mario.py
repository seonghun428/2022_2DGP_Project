from pico2d import *

class Mario:
    def __init__(self):
        self.x, self.y = 10, 25
        self.frame = 1
        self.size = 40
        self.jump_cnt = 0
        self.state = 0 # 0 기본 1 점프 2 사다리타기 3 아이템 사용 4 죽음
        self.dir = 0 # 1 오른쪽 -1 왼쪽
        self.face_dir = 1
        self.image = load_image('sprite/mario01.png')
        self.dying_image = load_image('sprite/mario02.png')

    def update(self):
        self.frame = (self.frame + 1) % 3
        self.x += self.dir * 3
        self.x = clamp(0, self.x, 700)        

    def jump(self):
        self.state = 1
        if self.jump_cnt < 5:
            self.y += 5
        else:
            self.y -= 5
        if self.jump_cnt == 9:
            self.state = 0
        self.jump_cnt = (self.jump_cnt + 1) % 10    
        delay(0.1)

    def draw(self):
        match self.state:
            case 0:
                if self.dir == 1:
                    self.image.clip_draw_to_origin(self.frame * 24, 0, 24, 24,  self.x, self.y, self.size, self.size)
                elif self.dir == -1:
                    self.image.clip_composite_draw_to_origin(self.frame * 24, 0, 24, 24, 0, 'h', self.x, self.y, self.size, self.size)
                else:
                    if self.face_dir == 1:
                        self.image.clip_draw_to_origin(24, 0, 24, 24,  self.x, self.y, self.size, self.size)
                    else:
                        self.image.clip_composite_draw_to_origin(24, 0, 24, 24, 0, 'h', self.x, self.y, self.size, self.size)
            case 1:
                match self.dir:
                    case 1:
                        self.image.clip_draw_to_origin(self.frame * 24, 0, 24, 24,  self.x, self.y, self.size, self.size)
                    case -1:
                        self.image.clip_composite_draw_to_origin(self.frame * 24, 0, 24, 24, 0, 'h', self.x, self.y, self.size, self.size)
                    case 0:
                        self.image.clip_draw_to_origin(self.frame * 24, 0, 24, 24,  self.x, self.y, self.size, self.size)
            case 4:
                self.dying_image.clip_draw_to_origin(self.frame * 24, 0, 24, 24,  self.x, self.y, self.size, self.size)
    
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_LEFT:
                    self.dir -= 1
                case pico2d.SDLK_RIGHT:
                    self.dir += 1
                case pico2d.SDLK_SPACE:
                    self.jump()
        elif event.type == SDL_KEYUP:
            match event.key:
                case pico2d.SDLK_LEFT:
                    self.dir += 1
                    self.face_dir = -1
                case pico2d.SDLK_RIGHT:
                    self.dir -= 1                    
                    self.face_dir = 1