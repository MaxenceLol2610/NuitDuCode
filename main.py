import mobs
import player
import startOver
import upgrades
import world
import pyxel

pyxel.init(256, 256, title="Seldha", fps=30)
print("Game Started")

Player = player.PLAYER

def update():
    frame = pyxel.frame_count
    if startOver.start == 0 and pyxel.btnp(pyxel.KEY_SPACE):
        startOver.start = 1
        Player.update(frame)
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnp(pyxel.KEY_U):
        upgrades.shop.toggle_visibility()
    if upgrades.shop.visible:
        upgrades.shop.update()

def draw():
    pyxel.cls(0)
    if startOver.start == 0 or startOver.start == -1:
        startOver.draw()
    else:
        world.draw()
        player.draw()
    
    upgrades.shop.draw()

pyxel.run(update, draw)
