from pico2d import *
import game_framework
import game_start

# 이벤트 정의
RD, LD, RU, LU, SPACE, UD, DD, UU, DU, TIMER, ATTACKED = range(11)
event_name = ['RD','LD','RU','LU','SPACE','UD','DD','UU','DU','TIMER','DIE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_UP): UD,
    (SDL_KEYDOWN, SDLK_DOWN): DD,
    (SDL_KEYUP, SDLK_UP): UU,
    (SDL_KEYUP, SDLK_DOWN): DU,
}

# character run speed
PIXEL_PER_METER = (10.0 / 0.2)
RUN_SPEED_KMPH = 5.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# character action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


# 상태 정의
class IDLE:
    @staticmethod
    def enter(self,event):
        self.jump_cnt = 50
        self.dir = 0
    
    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        self.frame = 1
        if self.go_down == True:
            self.y -= RUN_SPEED_PPS * game_framework.frame_time
        self.y = clamp(25, self.y, 680)

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw_to_origin(18, 0, 18, 18,  self.x, self.y, self.size, self.size)
        else:
            self.image.clip_composite_draw_to_origin(18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)

class RUN:
    @staticmethod
    def enter(self, event):
        self.jump_cnt = 50
        if event != TIMER:
            self.dir = 0
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    @staticmethod
    def exit(self, event):
        self.face_dir = self.dir

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(-20, self.x, 720 - self.size)
        if self.go_down == True:
            self.y -= RUN_SPEED_PPS * game_framework.frame_time            

    @staticmethod
    def draw(self):
        if self.dir == 1:
            self.image.clip_draw_to_origin(int(self.frame) * 18, 0, 18, 18,  self.x, self.y, self.size, self.size)
        elif self.dir == -1:
            self.image.clip_composite_draw_to_origin(int(self.frame) * 18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)

class JUMP:
    @staticmethod
    def enter(self,event):
        self.jump_sound.play(1)

    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        if self.jump_cnt >= 26:
            self.y += 3 * RUN_SPEED_PPS * game_framework.frame_time
        elif self.jump_cnt < 26 and self.jump_cnt >= 1:
            self.y -= 3 * RUN_SPEED_PPS * game_framework.frame_time
        elif self.jump_cnt <= 0:
            self.add_event(TIMER)
        self.jump_cnt -= 1

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw_to_origin(18, 0, 18, 18,  self.x, self.y, self.size, self.size)
        else:
            self.image.clip_composite_draw_to_origin(18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)

class RUN_JUMP:
    @staticmethod
    def enter(self,event):
        if event != SPACE:
            self.dir = 0
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1
        self.jump_sound.play(1)

    @staticmethod
    def exit(self,event):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        self.x = clamp(-20, self.x, 720 - self.size)
        
        if self.jump_cnt >= 26:
            self.y += 3 * RUN_SPEED_PPS * game_framework.frame_time
        elif self.jump_cnt < 26 and self.jump_cnt >= 1:
            self.y -= 3 * RUN_SPEED_PPS * game_framework.frame_time
        elif self.jump_cnt <= 0:
            self.add_event(TIMER)
        self.jump_cnt -= 1

    @staticmethod
    def draw(self):
        if self.dir == 1:
            self.image.clip_draw_to_origin(int(self.frame) * 18, 0, 18, 18,  self.x, self.y, self.size, self.size)
        elif self.dir == -1:
            self.image.clip_composite_draw_to_origin(int(self.frame) * 18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)

class LIFT_IDLE:
    @staticmethod
    def enter(self, event):
        self.can_go_h = False
        self.dir = 0

    @staticmethod
    def exit(self, event):
        self.can_go_h = True

    @staticmethod
    def do(self):
        self.frame = 0
        if self.go_down == False:
            pass

    @staticmethod
    def draw(self):
        self.lift_image.clip_draw_to_origin(18, 0, 18, 18, self.x, self.y, self.size, self.size)

class LIFT:
    @staticmethod
    def enter(self, event):
        self.can_go_h = False
        self.dir = 0
        if event == UD:
            self.dir += 1
        elif event == DD:
            self.dir -= 1
        elif event == UU:
            self.dir -= 1
        elif event == DU:
            self.dir += 1

    @staticmethod
    def exit(self, event):
        self.face_dir = 1
        self.can_go_h = True

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.y += self.dir * RUN_SPEED_PPS * game_framework.frame_time
    
    @staticmethod
    def draw(self):
        if self.dir == 1:
            self.lift_image.clip_draw_to_origin(int(self.frame) * 18, 0, 18, 18, self.x, self.y, self.size, self.size)
        elif self.dir == -1:
            self.lift_image.clip_composite_draw_to_origin(int(self.frame) * 18, 0, 18, 18, 0, 'h', self.x, self.y, self.size, self.size)

class HURT:
    @staticmethod
    def enter(self,event):
        pass
    
    @staticmethod
    def exit(self,event):
        pass
    
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.y -= RUN_SPEED_PPS * game_framework.frame_time
        if self.go_down == False:
            self.add_event(TIMER)
     
    @staticmethod
    def draw(self):
        self.dying_image.clip_draw_to_origin(int(self.frame) * 18,0,18,18,self.x,self.y,self.size,self.size)


class DIED:
    @staticmethod
    def enter(self,event):
        pass
    
    @staticmethod
    def exit(self,event):
        pass
    
    @staticmethod
    def do(self):
        self.frame = 4
    
    @staticmethod
    def draw(self):
        self.dying_image.clip_draw_to_origin(int(self.frame) * 18,0,18,18,self.x,self.y,self.size,self.size)
        self.font.draw(110,335,'GAME OVER',(255,255,255))
        delay(2)
        game_framework.change_state(game_start)

next_state = {
    IDLE: {RU: RUN, LU:RUN, RD: RUN, LD: RUN, SPACE: JUMP, UD: LIFT, DD: LIFT, UU: LIFT, DU: LIFT,ATTACKED: HURT},
    RUN: {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SPACE: RUN_JUMP, UD: LIFT, DD: LIFT, UU: LIFT, DU: LIFT,ATTACKED: HURT},
    JUMP: {TIMER: IDLE, RU: RUN_JUMP, LU:RUN_JUMP, RD: RUN_JUMP, LD: RUN_JUMP,ATTACKED: HURT},
    RUN_JUMP: {TIMER: RUN, RU: JUMP, LU: JUMP, RD: JUMP, LD: JUMP,ATTACKED: HURT},
    LIFT_IDLE: {UD: LIFT, DD: LIFT, UU: LIFT, DU: LIFT, RD: RUN, LD: RUN,ATTACKED: HURT},
    LIFT: {UD: LIFT_IDLE, DD: LIFT_IDLE, UU: LIFT_IDLE, DU: LIFT_IDLE,ATTACKED: HURT},
    HURT: {TIMER: DIED},
    DIED: {}
}

class Mario:
    def __init__(self,stagenum):
        if stagenum == 1:
            self.x, self.y = 150, 30
        elif stagenum == 2:            
            self.x, self.y = 150, 30
        self.frame = 1
        self.size = 40
        self.jump_cnt = 50
        self.dir = 0 # 1 오른쪽 -1 왼쪽
        self.image = load_image('sprite/mario01.png')
        self.dying_image = load_image('sprite/mario02.png')
        self.lift_image = load_image('sprite/mario03.png')
        self.face_dir = 1
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)
        self.before_state = IDLE
        self.go_down = True
        self.can_go_v = False
        self.can_go_h = True
        self.font = load_font('font/ARCADE.TTF', 100)
        self.jump_sound = load_wav('sound/16.wav')
        self.jump_sound.set_volume(32)

    def update(self):
        self.cur_state.do(self)
        self.go_down = True
        self.can_go_v = False
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                pass
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event == UD or key_event == UU or key_event == DD or key_event == DU:
                if self.can_go_v == False:
                    return
            self.add_event(key_event)

    def get_bb(self):
        return self.x, self.y, self.x + self.size, self.y + self.size - 2

    def handle_collision(self, other, group):
        if group == 'chara:land':
            if self.y >= other.y:
                self.go_down = False
                self.y = other.y + 5

        if group == 'chara:ladder':
            if self.x <= other.x and self.x + self.size >= other.x + 25:
                self.can_go_v = True
                if self.cur_state == LIFT_IDLE or self.cur_state == LIFT:
                    if self.y <= other.y + 25 and self.y >= other.y - 5:
                        self.y = clamp(other.y, self.y, other.y + 20)

        if group == 'chara:barrel':
            self.add_event(ATTACKED)

        if group == 'chara:gf':
            self.font.draw(110,335,'STAGE1 CLEAR',(255,255,255))
            delay(2)
            import stage02
            game_framework.change_state(stage02)