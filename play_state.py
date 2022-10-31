from pico2d import *
import game_framework
from background import BG
from mario import Mario

bg = None
chara = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            chara.handle_event(event)

def enter():
    global bg, chara
    bg = BG()
    chara = Mario()

def exit():
    global chara, bg
    del chara
    del bg

def update():
    chara.update()
    delay(0.1)

def draw_world():
    bg.draw()
    chara.draw()

def draw():
    clear_canvas()    
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def test_self():
    import play_state

    pico2d.open_canvas(700, 800)
    game_framework.run(play_state)
    pico2d.close_canvas()

if __name__ == '__main__':
    test_self()