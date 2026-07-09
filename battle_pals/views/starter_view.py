import raylib as rl
import random
import math
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_TYPE_FIRE, COLOR_TYPE_WATER, COLOR_TYPE_GRASS,
    COLOR_TYPE_NORMAL, COLOR_TYPE_ELECTRIC, COLOR_TYPE_ICE,
    COLOR_TYPE_EARTH, COLOR_TYPE_WIND, COLOR_TYPE_TOXIC,
    COLOR_TYPE_MIND, COLOR_TYPE_METAL, COLOR_TYPE_LIGHT,
    COLOR_TYPE_SHADOW
)
from battle_pals.models.species import SPECIES
from battle_pals.models.pal import Pal
from ai4animation import AI4Animation, Vector3

TYPE_COLORS = {
    "Fire": COLOR_TYPE_FIRE,
    "Water": COLOR_TYPE_WATER,
    "Grass": COLOR_TYPE_GRASS,
    "Normal": COLOR_TYPE_NORMAL,
    "Electric": COLOR_TYPE_ELECTRIC,
    "Ice": COLOR_TYPE_ICE,
    "Earth": COLOR_TYPE_EARTH,
    "Wind": COLOR_TYPE_WIND,
    "Toxic": COLOR_TYPE_TOXIC,
    "Mind": COLOR_TYPE_MIND,
    "Metal": COLOR_TYPE_METAL,
    "Light": COLOR_TYPE_LIGHT,
    "Shadow": COLOR_TYPE_SHADOW
}

def check_rect_collision(px, py, rx, ry, rw, rh):
    return rx <= px <= rx + rw and ry <= py <= ry + rh

class StarterView:
    def __init__(self):
        self.species_names = sorted(list(SPECIES.keys()))
        self.selected_index = 0
        self.scroll_offset = 0
        self.player_level = 5
        self.preview_pal = None
        self.select_species(self.selected_index)

    def select_species(self, idx):
        self.selected_index = idx
        name = self.species_names[idx]
        species = SPECIES[name]
        self.preview_pal = Pal(species, level=self.player_level, is_player=True)
        # Position at origin for 3D preview
        self.preview_pal.base_position = Vector3.Create(0.0, 0.8, 0.0)
        self.preview_pal.position = Vector3.Create(0.0, 0.8, 0.0)

    def set_level(self, val):
        self.player_level = max(1, min(100, val))
        if self.preview_pal:
            self.preview_pal.level = self.player_level
            # Recalculate stats
            self.preview_pal.max_hp = self.preview_pal.calculate_stat("hp")
            self.preview_pal.hp = self.preview_pal.max_hp
            self.preview_pal.base_attack = self.preview_pal.calculate_stat("attack")
            self.preview_pal.base_defense = self.preview_pal.calculate_stat("defense")
            self.preview_pal.base_speed = self.preview_pal.calculate_stat("speed")
            # Recalculate learnset moves
            self.preview_pal.learn_moves_for_level()

    def on_show_view(self):
        pass

    def on_update(self, dt):
        if self.preview_pal:
            self.preview_pal.update_animation(dt)

        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        mouse_pos = rl.GetMousePosition()
        mx, my = mouse_pos.x, mouse_pos.y

        # Handle mouse clicks
        if rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            # Left panel click detection (Species list)
            if check_rect_collision(mx, my, 40, 100, 280, 520):
                # Check Scroll Up
                if self.scroll_offset > 0 and check_rect_collision(mx, my, 40, 105, 280, 30):
                    self.scroll_offset -= 1
                # Check Scroll Down
                elif self.scroll_offset < len(self.species_names) - 10 and check_rect_collision(mx, my, 40, 585, 280, 30):
                    self.scroll_offset += 1
                # Check list items
                else:
                    for i in range(10):
                        item_y = 140 + i * 44
                        if check_rect_collision(mx, my, 40, item_y, 280, 40):
                            idx = self.scroll_offset + i
                            if idx < len(self.species_names):
                                self.select_species(idx)
                                break

            # Right panel click detection (Level / Stats / Start Battle)
            rx = sw - 360
            if check_rect_collision(mx, my, rx, 100, 320, 520):
                # Level buttons: [<<], [-], [+], [>>]
                # [<<] : x = rx + 10
                if check_rect_collision(mx, my, rx + 10, 150, 35, 35):
                    self.set_level(self.player_level - 10)
                # [-] : x = rx + 55
                elif check_rect_collision(mx, my, rx + 55, 150, 35, 35):
                    self.set_level(self.player_level - 1)
                # [+] : x = rx + 230
                elif check_rect_collision(mx, my, rx + 230, 150, 35, 35):
                    self.set_level(self.player_level + 1)
                # [>>] : x = rx + 275
                elif check_rect_collision(mx, my, rx + 275, 150, 35, 35):
                    self.set_level(self.player_level + 10)
                # Start Battle Button
                elif check_rect_collision(mx, my, rx + 20, 480, 280, 55):
                    # Player Pal is self.preview_pal
                    # Opponent Pal: random species, level close to player's level
                    opp_name = random.choice(self.species_names)
                    opp_species = SPECIES[opp_name]
                    opp_lvl = max(1, min(100, self.player_level + random.choice([-2, -1, 0, 1, 2])))
                    opponent_pal = Pal(opp_species, level=opp_lvl, is_player=False)

                    # Transition to BattleView
                    from battle_pals.views.battle_view import BattleView
                    from battle_pals.game import BattlePalsGame
                    BattlePalsGame.get_instance().switch_to_view(BattleView(self.preview_pal, opponent_pal))

    def on_draw(self):
        # Draw background arena floor in 3D scene space
        rl.DrawPlane([0.0, 0.0, 0.0], [30.0, 30.0], (28, 36, 24, 255))
        
        # Draw player preview Pal in 3D
        if self.preview_pal:
            # facing = 1.0 (looking at camera), scale = 1.2
            self.preview_pal.draw_3d(1.0, 1.2)

    def on_gui(self):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        mouse_pos = rl.GetMousePosition()
        mx, my = mouse_pos.x, mouse_pos.y

        # Header Title
        AI4Animation.Draw.Text("BATTLE ARENA SETUP", 0.5, 0.06, 0.035, COLOR_TEXT_PRIMARY, 0.5)
        AI4Animation.Draw.Text("Select your specimen, customize its level, and prepare to duel", 0.5, 0.11, 0.018, COLOR_TEXT_MUTED, 0.5)

        # ---------------- Left Panel: Species List ----------------
        rl.DrawRectangle(40, 100, 280, 520, COLOR_BG_PANEL)
        rl.DrawRectangleLinesEx([40, 100, 280, 520], 2, COLOR_BORDER)
        
        # Scroll Up
        if self.scroll_offset > 0:
            up_hover = check_rect_collision(mx, my, 40, 105, 280, 30)
            up_color = (60, 75, 100, 255) if up_hover else (45, 52, 68, 255)
            rl.DrawRectangle(40, 105, 280, 30, up_color)
            rl.DrawRectangleLinesEx([40, 105, 280, 30], 1, COLOR_BORDER)
            AI4Animation.Draw.Text("▲ Scroll Up ▲", (40 + 140) / sw, (105 + 15) / sh, 0.016, COLOR_TEXT_PRIMARY, 0.5)
            
        # Visible list
        for i in range(10):
            idx = self.scroll_offset + i
            if idx >= len(self.species_names):
                break
            name = self.species_names[idx]
            item_y = 140 + i * 44
            
            is_selected = (idx == self.selected_index)
            is_hover = check_rect_collision(mx, my, 40, item_y, 280, 40)
            
            # Panel color
            if is_selected:
                bg_col = (56, 120, 220, 255)
                border_col = (100, 180, 255, 255)
            elif is_hover:
                bg_col = (50, 60, 80, 255)
                border_col = COLOR_BORDER
            else:
                bg_col = (28, 32, 42, 255)
                border_col = (40, 48, 64, 255)
                
            rl.DrawRectangle(40, item_y, 280, 40, bg_col)
            rl.DrawRectangleLinesEx([40, item_y, 280, 40], 1, border_col)
            
            # Species name text
            txt_color = COLOR_TEXT_PRIMARY if (is_selected or is_hover) else COLOR_TEXT_MUTED
            AI4Animation.Draw.Text(name, (40 + 20) / sw, (item_y + 20) / sh, 0.018, txt_color, 0.0)

        # Scroll Down
        if self.scroll_offset < len(self.species_names) - 10:
            down_hover = check_rect_collision(mx, my, 40, 585, 280, 30)
            down_color = (60, 75, 100, 255) if down_hover else (45, 52, 68, 255)
            rl.DrawRectangle(40, 585, 280, 30, down_color)
            rl.DrawRectangleLinesEx([40, 585, 280, 30], 1, COLOR_BORDER)
            AI4Animation.Draw.Text("▼ Scroll Down ▼", (40 + 140) / sw, (585 + 15) / sh, 0.016, COLOR_TEXT_PRIMARY, 0.5)

        # ---------------- Right Panel: Specimen Details ----------------
        rx = sw - 360
        rl.DrawRectangle(rx, 100, 320, 520, COLOR_BG_PANEL)
        rl.DrawRectangleLinesEx([rx, 100, 320, 520], 2, COLOR_BORDER)

        # 1. Level Adjustments
        # Title
        AI4Animation.Draw.Text("TRAINING LEVEL", (rx + 160) / sw, 125 / sh, 0.018, COLOR_TEXT_MUTED, 0.5)
        # Level text
        AI4Animation.Draw.Text(f"Lv. {self.player_level}", (rx + 160) / sw, 168 / sh, 0.024, COLOR_TEXT_PRIMARY, 0.5)
        
        # Level buttons
        # [<<] Button
        b1_hover = check_rect_collision(mx, my, rx + 10, 150, 35, 35)
        b1_col = (70, 80, 95, 255) if b1_hover else (48, 56, 70, 255)
        rl.DrawRectangle(rx + 10, 150, 35, 35, b1_col)
        rl.DrawRectangleLinesEx([rx + 10, 150, 35, 35], 1, COLOR_BORDER)
        AI4Animation.Draw.Text("-10", (rx + 27) / sw, 168 / sh, 0.014, COLOR_TEXT_PRIMARY, 0.5)

        # [-] Button
        b2_hover = check_rect_collision(mx, my, rx + 55, 150, 35, 35)
        b2_col = (70, 80, 95, 255) if b2_hover else (48, 56, 70, 255)
        rl.DrawRectangle(rx + 55, 150, 35, 35, b2_col)
        rl.DrawRectangleLinesEx([rx + 55, 150, 35, 35], 1, COLOR_BORDER)
        AI4Animation.Draw.Text("-1", (rx + 72) / sw, 168 / sh, 0.015, COLOR_TEXT_PRIMARY, 0.5)

        # [+] Button
        b3_hover = check_rect_collision(mx, my, rx + 230, 150, 35, 35)
        b3_col = (70, 80, 95, 255) if b3_hover else (48, 56, 70, 255)
        rl.DrawRectangle(rx + 230, 150, 35, 35, b3_col)
        rl.DrawRectangleLinesEx([rx + 230, 150, 35, 35], 1, COLOR_BORDER)
        AI4Animation.Draw.Text("+1", (rx + 247) / sw, 168 / sh, 0.015, COLOR_TEXT_PRIMARY, 0.5)

        # [>>] Button
        b4_hover = check_rect_collision(mx, my, rx + 275, 150, 35, 35)
        b4_col = (70, 80, 95, 255) if b4_hover else (48, 56, 70, 255)
        rl.DrawRectangle(rx + 275, 150, 35, 35, b4_col)
        rl.DrawRectangleLinesEx([rx + 275, 150, 35, 35], 1, COLOR_BORDER)
        AI4Animation.Draw.Text("+10", (rx + 292) / sw, 168 / sh, 0.014, COLOR_TEXT_PRIMARY, 0.5)

        # Divider
        rl.DrawLineEx([rx + 20, 205], [rx + 300, 205], 1, COLOR_BORDER)

        # 2. Specimen metadata info
        species_name = self.species_names[self.selected_index]
        species = SPECIES[species_name]
        
        # Draw Type tags
        AI4Animation.Draw.Text("ELEMENTAL TYPE", (rx + 160) / sw, 222 / sh, 0.014, COLOR_TEXT_MUTED, 0.5)
        
        # Horizontal layout for type pills
        type_y = 232
        pills_w = 90
        pills_h = 24
        
        if len(species.types) == 1:
            t = species.types[0]
            col = TYPE_COLORS.get(t, COLOR_BORDER)
            p_x = rx + 160 - pills_w / 2
            rl.DrawRectangle(int(p_x), type_y, pills_w, pills_h, col)
            rl.DrawRectangleLinesEx([p_x, type_y, pills_w, pills_h], 1, COLOR_TEXT_PRIMARY)
            AI4Animation.Draw.Text(t.upper(), (p_x + pills_w / 2) / sw, (type_y + pills_h / 2) / sh, 0.014, COLOR_TEXT_PRIMARY, 0.5)
        else:
            t1, t2 = species.types[0], species.types[1]
            c1 = TYPE_COLORS.get(t1, COLOR_BORDER)
            c2 = TYPE_COLORS.get(t2, COLOR_BORDER)
            
            p1_x = rx + 160 - pills_w - 5
            rl.DrawRectangle(int(p1_x), type_y, pills_w, pills_h, c1)
            rl.DrawRectangleLinesEx([p1_x, type_y, pills_w, pills_h], 1, COLOR_TEXT_PRIMARY)
            AI4Animation.Draw.Text(t1.upper(), (p1_x + pills_w / 2) / sw, (type_y + pills_h / 2) / sh, 0.014, COLOR_TEXT_PRIMARY, 0.5)
            
            p2_x = rx + 160 + 5
            rl.DrawRectangle(int(p2_x), type_y, pills_w, pills_h, c2)
            rl.DrawRectangleLinesEx([p2_x, type_y, pills_w, pills_h], 1, COLOR_TEXT_PRIMARY)
            AI4Animation.Draw.Text(t2.upper(), (p2_x + pills_w / 2) / sw, (type_y + pills_h / 2) / sh, 0.014, COLOR_TEXT_PRIMARY, 0.5)

        # 3. Trait
        trait_desc = {
            "Clear Body": "Immune to enemy stat drops.",
            "Chlorophyll": "Boosts Speed in battle 1.5x.",
            "Overgrow": "Grass power boosted 1.5x at low HP.",
            "Blaze": "Fire power boosted 1.5x at low HP.",
            "Torrent": "Water power boosted 1.5x at low HP."
        }.get(species.trait, "No special effect.")
        
        AI4Animation.Draw.Text("BATTLE PASSIVE TRAIT", (rx + 160) / sw, 275 / sh, 0.014, COLOR_TEXT_MUTED, 0.5)
        AI4Animation.Draw.Text(f"{species.trait}", (rx + 160) / sw, 295 / sh, 0.018, COLOR_TYPE_ELECTRIC, 0.5)
        AI4Animation.Draw.Text(trait_desc, (rx + 160) / sw, 315 / sh, 0.013, COLOR_TEXT_MUTED, 0.5)

        # Divider
        rl.DrawLineEx([rx + 20, 335], [rx + 300, 335], 1, COLOR_BORDER)

        # 4. Stats chart
        AI4Animation.Draw.Text("BASE SPECIES STATS", (rx + 160) / sw, 350 / sh, 0.014, COLOR_TEXT_MUTED, 0.5)

        stats_keys = [
            ("HP", "hp", (230, 90, 80, 255)),
            ("ATK", "attack", (240, 160, 80, 255)),
            ("DEF", "defense", (80, 200, 120, 255)),
            ("SPD", "speed", (100, 170, 240, 255))
        ]

        for idx, (label, stat_key, color) in enumerate(stats_keys):
            y_pos = 370 + idx * 24
            base_val = species.base_stats.get(stat_key, 50)
            
            # Label
            AI4Animation.Draw.Text(label, (rx + 20) / sw, (y_pos + 10) / sh, 0.014, COLOR_TEXT_PRIMARY, 0.0)
            # Value
            AI4Animation.Draw.Text(str(base_val), (rx + 65) / sw, (y_pos + 10) / sh, 0.014, COLOR_TEXT_MUTED, 0.0)
            
            # Bar Track
            rl.DrawRectangle(rx + 100, y_pos + 3, 200, 12, (28, 32, 42, 255))
            # Bar Fill
            fill_w = int(200 * (base_val / 150.0))
            fill_w = max(4, min(200, fill_w))
            rl.DrawRectangle(rx + 100, y_pos + 3, fill_w, 12, color)

        # Divider
        rl.DrawLineEx([rx + 20, 465], [rx + 300, 465], 1, COLOR_BORDER)

        # 5. Start Battle Button
        sb_hover = check_rect_collision(mx, my, rx + 20, 480, 280, 55)
        sb_bg = (235, 94, 85, 255) if sb_hover else (180, 60, 55, 255)
        rl.DrawRectangle(rx + 20, 480, 280, 55, sb_bg)
        rl.DrawRectangleLinesEx([rx + 20, 480, 280, 55], 2, COLOR_TEXT_PRIMARY)
        AI4Animation.Draw.Text("ENTER ARENA", (rx + 160) / sw, 508 / sh, 0.024, COLOR_TEXT_PRIMARY, 0.5)
