import pyxel

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