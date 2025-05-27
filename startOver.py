import pyxel

start = 0

def welcome():
    pyxel.cls(0)
    pyxel.text(90, 128, "Bienvenue sur Seldha", 11)
    pyxel.text(60, 138, "Appuyez sur <ESPACE> pour commencer", 11)
    pyxel.text(55, 148, "Appuyez sur <ESC> ou <Q> pour quitter", 11)

    if pyxel.btn(pyxel.KEY_H) == True:
        help()

def help():
    pyxel.cls(0)
    pyxel.text(10, 10, "Aide:", 15)
    pyxel.text(25, 20, "Utilisez les touches du pave directionels pour bouger", 7)
    pyxel.text(25, 35, "Appuyez sur 'J' pour attaquer", 7)
    pyxel.text(25, 50, "Appuyez sur 'U' pour ouvrir le magasin", 7)
    pyxel.text(25, 60, "Appuyez sur 'H' pour afficher cette aide", 7)
    pyxel.text(25, 65, "Appuyez sur 'Q' ou 'Echape' pour quitter le jeu", 7)

def gameOver():
    pyxel.cls(0)
    pyxel.text(110, 128, "Game Over", 8)

def draw():
    pyxel.cls(0)
    if start == 0:
        welcome()
    elif start == -1:
        gameOver()