import pyxel

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnp(pyxel.KEY_R):
        pyxel.load("assets.pyxres")
        print("Assets reloaded")

def draw():
    pyxel.cls(0)
    pyxel.text(10, 10, "Press 'R' to reload assets", 7)
    pyxel.text(10, 20, "Press 'Q' to quit", 7)

def main():
    pyxel.init(160, 120, title="Asset Reload Example")
    pyxel.load("assets.pyxres")
    pyxel.run(update, draw)

if __name__ == "__main__":
    main()