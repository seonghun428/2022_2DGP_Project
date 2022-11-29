from pico2d import *
import game_framework

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

# character run speed
PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 4.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# character action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


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
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(0, self.x, 700 - self.size)

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw_to_origin(int(self.frame) * 18, 0, 18, 18,  self.x, self.y, self.size, self.size)
        elif self.dir == -1:
            self.image.clip_composite_draw_to_origin(int(self.frame) * 18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)


next_state = {
    IDLE: {RU: RUN, LU:RUN, RD: RUN, LD: RUN, SPACE: IDLE},
    RUN: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SPACE: RUN},
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
        draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb(self):
        return self.x, self.y, self.x + self.size, self.y + self.size

    def handle_collision(self, other, group):
        pass