import os
import json

class Move:
    def __init__(self, name, pal_type, power, accuracy, category="Physical", effect=None, description=""):
        self.name = name
        self.type = pal_type  # "Fire", "Water", "Grass", "Normal", etc.
        self.power = power
        self.accuracy = accuracy  # Float between 0.0 and 1.0
        self.category = category  # "Physical", "Special", "Status"
        self.effect = effect  # Optional dict for status effects, e.g., {"heal": 0.5} or {"stat": "attack", "mult": 0.8}
        self.description = description

    @classmethod
    def from_json(cls, data):
        return cls(
            name=data["name"],
            pal_type=data["type"],
            power=data["power"],
            accuracy=data.get("accuracy", 1.0),
            category=data.get("category", "Physical"),
            effect=data.get("effect"),
            description=data.get("description", "")
        )

# Global moves repository dictionary
MOVES = {}

def load_moves():
    global MOVES
    current_dir = os.path.dirname(os.path.abspath(__file__))
    moves_dir = os.path.join(current_dir, "..", "data", "moves")
    
    if os.path.exists(moves_dir):
        for filename in os.listdir(moves_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(moves_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        move = Move.from_json(data)
                        MOVES[move.name] = move
                except Exception as e:
                    print(f"Error loading move {filename}: {e}")
    else:
        print(f"Moves directory not found at {moves_dir}")

# Load all moves dynamically at module import time
load_moves()
