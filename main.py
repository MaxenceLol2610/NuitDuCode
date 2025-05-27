import mobs
import player
import startOver
import upgrades
import world
import pyxel

pyxel.init(256, 256, title="Seldha")
print("Game Started")

def update():
    startOver.update()

def draw():
    pyxel.cls(0)
    startOver.draw()

pyxel.run(update, draw)
