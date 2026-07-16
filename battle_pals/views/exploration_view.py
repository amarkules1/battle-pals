import raylib as rl
import random
import math
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_HP_GREEN, COLOR_HP_YELLOW, COLOR_HP_RED, COLOR_HP_BG,
    COLOR_TYPE_FIRE, COLOR_TYPE_WATER, COLOR_TYPE_GRASS, COLOR_TYPE_NORMAL,
    COLOR_TYPE_ELECTRIC, COLOR_TYPE_ICE, COLOR_TYPE_EARTH, COLOR_TYPE_WIND,
    COLOR_TYPE_TOXIC, COLOR_TYPE_MIND, COLOR_TYPE_METAL, COLOR_TYPE_LIGHT,
    COLOR_TYPE_SHADOW
)
from battle_pals.models.state import GameState, PRECINCTS
from battle_pals.models.pal import Pal
from ai4animation import AI4Animation, Vector3

TYPE_COLORS = {
    "Normal": COLOR_TYPE_NORMAL,
    "Fire": COLOR_TYPE_FIRE,
    "Water": COLOR_TYPE_WATER,
    "Grass": COLOR_TYPE_GRASS,
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

class ExplorationView:
    def __init__(self):
        self.state = GameState.get_instance()
        self.active_panel = "main"  # "main", "lab", "shop", "storage", "travel", "paldex"
        self.current_wild_preview = None
        self.preview_timer = 0.0
        
        # UI selection indices
        self.selected_party_idx = -1
        self.selected_box_idx = -1
        self.box_scroll = 0
        self.paldex_detail_idx = 0  # Party Pal index details
        self.status_msg = ""
        self.status_timer = 0.0

        self.spawn_wild_preview()

    def spawn_wild_preview(self):
        precinct = PRECINCTS[self.state.current_precinct]
        wild_species = random.choice(precinct["wilds"])
        avg_level = max(1, sum(p.level for p in self.state.party) // len(self.state.party))
        self.current_wild_preview = Pal(wild_species, level=avg_level, is_player=False)
        self.current_wild_preview.base_position = Vector3.Create(0.0, 0.8, 0.0)
        self.current_wild_preview.position = Vector3.Create(0.0, 0.8, 0.0)

    def set_status(self, msg):
        self.status_msg = msg
        self.status_timer = 3.0

    def on_show_view(self):
        self.spawn_wild_preview()
        self.selected_party_idx = -1
        self.selected_box_idx = -1

    def on_update(self, dt):
        if self.current_wild_preview:
            self.current_wild_preview.update_animation(dt)
        
        if self.status_timer > 0.0:
            self.status_timer -= dt
            if self.status_timer <= 0.0:
                self.status_msg = ""

        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        mouse_pos = rl.GetMousePosition()
        mx, my = mouse_pos.x, mouse_pos.y

        # Handle keyboard scroll for lists
        if self.active_panel == "storage":
            wheel = rl.GetMouseWheelMove()
            if wheel != 0:
                self.box_scroll = max(0, min(max(0, len(self.state.box) - 6), self.box_scroll - int(wheel)))

        if rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            # Left panel coordinates
            lx, ly, lw, lh = 50, 120, 300, sh - 200
            
            # --- MAIN PANEL ---
            if self.active_panel == "main":
                # Button 1: Explore Wilds (y = 140)
                if check_rect_collision(mx, my, lx + 20, 150, lw - 40, 50):
                    # Check if all party members are fainted
                    if all(p.hp <= 0 for p in self.state.party):
                        self.set_status("All your Pals are fainted! Heal at the Lab.")
                    else:
                        precinct = PRECINCTS[self.state.current_precinct]
                        wild_species = random.choice(precinct["wilds"])
                        avg_level = sum(p.level for p in self.state.party) // len(self.state.party)
                        opp_lvl = max(1, min(100, avg_level + random.choice([-2, -1, 0, 1, 2])))
                        wild_opponent = Pal(wild_species, level=opp_lvl, is_player=False)
                        
                        from battle_pals.views.battle_view import BattleView
                        from battle_pals.game import BattlePalsGame
                        BattlePalsGame.get_instance().switch_to_view(BattleView(self.state.party, wild_opponent, mode="WILD"))

                # Button 2: Challenge Bureaucrat Gate (y = 220)
                elif check_rect_collision(mx, my, lx + 20, 220, lw - 40, 50):
                    if self.state.current_precinct in self.state.defeated_bureaucrats:
                        self.set_status("You already defeated this precinct's Bureaucrat!")
                    elif all(p.hp <= 0 for p in self.state.party):
                        self.set_status("All your Pals are fainted! Heal at the Lab.")
                    else:
                        # Start boss fight
                        precinct = PRECINCTS[self.state.current_precinct]
                        boss_team_specs = [Pal(name, level=lvl, is_player=False) for name, lvl in precinct["boss_team"]]
                        
                        from battle_pals.views.battle_view import BattleView
                        from battle_pals.game import BattlePalsGame
                        BattlePalsGame.get_instance().switch_to_view(BattleView(self.state.party, boss_team_specs, mode="BOSS"))

                # Button 3: Visit Lab (y = 290)
                elif check_rect_collision(mx, my, lx + 20, 290, lw - 40, 50):
                    self.active_panel = "lab"

                # Button 4: Travel Gates (y = 360)
                elif check_rect_collision(mx, my, lx + 20, 360, lw - 40, 50):
                    self.active_panel = "travel"

                # Button 5: View Party & Paldex (y = 430)
                elif check_rect_collision(mx, my, lx + 20, 430, lw - 40, 50):
                    self.active_panel = "paldex"
                    self.paldex_detail_idx = 0

            # --- LAB MENU ---
            elif self.active_panel == "lab":
                # Heal clinic (y = 150)
                if check_rect_collision(mx, my, lx + 20, 150, lw - 40, 50):
                    self.state.heal_all_pals()
                    self.set_status("All your Pals have been fully healed!")
                
                # Swap Pal Storage Box (y = 220)
                elif check_rect_collision(mx, my, lx + 20, 220, lw - 40, 50):
                    self.active_panel = "storage"
                    self.selected_party_idx = -1
                    self.selected_box_idx = -1
                    self.box_scroll = 0

                # Black-Market Shop (y = 290)
                elif check_rect_collision(mx, my, lx + 20, 290, lw - 40, 50):
                    self.active_panel = "shop"

                # Back (y = 360)
                elif check_rect_collision(mx, my, lx + 20, 360, lw - 40, 50):
                    self.active_panel = "main"

            # --- SHOP MENU ---
            elif self.active_panel == "shop":
                # Buy Basic (100 RP) (y=150)
                if check_rect_collision(mx, my, lx + 20, 150, lw - 40, 50):
                    if self.state.research_points >= 100:
                        self.state.research_points -= 100
                        self.state.inventory["Basic Cube"] += 1
                        self.set_status("Bought 1 Basic Capture Cube!")
                    else:
                        self.set_status("Not enough RP!")

                # Buy Mega (250 RP) (y=220)
                elif check_rect_collision(mx, my, lx + 20, 220, lw - 40, 50):
                    if self.state.research_points >= 250:
                        self.state.research_points -= 250
                        self.state.inventory["Mega Cube"] += 1
                        self.set_status("Bought 1 Mega Capture Cube!")
                    else:
                        self.set_status("Not enough RP!")

                # Buy Ultra (500 RP) (y=290)
                elif check_rect_collision(mx, my, lx + 20, 290, lw - 40, 50):
                    if self.state.research_points >= 500:
                        self.state.research_points -= 500
                        self.state.inventory["Ultra Cube"] += 1
                        self.set_status("Bought 1 Ultra Capture Cube!")
                    else:
                        self.set_status("Not enough RP!")

                # Back to Lab (y = 360)
                elif check_rect_collision(mx, my, lx + 20, 360, lw - 40, 50):
                    self.active_panel = "lab"

            # --- STORAGE SWAP PANEL ---
            elif self.active_panel == "storage":
                rx = sw - 860
                
                # Check Party column selection (left side of storage panel)
                for i in range(10):
                    item_y = 150 + i * 44
                    if check_rect_collision(mx, my, rx + 20, item_y, 380, 38):
                        if i < len(self.state.party):
                            self.selected_party_idx = i
                            # Auto-perform swap if box is also selected
                            self.perform_storage_swap()
                        break
                
                # Check Box column selection (right side of storage panel)
                for i in range(6):
                    item_y = 150 + i * 50
                    if check_rect_collision(mx, my, rx + 440, item_y, 380, 44):
                        box_idx = self.box_scroll + i
                        if box_idx < len(self.state.box):
                            self.selected_box_idx = box_idx
                            self.perform_storage_swap()
                        break

                # Box scroll buttons
                if check_rect_collision(mx, my, rx + 440, 470, 180, 35):
                    self.box_scroll = max(0, self.box_scroll - 1)
                elif check_rect_collision(mx, my, rx + 640, 470, 180, 35):
                    self.box_scroll = min(max(0, len(self.state.box) - 6), self.box_scroll + 1)

                # Return to Lab Button
                if check_rect_collision(mx, my, sw // 2 - 100, sh - 100, 200, 45):
                    self.active_panel = "lab"
                    self.selected_party_idx = -1
                    self.selected_box_idx = -1

            # --- FAST TRAVEL PANEL ---
            elif self.active_panel == "travel":
                # Check precinct selection grid
                rx = sw - 860
                grid_w, grid_h = 240, 60
                
                for idx, p in enumerate(PRECINCTS):
                    row = idx // 3
                    col = idx % 3
                    bx = rx + 30 + col * 260
                    by = 160 + row * 80
                    
                    if check_rect_collision(mx, my, bx, by, grid_w, grid_h):
                        if idx in self.state.unlocked_precincts:
                            self.state.current_precinct = idx
                            self.spawn_wild_preview()
                            self.set_status(f"Fast-traveled to {p['name']}!")
                            self.active_panel = "main"
                        else:
                            self.set_status("Precinct Locked! Defeat previous Bureaucrats.")
                        break

                # Close travel (y = sh - 100)
                if check_rect_collision(mx, my, sw // 2 - 100, sh - 100, 200, 45):
                    self.active_panel = "main"

            # --- PARTY & PALDEX DETAIL VIEW ---
            elif self.active_panel == "paldex":
                # Check party list selection (left column)
                rx = sw - 860
                for i in range(10):
                    item_y = 150 + i * 44
                    if check_rect_collision(mx, my, rx + 20, item_y, 380, 38):
                        if i < len(self.state.party):
                            self.paldex_detail_idx = i
                        break

                # Close paldex details
                if check_rect_collision(mx, my, sw // 2 - 100, sh - 100, 200, 45):
                    self.active_panel = "main"

    def perform_storage_swap(self):
        """Swaps the selected Party Pal and Box Pal. Enables moving/depositing."""
        if self.selected_party_idx != -1 and self.selected_box_idx != -1:
            party_pal = self.state.party[self.selected_party_idx]
            box_pal = self.state.box[self.selected_box_idx]
            
            # Swapping
            self.state.party[self.selected_party_idx] = box_pal
            self.state.box[self.selected_box_idx] = party_pal
            
            self.set_status(f"Swapped {party_pal.name} with {box_pal.name}!")
            self.selected_party_idx = -1
            self.selected_box_idx = -1
        elif self.selected_party_idx != -1 and self.selected_box_idx == -1 and len(self.state.party) > 1:
            # Let player deposit to box directly if double clicked or click deposit button
            pass

    def on_draw(self):
        # Draw 3D floor grid space
        rl.DrawPlane([0.0, 0.0, 0.0], [30.0, 30.0], (20, 26, 38, 255))
        
        # Renders the spinning wild Pal model backdrop (only in Main explore and Travel mode)
        if self.current_wild_preview and self.active_panel in ["main", "travel"]:
            facing = math.sin(self.current_wild_preview.time * 0.6)
            self.current_wild_preview.draw_3d(facing, 1.25)

    def on_gui(self):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        precinct = PRECINCTS[self.state.current_precinct]

        # ----------------- HUD HEADER PANEL -----------------
        rl.DrawRectangle(0, 0, sw, 80, COLOR_BG_PANEL)
        rl.DrawLine(0, 80, sw, 80, COLOR_BORDER)
        
        gender_symbol = "♂" if self.state.player_gender == "Boy" else "♀"
        gender_col = COLOR_TYPE_WATER if self.state.player_gender == "Boy" else COLOR_TYPE_FIRE
        
        # Player Info
        AI4Animation.Draw.Text(f"Researcher {self.state.player_name}", 0.03, 0.02, 0.024, COLOR_TEXT_PRIMARY)
        AI4Animation.Draw.Text(gender_symbol, 0.18, 0.02, 0.024, gender_col)
        AI4Animation.Draw.Text(f"Licence Clearance: Rank {len(self.state.defeated_bureaucrats) + 1}", 0.03, 0.065, 0.015, COLOR_TEXT_MUTED)

        # Precinct Details
        AI4Animation.Draw.Text(f"Precinct {self.state.current_precinct + 1}: {precinct['name']}", 0.5, 0.02, 0.026, COLOR_TEXT_PRIMARY, 0.5)
        AI4Animation.Draw.Text(precinct["env"], 0.5, 0.065, 0.016, COLOR_TEXT_MUTED, 0.5)

        # Inventory details
        AI4Animation.Draw.Text(f"{self.state.research_points} RP", 0.85, 0.02, 0.022, COLOR_TEXT_PRIMARY, 1.0)
        AI4Animation.Draw.Text(f"Party: {len(self.state.party)}/10  |  Cubes: {self.state.inventory['Basic Cube']}/{self.state.inventory['Mega Cube']}/{self.state.inventory['Ultra Cube']}", 0.97, 0.065, 0.015, COLOR_TEXT_MUTED, 1.0)

        # Status Message Banner
        if len(self.status_msg) > 0:
            rl.DrawRectangle(sw // 2 - 250, sh - 145, 500, 36, (231, 76, 60, 200) if "not" in self.status_msg.lower() or "fainted" in self.status_msg.lower() else (46, 204, 113, 200))
            AI4Animation.Draw.Text(self.status_msg, 0.5, (sh - 135) / sh, 0.016, COLOR_TEXT_PRIMARY, 0.5)

        # ----------------- LEFT ACTION PANEL -----------------
        lx, ly, lw, lh = 50, 120, 300, sh - 200
        rl.DrawRectangle(lx, ly, lw, lh, COLOR_BG_PANEL)
        rl.DrawRectangleLines(lx, ly, lw, lh, COLOR_BORDER)

        if self.active_panel == "main":
            self.draw_main_panel(lx, ly, lw, lh, sw, sh)
        elif self.active_panel == "lab":
            self.draw_lab_panel(lx, ly, lw, lh, sw, sh)
        elif self.active_panel == "shop":
            self.draw_shop_panel(lx, ly, lw, lh, sw, sh)

        # ----------------- OVERLAY DETAILS PANEL (RIGHT SIDE) -----------------
        if self.active_panel not in ["main", "lab", "shop"]:
            rx, ry, rw, rh = sw - 860, 120, 810, sh - 200
            rl.DrawRectangle(rx, ry, rw, rh, COLOR_BG_PANEL)
            rl.DrawRectangleLines(rx, ry, rw, rh, COLOR_BORDER)
            
            if self.active_panel == "storage":
                self.draw_storage_panel(rx, ry, rw, rh, sw, sh)
            elif self.active_panel == "travel":
                self.draw_travel_panel(rx, ry, rw, rh, sw, sh)
            elif self.active_panel == "paldex":
                self.draw_paldex_panel(rx, ry, rw, rh, sw, sh)

    def draw_main_panel(self, lx, ly, lw, lh, sw, sh):
        AI4Animation.Draw.Text("PREVAILING ACTIONS", (lx + 20) / sw, (ly + 15) / sh, 0.016, COLOR_TEXT_MUTED)
        
        # Buttons (y coordinates: 150, 220, 290, 360, 430)
        labels = [
            ("Explore Wilds", 150),
            ("Challenge Bureaucrat", 220),
            ("Visit Precinct Lab", 290),
            ("Travel Gates", 360),
            ("Party & Paldex Details", 430)
        ]
        
        mx, my = rl.GetMousePosition().x, rl.GetMousePosition().y
        
        for text, by in labels:
            is_hover = check_rect_collision(mx, my, lx + 20, by, lw - 40, 50)
            
            # Additional logic for Boss button indicator
            border_col = COLOR_BORDER
            thickness = 1
            if text == "Challenge Bureaucrat":
                if self.state.current_precinct in self.state.defeated_bureaucrats:
                    # Draw a cleared green background
                    rl.DrawRectangle(lx + 20, by, lw - 40, 50, (46, 204, 113, 40))
                    border_col = (46, 204, 113, 255)
                    text = "Bureaucrat Defeated ✓"
                else:
                    border_col = (231, 76, 60, 255)
            
            bg_col = (55, 65, 85, 255) if is_hover else COLOR_BG_DARK
            if is_hover:
                thickness = 2
            
            rl.DrawRectangle(lx + 20, by, lw - 40, 50, bg_col)
            rl.DrawRectangleLinesEx([lx + 20, by, lw - 40, 50], thickness, border_col)
            AI4Animation.Draw.Text(text, (lx + lw // 2) / sw, (by + 16) / sh, 0.018, COLOR_TEXT_PRIMARY, 0.5)

    def draw_lab_panel(self, lx, ly, lw, lh, sw, sh):
        AI4Animation.Draw.Text("PRECINCT LAB SERVICES", (lx + 20) / sw, (ly + 15) / sh, 0.016, COLOR_TEXT_MUTED)
        
        labels = [
            ("Heal Party clinic", 150),
            ("Pal Storage Box", 220),
            ("Black-Market Shop", 290),
            ("Back to Precinct", 360)
        ]
        
        mx, my = rl.GetMousePosition().x, rl.GetMousePosition().y
        
        for text, by in labels:
            is_hover = check_rect_collision(mx, my, lx + 20, by, lw - 40, 50)
            bg_col = (55, 65, 85, 255) if is_hover else COLOR_BG_DARK
            rl.DrawRectangle(lx + 20, by, lw - 40, 50, bg_col)
            rl.DrawRectangleLinesEx([lx + 20, by, lw - 40, 50], 2 if is_hover else 1, COLOR_BORDER)
            AI4Animation.Draw.Text(text, (lx + lw // 2) / sw, (by + 16) / sh, 0.018, COLOR_TEXT_PRIMARY, 0.5)

    def draw_shop_panel(self, lx, ly, lw, lh, sw, sh):
        AI4Animation.Draw.Text("BLACK-MARKET SHOP", (lx + 20) / sw, (ly + 15) / sh, 0.016, COLOR_TEXT_MUTED)
        
        labels = [
            ("Basic Cube (100 RP)", 150),
            ("Mega Cube (250 RP)", 220),
            ("Ultra Cube (500 RP)", 290),
            ("Back to Clinic Menu", 360)
        ]
        
        mx, my = rl.GetMousePosition().x, rl.GetMousePosition().y
        
        for text, by in labels:
            is_hover = check_rect_collision(mx, my, lx + 20, by, lw - 40, 50)
            bg_col = (55, 65, 85, 255) if is_hover else COLOR_BG_DARK
            rl.DrawRectangle(lx + 20, by, lw - 40, 50, bg_col)
            rl.DrawRectangleLinesEx([lx + 20, by, lw - 40, 50], 2 if is_hover else 1, COLOR_BORDER)
            AI4Animation.Draw.Text(text, (lx + lw // 2) / sw, (by + 16) / sh, 0.018, COLOR_TEXT_PRIMARY, 0.5)

    def draw_storage_panel(self, rx, ry, rw, rh, sw, sh):
        AI4Animation.Draw.Text("PAL STORAGE SYSTEM (SWAP CABINET)", (rx + 30) / sw, (ry + 20) / sh, 0.02, COLOR_TEXT_PRIMARY)
        AI4Animation.Draw.Text("Select a Party slot on the left, and a Box slot on the right to swap them.", (rx + 30) / sw, (ry + 55) / sh, 0.014, COLOR_TEXT_MUTED)

        # 1. Left side: Party List (10 slots)
        AI4Animation.Draw.Text("ACTIVE PARTY (MAX 10)", (rx + 30) / sw, 120 / sh, 0.016, COLOR_TEXT_MUTED)
        for i in range(10):
            item_y = 150 + i * 44
            bg_col = COLOR_BG_DARK
            border_col = COLOR_BORDER
            
            if i == self.selected_party_idx:
                bg_col = (46, 204, 113, 80)
                border_col = (46, 204, 113, 255)
                
            rl.DrawRectangle(rx + 20, item_y, 380, 38, bg_col)
            rl.DrawRectangleLines(rx + 20, item_y, 380, 38, border_col)
            
            if i < len(self.state.party):
                p = self.state.party[i]
                type_str = "/".join(p.types)
                hp_percent = max(0.0, p.hp / p.max_hp)
                
                AI4Animation.Draw.Text(f"{i+1}. {p.name}", (rx + 35) / sw, (item_y + 11) / sh, 0.016, COLOR_TEXT_PRIMARY)
                AI4Animation.Draw.Text(f"Lv.{p.level}", (rx + 190) / sw, (item_y + 12) / sh, 0.014, COLOR_TEXT_MUTED)
                AI4Animation.Draw.Text(type_str, (rx + 240) / sw, (item_y + 12) / sh, 0.014, TYPE_COLORS.get(p.types[0], COLOR_TEXT_MUTED))
                
                # HP Bar
                bar_col = COLOR_HP_GREEN if hp_percent > 0.5 else (COLOR_HP_YELLOW if hp_percent > 0.2 else COLOR_HP_RED)
                rl.DrawRectangle(rx + 310, item_y + 14, 80, 10, COLOR_HP_BG)
                rl.DrawRectangle(rx + 310, item_y + 14, int(80 * hp_percent), 10, bar_col)
            else:
                AI4Animation.Draw.Text(f"{i+1}. [ EMPTY SLOT ]", (rx + 35) / sw, (item_y + 11) / sh, 0.016, COLOR_TEXT_MUTED)

        # 2. Right side: Box Storage (6 visible slots with scroll)
        AI4Animation.Draw.Text(f"BOX STORAGE ({len(self.state.box)} captured)", (rx + 450) / sw, 120 / sh, 0.016, COLOR_TEXT_MUTED)
        for i in range(6):
            box_idx = self.box_scroll + i
            item_y = 150 + i * 50
            bg_col = COLOR_BG_DARK
            border_col = COLOR_BORDER
            
            if box_idx == self.selected_box_idx:
                bg_col = (46, 204, 113, 80)
                border_col = (46, 204, 113, 255)

            rl.DrawRectangle(rx + 440, item_y, 380, 44, bg_col)
            rl.DrawRectangleLines(rx + 440, item_y, 380, 44, border_col)

            if box_idx < len(self.state.box):
                p = self.state.box[box_idx]
                type_str = "/".join(p.types)
                AI4Animation.Draw.Text(f"#{box_idx + 1}. {p.name}", (rx + 455) / sw, (item_y + 14) / sh, 0.017, COLOR_TEXT_PRIMARY)
                AI4Animation.Draw.Text(f"Lv.{p.level}", (rx + 620) / sw, (item_y + 15) / sh, 0.014, COLOR_TEXT_MUTED)
                AI4Animation.Draw.Text(type_str, (rx + 670) / sw, (item_y + 15) / sh, 0.014, TYPE_COLORS.get(p.types[0], COLOR_TEXT_MUTED))
            else:
                AI4Animation.Draw.Text("---", (rx + 455) / sw, (item_y + 14) / sh, 0.017, COLOR_TEXT_MUTED)

        # Scroll controls
        rl.DrawRectangle(rx + 440, 470, 180, 35, COLOR_BG_DARK)
        rl.DrawRectangleLines(rx + 440, 470, 180, 35, COLOR_BORDER)
        AI4Animation.Draw.Text("Scroll Up ▲", (rx + 530) / sw, 480 / sh, 0.015, COLOR_TEXT_PRIMARY, 0.5)

        rl.DrawRectangle(rx + 640, 470, 180, 35, COLOR_BG_DARK)
        rl.DrawRectangleLines(rx + 640, 470, 180, 35, COLOR_BORDER)
        AI4Animation.Draw.Text("Scroll Down ▼", (rx + 730) / sw, 480 / sh, 0.015, COLOR_TEXT_PRIMARY, 0.5)

        # Close Panel Button
        rl.DrawRectangle(sw // 2 - 100, sh - 100, 200, 45, (55, 65, 85, 255))
        rl.DrawRectangleLines(sw // 2 - 100, sh - 100, 200, 45, COLOR_BORDER)
        AI4Animation.Draw.Text("Back to Clinic", 0.5, (sh - 78) / sh, 0.018, COLOR_TEXT_PRIMARY, 0.5)

    def draw_travel_panel(self, rx, ry, rw, rh, sw, sh):
        AI4Animation.Draw.Text("PALTOPIAN BORDER GATE TRAVEL SYSTEM", (rx + 30) / sw, (ry + 20) / sh, 0.02, COLOR_TEXT_PRIMARY)
        AI4Animation.Draw.Text("Clear gates by defeating Bureaucrats to unlock fast-travel.", (rx + 30) / sw, (ry + 55) / sh, 0.014, COLOR_TEXT_MUTED)

        grid_w, grid_h = 240, 60
        mx, my = rl.GetMousePosition().x, rl.GetMousePosition().y

        for idx, p in enumerate(PRECINCTS):
            row = idx // 3
            col = idx % 3
            bx = rx + 30 + col * 260
            by = 160 + row * 80
            
            unlocked = idx in self.state.unlocked_precincts
            is_hover = check_rect_collision(mx, my, bx, by, grid_w, grid_h)
            
            bg_col = COLOR_BG_DARK
            border_col = COLOR_BORDER
            
            if unlocked:
                bg_col = (45, 55, 75, 255) if is_hover else (30, 40, 60, 255)
                border_col = TYPE_COLORS.get(p["type"], COLOR_BORDER)
            
            rl.DrawRectangle(bx, by, grid_w, grid_h, bg_col)
            rl.DrawRectangleLinesEx([bx, by, grid_w, grid_h], 2 if is_hover and unlocked else 1, border_col)
            
            # Print Details
            precinct_num = f"Precinct {idx + 1}"
            p_name = p["name"] if unlocked else "CLASSIFIED"
            type_text = f"({p['type']} Zone)" if unlocked else "LOCKED"
            
            AI4Animation.Draw.Text(precinct_num, (bx + grid_w // 2) / sw, (by + 12) / sh, 0.014, COLOR_TEXT_MUTED, 0.5)
            AI4Animation.Draw.Text(p_name, (bx + grid_w // 2) / sw, (by + 28) / sh, 0.017, COLOR_TEXT_PRIMARY if unlocked else COLOR_TEXT_MUTED, 0.5)
            AI4Animation.Draw.Text(type_text, (bx + grid_w // 2) / sw, (by + 46) / sh, 0.012, border_col if unlocked else COLOR_TEXT_MUTED, 0.5)

        # Close Panel Button
        rl.DrawRectangle(sw // 2 - 100, sh - 100, 200, 45, (55, 65, 85, 255))
        rl.DrawRectangleLines(sw // 2 - 100, sh - 100, 200, 45, COLOR_BORDER)
        AI4Animation.Draw.Text("Close Map", 0.5, (sh - 78) / sh, 0.018, COLOR_TEXT_PRIMARY, 0.5)

    def draw_paldex_panel(self, rx, ry, rw, rh, sw, sh):
        AI4Animation.Draw.Text("ACTIVE PARTY BIOLOGY & PALDEX STATUS", (rx + 30) / sw, (ry + 20) / sh, 0.02, COLOR_TEXT_PRIMARY)
        
        # Left Side: Clickable Party List
        AI4Animation.Draw.Text("SELECT PARTY MEMBER", (rx + 30) / sw, 120 / sh, 0.016, COLOR_TEXT_MUTED)
        for i in range(10):
            item_y = 150 + i * 44
            bg_col = COLOR_BG_DARK
            border_col = COLOR_BORDER
            
            if i == self.paldex_detail_idx:
                bg_col = (55, 75, 105, 255)
                border_col = COLOR_TEXT_PRIMARY
                
            rl.DrawRectangle(rx + 20, item_y, 380, 38, bg_col)
            rl.DrawRectangleLines(rx + 20, item_y, 380, 38, border_col)
            
            if i < len(self.state.party):
                p = self.state.party[i]
                AI4Animation.Draw.Text(f"{i+1}. {p.name}", (rx + 35) / sw, (item_y + 11) / sh, 0.016, COLOR_TEXT_PRIMARY)
                AI4Animation.Draw.Text(f"Lv.{p.level}", (rx + 330) / sw, (item_y + 12) / sh, 0.014, COLOR_TEXT_MUTED)
            else:
                AI4Animation.Draw.Text(f"{i+1}. ---", (rx + 35) / sw, (item_y + 11) / sh, 0.016, COLOR_TEXT_MUTED)

        # Right Side: Selected Pal Stats & Details
        detail_x = rx + 430
        rl.DrawRectangle(detail_x, 150, 360, 380, COLOR_BG_DARK)
        rl.DrawRectangleLines(detail_x, 150, 360, 380, COLOR_BORDER)
        
        if self.paldex_detail_idx < len(self.state.party):
            p = self.state.party[self.paldex_detail_idx]
            AI4Animation.Draw.Text(p.name, (detail_x + 180) / sw, 175 / sh, 0.024, COLOR_TEXT_PRIMARY, 0.5)
            AI4Animation.Draw.Text(f"Lv.{p.level} Specimen  |  HP: {p.hp}/{p.max_hp}", (detail_x + 180) / sw, 205 / sh, 0.016, COLOR_TEXT_MUTED, 0.5)
            
            # Type Badges
            type_str = " / ".join(p.types)
            AI4Animation.Draw.Text(type_str, (detail_x + 180) / sw, 230 / sh, 0.016, TYPE_COLORS.get(p.types[0], COLOR_TEXT_MUTED), 0.5)

            # Trait
            AI4Animation.Draw.Text(f"Trait: {p.species.trait or 'None'}", (detail_x + 20) / sw, 265 / sh, 0.015, COLOR_TEXT_PRIMARY)

            # Base Stats Bars
            stats = [
                ("HP", p.max_hp, 250),
                ("Attack", p.base_attack, 200),
                ("Defense", p.base_defense, 200),
                ("Speed", p.base_speed, 200)
            ]
            
            for idx, (s_name, val, max_val) in enumerate(stats):
                bar_y = 295 + idx * 28
                AI4Animation.Draw.Text(f"{s_name}: {val}", (detail_x + 20) / sw, bar_y / sh, 0.014, COLOR_TEXT_MUTED)
                # Draw bar
                fill = min(1.0, val / max_val)
                rl.DrawRectangle(detail_x + 100, bar_y + 2, 230, 10, COLOR_HP_BG)
                rl.DrawRectangle(detail_x + 100, bar_y + 2, int(230 * fill), 10, TYPE_COLORS.get(p.types[0], COLOR_BORDER))

            # Moves list
            AI4Animation.Draw.Text("Moves learnset:", (detail_x + 20) / sw, 415 / sh, 0.014, COLOR_TEXT_MUTED)
            for m_idx, mv in enumerate(p.moves):
                mv_y = 440 + m_idx * 20
                AI4Animation.Draw.Text(f"• {mv.name}", (detail_x + 30) / sw, mv_y / sh, 0.015, COLOR_TEXT_PRIMARY)
                AI4Animation.Draw.Text(f"({mv.type} | Power: {mv.power})", (detail_x + 180) / sw, mv_y / sh, 0.013, TYPE_COLORS.get(mv.type, COLOR_TEXT_MUTED))
        else:
            AI4Animation.Draw.Text("No Pal selected", (detail_x + 180) / sw, 300 / sh, 0.018, COLOR_TEXT_MUTED, 0.5)

        # Close Panel Button
        rl.DrawRectangle(sw // 2 - 100, sh - 100, 200, 45, (55, 65, 85, 255))
        rl.DrawRectangleLines(sw // 2 - 100, sh - 100, 200, 45, COLOR_BORDER)
        AI4Animation.Draw.Text("Close Paldex", 0.5, (sh - 78) / sh, 0.018, COLOR_TEXT_PRIMARY, 0.5)
