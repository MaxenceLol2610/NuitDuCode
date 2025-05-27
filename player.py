import math
import pyxel

UP,DOWN,LEFT,RIGHT = (pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_LEFT, pyxel.KEY_RIGHT)
ATTACK_1, ATTACK_2 = (pyxel.KEY_J, pyxel.KEY_K)


class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.looking = RIGHT
        self.health = 100
        self.is_moving = False
        self.coins = 0
        self.frame = 0

    def add_coins(self, amount):
        self.coins += amount
    def remove_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
    def get_coins(self):
        return self.coins

    def add_health(self, amount):
        self.health += amount
    def remove_health(self, amount):
        if self.health >= amount:
            self.health -= amount
    def get_health(self):
        return self.health

    def move(self, direction, distance):
        if direction == UP:
            self.y -= distance
        elif direction == DOWN:
            self.y += distance
        elif direction == LEFT:
            self.x -= distance
            self.looking = LEFT
        elif direction == RIGHT:
            self.x += distance
            self.looking = RIGHT
    
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
            self.move(UP, 5)
        if pyxel.btn(DOWN):
            self.move(DOWN, 5)
        if pyxel.btn(LEFT):
            self.move(LEFT, 5)
        if pyxel.btn(RIGHT):
            self.move(RIGHT, 5)
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
        #pyxel.rect(self.x, self.y, 8, 8, 7) #place holder for player sprite
        
        if self.is_moving:
            self.animate()
        else:
            if self.looking == RIGHT:
                pyxel.blt(self.x, self.y, 0, 0, 16, 16, 16, 2,0,2)
            if self.looking == LEFT:
                pyxel.blt(self.x, self.y, 0, 0, 16, -16, 16, 2,0,2)

    def animate(self):
        
        if self.looking == RIGHT:
            pyxel.blt(self.x, self.y, 0 , self.frame*16, 16, 16, 16, 2,0,2)
        if self.looking == LEFT:
            pyxel.blt(self.x, self.y, 0 , self.frame*16, 16, -16, 16, 2,0,2)
        print(self.frame)

    def check_if_moving(self):
        if pyxel.btn(UP) or pyxel.btn(DOWN) or pyxel.btn(LEFT) or pyxel.btn(RIGHT):
            self.is_moving = True
        else:
            self.is_moving = False

    def update(self,frame):
        self.frame = frame % 4
        self.controls()
        self.check_if_moving()
    
PLAYER = Player(128,128)

def demo():
    print("Game Started")
    pyxel.init(256, 256, title="Seldha")
    pyxel.load("2.pyxres")
    pyxel.run(update,draw)
    

def update():
    frame = pyxel.frame_count
    PLAYER.update(frame)
    if pyxel.btn(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    PLAYER.draw()
