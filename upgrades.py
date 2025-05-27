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
            
            # Apply the upgrade effects
            if item["name"] == "Speed":
                player.set_speed(item["level"])
            # Future upgrades for Health and Attack can be added here
            
            print(f"Purchased {item['name']} upgrade. New level: {item['level']}")
        else:
            print("Not enough coins or max level reached.")
    
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
        pyxel.text(window_x + 85, coin_box_y + 4, f"COINS: {player.get_coins()}", 7)
        
        item_start_y = coin_box_y + 25
        for i, item in enumerate(self.upgrade_items):
            y = item_start_y + i * 25
            
            if i == self.selected_item:
                highlight_height = 23
                pyxel.rect(
                    window_x + 10,
                    y -2,
                    200,
                    highlight_height,
                    1
                )
                pyxel.rectb(
                    window_x + 10,
                    y -2,
                    200,
                    highlight_height,
                    7 
                )
            
            color = 7 if i == self.selected_item else 0 
            max_level_text = f" (MAX)" if item["level"] == item["max_level"] else ""
            
            pyxel.text(window_x + 15, y + 2, f"{item['name']}", color)
            
            pyxel.text(window_x + 15, y + 9, f"Cost: {item['cost']}", 0)  # Black text
            
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