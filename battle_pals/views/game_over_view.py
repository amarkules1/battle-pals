import raylib as rl
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED
)
from ai4animation import AI4Animation, Vector3

class GameOverView:
    def __init__(self, victory, player_pal, opponent_pal):
        self.victory = victory
        self.player = player_pal
        self.opponent = opponent_pal
        self.btn_hovered = False

        # Button geometry
        self.btn_w = 300
        self.btn_h = 70
        self.btn_x = 0
        self.btn_y = 0

    def on_show_view(self):
        pass

    def on_update(self, dt):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        
        self.btn_x = (sw - self.btn_w) / 2
        self.btn_y = sh * 0.55

        # Check mouse hover
        mouse_pos = rl.GetMousePosition()
        mx, my = mouse_pos.x, mouse_pos.y
        self.btn_hovered = (self.btn_x <= mx <= self.btn_x + self.btn_w) and (self.btn_y <= my <= self.btn_y + self.btn_h)

        # Handle mouse press
        if rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT) and self.btn_hovered:
            from battle_pals.views.starter_view import StarterView
            from battle_pals.game import BattlePalsGame
            BattlePalsGame.get_instance().switch_to_view(StarterView())

    def on_draw(self):
        # Draw background arena floor
        # Dark forest green arena plane
        rl.DrawPlane([0.0, 0.0, 0.0], [30.0, 30.0], (28, 36, 24, 255))

    def on_gui(self):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()

        # Outcome title
        title = "VICTORY!" if self.victory else "DEFEAT..."
        title_color = (46, 204, 113, 255) if self.victory else (231, 76, 60, 255)

        # Draw Title
        AI4Animation.Draw.Text(
            title,
            0.5, 0.22, 0.07, title_color, 0.5
        )

        # Summary text
        if self.victory:
            summary = f"Your {self.player.name} defeated the wild {self.opponent.name}!"
        else:
            summary = f"Your {self.player.name} fainted in battle against {self.opponent.name}."

        AI4Animation.Draw.Text(
            summary,
            0.5, 0.35, 0.022, COLOR_TEXT_PRIMARY, 0.5
        )

        # Drawing the "Play Again" button
        bg_color = (45, 52, 68, 255) if self.btn_hovered else COLOR_BG_PANEL
        border_color = (46, 204, 113, 255) if self.btn_hovered else COLOR_BORDER
        border_thickness = 4 if self.btn_hovered else 2

        rl.DrawRectangle(int(self.btn_x), int(self.btn_y), int(self.btn_w), int(self.btn_h), bg_color)
        rl.DrawRectangleLinesEx([self.btn_x, self.btn_y, self.btn_w, self.btn_h], border_thickness, border_color)

        btn_cx_norm = (self.btn_x + self.btn_w / 2) / sw
        btn_cy_norm = (self.btn_y + self.btn_h / 2 - 12) / sh

        AI4Animation.Draw.Text(
            "PLAY AGAIN",
            btn_cx_norm, btn_cy_norm,
            0.024, COLOR_TEXT_PRIMARY, 0.5
        )
