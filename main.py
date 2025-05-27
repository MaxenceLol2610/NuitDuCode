import mobs
import player
import startOver
import upgrades
import world
import pyxel

pyxel.init(256, 256, title="Seldha", fps=30)
pyxel.load("2.pyxres")
print("Game Started")

start_frame = 0

Player = player.PLAYER
Mobs = mobs.MOBS

def update():
    frame = pyxel.frame_count
    Player.update(frame)
    Mobs.update(frame)
    if not pyxel.play_pos(0):
        pyxel.playm(0, loop=True)
    world.update()
    if startOver.start == 0 and pyxel.btnp(pyxel.KEY_SPACE):
        startOver.start = 1
        global start_frame
        start_frame = pyxel.frame_count
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnp(pyxel.KEY_U):
        upgrades.shop.toggle_visibility()
    if upgrades.shop.visible:
        upgrades.shop.update()

def draw():
    pyxel.cls(0)
    frame = pyxel.frame_count
    if startOver.start == 0 or startOver.start == -1:
        startOver.draw()
    else:
        global start_frame
        if frame - start_frame < 60:
            world.draw_welcome()
        else:
            world.draw()
        
    
    upgrades.shop.draw()

pyxel.run(update, draw)
