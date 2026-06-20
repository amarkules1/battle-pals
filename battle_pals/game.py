import raylib as rl
from ai4animation import AI4Animation, Vector3

class BattlePalsGame:
    _instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __init__(self):
        BattlePalsGame._instance = self
        self.active_view = None

    def Start(self):
        # Remove components of default scene grids/walls so they are not drawn or updated
        for entity in AI4Animation.Scene.Entities:
            if entity.Name in ["Ground", "Wall1", "Wall2", "Wall3", "Wall4"]:
                entity.Components = {}

        # Set up a fixed camera position
        # Overwrite default camera's GUI so it doesn't draw mode buttons
        if hasattr(AI4Animation.Standalone, "Camera"):
            AI4Animation.Standalone.Camera.Mode = -1  # Disable camera logic
            AI4Animation.Standalone.Camera.GUI = lambda: None # Hide debug panel
            
            rl_cam = AI4Animation.Standalone.Camera.Camera
            rl_cam.position = [0.0, 5.0, 10.0]
            rl_cam.target = [0.0, 2.0, 0.0]
            rl_cam.up = [0.0, 1.0, 0.0]

        # Start with the starter selection screen
        from battle_pals.views.starter_view import StarterView
        self.switch_to_view(StarterView())

    def switch_to_view(self, view):
        self.active_view = view
        if hasattr(self.active_view, "on_show_view"):
            self.active_view.on_show_view()

    def Update(self):
        if self.active_view and hasattr(self.active_view, "on_update"):
            self.active_view.on_update(rl.GetFrameTime())

    def Draw(self):
        if self.active_view and hasattr(self.active_view, "on_draw"):
            self.active_view.on_draw()

    def GUI(self):
        if self.active_view and hasattr(self.active_view, "on_gui"):
            self.active_view.on_gui()

def run_game():
    """Initializes the ai4animation framework and runs the game window."""
    game = BattlePalsGame()
    # Run in Standalone mode (Raylib window)
    ai4a = AI4Animation(game, mode=AI4Animation.Mode.STANDALONE)
