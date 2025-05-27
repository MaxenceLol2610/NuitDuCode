import pyxel

start = 0

def welcome():
    pyxel.cls(0)
    pyxel.text(90, 128, "Bienvenue sur Seldha", 11)
    if pyxel.btn(pyxel.KEY_H) == True:
        help()

def help():
    pyxel.cls(0)
    pyxel.text(10, 10, "Help: Use arrow keys to move", 7)
    pyxel.text(10, 20, "Press 'Q' to quit", 7)

def gameOver():
    pyxel.cls(0)
    pyxel.text(90, 128, "Game Over", 8)

def draw():
    pyxel.cls(0)
    if start == 0:
        welcome()
    elif start == -1:
        gameOver()