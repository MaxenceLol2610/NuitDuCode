import mobs
import movements
import startOver
import upgrades
import world
import pyxel

pyxel.init(256, 256, title="Seldha", fps=30)
print("Game Started")

def update():
    if startOver.start == 0 and pyxel.btnp(pyxel.KEY_SPACE):
        startOver.start = 1

def draw():
    pyxel.cls(0)
    if startOver.start == 0:
        startOver.draw()
    else:
        world.draw()


pyxel.run(update, draw)
