import pyxel
import player
import mobs
import random
import interace

Player = player.PLAYER
Mobs = mobs.MOBS
loot_box = []


def draw_welcome():
    pyxel.cls(0)
    pyxel.text(10, 10, "Welcome to the World of Seldha!", 7)
    pyxel.text(10, 20, "Explore and enjoy your adventure!", 7)
    pyxel.text(10, 30, "Press 'Q' to quit.", 7)


  
class Loot:
    def __init__(self, x=0, y=0):
        self.loot_list = ["Coin", "Health", "Sword"]
        self.loot = self.random_loot()
        self.x = x
        self.y = y

    def random_loot(self):
        return pyxel.rndi(0, len(self.loot_list) - 1)
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 32, 16, 16, 2, 0, 2)

def gen_loot():
    loot_box.append(Loot(random.randint(0, 224), random.randint(0, 224)))
                    
def update():
    frame = pyxel.frame_count
    if frame % 100*30 == 0:
        gen_loot()

def draw():
    pyxel.cls(9)
    Player.draw()
    Mobs.draw()
    for loot in loot_box:
        loot.draw()
    interace.draw_ui(Player)
"""
pyxel.init(256, 256, title="Seldha", fps=30)
def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
pyxel.run(update, draw_welcome)
"""

