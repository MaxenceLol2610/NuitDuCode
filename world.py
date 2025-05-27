import pyxel
import player
import mobs
import random
import math
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
        self.loot_list = ["Coin", "Health"]
        self.loot = self.random_loot()
        self.x = x
        self.y = y

    def random_loot(self):
        return self.loot_list[pyxel.rndi(0, len(self.loot_list) - 1)]
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 32, 16, 16, 2, 0, 2)
    
    def check_collision(self, player):
        player_x, player_y = player.get_position()
        distance = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
        
        if distance < 16:  # If player is within 16 pixels (hitbox)
            if self.loot == "Coin":
                player.add_coins(5)
            elif self.loot == "Health":
                player.add_health(20)
            return True
        return False


def gen_loot():
    loot_box.append(Loot(random.randint(0, 224), random.randint(0, 224)))
                    
def update():
    frame = pyxel.frame_count
    if frame % 100*30 == 0:
        gen_loot()
    
    # Check for collisions with loot boxes
    for loot in loot_box[:]:  # Use a slice copy to avoid modifying while iterating
        if loot.check_collision(Player):
            loot_box.remove(loot)

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

