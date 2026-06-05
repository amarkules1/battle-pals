import arcade
import random
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_HP_GREEN, COLOR_HP_YELLOW, COLOR_HP_RED, COLOR_HP_BG,
    COLOR_TYPE_FIRE, COLOR_TYPE_WATER, COLOR_TYPE_GRASS
)
from battle_pals.views.game_over_view import GameOverView

# Battle States
STATE_INTRO = 0
STATE_MOVE_SELECT = 1
STATE_COMBAT_LOGS = 2

class MoveButton:
    def __init__(self, move, x, y, width, height):
        self.move = move
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hovered = False

    def is_mouse_over(self, mx, my):
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        bottom = self.y - self.height / 2
        top = self.y + self.height / 2
        return left <= mx <= right and bottom <= my <= top

    def draw(self):
        # Match type colors
        type_colors = {
            "Fire": COLOR_TYPE_FIRE,
            "Water": COLOR_TYPE_WATER,
            "Grass": COLOR_TYPE_GRASS,
            "Normal": COLOR_TEXT_MUTED
        }
        accent_color = type_colors.get(self.move.type, COLOR_BORDER)
        
        bg_color = COLOR_BG_PANEL if not self.hovered else (45, 52, 68)
        border_color = accent_color if self.hovered else COLOR_BORDER
        border_width = 3 if self.hovered else 2

        arcade.draw_lbwh_rectangle_filled(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height, bg_color)
        arcade.draw_lbwh_rectangle_outline(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height, border_color, border_width)

        arcade.draw_text(
            self.move.name,
            self.x, self.y,
            COLOR_TEXT_PRIMARY,
            font_size=14,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

class BattleView(arcade.View):
    def __init__(self, player_pal, opponent_pal):
        super().__init__()
        self.player = player_pal
        self.opponent = opponent_pal
        
        # Reset modifiers
        self.player.reset_battle_stats()
        self.opponent.reset_battle_stats()

        self.state = STATE_INTRO
        self.log_queue = []
        self.current_log = ""
        
        # UI controls
        self.move_buttons = []
        
        # Blinking arrow timers
        self.blink_timer = 0.0
        self.show_arrow = True

    def on_show_view(self):
        arcade.set_background_color(COLOR_BG_DARK)
        
        # Log introductory messages
        self.log_queue = [
            f"A wild {self.opponent.name} appeared!",
            f"Go! {self.player.name}!"
        ]
        self.advance_log()

        # Build Move Buttons
        btn_width = 170
        btn_height = 45
        spacing_x = 20
        spacing_y = 15
        
        # 2x2 Layout on the bottom panel
        start_x = 120
        start_y = 90
        
        for idx, move in enumerate(self.player.moves):
            row = idx // 2
            col = idx % 2
            bx = start_x + col * (btn_width + spacing_x)
            by = start_y - row * (btn_height + spacing_y)
            self.move_buttons.append(MoveButton(move, bx, by, btn_width, btn_height))

    def advance_log(self):
        """Advances to the next message in the log, checking for end-of-battle conditions."""
        if self.log_queue:
            self.state = STATE_COMBAT_LOGS
            self.current_log = self.log_queue.pop(0)
        else:
            # Check for faint
            if self.player.hp <= 0:
                self.window.show_view(GameOverView(victory=False, player_pal=self.player, opponent_pal=self.opponent))
            elif self.opponent.hp <= 0:
                self.window.show_view(GameOverView(victory=True, player_pal=self.player, opponent_pal=self.opponent))
            else:
                # Return to move selection
                self.state = STATE_MOVE_SELECT
                self.current_log = ""

    def execute_turn(self, player_move):
        """Computes combat turns using Speeds to determine priority."""
        self.log_queue = []
        
        # Simple AI Move Selection (Randomly choose an available move)
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

    def on_update(self, delta_time):
        # Blinking cursor for dialogue
        self.blink_timer += delta_time
        if self.blink_timer >= 0.5:
            self.blink_timer = 0.0
            self.show_arrow = not self.show_arrow

    def on_draw(self):
        self.clear()

        # RENDER ARENA CREATURES
        # Draw Opponent Pal (Top Right)
        opp_color = COLOR_TYPE_FIRE if self.opponent.type == "Fire" else (COLOR_TYPE_WATER if self.opponent.type == "Water" else COLOR_TYPE_GRASS)
        arcade.draw_circle_filled(600, 360, 60, opp_color)
        # Face details
        arcade.draw_circle_filled(580, 370, 7, arcade.color.BLACK)
        arcade.draw_circle_filled(620, 370, 7, arcade.color.BLACK)
        arcade.draw_arc_outline(600, 345, 18, 12, arcade.color.BLACK, 0, 180, 3)

        # Draw Player Pal (Bottom Left)
        plr_color = COLOR_TYPE_FIRE if self.player.type == "Fire" else (COLOR_TYPE_WATER if self.player.type == "Water" else COLOR_TYPE_GRASS)
        arcade.draw_circle_filled(200, 240, 60, plr_color)
        # Face details
        arcade.draw_circle_filled(180, 250, 7, arcade.color.BLACK)
        arcade.draw_circle_filled(220, 250, 7, arcade.color.BLACK)
        arcade.draw_arc_outline(200, 225, 18, 12, arcade.color.BLACK, 180, 360, 3)

        # RENDER HUD BOXES
        # Opponent HUD (Top Left)
        self.draw_hud_box(100, 420, 300, 80, self.opponent)

        # Player HUD (Bottom Right)
        self.draw_hud_box(400, 180, 300, 80, self.player, show_numbers=True)

        # RENDER CONSOLE BOX (Bottom Panel)
        w = self.window.width - 40
        h = 110
        arcade.draw_lbwh_rectangle_filled(self.window.width / 2 - w / 2, 75 - h / 2, w, h, COLOR_BG_PANEL)
        arcade.draw_lbwh_rectangle_outline(self.window.width / 2 - w / 2, 75 - h / 2, w, h, COLOR_BORDER, 3)

        if self.state == STATE_COMBAT_LOGS or self.state == STATE_INTRO:
            # Draw Current Log Line
            arcade.draw_text(
                self.current_log,
                50, 80,
                COLOR_TEXT_PRIMARY,
                font_size=18,
                bold=True
            )
            # Arrow indicator
            if self.show_arrow:
                arcade.draw_text(
                    "▼",
                    self.window.width - 60, 40,
                    COLOR_TEXT_PRIMARY,
                    font_size=16
                )
                
        elif self.state == STATE_MOVE_SELECT:
            # Draw Move Selection interface
            for btn in self.move_buttons:
                btn.draw()
                
            # Draw hover description on the right side of the bottom panel
            hovered_btn = next((b for b in self.move_buttons if b.hovered), None)
            if hovered_btn:
                move = hovered_btn.move
                # Box divider line
                arcade.draw_line(500, 120, 500, 30, COLOR_BORDER, 2)
                
                arcade.draw_text(
                    f"Type: {move.type}",
                    520, 100,
                    COLOR_TEXT_PRIMARY,
                    font_size=13,
                    bold=True
                )
                arcade.draw_text(
                    f"Power: {move.power if move.power > 0 else '-'}",
                    520, 80,
                    COLOR_TEXT_MUTED,
                    font_size=11
                )
                arcade.draw_text(
                    move.description,
                    520, 45,
                    COLOR_TEXT_PRIMARY,
                    font_size=10,
                    multiline=True,
                    width=240
                )

    def draw_hud_box(self, x, y, width, height, pal, show_numbers=False):
        # Background panel
        arcade.draw_lbwh_rectangle_filled(x, y, width, height, COLOR_BG_PANEL)
        arcade.draw_lbwh_rectangle_outline(x, y, width, height, COLOR_BORDER, 2)

        # Name and Level
        arcade.draw_text(
            pal.name,
            x + 15, y + height - 25,
            COLOR_TEXT_PRIMARY,
            font_size=14,
            bold=True
        )
        
        arcade.draw_text(
            f"Lv{pal.level}",
            x + width - 60, y + height - 25,
            COLOR_TEXT_MUTED,
            font_size=12,
            bold=True
        )

        # HP Bar
        hp_percent = pal.hp / pal.max_hp
        bar_width = width - 30
        bar_height = 12
        bar_x = x + 15
        bar_y = y + 25

        # HP Bar Background
        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, COLOR_HP_BG)
        
        # Color based on HP status
        if hp_percent > 0.5:
            hp_color = COLOR_HP_GREEN
        elif hp_percent > 0.2:
            hp_color = COLOR_HP_YELLOW
        else:
            hp_color = COLOR_HP_RED

        # HP Bar Fill
        if hp_percent > 0:
            fill_w = bar_width * hp_percent
            arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, fill_w, bar_height, hp_color)

        # Health Numbers (Optional, typically for Player)
        if show_numbers:
            arcade.draw_text(
                f"{pal.hp} / {pal.max_hp}",
                x + width - 90, y + 8,
                COLOR_TEXT_PRIMARY,
                font_size=11,
                bold=True
            )

    def on_mouse_motion(self, x, y, dx, dy):
        if self.state == STATE_MOVE_SELECT:
            for btn in self.move_buttons:
                btn.hovered = btn.is_mouse_over(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == STATE_COMBAT_LOGS or self.state == STATE_INTRO:
            self.advance_log()
        elif self.state == STATE_MOVE_SELECT:
            for btn in self.move_buttons:
                if btn.is_mouse_over(x, y):
                    self.execute_turn(btn.move)
                    break
