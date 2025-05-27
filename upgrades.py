import pyxel
import player
player = player.PLAYER
class Shop:
    def __init__ (self):
        self.visible = False
        self.selected_item = 0
        self.upgrade_items = [
            {"name": "Health", "cost": 100, "level": 1, "max_level": 5},
            {"name": "Attack", "cost": 150, "level": 1, "max_level": 3},
            {"name": "Speed", "cost": 200, "level": 1, "max_level": 4},
        ]
        coins = player.get_coins()
    
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
        if player.get_coins() >= item["cost"] and item["level"] < item["max_level"]:
            player.remove_coins(item["cost"])
            item["level"] += 1
            print(f"Purchased {item['name']} upgrade. New level: {item['level']}")
        else:
            print("Not enough coins or max level reached.")
    
    def draw(self):
        if not self.visible:
            return
    
        pyxel.rect(18, 18, 204, 104, 1) 
        pyxel.rect(16, 16, 204, 104, 5) 
        pyxel.rectb(16, 16, 204, 104, 7)
        pyxel.rectb(18, 18, 200, 100, 7)

        pyxel.rect(16, 16, 204, 15, 6)
        pyxel.text(85, 20, "★ UPGRADES SHOP ★", 7)
    
        pyxel.rect(75, 35, 100, 12, 13) 
        pyxel.circ(80, 41, 3, 10)
        pyxel.text(85, 38, f"COINS: {player.get_coins()}", 7)

        for i, item in enumerate(self.upgrade_items):
            y = 55 + i * 20  # Increased vertical spacing
            color = 10 if i == self.selected_item else 7
            max_level_text = f" (MAX)" if item["level"] == item["max_level"] else ""

            if i == self.selected_item:
                for offset in range(3):
                    pyxel.rect(20, y - 2 + offset, 196, 15 - offset*2, 8 + offset)

            pyxel.text(30, y, f"{item['name']}", color)
            pyxel.text(30, y + 6, f"Cost: {item['cost']}", 6)
        
            pyxel.text(180, y, f"Lv.{item['level']}{max_level_text}", color)

            bar_width = 60
            pyxel.rect(100, y + 2, bar_width, 4, 1)
            progress = (item["level"] / item["max_level"]) * bar_width
            if progress > 0:
                pyxel.rect(100, y + 2, int(progress), 4, 11)

            for j in range(item["max_level"]):
                x = 100 + j * 8
                if j < item["level"]:
                    pyxel.circ(x + 3, y + 8, 2, 10)
                    pyxel.circb(x + 3, y + 8, 2, 7)
                else:
                    pyxel.circb(x + 3, y + 8, 2, 5)

        # Draw controls help
        pyxel.text(20, 115, "↑↓: Select  ENTER: Buy", 6)

shop = Shop()