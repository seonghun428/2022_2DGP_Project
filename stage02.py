from pico2d import *
import game_framework
import game_world

from background import BG, Land
from mario import Mario
from kong import Kong
from ladder import Ladder
from oil import Oil
from barrel import Barrel
from pauline import Pauline

bg = None
chara = None
boss = None
oil = None
gf = None
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
    global bg, chara, boss, lands, ladders, oil, barrels,gf
    bg = BG(2)
    
    for x in range(28):
        lands.append(Land(x * 25 ,20))

    for y in range(5):
        ladders.append(Ladder(25, y * 25 + 23))
    
    oil = Oil()
    
    boss = Kong()
    chara = Mario()
    gf = Pauline()
    
    game_world.add_object(bg, 0)
    game_world.add_objects(lands, 1)
    game_world.add_objects(ladders, 1)
    game_world.add_object(oil,1 )
    game_world.add_objects(barrels,1)
    game_world.add_object(boss, 1)
    game_world.add_object(chara, 1)
    game_world.add_object(gf,1)
    
    game_world.add_collision_pairs(chara, lands, 'chara:land')
    game_world.add_collision_pairs(chara, ladders, 'chara:ladder')
    game_world.add_collision_pairs(barrels,lands, 'barrel:land')
    game_world.add_collision_pairs(oil, barrels,'oil:barrel')
    game_world.add_collision_pairs(chara, gf, 'chara:gf')
    # game_world.add_collision_pairs(oil, barrels,'oil:barrel)

def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a,b,group in game_world.all_collision_pairs():
        if collide(a,b):
            a.handle_collision(b,group)
            b.handle_collision(a,group)
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

def collide(a,b):
    la,ba,ra,ta = a.get_bb()
    lb,bb,rb,tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

def test_self():
    import stage02

    pico2d.open_canvas(700,800)
    game_framework.run(stage02)
    pico2d.close_canvas()

if __name__ == '__main__':
    test_self()