import mobs
import movements
import startOver
import upgrades
import world
import pyxel

pyxel.init(256, 256, title="Seldha")
print("Game Started")

def update():
    startOver.update()
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if startOver.start == 0 and pyxel.btnp(pyxel.KEY_SPACE):
        startOver.start = 1
        world.draw()

def draw():
    pyxel.cls(0)
    startOver.draw()

pyxel.run(update, draw)
