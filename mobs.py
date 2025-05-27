import pyxel
import player
import math
import random

Player = player.PLAYER
player_health = Player.get_health()

class Mobs:
    def __init__(self):
        self.mob_speed = 1
        self.mob_spawn_rate = 30
        # initialisation of the ennemies
        self.ennemis_liste = []
        # Position of the player
        self.player_x = Player.get_position()[0]
        self.player_y = Player.get_position()[1]
        self.mob_frame = 0
        self.direction = 0  # Used for random movement of skeletons

    def mob_nature(self):
        """
        Gives a role to the mobs. 
        Can either be skeleton or mage. There is 25% chance for a mob to be a mage.
        """
        rnd_selector = random.randint(1, 10)
        if rnd_selector >= 2:
            return "skeleton"
        else:
            return "mage"

    def enemy_spawn(self):
        """Generates mobs in the game world.
        Takes in account the position of the player and the number of mobs already spawned."""
        # Check if the player is in the right position to spawn a mob
        if len(self.ennemis_liste) < 10:
            # Spawn a new mob at a random position
            x = pyxel.rndi(0, 224)
            y = pyxel.rndi(0, 224)
            n = self.mob_nature()
            if n == "skeleton":
                h= 40 # Health of the skeleton
            elif n == "mage":
                h = 20 # Health of the mage
            # Check if the mob is not too close to the player and not already spawned
            mob_exclusion_distance = 50
            mob_from_player = math.sqrt((self.player_x - x)**2+(self.player_y - y)**2)
            if [x, y, n, h] not in self.ennemis_liste and mob_from_player > mob_exclusion_distance:
                # Add the new mob to the list
                self.ennemis_liste.append([x ,y ,n, h])
    
    def mob_movement(self):
        """Defines the movement of the skeletons.
        Skeletons will move towards the player when it's health h is below 7.
        Mages will not move."""
        
        for mob in self.ennemis_liste:
            if mob[2] == "skeleton":
                if mob[3] < 7:
                    # Move towards the player
                    if mob[0] < self.player_x:
                        mob[0] += self.mob_speed
                    elif mob[0] > self.player_x:
                        mob[0]-= self.mob_speed
                    if mob[1] < self.player_y:
                        mob[1] += self.mob_speed
                    elif mob[1] > self.player_y:
                        mob[1] -= self.mob_speed
                else: 
                    # Move randomly
                    if self.mob_frame % 60 == 0:
                        self.direction += 1
                        print("direction change", self.direction)

                    if self.direction % 4 == 0:
                        mob[0] += self.mob_speed
                    elif self.direction % 4 == 1:
                        mob[1] -= self.mob_speed
                    elif self.direction % 4 == 2:
                        mob[0] -= self.mob_speed
                    elif self.direction % 4 == 3:
                        mob[1] += self.mob_speed

    def ennemis_supression(self):
        """Removes mobs that are dead"""
        pass

    def draw(self):
        for mob in self.ennemis_liste:
            if mob[2] == "skeleton":
                pyxel.blt(mob[0], mob[1], 0, 64, 16, 16, 16, 2,0,2)
            elif mob[2] == "mage":
                pyxel.blt(mob[0], mob[1], 0, 128, 16, 16, 16, 2,0,2)
    
    def update(self, frame):
        """Update the mobs"""
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

demo()