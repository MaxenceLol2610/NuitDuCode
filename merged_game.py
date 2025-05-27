import pyxel
import math
import random

# Player class
class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.looking = pyxel.KEY_RIGHT
        self.health = 100
        self.is_moving = False
        self.is_attacking = False
        self.coins = 0
        self.frame = 0
        self.speed = 1
        self.attack_cooldown = 0  # Number of frames left for attack to be active

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
        if direction == pyxel.KEY_UP:
            self.y -= actual_distance
        elif direction == pyxel.KEY_DOWN:
            self.y += actual_distance
        elif direction == pyxel.KEY_LEFT:
            self.x -= actual_distance
            self.looking = pyxel.KEY_LEFT
        elif direction == pyxel.KEY_RIGHT:
            self.x += actual_distance
            self.looking = pyxel.KEY_RIGHT

        self.x = max(0, min(self.x, 240))
        self.y = max(0, min(self.y, 240))

    def set_speed(self, level):
        self.speed = 2 + (level - 1) * 0.5

    def attack_1(self):
        self.is_attacking = True
        self.attack_cooldown = 8 

    def controls(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.move(pyxel.KEY_UP, 5)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.move(pyxel.KEY_DOWN, 5)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.move(pyxel.KEY_LEFT, 5)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.move(pyxel.KEY_RIGHT, 5)
        if pyxel.btnp(pyxel.KEY_J, 1, 30):
            self.is_attacking = True
            self.attack_1()

    def get_position(self):
        return (self.x, self.y)

    def distance_to(self, other_player):
        return math.sqrt((self.x - other_player.x) ** 2 + (self.y - other_player.y) ** 2)

    def draw(self):
        if self.is_moving:
            self.animate()
        else:
            if self.looking == pyxel.KEY_RIGHT:
                pyxel.blt(self.x, self.y, 0, 0, 16, 16, 16, 2, 0, 2)
            if self.looking == pyxel.KEY_LEFT:
                pyxel.blt(self.x, self.y, 0, 0, 16, -16, 16, 2, 0, 2)

        if self.is_attacking:
            attack_frame = self.frame
            self.attack_animation(attack_frame)

    def animate(self):
        if self.looking == pyxel.KEY_RIGHT:
            pyxel.blt(self.x, self.y, 0, (self.frame % 4) * 16, 16, 16, 16, 2, 0, 2)
        if self.looking == pyxel.KEY_LEFT:
            pyxel.blt(self.x, self.y, 0, (self.frame % 4) * 16, 16, -16, 16, 2, 0, 2)

    def attack_animation(self, attack_frame):
        if (start_frame - attack_frame) < 60:
            if self.looking == pyxel.KEY_RIGHT:
                pyxel.blt(self.x + 32, self.y, 0, 16, 64, 16, 16, 2, (attack_frame % 4) * 15, 2)
            if self.looking == pyxel.KEY_LEFT:
                pyxel.blt(self.x - 32, self.y, 0, 16, 64, -16, 16, 2, (attack_frame % 4) * 15, 2)
        self.is_attacking = False

    def check_if_moving(self):
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT):
            self.is_moving = True
        else:
            self.is_moving = False

    def update(self, frame):
        self.frame = frame
        self.controls()
        self.check_if_moving()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            self.is_attacking = True
        else:
            self.is_attacking = False
        if self.health <= 0:
            print("Player is dead")
            global start
            start = -1

PLAYER = Player(128, 128)
Player = PLAYER

# --- MOBS (from mobs.py) ---
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
                if player_health <= 10:
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
        for mob in self.ennemis_liste[:]:
            if mob[3] <= 0:
                self.ennemis_liste.remove(mob)

    def enemy_damage(self):
        if Player.is_attacking:
            for mob in self.ennemis_liste:
                dx_to_player = self.player_x - mob[0]
                dy_to_player = self.player_y - mob[1]
                if math.sqrt(dx_to_player*dx_to_player + dy_to_player*dy_to_player) < 64:
                    self.take_damage(mob)

    def take_damage(self, mob):
        mob[3] -= 10

    def draw(self):
        for mob in self.ennemis_liste:
            if mob[2] == "skeleton":
                pyxel.blt(mob[0], mob[1], 0, 64, 16, 16, 16, 2, 0, 2)
            elif mob[2] == "mage":
                pyxel.blt(mob[0], mob[1], 0, 128, 16, 16, 16, 2, 0, 2)
        for proj in self.mage_projectiles:
            x, y, _, _, frame = proj
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

# --- START OVER (from startOver.py) ---
start = 0

def welcome():
    pyxel.cls(0)
    pyxel.text(90, 128, "Bienvenue sur Seldha", 11)
    pyxel.text(60, 138, "Appuyez sur <ESPACE> pour commencer", 11)
    pyxel.text(55, 148, "Appuyez sur <ESC> ou <Q> pour quitter", 11)
    pyxel.text(55, 178, "Appuyez sur <H> pour afficher l'aide", 11)
    if pyxel.btn(pyxel.KEY_H):
        help_menu()

def help_menu():
    pyxel.cls(0)
    pyxel.text(10, 10, "Aide:", 15)
    pyxel.text(25, 20, "Utilisez les touches du pave directionels pour bouger", 7)
    pyxel.text(25, 35, "Appuyez sur 'J' pour attaquer", 7)
    pyxel.text(25, 50, "Appuyez sur 'U' pour ouvrir le magasin", 7)
    pyxel.text(25, 65, "Appuyez sur 'H' pour afficher cette aide", 7)
    pyxel.text(25, 80, "Appuyez sur 'Q' ou 'Echape' pour quitter le jeu", 7)

def gameOver():
    pyxel.cls(0)
    pyxel.text(110, 128, "Game Over", 8)

def startOver_draw():
    pyxel.cls(0)
    if start == 0:
        welcome()
    elif start == -1:
        gameOver()

# --- UPGRADES/SHOP (from upgrades.py) ---
class Shop:
    def __init__(self):
        self.visible = False
        self.selected_item = 0
        self.upgrade_items = [
            {"name": "Health", "cost": 100, "level": 1, "max_level": 5},
            {"name": "Attack", "cost": 150, "level": 1, "max_level": 3},
            {"name": "Speed", "cost": 200, "level": 1, "max_level": 4},
        ]
    def toggle_visibility(self):
        self.visible = not self.visible
    def update(self):
        if not self.visible:
            return
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_item = (self.selected_item - 1) % len(self.upgrade_items)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_item = (self.selected_item + 1) % len(self.upgrade_items)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.purchase_item()
    def purchase_item(self):
        item = self.upgrade_items[self.selected_item]
        if Player.get_coins() >= item["cost"] and item["level"] < item["max_level"]:
            Player.remove_coins(item["cost"])
            item["level"] += 1
            if item["name"] == "Speed":
                Player.set_speed(item["level"])
            # Add logic for Health/Attack upgrades if needed
        else:
            pass
    def draw(self):
        if not self.visible:
            return
        window_x = 10
        window_y = 10
        window_w = 220
        window_h = 140
        pyxel.rect(window_x + 4, window_y + 4, window_w, window_h, 0)
        pyxel.rect(window_x, window_y, window_w, window_h, 13)
        pyxel.rectb(window_x, window_y, window_w, window_h, 7)
        title_height = 24
        pyxel.rect(window_x, window_y, window_w, title_height, 12)
        pyxel.rectb(window_x, window_y, window_w, title_height, 7)
        title_text = "★ UPGRADES SHOP ★"
        text_x = window_x + (window_w - len(title_text) * 4) // 2
        pyxel.text(text_x, window_y + 8, title_text, 0)
        pyxel.text(text_x, window_y + 9, title_text, 7)
        tutorial_y = window_y + 26
        pyxel.text(window_x + 15, tutorial_y, "Press U to close shop", 0)
        coin_box_y = window_y + 35
        pyxel.rect(window_x + 65, coin_box_y, 120, 15, 4)
        pyxel.circ(window_x + 75, coin_box_y + 7, 4, 10)
        pyxel.text(window_x + 85, coin_box_y + 4, f"COINS: {Player.get_coins()}", 7)
        item_start_y = coin_box_y + 25
        for i, item in enumerate(self.upgrade_items):
            y = item_start_y + i * 25
            if i == self.selected_item:
                highlight_height = 23
                pyxel.rect(window_x + 10, y - 2, 200, highlight_height, 1)
                pyxel.rectb(window_x + 10, y - 2, 200, highlight_height, 7)
            color = 7 if i == self.selected_item else 0
            max_level_text = " (MAX)" if item["level"] == item["max_level"] else ""
            pyxel.text(window_x + 15, y + 2, f"{item['name']}", color)
            pyxel.text(window_x + 15, y + 9, f"Cost: {item['cost']}", 0)
            pyxel.text(window_x + 180, y + 5, f"Lv.{item['level']}{max_level_text}", color)
            bar_width = 80
            bar_x = window_x + 85
            bar_y = y + 5
            pyxel.rect(bar_x, bar_y, bar_width, 6, 5)
            progress = (item["level"] / item["max_level"]) * bar_width
            if progress > 0:
                pyxel.rect(bar_x, bar_y, int(progress), 6, 3)
            pyxel.rectb(bar_x, bar_y, bar_width, 6, 0)
            dot_y = y + 15
            for j in range(item["max_level"]):
                x = bar_x + j * 12
                if j < item["level"]:
                    pyxel.circ(x + 3, dot_y, 2, 8)
                    pyxel.circb(x + 3, dot_y, 2, 0)
                else:
                    pyxel.circb(x + 3, dot_y, 2, 0)
        pyxel.text(window_x + 60, window_y + window_h - 12, "↑↓: Select  ENTER: Buy", 0)

shop = Shop()

# --- INTERFACE (from interace.py) ---
def draw_heart(x, y, color, is_half=False):
    pyxel.circ(x, y+1, 2, color)
    pyxel.circ(x+4, y+1, 2, color)
    pyxel.tri(x-2, y+1, x+6, y+1, x+2, y+6, color)
    if is_half:
        pyxel.tri(x+2, y-1, x+2, y+6, x+6, y+1, 0)
        pyxel.tri(x+2, y-1, x+2, y+6, x+6, y+3, 0)

def draw_coin(x, y):
    pyxel.circ(x+4, y+4, 4, 10)
    pyxel.circ(x+4, y+4, 3, 9)

def draw_ui(player):
    health = player.get_health()
    full_hearts = health // 10
    has_half = health % 10 >= 5
    for i in range(full_hearts // 2):
        draw_heart(10 + (i * 12), 10, 8)
    if full_hearts % 2:
        draw_heart(10 + ((full_hearts // 2) * 12), 10, 8, True)
    draw_coin(10, 25)
    pyxel.text(22, 26, f"x{player.get_coins()}", 7)

# --- WORLD (from world.py) ---
loot_box = []

def world_draw_welcome():
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
        if self.loot == "Coin":
            pyxel.blt(self.x, self.y, 0, 32, 48, 16, 16, 2, 0, 2)
        elif self.loot == "Health":
            pyxel.blt(self.x, self.y, 0, 112, 48, 16, 16, 2, 0, 2)
    def check_collision(self, player):
        player_x, player_y = player.get_position()
        distance = math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
        if distance < 16:
            if self.loot == "Coin":
                player.add_coins(5)
            elif self.loot == "Health":
                player.add_health(20)
            return True
        return False

def gen_loot():
    loot_box.append(Loot(random.randint(0, 224), random.randint(0, 224)))

def world_update():
    frame = pyxel.frame_count
    # Always ensure at least one loot box exists
    if len(loot_box) == 0:
        gen_loot()
    # Spawn a new loot box every 300 frames (10 seconds at 30 FPS)
    if frame % 300 == 0:
        gen_loot()
    for loot in loot_box[:]:
        if loot.check_collision(Player):
            loot_box.remove(loot)

def world_draw():
    pyxel.cls(9)
    Player.draw()
    Mobs.draw()
    for loot in loot_box:
        loot.draw()
    draw_ui(Player)

# Main game logic
pyxel.init(256, 256, title="Seldha", fps=30)
pyxel.load("2.pyxres")
print("Game Started")

start_frame = 0

Player = PLAYER
Mobs = MOBS

# Update and draw functions
def update():
    frame = pyxel.frame_count
    Player.update(frame)
    Mobs.update(frame)
    if not pyxel.play_pos(0):
        pyxel.playm(0, loop=True)
    world_update()
    global start
    if start == 0 and pyxel.btnp(pyxel.KEY_SPACE):
        start = 1
        global start_frame
        start_frame = pyxel.frame_count
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnp(pyxel.KEY_U):
        shop.toggle_visibility()
    if shop.visible:
        shop.update()

def draw():
    pyxel.cls(0)
    frame = pyxel.frame_count
    global start
    if start == 0 or start == -1:
        startOver_draw()
    else:
        global start_frame
        if frame - start_frame < 60:
            world_draw_welcome()
        else:
            world_draw()
    shop.draw()

pyxel.run(update, draw)
