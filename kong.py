from pico2d import *
import game_framework

# 이벤트 정의
TIMER = 0
event_name = ['TIMER']
key_event_table = {

}

# boss run speed
PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 5.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# boss action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


# 상태 정의
class IDLE:
    @staticmethod
    def enter(self,event):
        pass
    
    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        self.frame = 1

    @staticmethod
    def draw(self):
        self.image.clip_draw_to_origin(int(self.frame) * 50, 0, 50, 36,  self.x, self.y, 100, 72)


class OPENING:
    def enter(self, event):
        self.timer = 400

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)

    def draw(self):
        self.opening_image.clip_draw_to_origin(int(self.frame) * 50, 0, 50, 36, self.x, self.y, 100, 72)


next_state = {
    OPENING: {TIMER: IDLE},
    IDLE: {}
}

class Kong:
    def __init__(self):
        self.x, self.y = 20, 538
        self.frame = 0
        self.opening_image = load_image('sprite/dk01.png')
        self.image = load_image('sprite/dk02.png')
        self.dying_image = load_image('sprite/dk03.png')
        self.timer = 100

        self.event_que = []
        self.cur_state = OPENING
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
        return self.x, self.y, self.x + 100, self.y + 72

    def handle_collision(self, other, group):
        pass