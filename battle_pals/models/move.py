class Move:
    def __init__(self, name, pal_type, power, accuracy, category="Physical", effect=None, description=""):
        self.name = name
        self.type = pal_type  # "Fire", "Water", "Grass", "Normal"
        self.power = power
        self.accuracy = accuracy  # Float between 0.0 and 1.0
        self.category = category  # "Physical", "Special", "Status"
        self.effect = effect  # Optional dict for status effects, e.g., {"heal": 0.5} or {"stat": "attack", "mult": 0.8}
        self.description = description

# Static definitions of Starter moves
MOVES = {
    # Normal moves
    "Tackle": Move(
        name="Tackle",
        pal_type="Normal",
        power=40,
        accuracy=1.0,
        description="A physical body charge attack."
    ),
    "Scratch": Move(
        name="Scratch",
        pal_type="Normal",
        power=40,
        accuracy=1.0,
        description="Scratches the enemy with sharp claws."
    ),
    # Wind moves
    "Gust": Move(
        name="Gust",
        pal_type="Wind",
        power=40,
        accuracy=1.0,
        description="Creates a strong gust of wind."
    ),

    # Ice moves
    "Ice Shard": Move(
        name="Ice Shard",
        pal_type="Ice",
        power=40,
        accuracy=1.0,
        description="Fires frozen ice shards at high speed."
    ),
    # Grass moves
    "Razor Leaf": Move(
        name="Razor Leaf",
        pal_type="Grass",
        power=55,
        accuracy=0.95,
        description="Launches sharp-edged leaves at the target."
    ),
    "Synthesize": Move(
        name="Synthesize",
        pal_type="Grass",
        power=0,
        accuracy=1.0,
        category="Status",
        effect={"heal": 0.5},
        description="Heals 50% of the user's max HP."
    ),

    # Fire moves
    "Ember": Move(
        name="Ember",
        pal_type="Fire",
        power=40,
        accuracy=1.0,
        description="Shoots tiny flames at the target."
    ),
    "Flame Wheel": Move(
        name="Flame Wheel",
        pal_type="Fire",
        power=60,
        accuracy=0.90,
        description="Launches a spinning ball of fire."
    ),
    "Growl": Move(
        name="Growl",
        pal_type="Normal",
        power=0,
        accuracy=1.0,
        category="Status",
        effect={"stat": "attack", "mult": 0.8},
        description="Intimidates the enemy, reducing their Attack power."
    ),

    # Water moves
    "Water Gun": Move(
        name="Water Gun",
        pal_type="Water",
        power=40,
        accuracy=1.0,
        description="Blasts water at the target."
    ),
    "Water Pulse": Move(
        name="Water Pulse",
        pal_type="Water",
        power=60,
        accuracy=1.0,
        description="A clean, pulsing water blast."
    ),
    "Tail Whip": Move(
        name="Tail Whip",
        pal_type="Normal",
        power=0,
        accuracy=1.0,
        category="Status",
        effect={"stat": "defense", "mult": 0.8},
        description="Wags tail cutely, reducing the target's Defense."
    ),
}
