import arcade
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED
)

class GameOverView(arcade.View):
    def __init__(self, victory, player_pal, opponent_pal):
        super().__init__()
        self.victory = victory
        self.player = player_pal
        self.opponent = opponent_pal
        self.btn_hovered = False

        # Button geometry
        self.btn_width = 240
        self.btn_height = 55
        self.btn_x = 0
        self.btn_y = 0

    def on_show_view(self):
        arcade.set_background_color(COLOR_BG_DARK)
        self.btn_x = self.window.width / 2
        self.btn_y = self.window.height / 2 - 100

    def on_draw(self):
        self.clear()

        # Outcome title
        title = "VICTORY!" if self.victory else "DEFEAT..."
        title_color = arcade.color.AQUAMARINE if self.victory else arcade.color.CORAL

        arcade.draw_text(
            title,
            self.window.width / 2,
            self.window.height - 150,
            title_color,
            font_size=42,
            anchor_x="center",
            bold=True
        )

        # Detailed logs/summary
        if self.victory:
            summary = f"Your {self.player.name} defeated the wild {self.opponent.name}!"
        else:
            summary = f"Your {self.player.name} fainted in battle against {self.opponent.name}."

        arcade.draw_text(
            summary,
            self.window.width / 2,
            self.window.height - 210,
            COLOR_TEXT_PRIMARY,
            font_size=16,
            anchor_x="center"
        )

        # Drawing the "Play Again" button
        bg_color = (45, 52, 68) if self.btn_hovered else COLOR_BG_PANEL
        border_color = arcade.color.AQUAMARINE if self.btn_hovered else COLOR_BORDER
        border_width = 3 if self.btn_hovered else 2

        arcade.draw_lbwh_rectangle_filled(self.btn_x - self.btn_width / 2, self.btn_y - self.btn_height / 2, self.btn_width, self.btn_height, bg_color)
        arcade.draw_lbwh_rectangle_outline(self.btn_x - self.btn_width / 2, self.btn_y - self.btn_height / 2, self.btn_width, self.btn_height, border_color, border_width)

        arcade.draw_text(
            "PLAY AGAIN",
            self.btn_x,
            self.btn_y,
            COLOR_TEXT_PRIMARY,
            font_size=16,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    def is_over_button(self, mx, my):
        left = self.btn_x - self.btn_width / 2
        right = self.btn_x + self.btn_width / 2
        bottom = self.btn_y - self.btn_height / 2
        top = self.btn_y + self.btn_height / 2
        return left <= mx <= right and bottom <= my <= top

    def on_mouse_motion(self, x, y, dx, dy):
        self.btn_hovered = self.is_over_button(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_over_button(x, y):
            # Return to starter view selection
            from battle_pals.views.starter_view import StarterView
            self.window.show_view(StarterView())
