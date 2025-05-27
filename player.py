import math
import pyxel
import mobs
import startOver

UP,DOWN,LEFT,RIGHT = (pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_LEFT, pyxel.KEY_RIGHT)
ATTACK_1, ATTACK_2 = (pyxel.KEY_J, pyxel.KEY_K)

start_frame = 0;

class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.looking = RIGHT
        self.health = 100
        self.is_moving = False
        self.is_attacking = False
        self.coins = 0
        self.frame = 0
        self.speed = 1

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
        actual_distance = distance * self.speed
        if direction == UP:
            self.y -= actual_distance
        elif direction == DOWN:
            self.y += actual_distance
        elif direction == LEFT:
            self.x -= actual_distance
            self.looking = LEFT
        elif direction == RIGHT:
            self.x += actual_distance
            self.looking = RIGHT
        
        # Keep player within screen bounds
        self.x = max(0, min(self.x, 240))
        self.y = max(0, min(self.y, 240))
    
    def set_speed(self, level):
        # Speed increases by 0.5 per level, starting from base speed of 2
        self.speed = 2 + (level - 1) * 0.5

    def attack_1(self):
        self.is_attacking = True


    def controls(self):
        if pyxel.btn(UP):
            self.move(UP, 5)
        if pyxel.btn(DOWN):
            self.move(DOWN, 5)
        if pyxel.btn(LEFT):
            self.move(LEFT, 5)
        if pyxel.btn(RIGHT):
            self.move(RIGHT, 5)
        if pyxel.btnp(ATTACK_1,1,30):
            self.is_attacking = True
            self.attack_1()

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
        
        if self.is_attacking:
            attack_frame=self.frame
            global start_frame
            start_frame = pyxel.frame_count
            self.attack_animation(attack_frame)

    def animate(self):
        if self.looking == RIGHT:
            pyxel.blt(self.x, self.y, 0 , (self.frame%4)*16, 16, 16, 16, 2,0,2)
        if self.looking == LEFT:
            pyxel.blt(self.x, self.y, 0 , (self.frame%4)*16, 16, -16, 16, 2,0,2)
        
    def attack_animation(self,attack_frame):
        global start_frame
        if (start_frame-attack_frame) < 60:
            if self.looking == RIGHT:
                pyxel.blt(self.x+32, self.y, 0, 16, 64, 16, 16, 2, (attack_frame%4)*15, 2)
            if self.looking == LEFT:
                pyxel.blt(self.x-32, self.y, 0, 16, 64, -16, 16, 2, (attack_frame%4)*15, 2)
        self.is_attacking = False
    def check_if_moving(self):
        if pyxel.btn(UP) or pyxel.btn(DOWN) or pyxel.btn(LEFT) or pyxel.btn(RIGHT):
            self.is_moving = True
        else:
            self.is_moving = False

    def update(self,frame):
        self.frame = frame
        self.controls()
        self.check_if_moving()
        if self.health <= 0:
            print("Player is dead")
            startOver.start = -1
    
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
