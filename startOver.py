import pyxel

def welcome():
    pyxel.cls(0)
    pyxel.text(50, 50, "Bienvenue sur Seldha", 7)

def update():
    if pyxel.btnp(pyxel.KEY_SPACE):
        print("Game Started")
        pyxel.quit() 

def draw():
    pyxel.cls(0)
    welcome()