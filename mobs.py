import pyxel
import player
import math
import random

Player = player.PLAYER

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
        self.last_attack = {}
        self.mage_projectiles = []
        self.attack_cooldowns = {
            "skeleton": 45,
            "mage": 90
        }
        self.attack_damages = {
            "skeleton": 10,
            "mage": 30
        }

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
                
                if player_health <= 10:  # Changed from 7 to 10
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
        for mob in self.ennemis_liste:
            if mob[3]<= 0:
                self.ennemis_liste.remove(mob)
    
    def enemy_damage(self):
        if Player.is_attacking:
            print("Player is attacking")
            for mob in self.ennemis_liste:
                dx_to_player = self.player_x - mob[0]
                dy_to_player = self.player_y - mob[1]
                if math.sqrt(dx_to_player*dx_to_player + dy_to_player*dy_to_player) < 64:
                    self.take_damage(mob)

    def take_damage(self, mob):
        mob[3] -= 10
        pyxel.blt(mob[0], mob[1], 0, 0, 96, 32, 16, 2, 0, 2)  # Flash effect on damage
        print("enemy damaged:", mob[2], "remaining health:", mob[3])

    def draw(self):
        for mob in self.ennemis_liste:
            if mob[2] == "skeleton":
                pyxel.blt(mob[0], mob[1], 0, 64, 16, 16, 16, 2, 0, 2)
            elif mob[2] == "mage":
                pyxel.blt(mob[0], mob[1], 0, 128, 16, 16, 16, 2, 0, 2)
        
        for proj in self.mage_projectiles:
            x, y, _, _, frame = proj
            u = frame * 16
            pyxel.blt(x, y, 0, 16, 80, 16, 16, 2, 0, 2)

    def update(self, frame):
        current_mobs = {id(mob) for mob in self.ennemis_liste}
        self.direction = {k: v for k, v in self.direction.items() if k in current_mobs}
        self.direction_timer = {k: v for k, v in self.direction_timer.items() if k in current_mobs}
        
        self.enemy_spawn()
        self.mob_movement()
        self.check_and_perform_attacks(frame)
        self.update_projectiles()
        self.ennemis_supression()
        self.enemy_damage()
        self.mob_frame = frame

    def check_and_perform_attacks(self, frame):
        for mob in self.ennemis_liste:
            mob_id = id(mob)
            x, y, mob_type, health = mob
            
            if mob_id not in self.last_attack:
                self.last_attack[mob_id] = 0
                
            if frame - self.last_attack[mob_id] < self.attack_cooldowns[mob_type]:
                continue
                
            dx = self.player_x - x
            dy = self.player_y - y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if mob_type == "skeleton" and distance <= 16:
                self.last_attack[mob_id] = frame
                Player.remove_health(self.attack_damages["skeleton"])
                
            elif mob_type == "mage" and distance <= 100:
                self.last_attack[mob_id] = frame
                norm = math.sqrt(dx*dx + dy*dy)
                if norm > 0:
                    dx = dx/norm * 2
                    dy = dy/norm * 2
                    self.mage_projectiles.append([x, y, dx, dy, 0])
                    
    def update_projectiles(self):
        for proj in self.mage_projectiles[:]:
            x, y, dx, dy, frame = proj
            proj[0] += dx
            proj[1] += dy
            proj[4] = (frame + 1) % 5
            
            dx_to_player = self.player_x - x
            dy_to_player = self.player_y - y
            if math.sqrt(dx_to_player*dx_to_player + dy_to_player*dy_to_player) < 16:
                Player.remove_health(self.attack_damages["mage"])
                self.mage_projectiles.remove(proj)
                continue
                
            if (x < 0 or x > 240 or y < 0 or y > 240):
                self.mage_projectiles.remove(proj)

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