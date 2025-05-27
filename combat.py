import pyxel
import player
import mobs


class combat:
    def __init__(self):
        self.player = player.PLAYER
        self.mobs = mobs.MOBS
        self.Phealth = self.player.get_health()
        self.ennemis_liste = self.mobs.ennemis_liste
    
    def player_attack(self):
        pass