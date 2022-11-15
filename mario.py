from pico2d import *

# 이벤트 정의
RD, LD, RU, LU, SPACE = range(5)
event_name = ['RD','LD','RU','LU','SPACE']
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}

# 상태 정의
class IDLE:
    @staticmethod
    def enter(self,event):
        self.dir = 0
    
    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        self.frame = 1

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw_to_origin(18, 0, 18, 18,  self.x, self.y, self.size, self.size)
        else:
            self.image.clip_composite_draw_to_origin(18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)

class RUN:
    def enter(self, event):
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    def exit(self, event):
        self.face_dir = self.dir

    def do(self):
        self.frame = (self.frame + 1) % 3
        self.x += self.dir
        self.x = clamp(0, self.x, 682)

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw_to_origin(self.frame * 18, 0, 18, 18,  self.x, self.y, self.size, self.size)
        elif self.dir == -1:
            self.image.clip_composite_draw_to_origin(self.frame * 18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)

class JUMP:
    def enter(self, event):
        self.dir = 0

    def exit(self, event):
        pass

    def do(self):
        self.frame = 2

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw_to_origin(18, 0, 18, 18,  self.x, self.y, self.size, self.size)
        else:
            self.image.clip_composite_draw_to_origin(18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)


next_state = {
    IDLE: {RU: RUN, LU:RUN, RD: RUN, LD: RUN, SPACE: JUMP},
    RUN: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SPACE: JUMP},
    JUMP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN}
}

class Mario:
    def __init__(self):
        self.x, self.y = 10, 25
        self.frame = 1
        self.size = 40
        self.jump_cnt = 0
        self.state = 0 # 0 기본 1 점프 2 사다리타기 3 아이템 사용 4 죽음
        self.dir = 0 # 1 오른쪽 -1 왼쪽
        self.image = load_image('sprite/mario01.png')
        self.dying_image = load_image('sprite/mario02.png')
        self.face_dir = 1
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: STATE {self.cur_state}, EVENT {event_name[event]}')
            self.cur_state.enter(self, event)
    
    def jump(self):
        pass

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)