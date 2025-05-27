import pyxel
import player
import math
import random

Player = player.PLAYER
player_health = Player.get_health()

class Mobs:
    def __init__(self):
        self.mob_speed = 0.5
        self.mob_spawn_rate = 30
        self.ennemis_liste = []
        self.player_x = Player.get_position()[0]
        self.player_y = Player.get_position()[1]
        self.mob_frame = 0
        self.direction = {}
        self.direction_timer = {}

    def mob_nature(self):
        rnd_selector = random.randint(1, 10)
        if rnd_selector >= 2:
            return "skeleton"
        else:
            return "mage"

    def enemy_spawn(self):
        if len(self.ennemis_liste) < 10:
            x = pyxel.rndi(0, 224)
            y = pyxel.rndi(0, 224)
            n = self.mob_nature()
            if n == "skeleton":
                h = 40
            elif n == "mage":
                h = 20
            mob_exclusion_distance = 50
            mob_from_player = math.sqrt((self.player_x - x)**2+(self.player_y - y)**2)
            if [x, y, n, h] not in self.ennemis_liste and mob_from_player > mob_exclusion_distance:
                self.ennemis_liste.append([x, y, n, h])
    def mob_movement(self):
        self.player_x, self.player_y = Player.get_position()
        player_health = Player.get_health()
        
        for mob in self.ennemis_liste:
            if mob[2] == "skeleton":
                mob_id = id(mob)
                if mob_id not in self.direction:
                    self.direction[mob_id] = random.randint(0, 3)
                    self.direction_timer[mob_id] = 0
                
                if player_health <= 7:
                    dx = self.player_x - mob[0]
                    dy = self.player_y - mob[1]
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance > 0:
                        dx = dx/distance * self.mob_speed
                        dy = dy/distance * self.mob_speed
                        mob[0] += dx
                        mob[1] += dy
                else:
                    self.direction_timer[mob_id] += 1
                    
                    if self.direction_timer[mob_id] >= 120 or random.random() < 0.01:
                        self.direction[mob_id] = random.randint(0, 3)
                        self.direction_timer[mob_id] = 0
                    
                    if self.direction[mob_id] == 0:
                        mob[0] += self.mob_speed
                    elif self.direction[mob_id] == 1:
                        mob[1] -= self.mob_speed
                    elif self.direction[mob_id] == 2:
                        mob[0] -= self.mob_speed
                    elif self.direction[mob_id] == 3:
                        mob[1] += self.mob_speed
                    
                    mob[0] = max(0, min(mob[0], 240))
                    mob[1] = max(0, min(mob[1], 240))

    def ennemis_supression(self):
        """Removes mobs that are dead"""
        for mob in self.ennemis_liste:
            if mob[3]<= 0:
                self.ennemis_liste.remove(mob)

    def draw(self):
        for mob in self.ennemis_liste:
            if mob[2] == "skeleton":
                pyxel.blt(mob[0], mob[1], 0, 64, 16, 16, 16, 2, 0, 2)
            elif mob[2] == "mage":
                pyxel.blt(mob[0], mob[1], 0, 128, 16, 16, 16, 2, 0, 2)
    def update(self, frame):
        """Update the mobs"""
        # Clean up any removed mobs from direction dictionaries
        current_mobs = {id(mob) for mob in self.ennemis_liste}
        self.direction = {k: v for k, v in self.direction.items() if k in current_mobs}
        self.direction_timer = {k: v for k, v in self.direction_timer.items() if k in current_mobs}
        
        self.enemy_spawn()
        self.mob_movement()
        self.mob_frame = frame

MOBS = Mobs()

def demo():
    pyxel.init(256, 256, title="Mobs Demo", fps=30)
    pyxel.load("2.pyxres")
    pyxel.run(update, draw)

def update():
    frame = pyxel.frame_count
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    MOBS.update(frame)

def draw():
    pyxel.cls(0)
    MOBS.draw()