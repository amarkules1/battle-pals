import random
from battle_pals.models.move import MOVES

class Pal:
    def __init__(self, name, pal_type, level, hp, attack, defense, speed, moves_list):
        self.name = name
        self.type = pal_type  # "Fire", "Water", "Grass"
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.base_speed = speed
        
        # Moves
        self.moves = [MOVES[m] for m in moves_list if m in MOVES]
        
        # Combat modifiers reset at start of battle
        self.stat_modifiers = {
            "attack": 1.0,
            "defense": 1.0,
            "speed": 1.0
        }

    @property
    def attack(self):
        return int(self.base_attack * self.stat_modifiers["attack"])

    @property
    def defense(self):
        return int(self.base_defense * self.stat_modifiers["defense"])

    @property
    def speed(self):
        return int(self.base_speed * self.stat_modifiers["speed"])

    def reset_battle_stats(self):
        """Resets battle stats (HP remains unchanged, but modifiers are reset)."""
        self.hp = self.max_hp
        self.stat_modifiers = {
            "attack": 1.0,
            "defense": 1.0,
            "speed": 1.0
        }

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    @staticmethod
    def get_effectiveness(move_type, target_type):
        """Standard Fire-Water-Grass type relationships."""
        relations = {
            ("Fire", "Grass"): 2.0,
            ("Grass", "Water"): 2.0,
            ("Water", "Fire"): 2.0,
            ("Grass", "Fire"): 0.5,
            ("Water", "Grass"): 0.5,
            ("Fire", "Water"): 0.5,
        }
        return relations.get((move_type, target_type), 1.0)

    def use_move(self, move, target):
        """
        Executes a move against a target Pal.
        Returns a list of outcome messages (combat log).
        """
        logs = [f"{self.name} used {move.name}!"]

        # Check accuracy
        if random.random() > move.accuracy:
            logs.append(f"But the attack missed!")
            return logs

        # 1. Damage Category
        if move.category == "Physical" or move.category == "Special":
            # Type effectiveness multiplier
            eff = self.get_effectiveness(move.type, target.type)
            
            # Simple standard Pokemon damage formula:
            # Damage = (((2 * Level / 5 + 2) * Power * A / D) / 50 + 2) * Modifier
            # With randomized variance (85% to 100%)
            a_d_ratio = self.attack / max(1, target.defense)
            base_dmg = (((2 * self.level / 5 + 2) * move.power * a_d_ratio) / 50) + 2
            
            random_factor = random.uniform(0.85, 1.0)
            critical_chance = random.random() < 0.0625  # 6.25% critical hit chance
            crit_multiplier = 1.5 if critical_chance else 1.0
            
            damage = int(base_dmg * eff * random_factor * crit_multiplier)
            damage = max(1, damage)  # Minimum 1 damage

            target.take_damage(damage)

            if critical_chance:
                logs.append("A critical hit!")

            if eff > 1.0:
                logs.append("It's super effective!")
            elif eff < 1.0:
                logs.append("It's not very effective...")

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
                
                # Apply target or self based on move description / type
                # For standard growl/tailwhip, it affects the target
                if stat in target.stat_modifiers:
                    target.stat_modifiers[stat] = max(0.4, target.stat_modifiers[stat] * multiplier)
                    change_text = "fell" if multiplier < 1.0 else "rose"
                    logs.append(f"{target.name}'s {stat.capitalize()} {change_text}!")
                
        return logs

# Starter Pal Presets
def create_leaflet():
    # Grass type - high HP / defense
    return Pal(
        name="Leaflet",
        pal_type="Grass",
        level=5,
        hp=24,
        attack=12,
        defense=14,
        speed=10,
        moves_list=["Tackle", "Razor Leaf", "Synthesize"]
    )

def create_pyropup():
    # Fire type - high attack / speed
    return Pal(
        name="Pyropup",
        pal_type="Fire",
        level=5,
        hp=20,
        attack=15,
        defense=10,
        speed=13,
        moves_list=["Scratch", "Ember", "Growl"]
    )

def create_aquasplash():
    # Water type - high HP / balanced stats
    return Pal(
        name="Aquasplash",
        pal_type="Water",
        level=5,
        hp=22,
        attack=13,
        defense=12,
        speed=11,
        moves_list=["Tackle", "Water Gun", "Tail Whip"]
    )

STARTERS = {
    "Leaflet": create_leaflet,
    "Pyropup": create_pyropup,
    "Aquasplash": create_aquasplash
}
