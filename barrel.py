from pico2d import *
import game_framework

# 이벤트 정의
LAND = 0
event_name = ['LAND']
key_event_table = {

}

# barrel run speed
PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 6.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# barrel action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

# 상태 정의
class DROP:
    @staticmethod
    def enter(self,event):
        pass

    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        pass

class ROLL:
    def enter(self,event):
        pass

    def exit(self,event):
        pass

    def do(self):
        pass

    def draw(self):
        pass

next_state = {
    DROP: {LAND: ROLL},
    ROLL: {}
}

class Barrel:
    def __init__(self):
        self.x = None
        self.y = None
        self.frame = 0
        self.image = None
        self.drop_image = None

        self.event_que = []
        self.cur_state = DROP
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
            self.cur_state.enter(self,event)

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0,event)

    def handle_event(self,event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)