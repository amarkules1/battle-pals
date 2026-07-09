import os
import json

# Define the moves data list
MOVES_DATA = [
    # --- Normal Moves (10) ---
    {
        "name": "Tackle",
        "type": "Normal",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "A basic physical body charge attack."
    },
    {
        "name": "Scratch",
        "type": "Normal",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Scratches the enemy with sharp claws."
    },
    {
        "name": "Slam",
        "type": "Normal",
        "power": 80,
        "accuracy": 0.75,
        "category": "Physical",
        "description": "Slams the target with a heavy tail or limb."
    },
    {
        "name": "Double Slap",
        "type": "Normal",
        "power": 15,
        "accuracy": 0.85,
        "category": "Physical",
        "description": "Repeatedly slaps the target."
    },
    {
        "name": "Swift",
        "type": "Normal",
        "power": 60,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires star-shaped rays that never miss."
    },
    {
        "name": "Hyper Beam",
        "type": "Normal",
        "power": 120,
        "accuracy": 0.9,
        "category": "Special",
        "description": "A high-power energy beam."
    },
    {
        "name": "Growl",
        "type": "Normal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 0.8},
        "description": "Intimidates the target, lowering their Attack."
    },
    {
        "name": "Tail Whip",
        "type": "Normal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 0.8},
        "description": "Lowers the target's Defense stat."
    },
    {
        "name": "Recover",
        "type": "Normal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"heal": 0.5},
        "description": "Restores 50% of the user's max HP."
    },
    {
        "name": "Harden",
        "type": "Normal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.3},
        "description": "Stiffens the body, boosting user's Defense."
    },

    # --- Fire Moves (6) ---
    {
        "name": "Ember",
        "type": "Fire",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Shoots tiny flames at the target."
    },
    {
        "name": "Flame Wheel",
        "type": "Fire",
        "power": 60,
        "accuracy": 0.95,
        "category": "Physical",
        "description": "Launches a spinning wheel of fire."
    },
    {
        "name": "Flamethrower",
        "type": "Fire",
        "power": 90,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Blasts an intense stream of fire."
    },
    {
        "name": "Fire Blast",
        "type": "Fire",
        "power": 110,
        "accuracy": 0.85,
        "category": "Special",
        "description": "An explosive star of fire."
    },
    {
        "name": "Sunny Day",
        "type": "Fire",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 1.3},
        "description": "Intensifies sunlight, boosting fire power."
    },
    {
        "name": "Heat Wave",
        "type": "Fire",
        "power": 95,
        "accuracy": 0.9,
        "category": "Special",
        "description": "Exhales a hot breath that burns."
    },

    # --- Water Moves (6) ---
    {
        "name": "Water Gun",
        "type": "Water",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Blasts water at the target."
    },
    {
        "name": "Water Pulse",
        "type": "Water",
        "power": 60,
        "accuracy": 1.0,
        "category": "Special",
        "description": "A clean, pulsing water blast."
    },
    {
        "name": "Surf",
        "type": "Water",
        "power": 90,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Swamps the target with a huge wave."
    },
    {
        "name": "Hydro Pump",
        "type": "Water",
        "power": 110,
        "accuracy": 0.8,
        "category": "Special",
        "description": "Blasts high-pressure water."
    },
    {
        "name": "Rain Dance",
        "type": "Water",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.3},
        "description": "Calls down rain to bolster defenses."
    },
    {
        "name": "Aqua Jet",
        "type": "Water",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Strikes first at high speed in water."
    },

    # --- Grass Moves (6) ---
    {
        "name": "Razor Leaf",
        "type": "Grass",
        "power": 55,
        "accuracy": 0.95,
        "category": "Physical",
        "description": "Launches sharp-edged leaves."
    },
    {
        "name": "Synthesize",
        "type": "Grass",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"heal": 0.5},
        "description": "Heals 50% of the user's max HP."
    },
    {
        "name": "Vine Whip",
        "type": "Grass",
        "power": 45,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Strikes the target with slender vines."
    },
    {
        "name": "Solar Beam",
        "type": "Grass",
        "power": 120,
        "accuracy": 0.9,
        "category": "Special",
        "description": "Charges solar energy and releases it."
    },
    {
        "name": "Spore",
        "type": "Grass",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "speed", "mult": 0.6},
        "description": "Scatters spores that slow the target."
    },
    {
        "name": "Mega Drain",
        "type": "Grass",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "effect": {"heal": 0.25},
        "description": "Absorbs target's energy to heal."
    },

    # --- Electric Moves (5) ---
    {
        "name": "Spark",
        "type": "Electric",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "A small jolt of electricity."
    },
    {
        "name": "Thunderbolt",
        "type": "Electric",
        "power": 90,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires a powerful electric bolt."
    },
    {
        "name": "Thunder",
        "type": "Electric",
        "power": 110,
        "accuracy": 0.7,
        "category": "Special",
        "description": "Strikes down a lightning bolt."
    },
    {
        "name": "Thunder Wave",
        "type": "Electric",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "speed", "mult": 0.5},
        "description": "Sends shock waves, cutting target's Speed."
    },
    {
        "name": "Volt Tackle",
        "type": "Electric",
        "power": 120,
        "accuracy": 0.85,
        "category": "Physical",
        "description": "A high-speed electric tackle."
    },

    # --- Ice Moves (5) ---
    {
        "name": "Ice Shard",
        "type": "Ice",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Fires quick shards of ice."
    },
    {
        "name": "Ice Beam",
        "type": "Ice",
        "power": 90,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires an icy beam to freeze the target."
    },
    {
        "name": "Blizzard",
        "type": "Ice",
        "power": 110,
        "accuracy": 0.7,
        "category": "Special",
        "description": "Creates a huge freezing blizzard storm."
    },
    {
        "name": "Haze",
        "type": "Ice",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 0.8},
        "description": "Exhales a freezing mist, reducing enemy attack."
    },
    {
        "name": "Frost Breath",
        "type": "Ice",
        "power": 60,
        "accuracy": 0.9,
        "category": "Special",
        "description": "Blows a cold icy breath."
    },

    # --- Earth Moves (4) ---
    {
        "name": "Mud Slap",
        "type": "Earth",
        "power": 20,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Hurls mud to blind and damage target."
    },
    {
        "name": "Earthquake",
        "type": "Earth",
        "power": 100,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Triggers a massive tectonic earthquake."
    },
    {
        "name": "Rock Throw",
        "type": "Earth",
        "power": 50,
        "accuracy": 0.9,
        "category": "Physical",
        "description": "Throws small stones at the target."
    },
    {
        "name": "Sandstorm",
        "type": "Earth",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.3},
        "description": "Summons a sandstorm, boosting defense."
    },

    # --- Wind Moves (4) ---
    {
        "name": "Gust",
        "type": "Wind",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Creates a strong gust of wind."
    },
    {
        "name": "Hurricane",
        "type": "Wind",
        "power": 110,
        "accuracy": 0.7,
        "category": "Special",
        "description": "Traps target in a violent hurricane."
    },
    {
        "name": "Wing Attack",
        "type": "Wind",
        "power": 60,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Strikes target with wings."
    },
    {
        "name": "Tailwind",
        "type": "Wind",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "speed", "mult": 1.5},
        "description": "Summons gale winds, boosting Speed."
    },

    # --- Toxic Moves (4) ---
    {
        "name": "Acid",
        "type": "Toxic",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Sprays melting acid at target."
    },
    {
        "name": "Toxic",
        "type": "Toxic",
        "power": 0,
        "accuracy": 0.9,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 0.7},
        "description": "Infects target, corroding their Defense."
    },
    {
        "name": "Poison Fang",
        "type": "Toxic",
        "power": 50,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Bites target with toxic fangs."
    },
    {
        "name": "Sludge Bomb",
        "type": "Toxic",
        "power": 90,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Hurls toxic sludge bombs."
    },

    # --- Mind Moves (4) ---
    {
        "name": "Confusion",
        "type": "Mind",
        "power": 50,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Launches a telekinetic attack."
    },
    {
        "name": "Psychic",
        "type": "Mind",
        "power": 90,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Blasts target with psychic energy."
    },
    {
        "name": "Calm Mind",
        "type": "Mind",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 1.3},
        "description": "Focuses the mind to boost Attack."
    },
    {
        "name": "Psybeam",
        "type": "Mind",
        "power": 65,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires a colorful telekinetic beam."
    },

    # --- Metal Moves (4) ---
    {
        "name": "Metal Claw",
        "type": "Metal",
        "power": 50,
        "accuracy": 0.95,
        "category": "Physical",
        "description": "Strikes target with metallic claws."
    },
    {
        "name": "Iron Defense",
        "type": "Metal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.5},
        "description": "Hardens skin like iron, boosting Defense."
    },
    {
        "name": "Iron Head",
        "type": "Metal",
        "power": 80,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Slams target with an iron helmet head."
    },
    {
        "name": "Flash Cannon",
        "type": "Metal",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires a burst of metallic light energy."
    },

    # --- Light Moves (4) ---
    {
        "name": "Flash",
        "type": "Light",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 0.8},
        "description": "Flashes a bright light, lowering target attack."
    },
    {
        "name": "Light Screen",
        "type": "Light",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.4},
        "description": "Creates a light barrier, boosting Defense."
    },
    {
        "name": "Solar Flare",
        "type": "Light",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Blasts target with a burst of solar light."
    },
    {
        "name": "Judgment",
        "type": "Light",
        "power": 100,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires light beams from the heavens."
    },

    # --- Shadow Moves (4) ---
    {
        "name": "Shadow Claw",
        "type": "Shadow",
        "power": 70,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Strikes target with dark shadow claws."
    },
    {
        "name": "Shadow Ball",
        "type": "Shadow",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Hurls a shadowy energy ball."
    },
    {
        "name": "Dark Pulse",
        "type": "Shadow",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Releases a dark energy wave."
    },
    {
        "name": "Nasty Plot",
        "type": "Shadow",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 1.5},
        "description": "Plots in the shadows, boosting Attack."
    }
]

def generate():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "battle_pals", "data", "moves")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating {len(MOVES_DATA)} move JSON files inside: {output_dir}")
    
    for m in MOVES_DATA:
        # Convert move name to lowercase snake case for filename
        filename = m["name"].lower().replace(" ", "_") + ".json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=4, ensure_ascii=False)
            
    print("Move JSON files generated successfully!")

if __name__ == "__main__":
    generate()
