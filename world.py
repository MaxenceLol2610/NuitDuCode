import pyxel

def draw():
    world_frame = pyxel.frame_count
    if world_frame < 30*5:  # Show the welcome message for 5 seconds
        print("World Frame:", world_frame)
        pyxel.text(10, 10, "Welcome to the World of Seldha!", 7)
        pyxel.text(10, 20, "Explore and enjoy your adventure!", 7)
        pyxel.text(10, 30, "Press 'Q' to quit.", 7)

