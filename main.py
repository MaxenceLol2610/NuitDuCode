import mobs
import player
import startOver
import upgrades
import world
import pyxel

pyxel.init(256, 256, title="Seldha", fps=30)
print("Game Started")

def update():
    if startOver.start == 0 and pyxel.btnp(pyxel.KEY_SPACE):
        startOver.start = 1
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    if startOver.start == 0 or startOver.start == -1:
        startOver.draw()
        
    else:
        world.draw()
    


pyxel.run(update, draw)
