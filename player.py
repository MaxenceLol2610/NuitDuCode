import math
import pyxel

UP,DOWN,LEFT,RIGHT = (pyxel.KEY_W, pyxel.KEY_S, pyxel.KEY_A, pyxel.KEY_D)
ATTACK_1, ATTACK_2 = (pyxel.KEY_J, pyxel.KEY_K)





class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.health = 100

    def move(self, direction, distance):
        if direction == UP:
            self.y -= distance
        elif direction == DOWN:
            self.y += distance
        elif direction == LEFT:
            self.x -= distance
        elif direction == RIGHT:
            self.x += distance
    
    def attack_1(self):
        # Placeholder for attack 1 logic
        # Animation of attack 1 and effect the mob
        # Melee attack
        print("Performing Attack 1")
    def attack_2(self):
        # Placeholder for attack 2 logic
        # Animation of attack 1 and effect the mob
        # Range attack
        print("Performing Attack 2")

    def controls(self):
        if pyxel.btn(UP):
            self.move(UP, 1)
        if pyxel.btn(DOWN):
            self.move(DOWN, 1)
        if pyxel.btn(LEFT):
            self.move(LEFT, 1)
        if pyxel.btn(RIGHT):
            self.move(RIGHT, 1)
        if pyxel.btn(ATTACK_1):
            print("Attack 1")
            self.attack_1()
        if pyxel.btn(ATTACK_2):
            print("Attack 2")
            self.attack_2()

    def get_position(self):
        return (self.x, self.y)

    def distance_to(self, other_player):
        return math.sqrt((self.x - other_player.x) ** 2 + (self.y - other_player.y) ** 2)
    
    def draw(self):
        pyxel.rect(self.x, self.y, 8, 8, 7) #place holder for player sprite
    
    def update(self):
        self.controls()

PLAYER = Player(128,128)

def demo():
    pyxel.init(256, 256, title="Seldha")
    pyxel.run(update,draw)

def update():
    PLAYER.controls()
    if pyxel.btn(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    PLAYER.draw()

