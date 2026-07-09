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
from battle_pals.views.game_over_view import GameOverView
from ai4animation import AI4Animation, Vector3

# Battle States
STATE_INTRO = 0
STATE_MOVE_SELECT = 1
STATE_COMBAT_LOGS = 2

class MoveButton:
    def __init__(self, move, lx, ty, w, h):
        self.move = move
        self.lx = lx
        self.ty = ty
        self.w = w
        self.h = h
        self.hovered = False

    def check_mouse(self, mx, my):
        self.hovered = (self.lx <= mx <= self.lx + self.w) and (self.ty <= my <= self.ty + self.h)
        return self.hovered

    def draw(self, sw, sh):
        type_colors = {
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
        accent_color = type_colors.get(self.move.type, COLOR_BORDER)
        
        bg_color = COLOR_BG_PANEL if not self.hovered else (45, 52, 68, 255)
        border_color = accent_color if self.hovered else COLOR_BORDER
        border_thickness = 4 if self.hovered else 2

        rl.DrawRectangle(int(self.lx), int(self.ty), int(self.w), int(self.h), bg_color)
        rl.DrawRectangleLinesEx([self.lx, self.ty, self.w, self.h], border_thickness, border_color)

        cx_norm = (self.lx + self.w / 2) / sw
        cy_norm = (self.ty + self.h / 2 - 10) / sh
        
        AI4Animation.Draw.Text(
            self.move.name,
            cx_norm, cy_norm,
            0.02, COLOR_TEXT_PRIMARY, 0.5
        )

class BattleView:
    def __init__(self, player_pal, opponent_pal):
        self.player = player_pal
        self.opponent = opponent_pal
        
        # Reset modifiers
        self.player.reset_battle_stats()
        self.opponent.reset_battle_stats()

        self.state = STATE_INTRO
        self.log_queue = []
        self.current_log = ""
        
        self.move_buttons = []
        
        # Timers
        self.blink_timer = 0.0
        self.show_arrow = True
        
        # Game Over trigger state
        self.game_ending = False

    def on_show_view(self):
        # Log introductory messages
        self.log_queue = [
            f"A wild {self.opponent.name} appeared!",
            f"Go! {self.player.name}!"
        ]
        self.advance_log()

        # Build Move Buttons
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        
        btn_w = sw * 0.12 # ~230 pixels
        btn_h = sh * 0.055 # ~60 pixels
        spacing_x = sw * 0.015
        spacing_y = sh * 0.015
        
        start_x = sw * 0.08
        start_y = sh * 0.81
        
        for idx, move in enumerate(self.player.moves):
            row = idx // 2
            col = idx % 2
            bx = start_x + col * (btn_w + spacing_x)
            by = start_y + row * (btn_h + spacing_y)
            self.move_buttons.append(MoveButton(move, bx, by, btn_w, btn_h))

    def advance_log(self):
        """Advances to the next message in the log, checking for end-of-battle conditions."""
        if self.log_queue:
            self.state = STATE_COMBAT_LOGS
            self.current_log = self.log_queue.pop(0)
        else:
            # Check for faint conditions
            if self.player.hp <= 0 or self.opponent.hp <= 0:
                if self.player.hp <= 0 and not self.player.is_fainted:
                    self.player.faint_timer = 0.01
                    self.log_queue.append(f"{self.player.name} fainted!")
                    self.game_ending = True
                    self.advance_log()
                elif self.opponent.hp <= 0 and not self.opponent.is_fainted:
                    self.opponent.faint_timer = 0.01
                    self.log_queue.append(f"The wild {self.opponent.name} fainted!")
                    self.game_ending = True
                    self.advance_log()
                else:
                    # Redirect to game over
                    victory = self.opponent.hp <= 0
                    from battle_pals.game import BattlePalsGame
                    BattlePalsGame.get_instance().switch_to_view(
                        GameOverView(victory=victory, player_pal=self.player, opponent_pal=self.opponent)
                    )
            else:
                # Return to move selection
                self.state = STATE_MOVE_SELECT
                self.current_log = ""

    def execute_turn(self, player_move):
        """Computes combat turns using Speeds to determine priority."""
        self.log_queue = []
        
        # Simple AI Move Selection
        opponent_move = random.choice(self.opponent.moves)

        # Check Speeds
        player_first = self.player.speed >= self.opponent.speed
        
        if player_first:
            # 1. Player attacks
            p_logs = self.player.use_move(player_move, self.opponent)
            self.log_queue.extend(p_logs)
            
            # Check if opponent fainted
            if self.opponent.hp > 0:
                o_logs = self.opponent.use_move(opponent_move, self.player)
                self.log_queue.extend(o_logs)
        else:
            # 1. Opponent attacks
            o_logs = self.opponent.use_move(opponent_move, self.player)
            self.log_queue.extend(o_logs)
            
            # Check if player fainted
            if self.player.hp > 0:
                p_logs = self.player.use_move(player_move, self.opponent)
                self.log_queue.extend(p_logs)

        # Start printing log sequence
        self.advance_log()

    def on_update(self, dt):
        # Blinking cursor for dialogue
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.blink_timer = 0.0
            self.show_arrow = not self.show_arrow

        # Update Pal animations
        self.player.update_animation(dt)
        self.opponent.update_animation(dt)

        # Check hover states & clicks
        mouse_pos = rl.GetMousePosition()
        mx, my = mouse_pos.x, mouse_pos.y

        if self.state == STATE_MOVE_SELECT:
            for btn in self.move_buttons:
                btn.check_mouse(mx, my)

        # Handle click event
        if rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            if self.state == STATE_COMBAT_LOGS or self.state == STATE_INTRO:
                self.advance_log()
            elif self.state == STATE_MOVE_SELECT:
                for btn in self.move_buttons:
                    if btn.hovered:
                        self.execute_turn(btn.move)
                        break

    def draw_pal_3d(self, pal):
        # If faint animation is fully complete, don't draw
        if pal.is_fainted:
            return
            
        pos = pal.position
        facing = 1.0 if pal.is_player else -1.0
        
        # Scale modifier based on fainting
        scale = 1.0
        if pal.faint_timer > 0.0:
            scale = max(0.01, 1.0 - pal.faint_timer)
            
        # Determine color override (flash red when taking damage)
        def get_color(base_c):
            if pal.flash_timer > 0.0 and int(pal.flash_timer * 15.0) % 2 == 0:
                return rl.colors.RED
            return base_c

        def parse_color(c):
            if isinstance(c, list) or isinstance(c, tuple):
                return (c[0], c[1], c[2], c[3] if len(c) > 3 else 255)
            return rl.colors.GRAY

        # Define common colors
        color_eye_bg = rl.colors.BLACK
        color_eye_fg = rl.colors.WHITE
        color_mouth = (231, 76, 60, 255) # Rose/red
        color_cheek = (255, 128, 128, 128) # Translucent blush

        # Get species appearance settings
        app = pal.species.appearance
        base_shape = app.get("base_shape", "quadruped")
        
        color_body = get_color(parse_color(app.get("body_color")))
        color_accent = get_color(parse_color(app.get("accent_color")))
        color_belly = get_color(parse_color(app.get("belly_color")))
        color_eye = parse_color(app.get("eye_color", [0, 0, 0, 255]))

        # --- 3D Character Rendering ---
        if base_shape == "quadruped" or base_shape == "biped" or base_shape == "demon" or base_shape == "dragon":
            body_center = Vector3.Create(pos[0], pos[1] - 0.2 * scale, pos[2] + 0.1 * facing * scale)
            head_center = Vector3.Create(pos[0], pos[1] + 0.7 * scale, pos[2] - 0.3 * facing * scale)
            AI4Animation.Draw.Sphere(body_center, 1.0 * scale, 12, color_body)
            AI4Animation.Draw.Sphere(head_center, 0.85 * scale, 12, color_body)
            
            # Belly Patch
            belly_center = Vector3.Create(pos[0], pos[1] - 0.1 * scale, pos[2] - 0.7 * facing * scale)
            AI4Animation.Draw.Sphere(belly_center, 0.5 * scale, 8, color_belly)
            
        elif base_shape == "aquatic":
            body_center = Vector3.Create(pos[0], pos[1] - 0.1 * scale, pos[2] * scale)
            head_center = Vector3.Create(pos[0], pos[1] + 0.5 * scale, pos[2] - 0.4 * facing * scale)
            AI4Animation.Draw.Sphere(body_center, 1.0 * scale, 12, color_body)
            AI4Animation.Draw.Sphere(head_center, 0.8 * scale, 12, color_body)
            
            belly_center = Vector3.Create(pos[0], pos[1] - 0.15 * scale, pos[2] - 0.65 * facing * scale)
            AI4Animation.Draw.Sphere(belly_center, 0.45 * scale, 8, color_belly)
            
        elif base_shape == "bird":
            body_center = Vector3.Create(pos[0], pos[1] - 0.1 * scale, pos[2] * scale)
            head_center = Vector3.Create(pos[0], pos[1] + 0.6 * scale, pos[2] - 0.2 * facing * scale)
            AI4Animation.Draw.Sphere(body_center, 0.9 * scale, 12, color_body)
            AI4Animation.Draw.Sphere(head_center, 0.75 * scale, 12, color_body)
            
            belly_center = Vector3.Create(pos[0], pos[1] - 0.1 * scale, pos[2] - 0.5 * facing * scale)
            AI4Animation.Draw.Sphere(belly_center, 0.4 * scale, 8, color_belly)
            
        else: # blob / ghost
            body_center = Vector3.Create(pos[0], pos[1] + 0.2 * scale, pos[2] * scale)
            AI4Animation.Draw.Sphere(body_center, 1.1 * scale, 12, color_body)
            head_center = body_center
            
            belly_center = Vector3.Create(pos[0], pos[1] + 0.1 * scale, pos[2] - 0.8 * facing * scale)
            AI4Animation.Draw.Sphere(belly_center, 0.35 * scale, 8, color_belly)

        # Face details
        eye_y = head_center[1] + 0.2 * scale
        eye_z = head_center[2] - 0.65 * facing * scale
        
        # Left eye
        eye_l_x = head_center[0] - 0.35 * scale
        eye_l_center = Vector3.Create(eye_l_x, eye_y, eye_z)
        AI4Animation.Draw.Sphere(eye_l_center, 0.15 * scale, 6, get_color(color_eye_bg))
        AI4Animation.Draw.Sphere(Vector3.Create(eye_l_x - 0.05 * scale, eye_y + 0.05 * scale, eye_z - 0.05 * facing * scale), 0.06 * scale, 4, get_color(color_eye_fg))
        
        # Right eye
        eye_r_x = head_center[0] + 0.35 * scale
        eye_r_center = Vector3.Create(eye_r_x, eye_y, eye_z)
        AI4Animation.Draw.Sphere(eye_r_center, 0.15 * scale, 6, get_color(color_eye_bg))
        AI4Animation.Draw.Sphere(Vector3.Create(eye_r_x + 0.05 * scale, eye_y + 0.05 * scale, eye_z - 0.05 * facing * scale), 0.06 * scale, 4, get_color(color_eye_fg))

        # Mouth or Beak
        if base_shape == "bird":
            beak_center = Vector3.Create(head_center[0], head_center[1] - 0.1 * scale, head_center[2] - 0.8 * facing * scale)
            AI4Animation.Draw.Sphere(beak_center, 0.15 * scale, 4, color_accent)
        else:
            mouth_center = Vector3.Create(head_center[0], head_center[1] - 0.15 * scale, head_center[2] - 0.7 * facing * scale)
            AI4Animation.Draw.Sphere(mouth_center, 0.1 * scale, 4, get_color(color_mouth))

        # Blushing cheeks
        AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] - 0.5 * scale, head_center[1] - 0.05 * scale, head_center[2] - 0.65 * facing * scale), 0.12 * scale, 4, get_color(color_cheek))
        AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] + 0.5 * scale, head_center[1] - 0.05 * scale, head_center[2] - 0.65 * facing * scale), 0.12 * scale, 4, get_color(color_cheek))

        # Limbs
        if base_shape == "quadruped":
            leg_y = pos[1] - 0.8 * scale
            leg_w = 0.25 * scale
            rl.DrawCylinderEx([pos[0] - 0.5 * scale, pos[1] - 0.3 * scale, pos[2] - 0.4 * facing * scale], [pos[0] - 0.5 * scale, leg_y, pos[2] - 0.4 * facing * scale], leg_w, leg_w, 6, color_body)
            rl.DrawCylinderEx([pos[0] + 0.5 * scale, pos[1] - 0.3 * scale, pos[2] - 0.4 * facing * scale], [pos[0] + 0.5 * scale, leg_y, pos[2] - 0.4 * facing * scale], leg_w, leg_w, 6, color_body)
            rl.DrawCylinderEx([pos[0] - 0.6 * scale, pos[1] - 0.3 * scale, pos[2] + 0.5 * facing * scale], [pos[0] - 0.6 * scale, leg_y, pos[2] + 0.5 * facing * scale], leg_w, leg_w, 6, color_body)
            rl.DrawCylinderEx([pos[0] + 0.6 * scale, pos[1] - 0.3 * scale, pos[2] + 0.5 * facing * scale], [pos[0] + 0.6 * scale, leg_y, pos[2] + 0.5 * facing * scale], leg_w, leg_w, 6, color_body)
            
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] - 0.5 * scale, leg_y, pos[2] - 0.55 * facing * scale), 0.25 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] + 0.5 * scale, leg_y, pos[2] - 0.55 * facing * scale), 0.25 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] - 0.6 * scale, leg_y, pos[2] + 0.45 * facing * scale), 0.25 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] + 0.6 * scale, leg_y, pos[2] + 0.45 * facing * scale), 0.25 * scale, 6, color_accent)
            
        elif base_shape == "biped" or base_shape == "demon" or base_shape == "dragon":
            leg_y = pos[1] - 0.8 * scale
            leg_w = 0.28 * scale
            rl.DrawCylinderEx([pos[0] - 0.4 * scale, pos[1] - 0.3 * scale, pos[2]], [pos[0] - 0.4 * scale, leg_y, pos[2]], leg_w, leg_w, 6, color_body)
            rl.DrawCylinderEx([pos[0] + 0.4 * scale, pos[1] - 0.3 * scale, pos[2]], [pos[0] + 0.4 * scale, leg_y, pos[2]], leg_w, leg_w, 6, color_body)
            
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] - 0.4 * scale, leg_y, pos[2] - 0.2 * facing * scale), 0.3 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] + 0.4 * scale, leg_y, pos[2] - 0.2 * facing * scale), 0.3 * scale, 6, color_accent)
            
            arm_y = pos[1] + 0.1 * scale
            rl.DrawCylinderEx([body_center[0] - 0.8 * scale, arm_y, body_center[2]], [body_center[0] - 1.2 * scale, arm_y - 0.3 * scale, body_center[2] - 0.2 * facing * scale], 0.18 * scale, 0.18 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0] - 1.2 * scale, arm_y - 0.3 * scale, body_center[2] - 0.25 * facing * scale), 0.2 * scale, 6, color_accent)
            
            rl.DrawCylinderEx([body_center[0] + 0.8 * scale, arm_y, body_center[2]], [body_center[0] + 1.2 * scale, arm_y - 0.3 * scale, body_center[2] - 0.2 * facing * scale], 0.18 * scale, 0.18 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0] + 1.2 * scale, arm_y - 0.3 * scale, body_center[2] - 0.25 * facing * scale), 0.2 * scale, 6, color_accent)
            
        elif base_shape == "bird":
            leg_y = pos[1] - 0.7 * scale
            rl.DrawCylinderEx([pos[0] - 0.3 * scale, pos[1] - 0.3 * scale, pos[2]], [pos[0] - 0.3 * scale, leg_y, pos[2]], 0.1 * scale, 0.1 * scale, 4, color_accent)
            rl.DrawCylinderEx([pos[0] + 0.3 * scale, pos[1] - 0.3 * scale, pos[2]], [pos[0] + 0.3 * scale, leg_y, pos[2]], 0.1 * scale, 0.1 * scale, 4, color_accent)
            
        elif base_shape == "aquatic":
            # Side flippers/fins
            rl.DrawCylinderEx([body_center[0] - 0.8 * scale, body_center[1] - 0.2 * scale, body_center[2]], [body_center[0] - 1.3 * scale, body_center[1] - 0.4 * scale, body_center[2] - 0.1 * facing * scale], 0.18 * scale, 0.05 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0] - 1.3 * scale, body_center[1] - 0.4 * scale, body_center[2] - 0.1 * facing * scale), 0.12 * scale, 6, color_accent)
            
            rl.DrawCylinderEx([body_center[0] + 0.8 * scale, body_center[1] - 0.2 * scale, body_center[2]], [body_center[0] + 1.3 * scale, body_center[1] - 0.4 * scale, body_center[2] - 0.1 * facing * scale], 0.18 * scale, 0.05 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0] + 1.3 * scale, body_center[1] - 0.4 * scale, body_center[2] - 0.1 * facing * scale), 0.12 * scale, 6, color_accent)
            
            # Dolphin-like back fin
            rl.DrawCylinderEx([body_center[0], body_center[1] + 0.5 * scale, body_center[2] + 0.3 * facing * scale], [body_center[0], body_center[1] + 1.3 * scale, body_center[2] + 0.9 * facing * scale], 0.16 * scale, 0.01 * scale, 6, color_body)

        # Wings
        wings_type = app.get("wings", "none")
        if wings_type == "feathered":
            wing_z = body_center[2] + 0.3 * facing * scale
            rl.DrawCylinderEx([body_center[0] - 0.8 * scale, body_center[1] + 0.2 * scale, wing_z], [body_center[0] - 2.0 * scale, body_center[1] + 1.0 * scale, wing_z + 0.5 * facing * scale], 0.1 * scale, 0.3 * scale, 6, color_accent)
            rl.DrawCylinderEx([body_center[0] + 0.8 * scale, body_center[1] + 0.2 * scale, wing_z], [body_center[0] + 2.0 * scale, body_center[1] + 1.0 * scale, wing_z + 0.5 * facing * scale], 0.1 * scale, 0.3 * scale, 6, color_accent)
        elif wings_type == "bat":
            wing_z = body_center[2] + 0.3 * facing * scale
            color_bat = (40, 40, 40, 200)
            rl.DrawCylinderEx([body_center[0] - 0.8 * scale, body_center[1] + 0.1 * scale, wing_z], [body_center[0] - 2.2 * scale, body_center[1] + 0.8 * scale, wing_z + 0.4 * facing * scale], 0.05 * scale, 0.25 * scale, 6, color_bat)
            rl.DrawCylinderEx([body_center[0] + 0.8 * scale, body_center[1] + 0.1 * scale, wing_z], [body_center[0] + 2.2 * scale, body_center[1] + 0.8 * scale, wing_z + 0.4 * facing * scale], 0.05 * scale, 0.25 * scale, 6, color_bat)

        # Ears
        ears_type = app.get("ears", "none")
        if ears_type == "leaf":
            rl.DrawCylinderEx([head_center[0] - 0.5 * scale, head_center[1] + 0.5 * scale, head_center[2]], [head_center[0] - 1.2 * scale, head_center[1] + 1.2 * scale, head_center[2] - 0.3 * facing * scale], 0.18 * scale, 0.01 * scale, 8, color_accent)
            rl.DrawCylinderEx([head_center[0] + 0.5 * scale, head_center[1] + 0.5 * scale, head_center[2]], [head_center[0] + 1.2 * scale, head_center[1] + 1.2 * scale, head_center[2] - 0.3 * facing * scale], 0.18 * scale, 0.01 * scale, 8, color_accent)
        elif ears_type == "puppy":
            rl.DrawCylinderEx([head_center[0] - 0.55 * scale, head_center[1] + 0.4 * scale, head_center[2]], [head_center[0] - 0.8 * scale, head_center[1] - 0.3 * scale, head_center[2] - 0.1 * facing * scale], 0.16 * scale, 0.16 * scale, 8, color_accent)
            rl.DrawCylinderEx([head_center[0] + 0.55 * scale, head_center[1] + 0.4 * scale, head_center[2]], [head_center[0] + 0.8 * scale, head_center[1] - 0.3 * scale, head_center[2] - 0.1 * facing * scale], 0.16 * scale, 0.16 * scale, 8, color_accent)
        elif ears_type == "fins":
            rl.DrawCylinderEx([head_center[0] - 0.55 * scale, head_center[1] - 0.05 * scale, head_center[2]], [head_center[0] - 1.1 * scale, head_center[1] - 0.25 * scale, head_center[2] - 0.2 * facing * scale], 0.15 * scale, 0.02 * scale, 8, color_accent)
            rl.DrawCylinderEx([head_center[0] + 0.55 * scale, head_center[1] - 0.05 * scale, head_center[2]], [head_center[0] + 1.1 * scale, head_center[1] - 0.25 * scale, head_center[2] - 0.2 * facing * scale], 0.15 * scale, 0.02 * scale, 8, color_accent)
        elif ears_type == "pointy":
            rl.DrawCylinderEx([head_center[0] - 0.5 * scale, head_center[1] + 0.6 * scale, head_center[2]], [head_center[0] - 0.7 * scale, head_center[1] + 1.3 * scale, head_center[2] - 0.1 * facing * scale], 0.18 * scale, 0.05 * scale, 6, color_accent)
            rl.DrawCylinderEx([head_center[0] + 0.5 * scale, head_center[1] + 0.6 * scale, head_center[2]], [head_center[0] + 0.7 * scale, head_center[1] + 1.3 * scale, head_center[2] - 0.1 * facing * scale], 0.18 * scale, 0.05 * scale, 6, color_accent)

        # Tail
        tail_type = app.get("tail", "none")
        tail_base = Vector3.Create(body_center[0], body_center[1] - 0.3 * scale, body_center[2] + 0.7 * facing * scale)
        if tail_type == "leaf":
            tail_tip = Vector3.Create(body_center[0], body_center[1] + 0.5 * scale, body_center[2] + 1.7 * facing * scale)
            AI4Animation.Draw.Cylinder(tail_base, tail_tip, 0.15 * scale, 0.05 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(tail_tip[0], tail_tip[1], tail_tip[2]), 0.3 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(tail_base[0] * 0.4 + tail_tip[0] * 0.6, tail_base[1] * 0.4 + tail_tip[1] * 0.6, tail_base[2] * 0.4 + tail_tip[2] * 0.6), 0.25 * scale, 6, color_accent)
        elif tail_type == "flame":
            tail_mid = Vector3.Create(body_center[0], body_center[1] + 0.2 * scale, body_center[2] + 1.3 * facing * scale)
            tail_tip = Vector3.Create(body_center[0], body_center[1] + 0.8 * scale, body_center[2] + 1.6 * facing * scale)
            AI4Animation.Draw.Cylinder(tail_base, tail_mid, 0.12 * scale, 0.08 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(tail_tip, 0.35 * scale, 8, get_color((231, 76, 60, 255)))
            AI4Animation.Draw.Sphere(Vector3.Create(tail_tip[0], tail_tip[1] + 0.25 * scale, tail_tip[2] - 0.15 * facing * scale), 0.25 * scale, 6, get_color((243, 156, 18, 255)))
            AI4Animation.Draw.Sphere(Vector3.Create(tail_tip[0], tail_tip[1] + 0.45 * scale, tail_tip[2] - 0.25 * facing * scale), 0.15 * scale, 6, get_color((241, 196, 15, 255)))
        elif tail_type == "flipper":
            tail_end = Vector3.Create(body_center[0], body_center[1] - 0.4 * scale, body_center[2] + 1.5 * facing * scale)
            AI4Animation.Draw.Cylinder(tail_base, tail_end, 0.16 * scale, 0.1 * scale, 6, color_body)
            rl.DrawCylinderEx(tail_end, Vector3.Create(tail_end[0] - 0.45 * scale, tail_end[1] - 0.1 * scale, tail_end[2] + 0.3 * facing * scale), 0.08 * scale, 0.01 * scale, 6, color_accent)
            rl.DrawCylinderEx(tail_end, Vector3.Create(tail_end[0] + 0.45 * scale, tail_end[1] - 0.1 * scale, tail_end[2] + 0.3 * facing * scale), 0.08 * scale, 0.01 * scale, 6, color_accent)
        elif tail_type == "spikes":
            tail_end = Vector3.Create(body_center[0], body_center[1] - 0.1 * scale, body_center[2] + 1.4 * facing * scale)
            AI4Animation.Draw.Cylinder(tail_base, tail_end, 0.2 * scale, 0.12 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(tail_end[0], tail_end[1], tail_end[2]), 0.35 * scale, 6, color_accent)
        elif tail_type == "fluffy":
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0], body_center[1] + 0.2 * scale, body_center[2] + 1.0 * facing * scale), 0.45 * scale, 8, color_accent)

        # Head sprout
        if app.get("head_sprout", False):
            sprout_base = Vector3.Create(head_center[0], head_center[1] + 0.7 * scale, head_center[2])
            sprout_tip = Vector3.Create(head_center[0], head_center[1] + 1.2 * scale, head_center[2] - 0.2 * facing * scale)
            AI4Animation.Draw.Cylinder(sprout_base, sprout_tip, 0.06 * scale, 0.04 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(sprout_tip, 0.12 * scale, 6, get_color(rl.colors.YELLOW))

        # Horn
        horn_type = app.get("horn", "none")
        if horn_type == "single":
            horn_base = [head_center[0], head_center[1] + 0.6 * scale, head_center[2] - 0.4 * facing * scale]
            horn_tip = [head_center[0], head_center[1] + 1.2 * scale, head_center[2] - 0.8 * facing * scale]
            rl.DrawCylinderEx(horn_base, horn_tip, 0.15 * scale, 0.02 * scale, 6, color_accent)
        elif horn_type == "dual":
            horn_base_l = [head_center[0] - 0.35 * scale, head_center[1] + 0.7 * scale, head_center[2] - 0.2 * facing * scale]
            horn_tip_l = [head_center[0] - 0.5 * scale, head_center[1] + 1.3 * scale, head_center[2] - 0.4 * facing * scale]
            rl.DrawCylinderEx(horn_base_l, horn_tip_l, 0.1 * scale, 0.02 * scale, 6, color_accent)
            
            horn_base_r = [head_center[0] + 0.35 * scale, head_center[1] + 0.7 * scale, head_center[2] - 0.2 * facing * scale]
            horn_tip_r = [head_center[0] + 0.5 * scale, head_center[1] + 1.3 * scale, head_center[2] - 0.4 * facing * scale]
            rl.DrawCylinderEx(horn_base_r, horn_tip_r, 0.1 * scale, 0.02 * scale, 6, color_accent)

    def on_draw(self):
        # Draw battle platform
        # Dark forest green arena circle floor
        rl.DrawPlane([0.0, 0.0, 0.0], [30.0, 30.0], (28, 36, 24, 255))
        
        # Player platform
        rl.DrawPlane([-4.0, 0.02, -2.0], [4.5, 4.5], (56, 68, 88, 255))
        
        # Opponent platform
        rl.DrawPlane([4.0, 0.02, 2.0], [4.5, 4.5], (56, 68, 88, 255))

        # Render Pals
        self.draw_pal_3d(self.player)
        self.draw_pal_3d(self.opponent)

    def on_gui(self):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()

        # Draw HUD Box details
        # Opponent HUD (Top Left)
        self.draw_hud_box(sw * 0.06, sh * 0.08, sw * 0.28, sh * 0.12, self.opponent)
        
        # Player HUD (Bottom Right)
        self.draw_hud_box(sw * 0.66, sh * 0.60, sw * 0.28, sh * 0.12, self.player, show_numbers=True)

        # Draw Dialogue Console Box (Bottom Panel)
        panel_w = sw * 0.90
        panel_h = sh * 0.22
        panel_x = (sw - panel_w) / 2
        panel_y = sh * 0.74
        
        rl.DrawRectangle(int(panel_x), int(panel_y), int(panel_w), int(panel_h), COLOR_BG_PANEL)
        rl.DrawRectangleLinesEx([panel_x, panel_y, panel_w, panel_h], 3, COLOR_BORDER)

        if self.state == STATE_COMBAT_LOGS or self.state == STATE_INTRO:
            # Draw Dialogue Text
            # We want to display current_log
            AI4Animation.Draw.Text(
                self.current_log,
                (panel_x + sw * 0.03) / sw,
                (panel_y + sh * 0.04) / sh,
                0.028, COLOR_TEXT_PRIMARY, 0.0
            )
            # Arrow indicator
            if self.show_arrow:
                AI4Animation.Draw.Text(
                    "▼",
                    (panel_x + panel_w - sw * 0.03) / sw,
                    (panel_y + panel_h - sh * 0.05) / sh,
                    0.025, COLOR_TEXT_PRIMARY, 0.5
                )
                
        elif self.state == STATE_MOVE_SELECT:
            # Draw Move Buttons
            for btn in self.move_buttons:
                btn.draw(sw, sh)
                
            # Draw Hover Info Panel on the right side of the bottom panel
            hovered_btn = next((b for b in self.move_buttons if b.hovered), None)
            if hovered_btn:
                move = hovered_btn.move
                
                # Vertical Divider Line
                divider_x = panel_x + panel_w * 0.4
                rl.DrawLineEx([divider_x, panel_y + 15], [divider_x, panel_y + panel_h - 15], 2, COLOR_BORDER)
                
                details_x = (divider_x + sw * 0.02) / sw
                
                # Move details
                AI4Animation.Draw.Text(
                    f"Type: {move.type}",
                    details_x, (panel_y + sh * 0.03) / sh,
                    0.022, COLOR_TEXT_PRIMARY, 0.0
                )
                AI4Animation.Draw.Text(
                    f"Power: {move.power if move.power > 0 else '-'}",
                    details_x, (panel_y + sh * 0.07) / sh,
                    0.016, COLOR_TEXT_MUTED, 0.0
                )
                AI4Animation.Draw.Text(
                    move.description,
                    details_x, (panel_y + sh * 0.12) / sh,
                    0.016, COLOR_TEXT_PRIMARY, 0.0
                )

    def draw_hud_box(self, lx, ty, w, h, pal, show_numbers=False):
        # Draw background and border
        rl.DrawRectangle(int(lx), int(ty), int(w), int(h), COLOR_BG_PANEL)
        rl.DrawRectangleLinesEx([lx, ty, w, h], 2, COLOR_BORDER)

        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()

        # Pal Name
        AI4Animation.Draw.Text(
            pal.name,
            (lx + w * 0.05) / sw,
            (ty + h * 0.15) / sh,
            0.022, COLOR_TEXT_PRIMARY, 0.0
        )
        
        # Pal Level
        AI4Animation.Draw.Text(
            f"Lv{pal.level}",
            (lx + w * 0.95) / sw,
            (ty + h * 0.15) / sh,
            0.018, COLOR_TEXT_MUTED, 1.0
        )

        # HP Bar geometry
        bar_w = w * 0.90
        bar_h = h * 0.15
        bar_x = lx + w * 0.05
        bar_y = ty + h * 0.50

        # Background
        rl.DrawRectangle(int(bar_x), int(bar_y), int(bar_w), int(bar_h), COLOR_HP_BG)
        
        # Calculate HP Fill
        hp_percent = pal.hp / pal.max_hp
        if hp_percent > 0.5:
            hp_color = COLOR_HP_GREEN
        elif hp_percent > 0.2:
            hp_color = COLOR_HP_YELLOW
        else:
            hp_color = COLOR_HP_RED

        if hp_percent > 0:
            fill_w = bar_w * hp_percent
            rl.DrawRectangle(int(bar_x), int(bar_y), int(fill_w), int(bar_h), hp_color)

        # Health Numbers
        if show_numbers:
            AI4Animation.Draw.Text(
                f"{pal.hp} / {pal.max_hp}",
                (lx + w * 0.95) / sw,
                (ty + h * 0.72) / sh,
                0.015, COLOR_TEXT_PRIMARY, 1.0
            )
