from pico2d import *
import game_framework
import game_world

from background import BG

bg = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                import stage01
                game_framework.change_state(stage01)

def enter():
    global bg

    bg = BG(0)
    game_world.add_object(bg,0)

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
    import game_start

    pico2d.open_canvas(700, 800)
    game_framework.run(game_start)
    pico2d.close_canvas()

if __name__ == '__main__':
    test_self()