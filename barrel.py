from pico2d import *
import game_framework
import game_world

# 이벤트 정의
TIMER, LAND, AIR = 0, 1, 2
event_name = ['TIMER','LAND','AIR']

# barrel run speed
PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 7.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# barrel action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

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
        pass
    
    @staticmethod
    def draw(self):
        pass

class DROP:
    @staticmethod
    def enter(self,event):
        self.dir = 0

    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        self.y -= RUN_SPEED_PPS * game_framework.frame_time
        if self.go_down == False:
            if self.stage == 1:
                if self.x >= 650 or self.x <= 49:
                    self.drop_cnt += 1
            elif self.stage == 2:
                if self.x >= 575 or self.x <= 125:
                    self.drop_cnt += 1
            self.add_event(LAND)

    @staticmethod
    def draw(self):
        self.image.clip_draw_to_origin(int(self.frame) * 14, 0, 14, 10,  self.x, self.y, self.size, self.size)

class ROLL:
    def enter(self,event):
        if self.drop_cnt % 2 == 1:
            self.dir = 1
        elif self.drop_cnt % 2 == 0:
            self.dir = -1

    def exit(self,event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(-10, self.x, 710 - self.size)
        if self.go_down == True:
            self.add_event(AIR)

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw_to_origin(int(self.frame) * 14, 0, 14, 10,  self.x, self.y, self.size, self.size)
        elif self.dir == -1:
            self.image.clip_composite_draw_to_origin(int(self.frame) * 14, 0, 14, 10, 0, 'h', self.x, self.y, self.size, self.size)


next_state = {
    IDLE: {TIMER: ROLL},
    DROP: {LAND: ROLL},
    ROLL: {AIR: DROP}
}

class Barrel:
    def __init__(self,stagenum):
        if stagenum == 1:
            self.x, self.y = 50, 538
            self.stage = 1
        elif stagenum == 2:
            self.x, self.y = 370, 538
            self.stage = 2
        self.size = 30
        self.dir = 0
        self.drop_cnt = 0
        self.frame = 0
        self.go_down = True
        self.image = load_image('sprite/barrel02.png')

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        self.go_down = True
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
        draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0,event)

    def get_bb(self):
        return self.x,self.y,self.x+self.size,self.y+self.size

    def handle_collision(self,other,group):
        if group == 'barrel:land':
            if self.y >= other.y:
                self.go_down = False
                self.y = other.y + 5

        if group == 'oil:barrel':
            game_world.remove_object(self)
            
        if group == 'chara:barrel':
            game_world.remove_object(self)