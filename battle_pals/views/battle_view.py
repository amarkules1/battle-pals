import raylib as rl
import random
import math
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_HP_GREEN, COLOR_HP_YELLOW, COLOR_HP_RED, COLOR_HP_BG,
    COLOR_TYPE_FIRE, COLOR_TYPE_WATER, COLOR_TYPE_GRASS
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
            "Fire": COLOR_TYPE_FIRE,
            "Water": COLOR_TYPE_WATER,
            "Grass": COLOR_TYPE_GRASS,
            "Normal": COLOR_TEXT_MUTED
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

        # Define common colors
        color_eye_bg = rl.colors.BLACK
        color_eye_fg = rl.colors.WHITE
        color_mouth = (231, 76, 60, 255) # Rose/red
        color_cheek = (255, 128, 128, 128) # Translucent blush

        # --- 3D Character Rendering ---
        if pal.type == "Grass":
            color_body = get_color((115, 198, 80, 255))   # Pale green
            color_accent = get_color((46, 204, 113, 255))  # Emerald green
            color_belly = get_color((215, 235, 150, 255))   # Yellow green
            
            # 1. Body & Head
            body_center = Vector3.Create(pos[0], pos[1] - 0.2 * scale, pos[2] + 0.1 * facing * scale)
            head_center = Vector3.Create(pos[0], pos[1] + 0.7 * scale, pos[2] - 0.3 * facing * scale)
            AI4Animation.Draw.Sphere(body_center, 1.0 * scale, 12, color_body)
            AI4Animation.Draw.Sphere(head_center, 0.85 * scale, 12, color_body)
            
            # 2. Chest Belly Patch
            belly_center = Vector3.Create(pos[0], pos[1] - 0.1 * scale, pos[2] - 0.7 * facing * scale)
            AI4Animation.Draw.Sphere(belly_center, 0.5 * scale, 8, color_belly)
            
            # 3. Face
            # Eyes
            eye_y = head_center[1] + 0.15 * scale
            eye_z = head_center[2] - 0.65 * facing * scale
            eye_xl = head_center[0] - 0.3 * scale
            eye_xr = head_center[0] + 0.3 * scale
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xl, eye_y, eye_z), 0.12 * scale, 6, get_color(color_eye_bg))
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xr, eye_y, eye_z), 0.12 * scale, 6, get_color(color_eye_bg))
            # Eye Highlights
            hl_z = eye_z - 0.08 * facing * scale
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xl + 0.04 * scale, eye_y + 0.04 * scale, hl_z), 0.04 * scale, 4, get_color(color_eye_fg))
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xr + 0.04 * scale, eye_y + 0.04 * scale, hl_z), 0.04 * scale, 4, get_color(color_eye_fg))
            # Cheeks
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] - 0.45 * scale, head_center[1] - 0.05 * scale, eye_z), 0.12 * scale, 6, get_color(color_cheek))
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] + 0.45 * scale, head_center[1] - 0.05 * scale, eye_z), 0.12 * scale, 6, get_color(color_cheek))
            # Mouth
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0], head_center[1] - 0.15 * scale, eye_z - 0.05 * facing * scale), 0.07 * scale, 6, get_color(color_mouth))

            # 4. Leaf Ears (Decorations)
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0] - 0.5 * scale, head_center[1] + 0.3 * scale, head_center[2]),
                Vector3.Create(head_center[0] - 1.2 * scale, head_center[1] + 1.2 * scale, head_center[2] - 0.3 * facing * scale),
                0.18 * scale, 0.01 * scale, 8, color_accent
            )
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0] + 0.5 * scale, head_center[1] + 0.3 * scale, head_center[2]),
                Vector3.Create(head_center[0] + 1.2 * scale, head_center[1] + 1.2 * scale, head_center[2] - 0.3 * facing * scale),
                0.18 * scale, 0.01 * scale, 8, color_accent
            )
            
            # 5. Top Head Sprout
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0], head_center[1] + 0.7 * scale, head_center[2]),
                Vector3.Create(head_center[0], head_center[1] + 1.2 * scale, head_center[2] - 0.2 * facing * scale),
                0.06 * scale, 0.04 * scale, 6, color_accent
            )
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0], head_center[1] + 1.2 * scale, head_center[2] - 0.2 * facing * scale), 0.12 * scale, 6, get_color(rl.colors.YELLOW))

            # 6. Stout Lizard Legs (4 limbs)
            leg_offsets = [
                (-0.4, -0.3, -0.4),
                (0.4, -0.3, -0.4),
                (-0.4, -0.3, 0.4),
                (0.4, -0.3, 0.4)
            ]
            for ox, oy, oz in leg_offsets:
                leg_start = Vector3.Create(body_center[0] + ox * scale, body_center[1] + oy * scale, body_center[2] + oz * facing * scale)
                leg_end = Vector3.Create(body_center[0] + ox * scale, body_center[1] - 0.9 * scale, body_center[2] + oz * facing * scale)
                AI4Animation.Draw.Cylinder(leg_start, leg_end, 0.16 * scale, 0.16 * scale, 6, color_body)
                AI4Animation.Draw.Sphere(leg_end, 0.22 * scale, 6, color_accent) # feet

            # 7. Leaf Tail
            tail_base = Vector3.Create(body_center[0], body_center[1] - 0.3 * scale, body_center[2] + 0.8 * facing * scale)
            tail_tip = Vector3.Create(body_center[0], body_center[1] + 0.5 * scale, body_center[2] + 1.7 * facing * scale)
            AI4Animation.Draw.Cylinder(tail_base, tail_tip, 0.15 * scale, 0.05 * scale, 6, color_body)
            # Decorative tail leaf spheres
            AI4Animation.Draw.Sphere(Vector3.Create(tail_tip[0], tail_tip[1], tail_tip[2]), 0.3 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(tail_base[0] * 0.4 + tail_tip[0] * 0.6, tail_base[1] * 0.4 + tail_tip[1] * 0.6, tail_base[2] * 0.4 + tail_tip[2] * 0.6), 0.25 * scale, 6, color_accent)

        elif pal.type == "Fire":
            color_body = get_color((243, 156, 18, 255))   # Bright Orange
            color_accent = get_color((231, 76, 60, 255))  # Red
            color_belly = get_color((241, 196, 15, 255))   # Yellow
            
            # 1. Body & Head
            body_center = Vector3.Create(pos[0], pos[1] - 0.2 * scale, pos[2] + 0.1 * facing * scale)
            head_center = Vector3.Create(pos[0], pos[1] + 0.7 * scale, pos[2] - 0.3 * facing * scale)
            AI4Animation.Draw.Sphere(body_center, 0.95 * scale, 12, color_body)
            AI4Animation.Draw.Sphere(head_center, 0.85 * scale, 12, color_body)
            
            # 2. Chest Flame Bib
            belly_center = Vector3.Create(pos[0], pos[1] - 0.15 * scale, pos[2] - 0.65 * facing * scale)
            AI4Animation.Draw.Sphere(belly_center, 0.45 * scale, 8, color_belly)
            
            # 3. Snout & Nose
            snout_center = Vector3.Create(head_center[0], head_center[1] - 0.05 * scale, head_center[2] - 0.7 * facing * scale)
            AI4Animation.Draw.Sphere(snout_center, 0.22 * scale, 6, color_body)
            nose_center = Vector3.Create(snout_center[0], snout_center[1] + 0.08 * scale, snout_center[2] - 0.15 * facing * scale)
            AI4Animation.Draw.Sphere(nose_center, 0.06 * scale, 4, get_color(color_eye_bg))

            # 4. Face
            # Eyes
            eye_y = head_center[1] + 0.15 * scale
            eye_z = head_center[2] - 0.65 * facing * scale
            eye_xl = head_center[0] - 0.3 * scale
            eye_xr = head_center[0] + 0.3 * scale
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xl, eye_y, eye_z), 0.12 * scale, 6, get_color(color_eye_bg))
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xr, eye_y, eye_z), 0.12 * scale, 6, get_color(color_eye_bg))
            # Eye Highlights
            hl_z = eye_z - 0.08 * facing * scale
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xl + 0.04 * scale, eye_y + 0.04 * scale, hl_z), 0.04 * scale, 4, get_color(color_eye_fg))
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xr + 0.04 * scale, eye_y + 0.04 * scale, hl_z), 0.04 * scale, 4, get_color(color_eye_fg))
            # Cheeks
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] - 0.45 * scale, head_center[1] - 0.05 * scale, eye_z), 0.12 * scale, 6, get_color(color_cheek))
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] + 0.45 * scale, head_center[1] - 0.05 * scale, eye_z), 0.12 * scale, 6, get_color(color_cheek))

            # 5. Floppy/Pointy Puppy Ears
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0] - 0.55 * scale, head_center[1] + 0.4 * scale, head_center[2]),
                Vector3.Create(head_center[0] - 0.8 * scale, head_center[1] + 1.1 * scale, head_center[2] - 0.1 * facing * scale),
                0.16 * scale, 0.04 * scale, 8, color_accent
            )
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0] + 0.55 * scale, head_center[1] + 0.4 * scale, head_center[2]),
                Vector3.Create(head_center[0] + 0.8 * scale, head_center[1] + 1.1 * scale, head_center[2] - 0.1 * facing * scale),
                0.16 * scale, 0.04 * scale, 8, color_accent
            )

            # 6. Dog Legs
            leg_offsets = [
                (-0.35, -0.3, -0.4),
                (0.35, -0.3, -0.4),
                (-0.35, -0.3, 0.4),
                (0.35, -0.3, 0.4)
            ]
            for ox, oy, oz in leg_offsets:
                leg_start = Vector3.Create(body_center[0] + ox * scale, body_center[1] + oy * scale, body_center[2] + oz * facing * scale)
                leg_end = Vector3.Create(body_center[0] + ox * scale, body_center[1] - 0.9 * scale, body_center[2] + oz * facing * scale)
                AI4Animation.Draw.Cylinder(leg_start, leg_end, 0.14 * scale, 0.14 * scale, 6, color_body)
                AI4Animation.Draw.Sphere(leg_end, 0.2 * scale, 6, color_belly) # yellow paws

            # 7. Flaming Tail
            tail_base = Vector3.Create(body_center[0], body_center[1] - 0.3 * scale, body_center[2] + 0.7 * facing * scale)
            tail_mid = Vector3.Create(body_center[0], body_center[1] + 0.2 * scale, body_center[2] + 1.3 * facing * scale)
            tail_tip = Vector3.Create(body_center[0], body_center[1] + 0.8 * scale, body_center[2] + 1.6 * facing * scale)
            AI4Animation.Draw.Cylinder(tail_base, tail_mid, 0.12 * scale, 0.08 * scale, 6, color_accent)
            # Flame spheres at the tip
            AI4Animation.Draw.Sphere(tail_tip, 0.35 * scale, 8, get_color((231, 76, 60, 255))) # red
            AI4Animation.Draw.Sphere(Vector3.Create(tail_tip[0], tail_tip[1] + 0.25 * scale, tail_tip[2] - 0.15 * facing * scale), 0.25 * scale, 6, get_color((243, 156, 18, 255))) # orange
            AI4Animation.Draw.Sphere(Vector3.Create(tail_tip[0], tail_tip[1] + 0.45 * scale, tail_tip[2] - 0.25 * facing * scale), 0.15 * scale, 6, get_color((241, 196, 15, 255))) # yellow

        elif pal.type == "Water":
            color_body = get_color((52, 152, 219, 255))   # Bright Blue
            color_accent = get_color((174, 214, 241, 255)) # Light Blue
            color_belly = get_color((240, 248, 255, 255))  # Alice White
            
            # 1. Body & Head
            body_center = Vector3.Create(pos[0], pos[1] - 0.2 * scale, pos[2] + 0.1 * facing * scale)
            head_center = Vector3.Create(pos[0], pos[1] + 0.7 * scale, pos[2] - 0.3 * facing * scale)
            AI4Animation.Draw.Sphere(body_center, 1.05 * scale, 12, color_body)
            AI4Animation.Draw.Sphere(head_center, 0.85 * scale, 12, color_body)
            
            # 2. White Belly Patch
            belly_center = Vector3.Create(pos[0], pos[1] - 0.1 * scale, pos[2] - 0.7 * facing * scale)
            AI4Animation.Draw.Sphere(belly_center, 0.5 * scale, 8, color_belly)

            # 3. Face
            # Eyes
            eye_y = head_center[1] + 0.15 * scale
            eye_z = head_center[2] - 0.65 * facing * scale
            eye_xl = head_center[0] - 0.3 * scale
            eye_xr = head_center[0] + 0.3 * scale
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xl, eye_y, eye_z), 0.12 * scale, 6, get_color(color_eye_bg))
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xr, eye_y, eye_z), 0.12 * scale, 6, get_color(color_eye_bg))
            # Eye Highlights
            hl_z = eye_z - 0.08 * facing * scale
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xl + 0.04 * scale, eye_y + 0.04 * scale, hl_z), 0.04 * scale, 4, get_color(color_eye_fg))
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xr + 0.04 * scale, eye_y + 0.04 * scale, hl_z), 0.04 * scale, 4, get_color(color_eye_fg))
            # Cheeks
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] - 0.45 * scale, head_center[1] - 0.05 * scale, eye_z), 0.12 * scale, 6, get_color(color_cheek))
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] + 0.45 * scale, head_center[1] - 0.05 * scale, eye_z), 0.12 * scale, 6, get_color(color_cheek))
            # Mouth
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0], head_center[1] - 0.15 * scale, eye_z - 0.05 * facing * scale), 0.07 * scale, 6, get_color(color_mouth))

            # 4. Flipper Ears (Side Fins)
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0] - 0.55 * scale, head_center[1] - 0.05 * scale, head_center[2]),
                Vector3.Create(head_center[0] - 1.1 * scale, head_center[1] - 0.25 * scale, head_center[2] - 0.2 * facing * scale),
                0.15 * scale, 0.02 * scale, 8, color_accent
            )
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0] + 0.55 * scale, head_center[1] - 0.05 * scale, head_center[2]),
                Vector3.Create(head_center[0] + 1.1 * scale, head_center[1] - 0.25 * scale, head_center[2] - 0.2 * facing * scale),
                0.15 * scale, 0.02 * scale, 8, color_accent
            )

            # 5. Dorsal Fin on Back
            AI4Animation.Draw.Cylinder(
                Vector3.Create(body_center[0], body_center[1] + 0.5 * scale, body_center[2] + 0.3 * facing * scale),
                Vector3.Create(body_center[0], body_center[1] + 1.3 * scale, body_center[2] + 0.9 * facing * scale),
                0.16 * scale, 0.01 * scale, 6, color_body
            )

            # 6. Otter Flippers (Limbs)
            flipper_offsets = [
                (-0.45, -0.4, -0.4, -1.0, -0.7, -0.6),
                (0.45, -0.4, -0.4, 1.0, -0.7, -0.6)
            ]
            for ox, oy, oz, dx, dy, dz in flipper_offsets:
                start_p = Vector3.Create(body_center[0] + ox * scale, body_center[1] + oy * scale, body_center[2] + oz * facing * scale)
                end_p = Vector3.Create(body_center[0] + dx * scale, body_center[1] + dy * scale, body_center[2] + dz * facing * scale)
                AI4Animation.Draw.Cylinder(start_p, end_p, 0.18 * scale, 0.05 * scale, 6, color_body)
                AI4Animation.Draw.Sphere(end_p, 0.1 * scale, 6, color_accent) # Flipper tip

            # 7. Seal Tail (Whale/Otter Flipper)
            tail_base = Vector3.Create(body_center[0], body_center[1] - 0.3 * scale, body_center[2] + 0.8 * facing * scale)
            tail_end = Vector3.Create(body_center[0], body_center[1] - 0.4 * scale, body_center[2] + 1.5 * facing * scale)
            AI4Animation.Draw.Cylinder(tail_base, tail_end, 0.16 * scale, 0.1 * scale, 6, color_body)
            # V-Shape tail fins
            AI4Animation.Draw.Cylinder(
                tail_end,
                Vector3.Create(tail_end[0] - 0.45 * scale, tail_end[1] - 0.1 * scale, tail_end[2] + 0.3 * facing * scale),
                0.08 * scale, 0.01 * scale, 6, color_accent
            )
            AI4Animation.Draw.Cylinder(
                tail_end,
                Vector3.Create(tail_end[0] + 0.45 * scale, tail_end[1] - 0.1 * scale, tail_end[2] + 0.3 * facing * scale),
                0.08 * scale, 0.01 * scale, 6, color_accent
            )

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
