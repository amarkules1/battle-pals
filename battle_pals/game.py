import arcade
from battle_pals.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from battle_pals.views.starter_view import StarterView

def run_game():
    """Initializes the window, sets the starting view, and runs the Arcade loop."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    # Start with the starter selection screen
    starter_view = StarterView()
    window.show_view(starter_view)
    
    arcade.run()
