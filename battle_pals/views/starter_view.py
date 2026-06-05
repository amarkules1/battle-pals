import arcade
import random
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_TYPE_FIRE, COLOR_TYPE_WATER, COLOR_TYPE_GRASS
)
from battle_pals.models.pal import create_leaflet, create_pyropup, create_aquasplash

class StarterCard:
    def __init__(self, name, pal_type, creator, x, y, width, height, color):
        self.name = name
        self.type = pal_type
        self.creator = creator
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hovered = False

    def is_mouse_over(self, mx, my):
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        bottom = self.y - self.height / 2
        top = self.y + self.height / 2
        return left <= mx <= right and bottom <= my <= top

    def draw(self):
        # Determine background and border colors based on hover state
        bg_color = COLOR_BG_PANEL
        border_color = self.color if self.hovered else COLOR_BORDER
        border_width = 3 if self.hovered else 2

        # Draw card panel
        arcade.draw_lbwh_rectangle_filled(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height, bg_color)
        arcade.draw_lbwh_rectangle_outline(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height, border_color, border_width)

        # Draw Pal Symbol / Avatar (Procedural drawing)
        avatar_y = self.y + 40
        arcade.draw_circle_filled(self.x, avatar_y, 40, self.color)
        # Draw eyes and a cute mouth on the symbol
        arcade.draw_circle_filled(self.x - 12, avatar_y + 8, 5, arcade.color.BLACK)
        arcade.draw_circle_filled(self.x + 12, avatar_y + 8, 5, arcade.color.BLACK)
        # Cute mouth
        arcade.draw_arc_outline(self.x, avatar_y - 8, 12, 10, arcade.color.BLACK, 180, 360, 3)

        # Draw details
        arcade.draw_text(
            self.name,
            self.x, self.y - 20,
            COLOR_TEXT_PRIMARY,
            font_size=18,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            f"Type: {self.type}",
            self.x, self.y - 45,
            self.color,
            font_size=12,
            anchor_x="center"
        )
        
        # Display base stat summary
        temp_pal = self.creator()
        stats_text = f"HP:{temp_pal.max_hp} ATK:{temp_pal.base_attack} DEF:{temp_pal.base_defense}"
        arcade.draw_text(
            stats_text,
            self.x, self.y - 70,
            COLOR_TEXT_MUTED,
            font_size=10,
            anchor_x="center"
        )

class StarterView(arcade.View):
    def __init__(self):
        super().__init__()
        self.cards = []

    def on_show_view(self):
        arcade.set_background_color(COLOR_BG_DARK)
        
        # Generate cards centered horizontally
        card_width = 180
        card_height = 240
        spacing = 40
        start_x = (self.window.width - (3 * card_width + 2 * spacing)) / 2 + card_width / 2
        y = self.window.height / 2 - 10

        self.cards = [
            StarterCard("Leaflet", "Grass", create_leaflet, start_x, y, card_width, card_height, COLOR_TYPE_GRASS),
            StarterCard("Pyropup", "Fire", create_pyropup, start_x + (card_width + spacing), y, card_width, card_height, COLOR_TYPE_FIRE),
            StarterCard("Aquasplash", "Water", create_aquasplash, start_x + 2 * (card_width + spacing), y, card_width, card_height, COLOR_TYPE_WATER)
        ]

    def on_draw(self):
        self.clear()

        # Main Title
        arcade.draw_text(
            "CHOOSE YOUR STARTER PAL",
            self.window.width / 2,
            self.window.height - 80,
            COLOR_TEXT_PRIMARY,
            font_size=28,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            "Click on a Pal to begin your battle arena trial",
            self.window.width / 2,
            self.window.height - 110,
            COLOR_TEXT_MUTED,
            font_size=13,
            anchor_x="center"
        )

        # Draw Cards
        for card in self.cards:
            card.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # Update hover states
        for card in self.cards:
            card.hovered = card.is_mouse_over(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        for card in self.cards:
            if card.is_mouse_over(x, y):
                # Player selection
                player_pal = card.creator()
                
                # Opponent selection (random from other two)
                others = [c for c in self.cards if c.name != card.name]
                opponent_card = random.choice(others)
                opponent_pal = opponent_card.creator()

                # Transition to BattleView
                from battle_pals.views.battle_view import BattleView
                battle_view = BattleView(player_pal, opponent_pal)
                self.window.show_view(battle_view)
                break
