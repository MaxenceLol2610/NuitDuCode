import pyxel
import player

Player = player.PLAYER

def draw_welcome():
    pyxel.cls(0)
    pyxel.text(10, 10, "Welcome to the World of Seldha!", 7)
    pyxel.text(10, 20, "Explore and enjoy your adventure!", 7)
    pyxel.text(10, 30, "Press 'Q' to quit.", 7)

def draw():
    pyxel.cls(9)
    Player.draw()
    
"""
pyxel.init(256, 256, title="Seldha", fps=30)
def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
pyxel.run(update, draw_welcome)
"""

