from pico2d import *
import game_framework
import game_world

from background import BG
from mario import Mario
from kong import Kong

bg = None
chara = None
boss = None

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
    global bg, chara, boss
    bg = BG()
    chara = Mario()
    boss = Kong()
    game_world.add_object(bg, 0)
    game_world.add_object(chara, 1)
    game_world.add_object(boss, 1)

def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()
    delay(0.01)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

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