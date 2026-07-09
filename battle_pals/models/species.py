import os
import json

class Species:
    def __init__(self, name, types, base_stats, learnset, trait=None, 
                 evolves_from=None, evolves_into=None, evolution_level=None, 
                 description="", appearance=None):
        self.name = name
        self.types = types  # ["Grass", "Wind"] etc.
        self.base_stats = base_stats  # {"hp": int, "attack": int, "defense": int, "speed": int}
        self.learnset = learnset  # [{"level": int, "move": str}]
        self.trait = trait
        self.evolves_from = evolves_from
        self.evolves_into = evolves_into
        self.evolution_level = evolution_level
        self.description = description
        self.appearance = appearance or {
            "base_shape": "quadruped",
            "body_color": [128, 128, 128, 255],
            "accent_color": [100, 100, 100, 255],
            "belly_color": [200, 200, 200, 255],
            "ears": "none",
            "tail": "none",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            name=data["name"],
            types=data["types"],
            base_stats=data["base_stats"],
            learnset=data.get("learnset", []),
            trait=data.get("trait"),
            evolves_from=data.get("evolves_from"),
            evolves_into=data.get("evolves_into"),
            evolution_level=data.get("evolution_level"),
            description=data.get("description", ""),
            appearance=data.get("appearance")
        )

# Global species registry dictionary
SPECIES = {}

def load_species():
    global SPECIES
    current_dir = os.path.dirname(os.path.abspath(__file__))
    species_dir = os.path.join(current_dir, "..", "data", "species")
    
    if os.path.exists(species_dir):
        for filename in os.listdir(species_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(species_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        spec = Species.from_json(data)
                        SPECIES[spec.name] = spec
                except Exception as e:
                    print(f"Error loading species {filename}: {e}")
    else:
        print(f"Species directory not found at {species_dir}")

# Load all species dynamically at module import time
load_species()
