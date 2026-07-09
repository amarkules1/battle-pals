import os
import csv
import random
import math
import raylib as rl
from battle_pals.models.move import MOVES
from ai4animation import AI4Animation, Vector3

# Dynamic type matrix loaded from CSV
TYPE_MATRIX = {}

def load_type_matrix():
    global TYPE_MATRIX
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "..", "type_matrix.csv")
    
    if os.path.exists(csv_path):
        try:
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader) # headers: ["Attacker", "Normal", "Fire", ...]
                defender_types = [h.strip() for h in headers[1:]]
                
                for row in reader:
                    if not row or not row[0].strip():
                        continue
                    attacker = row[0].strip()
                    for idx, val in enumerate(row[1:]):
                        if idx < len(defender_types):
                            defender = defender_types[idx]
                            TYPE_MATRIX[(attacker, defender)] = float(val)
        except Exception as e:
            print(f"Error loading type matrix CSV: {e}")
            initialize_fallback_matrix()
    else:
        print(f"Type matrix CSV not found at {csv_path}. Using fallback.")
        initialize_fallback_matrix()

def initialize_fallback_matrix():
    global TYPE_MATRIX
    fallback = {
        ("Fire", "Grass"): 2.0,
        ("Grass", "Water"): 2.0,
        ("Water", "Fire"): 2.0,
        ("Grass", "Fire"): 0.5,
        ("Water", "Grass"): 0.5,
        ("Fire", "Water"): 0.5,
    }
    TYPE_MATRIX.clear()
    TYPE_MATRIX.update(fallback)

# Load at import time
load_type_matrix()

class Pal:
    def __init__(self, species_or_name, level, is_player=False, stat_variations=None):
        from battle_pals.models.species import SPECIES, Species
        if isinstance(species_or_name, str):
            species = SPECIES.get(species_or_name)
            if not species:
                species = Species(
                    name=species_or_name,
                    types=["Normal"],
                    base_stats={"hp": 50, "attack": 50, "defense": 50, "speed": 50},
                    learnset=[]
                )
        else:
            species = species_or_name

        self.species = species
        self.name = species.name
        self.types = species.types
        self.type = species.types[0] if species.types else "Normal"
        self.level = level
        self.is_player = is_player

        # Set up stat variations (IVs: 0-15)
        if stat_variations is None:
            self.stat_variations = {
                "hp": random.randint(0, 15),
                "attack": random.randint(0, 15),
                "defense": random.randint(0, 15),
                "speed": random.randint(0, 15)
            }
        else:
            self.stat_variations = stat_variations

        # Compute level-scaled stats from species base and variation
        self.max_hp = self.calculate_stat("hp")
        self.hp = self.max_hp
        self.base_attack = self.calculate_stat("attack")
        self.base_defense = self.calculate_stat("defense")
        self.base_speed = self.calculate_stat("speed")

        # Teach moves based on species learnset and current level
        self.moves = []
        self.learn_moves_for_level()

        # Status conditions
        self.status_effects = []

        # Combat modifiers reset at start of battle
        self.stat_modifiers = {
            "attack": 1.0,
            "defense": 1.0,
            "speed": 1.0
        }

        # Animation states
        self.time = 0.0
        self.base_position = Vector3.Create(-4.0, 1.5, -2.0) if is_player else Vector3.Create(4.0, 3.5, 2.0)
        self.position = Vector3.Create(-4.0, 1.5, -2.0) if is_player else Vector3.Create(4.0, 3.5, 2.0)
        
        self.float_amp = 0.15
        self.float_freq = 2.0
        
        self.shake_timer = 0.0
        self.shake_intensity = 0.0
        
        self.attack_timer = 0.0
        self.attack_duration = 0.5
        
        self.flash_timer = 0.0
        self.faint_timer = 0.0
        self.is_fainted = False

    def calculate_stat(self, stat_name):
        base = self.species.base_stats.get(stat_name, 50)
        variation = self.stat_variations.get(stat_name, 0)
        if stat_name == "hp":
            return int(((2 * base + variation) * self.level) / 50) + self.level + 10
        else:
            return int(((2 * base + variation) * self.level) / 50) + 5

    def learn_moves_for_level(self):
        available_moves = []
        for learn_info in self.species.learnset:
            if learn_info["level"] <= self.level:
                available_moves.append(learn_info["move"])
        unique_moves = []
        for m_name in reversed(available_moves):
            if m_name not in unique_moves:
                unique_moves.append(m_name)
            if len(unique_moves) >= 4:
                break
        from battle_pals.models.move import MOVES
        self.moves = [MOVES[name] for name in reversed(unique_moves) if name in MOVES]

    @property
    def attack(self):
        return int(self.base_attack * self.stat_modifiers["attack"])

    @property
    def defense(self):
        return int(self.base_defense * self.stat_modifiers["defense"])

    @property
    def speed(self):
        mult = self.stat_modifiers["speed"]
        if self.species.trait == "Chlorophyll":
            mult *= 1.5
        return int(self.base_speed * mult)

    def reset_battle_stats(self):
        """Resets battle stats (HP remains unchanged, but modifiers are reset)."""
        self.hp = self.max_hp
        self.stat_modifiers = {
            "attack": 1.0,
            "defense": 1.0,
            "speed": 1.0
        }
        self.shake_timer = 0.0
        self.flash_timer = 0.0
        self.attack_timer = 0.0
        self.faint_timer = 0.0
        self.is_fainted = False
        self.time = 0.0
        self.position = Vector3.Create(-4.0, 1.5, -2.0) if self.is_player else Vector3.Create(4.0, 3.5, 2.0)

    def draw_3d(self, facing=1.0, scale=1.0):
        pos = self.position
        
        # Safe wrapper for Raylib CFFI DrawCylinderEx which requires lists of standard floats
        def draw_cylinder(start, end, r1, r2, res, col):
            def clean(v):
                if hasattr(v, "tolist"):
                    arr = v.tolist()
                else:
                    arr = list(v)
                return [float(x) for x in arr]
            rl.DrawCylinderEx(clean(start), clean(end), float(r1), float(r2), int(res), col)

        # Determine color override (flash red when taking damage)
        def get_color(base_c):
            if hasattr(self, "flash_timer") and self.flash_timer > 0.0 and int(self.flash_timer * 15.0) % 2 == 0:
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
        app = self.species.appearance
        base_shape = app.get("base_shape", "quadruped")
        
        color_body = get_color(parse_color(app.get("body_color")))
        color_accent = get_color(parse_color(app.get("accent_color")))
        color_belly = get_color(parse_color(app.get("belly_color")))

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
            draw_cylinder([pos[0] - 0.5 * scale, pos[1] - 0.3 * scale, pos[2] - 0.4 * facing * scale], [pos[0] - 0.5 * scale, leg_y, pos[2] - 0.4 * facing * scale], leg_w, leg_w, 6, color_body)
            draw_cylinder([pos[0] + 0.5 * scale, pos[1] - 0.3 * scale, pos[2] - 0.4 * facing * scale], [pos[0] + 0.5 * scale, leg_y, pos[2] - 0.4 * facing * scale], leg_w, leg_w, 6, color_body)
            draw_cylinder([pos[0] - 0.6 * scale, pos[1] - 0.3 * scale, pos[2] + 0.5 * facing * scale], [pos[0] - 0.6 * scale, leg_y, pos[2] + 0.5 * facing * scale], leg_w, leg_w, 6, color_body)
            draw_cylinder([pos[0] + 0.6 * scale, pos[1] - 0.3 * scale, pos[2] + 0.5 * facing * scale], [pos[0] + 0.6 * scale, leg_y, pos[2] + 0.5 * facing * scale], leg_w, leg_w, 6, color_body)
            
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] - 0.5 * scale, leg_y, pos[2] - 0.55 * facing * scale), 0.25 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] + 0.5 * scale, leg_y, pos[2] - 0.55 * facing * scale), 0.25 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] - 0.6 * scale, leg_y, pos[2] + 0.45 * facing * scale), 0.25 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] + 0.6 * scale, leg_y, pos[2] + 0.45 * facing * scale), 0.25 * scale, 6, color_accent)
            
        elif base_shape == "biped" or base_shape == "demon" or base_shape == "dragon":
            leg_y = pos[1] - 0.8 * scale
            leg_w = 0.28 * scale
            draw_cylinder([pos[0] - 0.4 * scale, pos[1] - 0.3 * scale, pos[2]], [pos[0] - 0.4 * scale, leg_y, pos[2]], leg_w, leg_w, 6, color_body)
            draw_cylinder([pos[0] + 0.4 * scale, pos[1] - 0.3 * scale, pos[2]], [pos[0] + 0.4 * scale, leg_y, pos[2]], leg_w, leg_w, 6, color_body)
            
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] - 0.4 * scale, leg_y, pos[2] - 0.2 * facing * scale), 0.3 * scale, 6, color_accent)
            AI4Animation.Draw.Sphere(Vector3.Create(pos[0] + 0.4 * scale, leg_y, pos[2] - 0.2 * facing * scale), 0.3 * scale, 6, color_accent)
            
            arm_y = pos[1] + 0.1 * scale
            draw_cylinder([body_center[0] - 0.8 * scale, arm_y, body_center[2]], [body_center[0] - 1.2 * scale, arm_y - 0.3 * scale, body_center[2] - 0.2 * facing * scale], 0.18 * scale, 0.18 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0] - 1.2 * scale, arm_y - 0.3 * scale, body_center[2] - 0.25 * facing * scale), 0.2 * scale, 6, color_accent)
            
            draw_cylinder([body_center[0] + 0.8 * scale, arm_y, body_center[2]], [body_center[0] + 1.2 * scale, arm_y - 0.3 * scale, body_center[2] - 0.2 * facing * scale], 0.18 * scale, 0.18 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0] + 1.2 * scale, arm_y - 0.3 * scale, body_center[2] - 0.25 * facing * scale), 0.2 * scale, 6, color_accent)
            
        elif base_shape == "bird":
            leg_y = pos[1] - 0.7 * scale
            draw_cylinder([pos[0] - 0.3 * scale, pos[1] - 0.3 * scale, pos[2]], [pos[0] - 0.3 * scale, leg_y, pos[2]], 0.1 * scale, 0.1 * scale, 4, color_accent)
            draw_cylinder([pos[0] + 0.3 * scale, pos[1] - 0.3 * scale, pos[2]], [pos[0] + 0.3 * scale, leg_y, pos[2]], 0.1 * scale, 0.1 * scale, 4, color_accent)
            
        elif base_shape == "aquatic":
            draw_cylinder([body_center[0] - 0.8 * scale, body_center[1] - 0.2 * scale, body_center[2]], [body_center[0] - 1.3 * scale, body_center[1] - 0.4 * scale, body_center[2] - 0.1 * facing * scale], 0.18 * scale, 0.05 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0] - 1.3 * scale, body_center[1] - 0.4 * scale, body_center[2] - 0.1 * facing * scale), 0.12 * scale, 6, color_accent)
            
            draw_cylinder([body_center[0] + 0.8 * scale, body_center[1] - 0.2 * scale, body_center[2]], [body_center[0] + 1.3 * scale, body_center[1] - 0.4 * scale, body_center[2] - 0.1 * facing * scale], 0.18 * scale, 0.05 * scale, 6, color_body)
            AI4Animation.Draw.Sphere(Vector3.Create(body_center[0] + 1.3 * scale, body_center[1] - 0.4 * scale, body_center[2] - 0.1 * facing * scale), 0.12 * scale, 6, color_accent)
            
            draw_cylinder([body_center[0], body_center[1] + 0.5 * scale, body_center[2] + 0.3 * facing * scale], [body_center[0], body_center[1] + 1.3 * scale, body_center[2] + 0.9 * facing * scale], 0.16 * scale, 0.01 * scale, 6, color_body)

        # Wings
        wings_type = app.get("wings", "none")
        if wings_type == "feathered":
            wing_z = body_center[2] + 0.3 * facing * scale
            draw_cylinder([body_center[0] - 0.8 * scale, body_center[1] + 0.2 * scale, wing_z], [body_center[0] - 2.0 * scale, body_center[1] + 1.0 * scale, wing_z + 0.5 * facing * scale], 0.1 * scale, 0.3 * scale, 6, color_accent)
            draw_cylinder([body_center[0] + 0.8 * scale, body_center[1] + 0.2 * scale, wing_z], [body_center[0] + 2.0 * scale, body_center[1] + 1.0 * scale, wing_z + 0.5 * facing * scale], 0.1 * scale, 0.3 * scale, 6, color_accent)
        elif wings_type == "bat":
            wing_z = body_center[2] + 0.3 * facing * scale
            color_bat = (40, 40, 40, 200)
            draw_cylinder([body_center[0] - 0.8 * scale, body_center[1] + 0.1 * scale, wing_z], [body_center[0] - 2.2 * scale, body_center[1] + 0.8 * scale, wing_z + 0.4 * facing * scale], 0.05 * scale, 0.25 * scale, 6, color_bat)
            draw_cylinder([body_center[0] + 0.8 * scale, body_center[1] + 0.1 * scale, wing_z], [body_center[0] + 2.2 * scale, body_center[1] + 0.8 * scale, wing_z + 0.4 * facing * scale], 0.05 * scale, 0.25 * scale, 6, color_bat)

        # Ears
        ears_type = app.get("ears", "none")
        if ears_type == "leaf":
            draw_cylinder([head_center[0] - 0.5 * scale, head_center[1] + 0.5 * scale, head_center[2]], [head_center[0] - 1.2 * scale, head_center[1] + 1.2 * scale, head_center[2] - 0.3 * facing * scale], 0.18 * scale, 0.01 * scale, 8, color_accent)
            draw_cylinder([head_center[0] + 0.5 * scale, head_center[1] + 0.5 * scale, head_center[2]], [head_center[0] + 1.2 * scale, head_center[1] + 1.2 * scale, head_center[2] - 0.3 * facing * scale], 0.18 * scale, 0.01 * scale, 8, color_accent)
        elif ears_type == "puppy":
            draw_cylinder([head_center[0] - 0.55 * scale, head_center[1] + 0.4 * scale, head_center[2]], [head_center[0] - 0.8 * scale, head_center[1] - 0.3 * scale, head_center[2] - 0.1 * facing * scale], 0.16 * scale, 0.16 * scale, 8, color_accent)
            draw_cylinder([head_center[0] + 0.55 * scale, head_center[1] + 0.4 * scale, head_center[2]], [head_center[0] + 0.8 * scale, head_center[1] - 0.3 * scale, head_center[2] - 0.1 * facing * scale], 0.16 * scale, 0.16 * scale, 8, color_accent)
        elif ears_type == "fins":
            draw_cylinder([head_center[0] - 0.55 * scale, head_center[1] - 0.05 * scale, head_center[2]], [head_center[0] - 1.1 * scale, head_center[1] - 0.25 * scale, head_center[2] - 0.2 * facing * scale], 0.15 * scale, 0.02 * scale, 8, color_accent)
            draw_cylinder([head_center[0] + 0.55 * scale, head_center[1] - 0.05 * scale, head_center[2]], [head_center[0] + 1.1 * scale, head_center[1] - 0.25 * scale, head_center[2] - 0.2 * facing * scale], 0.15 * scale, 0.02 * scale, 8, color_accent)
        elif ears_type == "pointy":
            draw_cylinder([head_center[0] - 0.5 * scale, head_center[1] + 0.6 * scale, head_center[2]], [head_center[0] - 0.7 * scale, head_center[1] + 1.3 * scale, head_center[2] - 0.1 * facing * scale], 0.18 * scale, 0.05 * scale, 6, color_accent)
            draw_cylinder([head_center[0] + 0.5 * scale, head_center[1] + 0.6 * scale, head_center[2]], [head_center[0] + 0.7 * scale, head_center[1] + 1.3 * scale, head_center[2] - 0.1 * facing * scale], 0.18 * scale, 0.05 * scale, 6, color_accent)

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
            draw_cylinder(tail_base, tail_end, 0.16 * scale, 0.1 * scale, 6, color_body)
            draw_cylinder(tail_end, Vector3.Create(tail_end[0] - 0.45 * scale, tail_end[1] - 0.1 * scale, tail_end[2] + 0.3 * facing * scale), 0.08 * scale, 0.01 * scale, 6, color_accent)
            draw_cylinder(tail_end, Vector3.Create(tail_end[0] + 0.45 * scale, tail_end[1] - 0.1 * scale, tail_end[2] + 0.3 * facing * scale), 0.08 * scale, 0.01 * scale, 6, color_accent)
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
            draw_cylinder(horn_base, horn_tip, 0.15 * scale, 0.02 * scale, 6, color_accent)
        elif horn_type == "dual":
            horn_base_l = [head_center[0] - 0.35 * scale, head_center[1] + 0.7 * scale, head_center[2] - 0.2 * facing * scale]
            horn_tip_l = [head_center[0] - 0.5 * scale, head_center[1] + 1.3 * scale, head_center[2] - 0.4 * facing * scale]
            draw_cylinder(horn_base_l, horn_tip_l, 0.1 * scale, 0.02 * scale, 6, color_accent)
            
            horn_base_r = [head_center[0] + 0.35 * scale, head_center[1] + 0.7 * scale, head_center[2] - 0.2 * facing * scale]
            horn_tip_r = [head_center[0] + 0.5 * scale, head_center[1] + 1.3 * scale, head_center[2] - 0.4 * facing * scale]
            draw_cylinder(horn_base_r, horn_tip_r, 0.1 * scale, 0.02 * scale, 6, color_accent)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        self.shake_timer = 0.4
        self.shake_intensity = 0.3
        self.flash_timer = 0.4

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        self.flash_timer = 0.4  # Flashes white/green

    def update_animation(self, dt):
        if self.is_fainted:
            return
            
        self.time += dt
        
        # 1. Floating animation
        float_y = math.sin(self.time * self.float_freq) * self.float_amp
        self.position = Vector3.Create(self.base_position[0], self.base_position[1] + float_y, self.base_position[2])
        
        # 2. Attack slide animation
        if self.attack_timer > 0.0:
            self.attack_timer -= dt
            progress = (self.attack_duration - self.attack_timer) / self.attack_duration
            slide_dist = math.sin(progress * math.pi) * 3.0
            direction = 1.0 if self.is_player else -1.0
            self.position = Vector3.Create(
                self.position[0] + direction * slide_dist,
                self.position[1],
                self.position[2] + direction * slide_dist * 0.5
            )
            
        # 3. Shake animation
        if self.shake_timer > 0.0:
            self.shake_timer -= dt
            shake_x = math.sin(self.shake_timer * 40.0) * self.shake_intensity
            self.position = Vector3.Create(self.position[0] + shake_x, self.position[1], self.position[2])
            
        # 4. Flashing timer
        if self.flash_timer > 0.0:
            self.flash_timer -= dt
            
        # 5. Fainting animation
        if self.faint_timer > 0.0:
            self.faint_timer += dt
            # Spin and drop down
            self.position = Vector3.Create(
                self.base_position[0],
                self.base_position[1] - min(2.0, self.faint_timer * 2.0),
                self.base_position[2]
            )
            if self.faint_timer > 1.0:
                self.is_fainted = True

    @staticmethod
    def get_effectiveness(move_type, target_types):
        """Calculates effectiveness of move against target type list or slash-separated string."""
        if isinstance(target_types, str):
            target_types = [t.strip() for t in target_types.split("/") if t.strip()]
            
        mult = 1.0
        for defender_type in target_types:
            mult *= TYPE_MATRIX.get((move_type, defender_type), 1.0)
        return mult

    def use_move(self, move, target):
        """
        Executes a move against a target Pal.
        Returns a list of outcome messages (combat log).
        """
        logs = [f"{self.name} used {move.name}!"]
        
        # Trigger attack animation
        self.attack_timer = self.attack_duration

        # Check accuracy
        if random.random() > move.accuracy:
            logs.append(f"But the attack missed!")
            return logs

        # 1. Damage Category
        if move.category == "Physical" or move.category == "Special":
            eff = self.get_effectiveness(move.type, target.types)
            
            a_d_ratio = self.attack / max(1, target.defense)
            base_dmg = (((2 * self.level / 5 + 2) * move.power * a_d_ratio) / 50) + 2
            
            random_factor = random.uniform(0.85, 1.0)
            critical_chance = random.random() < 0.0625  # 6.25% critical hit chance
            crit_multiplier = 1.5 if critical_chance else 1.0
            
            # Apply low-HP trait modifier (Blaze/Torrent/Overgrow)
            trait_mult = 1.0
            is_low_hp = (self.hp / self.max_hp) <= 0.33
            if is_low_hp:
                if self.species.trait == "Blaze" and move.type == "Fire":
                    trait_mult = 1.5
                elif self.species.trait == "Torrent" and move.type == "Water":
                    trait_mult = 1.5
                elif self.species.trait == "Overgrow" and move.type == "Grass":
                    trait_mult = 1.5
            
            damage = int(base_dmg * eff * random_factor * crit_multiplier * trait_mult)
            damage = max(1, damage)  # Minimum 1 damage

            # If immune, damage is 0
            if eff == 0.0:
                damage = 0

            if damage > 0:
                target.take_damage(damage)

            if critical_chance:
                logs.append("A critical hit!")

            if trait_mult > 1.0:
                logs.append(f"{self.name}'s {self.species.trait} boosted the attack!")

            if eff > 1.0:
                logs.append("It's super effective!")
            elif 0.0 < eff < 1.0:
                logs.append("It's not very effective...")
            elif eff == 0.0:
                logs.append(f"It doesn't affect {target.name}...")

            if damage > 0:
                logs.append(f"{target.name} took {damage} damage!")

        # 2. Status Category
        elif move.category == "Status" and move.effect:
            effect = move.effect
            
            # Heal effect
            if "heal" in effect:
                heal_amt = int(self.max_hp * effect["heal"])
                self.heal(heal_amt)
                logs.append(f"{self.name} recovered {heal_amt} HP!")
            
            # Stat reduction / increase effect
            if "stat" in effect:
                stat = effect["stat"]
                multiplier = effect["mult"]
                
                if stat in target.stat_modifiers:
                    if multiplier < 1.0 and target.species.trait == "Clear Body":
                        logs.append(f"{target.name}'s Clear Body prevents stat reduction!")
                    else:
                        target.stat_modifiers[stat] = max(0.4, target.stat_modifiers[stat] * multiplier)
                        change_text = "fell" if multiplier < 1.0 else "rose"
                        logs.append(f"{target.name}'s {stat.capitalize()} {change_text}!")
                
        return logs

# Starter Pal Presets
def create_leaflet(is_player=False):
    from battle_pals.models.species import SPECIES
    species = SPECIES.get("Leaflet")
    return Pal(species, level=5, is_player=is_player)

def create_pyropup(is_player=False):
    from battle_pals.models.species import SPECIES
    species = SPECIES.get("Pyropup")
    return Pal(species, level=5, is_player=is_player)

def create_aquasplash(is_player=False):
    from battle_pals.models.species import SPECIES
    species = SPECIES.get("Aquasplash")
    return Pal(species, level=5, is_player=is_player)

STARTERS = {
    "Leaflet": create_leaflet,
    "Pyropup": create_pyropup,
    "Aquasplash": create_aquasplash
}
