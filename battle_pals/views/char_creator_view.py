import raylib as rl
import math
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_TYPE_FIRE, COLOR_TYPE_WATER, COLOR_TYPE_GRASS
)
from battle_pals.models.pal import Pal
from battle_pals.models.state import GameState
from ai4animation import AI4Animation, Vector3

def check_rect_collision(px, py, rx, ry, rw, rh):
    return rx <= px <= rx + rw and ry <= py <= ry + rh

class CharCreatorView:
    def __init__(self):
        self.name_buffer = "Robin"
        self.selected_gender = "Boy"
        self.selected_starter = "Leaflet"
        self.preview_pal = None
        self.cursor_timer = 0.0
        self.update_preview()

    def update_preview(self):
        self.preview_pal = Pal(self.selected_starter, level=5, is_player=True)
        self.preview_pal.base_position = Vector3.Create(0.0, 0.8, 0.0)
        self.preview_pal.position = Vector3.Create(0.0, 0.8, 0.0)

    def on_show_view(self):
        pass

    def on_update(self, dt):
        if self.preview_pal:
            self.preview_pal.update_animation(dt)
        self.cursor_timer += dt

        # Handle text typing keys
        key = rl.GetCharPressed()
        while key > 0:
            if (32 <= key <= 125) and len(self.name_buffer) < 12:
                self.name_buffer += chr(key)
            key = rl.GetCharPressed()

        # Handle backspace key
        if rl.IsKeyPressed(rl.KEY_BACKSPACE) and len(self.name_buffer) > 0:
            self.name_buffer = self.name_buffer[:-1]

        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        mouse_pos = rl.GetMousePosition()
        mx, my = mouse_pos.x, mouse_pos.y

        # Handle clicks
        if rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            # Gender Selection Clicks
            if check_rect_collision(mx, my, 80, 350, 120, 50):
                self.selected_gender = "Boy"
            elif check_rect_collision(mx, my, 220, 350, 120, 50):
                self.selected_gender = "Girl"

            # Starter Selection Clicks
            rx = sw - 360
            if check_rect_collision(mx, my, rx, 200, 280, 60):
                self.selected_starter = "Leaflet"
                self.update_preview()
            elif check_rect_collision(mx, my, rx, 280, 280, 60):
                self.selected_starter = "Pyropup"
                self.update_preview()
            elif check_rect_collision(mx, my, rx, 360, 280, 60):
                self.selected_starter = "Aquasplash"
                self.update_preview()

            # Begin Journey Click
            bx = sw // 2 - 150
            by = sh - 100
            if check_rect_collision(mx, my, bx, by, 300, 60):
                if len(self.name_buffer.strip()) > 0:
                    # Initialize global campaign state
                    state = GameState(self.name_buffer.strip(), self.selected_gender, self.selected_starter)
                    GameState.set_instance(state)
                    
                    # Transition to campaign exploration view
                    from battle_pals.views.exploration_view import ExplorationView
                    from battle_pals.game import BattlePalsGame
                    BattlePalsGame.get_instance().switch_to_view(ExplorationView())

    def on_draw(self):
        # Draw 3D floor plane
        rl.DrawPlane([0.0, 0.0, 0.0], [30.0, 30.0], (25, 30, 42, 255))
        
        # Draw rotating preview Pal in 3D
        if self.preview_pal:
            # facing changes slowly side-to-side to show profile
            facing_angle = math.cos(self.preview_pal.time * 0.7)
            self.preview_pal.draw_3d(facing_angle, 1.2)

    def on_gui(self):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()

        # Title
        AI4Animation.Draw.Text("BATTLE PALS: RESEARCH CAMPING", 0.5, 0.06, 0.038, COLOR_TEXT_PRIMARY, 0.5)
        AI4Animation.Draw.Text("Enter your credentials and select your research companion", 0.5, 0.11, 0.018, COLOR_TEXT_MUTED, 0.5)

        # ----------------- LEFT PANEL (PROFILE) -----------------
        # Name Input Box
        rl.DrawRectangle(60, 140, 320, 120, COLOR_BG_PANEL)
        rl.DrawRectangleLines(60, 140, 320, 120, COLOR_BORDER)
        AI4Animation.Draw.Text("RESEARCHER NAME", 80 / sw, 155 / sh, 0.016, COLOR_TEXT_MUTED)
        
        # Name Field Background
        rl.DrawRectangle(80, 195, 280, 45, COLOR_BG_DARK)
        rl.DrawRectangleLines(80, 195, 280, 45, COLOR_BORDER)
        
        # Draw Cursor
        cursor = ""
        if int(self.cursor_timer * 2.0) % 2 == 0:
            cursor = "|"
        AI4Animation.Draw.Text(f"{self.name_buffer}{cursor}", 95 / sw, 206 / sh, 0.022, COLOR_TEXT_PRIMARY)

        # Gender Selection Box
        rl.DrawRectangle(60, 280, 320, 150, COLOR_BG_PANEL)
        rl.DrawRectangleLines(60, 280, 320, 150, COLOR_BORDER)
        AI4Animation.Draw.Text("RESEARCHER GENDER", 80 / sw, 295 / sh, 0.016, COLOR_TEXT_MUTED)
        
        # Boy Button
        boy_bg = (55, 65, 85, 255) if self.selected_gender == "Boy" else COLOR_BG_DARK
        boy_border = COLOR_TYPE_WATER if self.selected_gender == "Boy" else COLOR_BORDER
        rl.DrawRectangle(80, 340, 120, 50, boy_bg)
        rl.DrawRectangleLinesEx([80, 340, 120, 50], 2 if self.selected_gender == "Boy" else 1, boy_border)
        AI4Animation.Draw.Text("MALE", 140 / sw, 353 / sh, 0.018, COLOR_TEXT_PRIMARY, 0.5)

        # Girl Button
        girl_bg = (55, 65, 85, 255) if self.selected_gender == "Girl" else COLOR_BG_DARK
        girl_border = COLOR_TYPE_FIRE if self.selected_gender == "Girl" else COLOR_BORDER
        rl.DrawRectangle(220, 340, 120, 50, girl_bg)
        rl.DrawRectangleLinesEx([220, 340, 120, 50], 2 if self.selected_gender == "Girl" else 1, girl_border)
        AI4Animation.Draw.Text("FEMALE", 280 / sw, 353 / sh, 0.018, COLOR_TEXT_PRIMARY, 0.5)

        # ----------------- RIGHT PANEL (STARTER CHOOSE) -----------------
        rx = sw - 380
        rl.DrawRectangle(rx, 140, 320, 350, COLOR_BG_PANEL)
        rl.DrawRectangleLines(rx, 140, 320, 350, COLOR_BORDER)
        AI4Animation.Draw.Text("SELECT STARTER PAL", (rx + 20) / sw, 155 / sh, 0.016, COLOR_TEXT_MUTED)

        # Leaflet Button
        l_bg = (40, 50, 40, 255) if self.selected_starter == "Leaflet" else COLOR_BG_DARK
        l_border = COLOR_TYPE_GRASS if self.selected_starter == "Leaflet" else COLOR_BORDER
        rl.DrawRectangle(rx + 20, 200, 280, 60, l_bg)
        rl.DrawRectangleLinesEx([rx + 20, 200, 280, 60], 2 if self.selected_starter == "Leaflet" else 1, l_border)
        AI4Animation.Draw.Text("LEAFLET (Grass)", (rx + 160) / sw, 218 / sh, 0.02, COLOR_TEXT_PRIMARY, 0.5)

        # Pyropup Button
        p_bg = (50, 40, 40, 255) if self.selected_starter == "Pyropup" else COLOR_BG_DARK
        p_border = COLOR_TYPE_FIRE if self.selected_starter == "Pyropup" else COLOR_BORDER
        rl.DrawRectangle(rx + 20, 280, 280, 60, p_bg)
        rl.DrawRectangleLinesEx([rx + 20, 280, 280, 60], 2 if self.selected_starter == "Pyropup" else 1, p_border)
        AI4Animation.Draw.Text("PYROPUP (Fire)", (rx + 160) / sw, 298 / sh, 0.02, COLOR_TEXT_PRIMARY, 0.5)

        # Aquasplash Button
        a_bg = (40, 40, 50, 255) if self.selected_starter == "Aquasplash" else COLOR_BG_DARK
        a_border = COLOR_TYPE_WATER if self.selected_starter == "Aquasplash" else COLOR_BORDER
        rl.DrawRectangle(rx + 20, 360, 280, 60, a_bg)
        rl.DrawRectangleLinesEx([rx + 20, 360, 280, 60], 2 if self.selected_starter == "Aquasplash" else 1, a_border)
        AI4Animation.Draw.Text("AQUASPLASH (Water)", (rx + 160) / sw, 378 / sh, 0.02, COLOR_TEXT_PRIMARY, 0.5)

        # Starter Description Text
        desc_text = "Select a Pal to review its biology profile."
        if self.selected_starter == "Leaflet":
            desc_text = "Grass/Wind type. Grows a yellow bulb and sprouts green leaves."
        elif self.selected_starter == "Pyropup":
            desc_text = "Fire type. Fluffy floppy ears and a tail covered in bright embers."
        elif self.selected_starter == "Aquasplash":
            desc_text = "Water type. Has smooth flipper fins and a split rudder tail."
        AI4Animation.Draw.Text(desc_text, (rx + 160) / sw, 445 / sh, 0.015, COLOR_TEXT_MUTED, 0.5)

        # ----------------- BEGIN JOURNEY BUTTON -----------------
        bx = sw // 2 - 150
        by = sh - 100
        # Highlight check
        mouse_over = check_rect_collision(rl.GetMousePosition().x, rl.GetMousePosition().y, bx, by, 300, 60)
        btn_col = (72, 85, 115, 255) if mouse_over else (55, 65, 85, 255)
        rl.DrawRectangle(bx, by, 300, 60, btn_col)
        rl.DrawRectangleLinesEx([bx, by, 300, 60], 2 if mouse_over else 1, COLOR_BORDER)
        AI4Animation.Draw.Text("BEGIN JOURNEY", 0.5, (by + 20) / sh, 0.022, COLOR_TEXT_PRIMARY, 0.5)
