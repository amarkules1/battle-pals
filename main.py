import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Battle Pals"

MOVEMENT_SPEED = 5

class Pal:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.x += self.change_x
        self.y += self.change_y

        # Keep within the screen boundaries
        if self.x < self.radius:
            self.x = self.radius
        if self.x > SCREEN_WIDTH - self.radius:
            self.x = SCREEN_WIDTH - self.radius
        if self.y < self.radius:
            self.y = self.radius
        if self.y > SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius

    def draw(self):
        # Draw the main pal body
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        # Draw eyes to give it some character
        arcade.draw_circle_filled(self.x - 6, self.y + 4, 3, arcade.color.BLACK)
        arcade.draw_circle_filled(self.x + 6, self.y + 4, 3, arcade.color.BLACK)

class BattlePalsGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.csscolor.DARK_SLATE_GRAY
        self.player = None

    def setup(self):
        """Set up the game session."""
        self.player = Pal(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 20, arcade.color.AQUAMARINE)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        
        # Draw the player Pal
        self.player.draw()
        
        # Draw HUD instructions
        arcade.draw_text(
            "Use WASD or Arrow Keys to move your Pal!",
            20, 20,
            arcade.color.LIGHT_GRAY,
            font_size=12
        )

    def on_update(self, delta_time):
        """Movement and game logic."""
        self.player.update()

    def on_key_press(self, key, modifiers):
        """Handle movement keys pressed."""
        if key in (arcade.key.UP, arcade.key.W):
            self.player.change_y = MOVEMENT_SPEED
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.change_y = -MOVEMENT_SPEED
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Handle movement keys released."""
        if key in (arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S):
            self.player.change_y = 0
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = 0

def main():
    window = BattlePalsGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
