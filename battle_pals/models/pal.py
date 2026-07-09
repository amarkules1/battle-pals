import os
import csv
import random
import math
from battle_pals.models.move import MOVES
from ai4animation.Math import Vector3

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
