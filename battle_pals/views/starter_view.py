import raylib as rl
import random
from battle_pals.constants import (
    COLOR_BG_DARK, COLOR_BG_PANEL, COLOR_BORDER, 
    COLOR_TEXT_PRIMARY, COLOR_TEXT_MUTED,
    COLOR_TYPE_FIRE, COLOR_TYPE_WATER, COLOR_TYPE_GRASS
)
from battle_pals.models.pal import create_leaflet, create_pyropup, create_aquasplash
from ai4animation import AI4Animation, Vector3

class StarterCard:
    def __init__(self, name, pal_type, creator, color):
        self.name = name
        self.type = pal_type
        self.creator = creator
        self.color = color
        self.hovered = False
        
        # Dimensions determined during draw
        self.lx = 0
        self.ty = 0
        self.w = 0
        self.h = 0

    def check_mouse(self, mx, my, lx, ty, w, h):
        self.lx = lx
        self.ty = ty
        self.w = w
        self.h = h
        self.hovered = (lx <= mx <= lx + w) and (ty <= my <= ty + h)
        return self.hovered

    def draw(self, sw, sh):
        # Draw background and outline
        bg_color = COLOR_BG_PANEL if not self.hovered else (45, 52, 68, 255)
        border_color = self.color if self.hovered else COLOR_BORDER
        border_width = 4 if self.hovered else 2

        rl.DrawRectangle(int(self.lx), int(self.ty), int(self.w), int(self.h), bg_color)
        rl.DrawRectangleLinesEx([self.lx, self.ty, self.w, self.h], border_width, border_color)

        # Draw Pal Symbol / Avatar (Procedural drawing)
        avatar_cx = self.lx + self.w / 2
        avatar_cy = self.ty + self.h * 0.32
        avatar_radius = self.w * 0.26
        rl.DrawCircle(int(avatar_cx), int(avatar_cy), int(avatar_radius), self.color)
        
        # Cute face details on the avatar circle
        eye_offset = self.w * 0.08
        rl.DrawCircle(int(avatar_cx - eye_offset), int(avatar_cy - 4), 6, rl.colors.BLACK)
        rl.DrawCircle(int(avatar_cx + eye_offset), int(avatar_cy - 4), 6, rl.colors.BLACK)
        
        # Cute smile mouth
        rl.DrawLineEx([avatar_cx - 12, avatar_cy + 12], [avatar_cx, avatar_cy + 18], 3, rl.colors.BLACK)
        rl.DrawLineEx([avatar_cx, avatar_cy + 18], [avatar_cx + 12, avatar_cy + 12], 3, rl.colors.BLACK)

        # Details
        cx_norm = avatar_cx / sw
        
        # Pal Name
        AI4Animation.Draw.Text(
            self.name,
            cx_norm, (self.ty + self.h * 0.65) / sh,
            0.025, COLOR_TEXT_PRIMARY, 0.5
        )

        # Pal Type
        AI4Animation.Draw.Text(
            f"Type: {self.type}",
            cx_norm, (self.ty + self.h * 0.74) / sh,
            0.018, self.color, 0.5
        )
        
        # Base stats summary
        temp_pal = self.creator()
        stats_text = f"HP:{temp_pal.max_hp} ATK:{temp_pal.base_attack} DEF:{temp_pal.base_defense}"
        AI4Animation.Draw.Text(
            stats_text,
            cx_norm, (self.ty + self.h * 0.83) / sh,
            0.015, COLOR_TEXT_MUTED, 0.5
        )

class StarterView:
    def __init__(self):
        self.cards = [
            StarterCard("Leaflet", "Grass/Wind", create_leaflet, COLOR_TYPE_GRASS),
            StarterCard("Pyropup", "Fire", create_pyropup, COLOR_TYPE_FIRE),
            StarterCard("Aquasplash", "Water/Ice", create_aquasplash, COLOR_TYPE_WATER)
        ]

    def on_show_view(self):
        pass

    def on_update(self, dt):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()
        
        # Mouse Position
        mouse_pos = rl.GetMousePosition()
        mx, my = mouse_pos.x, mouse_pos.y

        # Calculate card geometries for collision checks
        cw = sw * 0.18
        ch = sh * 0.45
        spacing = sw * 0.04
        total_width = 3 * cw + 2 * spacing
        start_x = (sw - total_width) / 2
        ty = sh * 0.35

        for idx, card in enumerate(self.cards):
            lx = start_x + idx * (cw + spacing)
            card.check_mouse(mx, my, lx, ty, cw, ch)

        # Handle mouse clicks
        if rl.IsMouseButtonPressed(rl.MOUSE_BUTTON_LEFT):
            for card in self.cards:
                if card.hovered:
                    # Player selection
                    player_pal = card.creator(is_player=True)
                    
                    # Opponent selection (random from other two)
                    others = [c for c in self.cards if c.name != card.name]
                    opponent_card = random.choice(others)
                    opponent_pal = opponent_card.creator(is_player=False)

                    # Transition to BattleView
                    from battle_pals.views.battle_view import BattleView
                    from battle_pals.game import BattlePalsGame
                    BattlePalsGame.get_instance().switch_to_view(BattleView(player_pal, opponent_pal))
                    break

    def on_draw(self):
        # Draw background arena floor in 3D scene space
        # Dark premium forest green grass plane
        rl.DrawPlane([0.0, 0.0, 0.0], [30.0, 30.0], (28, 36, 24, 255))

    def on_gui(self):
        sw = rl.GetScreenWidth()
        sh = rl.GetScreenHeight()

        # Main Title
        AI4Animation.Draw.Text(
            "CHOOSE YOUR STARTER PAL",
            0.5, 0.12, 0.04, COLOR_TEXT_PRIMARY, 0.5
        )

        AI4Animation.Draw.Text(
            "Click on a Pal to begin your battle arena trial",
            0.5, 0.18, 0.018, COLOR_TEXT_MUTED, 0.5
        )

        # Draw Cards
        for card in self.cards:
            card.draw(sw, sh)
