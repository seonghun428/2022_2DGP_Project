from pico2d import *
import game_framework
import game_world

from background import BG, Land
from mario import Mario
from kong import Kong
from ladder import Ladder
from oil import Oil
from barrel import Barrel

bg = None
chara = None
boss = None
oil = None
lands = []
ladders = []
barrels = []

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
    global bg, chara, boss, lands, ladders, oil, barrels
    bg = BG(1)

    for x in range(14):
        lands.append(Land(x * 25, 20))
    for y in range(7):
        for x in range(2):
            lands.append(Land((x + 14 + y * 2) * 25, (y + 1) * 3 + 20))
    for y in range(13):
        for x in range(2):
            lands.append(Land((x + y * 2) * 25 - 1, 145 - y * 3))
    for y in range(13):
        for x in range(2):
            lands.append(Land(49 + (x + y * 2) * 25, 210 + y * 3))         
    for y in range(13):
        for x in range(2):
            lands.append(Land((x + y * 2) * 25 - 1, 350 - y * 3))
    for y in range(13):
        for x in range(2):
            lands.append(Land(49 + (x + y * 2) * 25, 417 + y * 3))
    for x in range(18):
        lands.append(Land(x * 25 - 1, 532))
    for y in range(4):
        for x in range(2):
            lands.append(Land(449 + (x + y * 2) * 25, 529 - y * 3))
    for x in range(6):
        lands.append(Land(273 + x * 25, 619))

    ladders.append(Ladder(248,25))
    for y in range(3):
        ladders.append(Ladder(574, y * 25 + 40))
    
    barrels.append(Barrel())

    oil = Oil()

    boss = Kong()
    chara = Mario()
    game_world.add_object(bg, 0)
    game_world.add_objects(lands, 1)
    game_world.add_objects(ladders, 1)
    game_world.add_object(oil,1 )
    game_world.add_objects(barrels,1)
    game_world.add_object(boss, 1)
    game_world.add_object(chara, 1)

    game_world.add_collision_pairs(chara, lands, 'chara:land')
    game_world.add_collision_pairs(chara, ladders, 'chara:ladder')
    game_world.add_collision_pairs(barrels,lands, 'barrel:land')
    game_world.add_collision_pairs(oil, barrels,'oil:barrel')
    # game_world.add_collision_pairs(chara, barrels, 'chara:barrel')

def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a,b,group in game_world.all_collision_pairs():
        if collide(a, b):
            # print(f'Collision ', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)
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

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

def test_self():
    import stage01

    pico2d.open_canvas(700, 800)
    game_framework.run(stage01)
    pico2d.close_canvas()

if __name__ == '__main__':
    test_self()