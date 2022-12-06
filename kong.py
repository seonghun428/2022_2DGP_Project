from pico2d import *
import game_framework
import game_world

from barrel import Barrel

# 이벤트 정의
TIMER = 0
event_name = ['TIMER']

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
        self.timer = 250
        if self.stage == 1:
            self.stage1_sound.repeat_play()
        elif self.stage == 2:
            self.stage2_sound.repeat_play()
    
    @staticmethod
    def exit(self,event):
        if self.stage == 1:
            self.stage1_sound.stop()
        elif self.stage == 2:
            self.stage2_sound.stop()

    @staticmethod
    def do(self):
        self.frame = 1
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)

    @staticmethod
    def draw(self):
        self.image.clip_draw_to_origin(int(self.frame) * 50, 0, 50, 36,  self.x, self.y, 100, 72)


class OPENING:
    @staticmethod
    def enter(self, event):
        self.timer = 350
        if self.stage == 1:
            self.start1_sound.play(1)
        elif self.stage == 2:
            self.start2_sound.play(1)

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)

    @staticmethod
    def draw(self):
        self.opening_image.clip_draw_to_origin(int(self.frame) * 50, 0, 50, 36, self.x, self.y, 100, 72)

class THROW:
    @staticmethod
    def enter(self,event):
        self.timer = 90
        self.throw()

    @staticmethod
    def exit(self,event):
        pass
    
    @staticmethod
    def do(self):
        if self.stage == 1:
            self.frame = 2
        elif self.stage == 2:
            self.frame = 0
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)
    
    @staticmethod
    def draw(self):
        self.image.clip_draw_to_origin(int(self.frame) * 50, 0, 50, 36,  self.x, self.y, 100, 72)

next_state = {
    OPENING: {TIMER: IDLE},
    IDLE: {TIMER: THROW},
    THROW: {TIMER: IDLE}
}

class Kong:
    # barrels = []
    def __init__(self,stagenum):
        if stagenum == 1:
            self.x, self.y = 20, 538
        elif stagenum == 2:
            self.x, self.y = 290, 525
        self.stage = stagenum
        self.barrels = [Barrel(self.stage) for _ in range(100)]
        self.cnt = 0
        self.frame = 0
        self.opening_image = load_image('sprite/dk01.png')
        self.image = load_image('sprite/dk02.png')
        self.dying_image = load_image('sprite/dk03.png')
        self.timer = 100
        self.start1_sound = load_music('sound/03.mp3')
        self.start1_sound.set_volume(32)
        self.start2_sound = load_music('sound/04.mp3')
        self.start2_sound.set_volume(32)
        self.stage1_sound = load_music('sound/06.mp3')
        self.stage1_sound.set_volume(32)
        self.stage2_sound = load_music('sound/10.mp3')
        self.stage2_sound.set_volume(32)

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

    def get_bb(self):
        return self.x, self.y, self.x + 100, self.y + 72

    def handle_collision(self, other, group):
        pass

    def throw(self):
        self.barrels[self.cnt].add_event(TIMER)
        self.cnt += 1