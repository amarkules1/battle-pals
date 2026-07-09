import os
import json

# Define the moves data list (166 unique moves)
MOVES_DATA = [
    # === Existing Moves (66) ===
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
    },

    # === NEW MOVES (100) ===
    # --- Normal Moves (17) ---
    {
        "name": "Pound",
        "type": "Normal",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Pounds target with limbs."
    },
    {
        "name": "Mega Punch",
        "type": "Normal",
        "power": 80,
        "accuracy": 0.85,
        "category": "Physical",
        "description": "A hard punch packed with power."
    },
    {
        "name": "Mega Kick",
        "type": "Normal",
        "power": 120,
        "accuracy": 0.75,
        "category": "Physical",
        "description": "A high-power kick."
    },
    {
        "name": "Cut",
        "type": "Normal",
        "power": 50,
        "accuracy": 0.95,
        "category": "Physical",
        "description": "Cuts the target with claws or blades."
    },
    {
        "name": "Horn Attack",
        "type": "Normal",
        "power": 65,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Jabs target with sharp horns."
    },
    {
        "name": "Fury Attack",
        "type": "Normal",
        "power": 15,
        "accuracy": 0.85,
        "category": "Physical",
        "description": "Repeatedly jabs target."
    },
    {
        "name": "Body Slam",
        "type": "Normal",
        "power": 85,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Slam attack that can paralyze."
    },
    {
        "name": "Take Down",
        "type": "Normal",
        "power": 90,
        "accuracy": 0.85,
        "category": "Physical",
        "description": "A reckless charge attack."
    },
    {
        "name": "Double-Edge",
        "type": "Normal",
        "power": 120,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "A life-risking tackle."
    },
    {
        "name": "Roar",
        "type": "Normal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 0.8},
        "description": "Roars loudly, lowering enemy attack."
    },
    {
        "name": "Disable",
        "type": "Normal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "speed", "mult": 0.8},
        "description": "Slows target down by disabling them."
    },
    {
        "name": "Minimize",
        "type": "Normal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.2},
        "description": "Compresses cells to boost Defense."
    },
    {
        "name": "Defense Curl",
        "type": "Normal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.2},
        "description": "Curls up to conceal weak spots."
    },
    {
        "name": "Quick Attack",
        "type": "Normal",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "An extremely fast attack."
    },
    {
        "name": "Pound Heavy",
        "type": "Normal",
        "power": 70,
        "accuracy": 0.9,
        "category": "Physical",
        "description": "Pounds target with massive weight."
    },
    {
        "name": "Pound Light",
        "type": "Normal",
        "power": 30,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Quick slap with light weight."
    },
    {
        "name": "Sing",
        "type": "Normal",
        "power": 0,
        "accuracy": 0.55,
        "category": "Status",
        "effect": {"stat": "speed", "mult": 0.5},
        "description": "Sings to put target to sleep (slows down)."
    },

    # --- Fire Moves (9) ---
    {
        "name": "Fire Punch",
        "type": "Fire",
        "power": 75,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "An explosive fiery punch."
    },
    {
        "name": "Fire Spin",
        "type": "Fire",
        "power": 35,
        "accuracy": 0.85,
        "category": "Special",
        "description": "Traps the target in fire."
    },
    {
        "name": "Lava Plume",
        "type": "Fire",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Scarlet flames torch everything."
    },
    {
        "name": "Inferno",
        "type": "Fire",
        "power": 100,
        "accuracy": 0.5,
        "category": "Special",
        "description": "Engulfs target in intense flame."
    },
    {
        "name": "Will-O-Wisp",
        "type": "Fire",
        "power": 0,
        "accuracy": 0.85,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 0.5},
        "description": "Inflicts burn, cutting enemy attack in half."
    },
    {
        "name": "Overheat",
        "type": "Fire",
        "power": 130,
        "accuracy": 0.9,
        "category": "Special",
        "description": "Releases full fire potential."
    },
    {
        "name": "Burn Up",
        "type": "Fire",
        "power": 130,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Burns out the user's fire power."
    },
    {
        "name": "Fire Spin Vortex",
        "type": "Fire",
        "power": 50,
        "accuracy": 0.9,
        "category": "Special",
        "description": "Traps target in a fire vortex."
    },
    {
        "name": "Flame Charge",
        "type": "Fire",
        "power": 50,
        "accuracy": 1.0,
        "category": "Physical",
        "effect": {"stat": "speed", "mult": 1.2},
        "description": "Tackles target, boosting user speed."
    },

    # --- Water Moves (10) ---
    {
        "name": "Bubble",
        "type": "Water",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Sprays bubbles at the target."
    },
    {
        "name": "Bubble Beam",
        "type": "Water",
        "power": 65,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Blasts bubbles at high speed."
    },
    {
        "name": "Water Spout",
        "type": "Water",
        "power": 150,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Spouts water; power scales with HP."
    },
    {
        "name": "Waterfall",
        "type": "Water",
        "power": 80,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Charges target with waterfall force."
    },
    {
        "name": "Clamp",
        "type": "Water",
        "power": 35,
        "accuracy": 0.85,
        "category": "Physical",
        "description": "Clamps the target with shells."
    },
    {
        "name": "Whirlpool",
        "type": "Water",
        "power": 35,
        "accuracy": 0.85,
        "category": "Special",
        "description": "Traps the target in a whirlpool."
    },
    {
        "name": "Aqua Ring",
        "type": "Water",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"heal": 0.1},
        "description": "Envelops user in water to heal."
    },
    {
        "name": "Muddy Water",
        "type": "Water",
        "power": 90,
        "accuracy": 0.85,
        "category": "Special",
        "description": "Sprays muddy water to blind."
    },
    {
        "name": "Aqua Ring Surge",
        "type": "Water",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"heal": 0.25},
        "description": "Aqua ring heals user significantly."
    },
    {
        "name": "Water Pulse Ray",
        "type": "Water",
        "power": 75,
        "accuracy": 0.95,
        "category": "Special",
        "description": "Fires pulsing water rays."
    },

    # --- Grass Moves (9) ---
    {
        "name": "Leaf Blade",
        "type": "Grass",
        "power": 90,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Slashes target with sharp leaves."
    },
    {
        "name": "Leech Seed",
        "type": "Grass",
        "power": 0,
        "accuracy": 0.9,
        "category": "Status",
        "effect": {"heal": 0.15},
        "description": "Steals target's HP to heal user."
    },
    {
        "name": "Grass Knot",
        "type": "Grass",
        "power": 60,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Trips the target with grass vines."
    },
    {
        "name": "Seed Bomb",
        "type": "Grass",
        "power": 80,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Hurls hard seed bombs."
    },
    {
        "name": "Wood Hammer",
        "type": "Grass",
        "power": 120,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Slams target with a heavy branch."
    },
    {
        "name": "Giga Drain",
        "type": "Grass",
        "power": 75,
        "accuracy": 1.0,
        "category": "Special",
        "effect": {"heal": 0.4},
        "description": "Drains HP from the target."
    },
    {
        "name": "Petal Dance",
        "type": "Grass",
        "power": 120,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Dances in petals to assault target."
    },
    {
        "name": "Spiky Shield Guard",
        "type": "Grass",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.5},
        "description": "Shields with sharp spikes."
    },
    {
        "name": "Mega Drain Blast",
        "type": "Grass",
        "power": 60,
        "accuracy": 1.0,
        "category": "Special",
        "effect": {"heal": 0.3},
        "description": "Drains target energy."
    },

    # --- Electric Moves (9) ---
    {
        "name": "Thunder Shock",
        "type": "Electric",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Jolts target with electricity."
    },
    {
        "name": "Electro Ball",
        "type": "Electric",
        "power": 60,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Hurls a ball of electricity."
    },
    {
        "name": "Discharge",
        "type": "Electric",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Discharges electricity to all nearby."
    },
    {
        "name": "Wild Charge",
        "type": "Electric",
        "power": 90,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Shrouds self in electricity and tackles."
    },
    {
        "name": "Zap Cannon",
        "type": "Electric",
        "power": 120,
        "accuracy": 0.5,
        "category": "Special",
        "description": "Blasts a huge electric cannonball."
    },
    {
        "name": "Charge",
        "type": "Electric",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.2},
        "description": "Charges electric power to boost defense."
    },
    {
        "name": "Electro Web",
        "type": "Electric",
        "power": 55,
        "accuracy": 0.95,
        "category": "Special",
        "description": "Traps target in an electric web."
    },
    {
        "name": "Volt Charge",
        "type": "Electric",
        "power": 50,
        "accuracy": 1.0,
        "category": "Special",
        "effect": {"stat": "speed", "mult": 1.2},
        "description": "Shoots electric bolt, boosting speed."
    },
    {
        "name": "Discharge Overdrive",
        "type": "Electric",
        "power": 95,
        "accuracy": 0.9,
        "category": "Special",
        "description": "A full electric discharge."
    },

    # --- Ice Moves (8) ---
    {
        "name": "Powder Snow",
        "type": "Ice",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Blasts target with powder snow."
    },
    {
        "name": "Ice Punch",
        "type": "Ice",
        "power": 75,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "An icy cold punch."
    },
    {
        "name": "Freeze-Dry",
        "type": "Ice",
        "power": 70,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Freezes target instantly."
    },
    {
        "name": "Icicle Crash",
        "type": "Ice",
        "power": 85,
        "accuracy": 0.9,
        "category": "Physical",
        "description": "Crashes large icicles from above."
    },
    {
        "name": "Icicle Spear",
        "type": "Ice",
        "power": 25,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Fires icicle spears in succession."
    },
    {
        "name": "Sheer Cold",
        "type": "Ice",
        "power": 150,
        "accuracy": 0.3,
        "category": "Special",
        "description": "Absolute zero cold blast."
    },
    {
        "name": "Frost Wave",
        "type": "Ice",
        "power": 45,
        "accuracy": 1.0,
        "category": "Special",
        "effect": {"stat": "speed", "mult": 0.8},
        "description": "Cold frost wave that slows target."
    },
    {
        "name": "Ice Spikes",
        "type": "Ice",
        "power": 60,
        "accuracy": 0.95,
        "category": "Physical",
        "description": "Throws sharp ice spikes."
    },

    # --- Earth Moves (8) ---
    {
        "name": "Rock Slide",
        "type": "Earth",
        "power": 75,
        "accuracy": 0.9,
        "category": "Physical",
        "description": "Slides large rocks onto target."
    },
    {
        "name": "Stone Edge",
        "type": "Earth",
        "power": 100,
        "accuracy": 0.8,
        "category": "Physical",
        "description": "Stabs target with sharp stones."
    },
    {
        "name": "Mud Shot",
        "type": "Earth",
        "power": 55,
        "accuracy": 0.95,
        "category": "Special",
        "description": "Shoots mud to slow speed."
    },
    {
        "name": "Bulldoze",
        "type": "Earth",
        "power": 60,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Bulldozes the ground to hit."
    },
    {
        "name": "Earth Power",
        "type": "Earth",
        "power": 90,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Erupts earth beneath the target."
    },
    {
        "name": "Sand Tomb",
        "type": "Earth",
        "power": 35,
        "accuracy": 0.85,
        "category": "Physical",
        "description": "Traps target in a quicksand tomb."
    },
    {
        "name": "Mud Shield",
        "type": "Earth",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.4},
        "description": "Mud shield raises defense."
    },
    {
        "name": "Stone Blast",
        "type": "Earth",
        "power": 70,
        "accuracy": 0.9,
        "category": "Special",
        "description": "Launches stone blasts."
    },

    # --- Wind Moves (7) ---
    {
        "name": "Air Cutter",
        "type": "Wind",
        "power": 60,
        "accuracy": 0.95,
        "category": "Special",
        "description": "Slashes target with wind blades."
    },
    {
        "name": "Air Slash",
        "type": "Wind",
        "power": 75,
        "accuracy": 0.95,
        "category": "Special",
        "description": "Slashes target with air currents."
    },
    {
        "name": "Defog",
        "type": "Wind",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 0.8},
        "description": "Blows wind to blow away defense barriers."
    },
    {
        "name": "Feather Dance",
        "type": "Wind",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 0.5},
        "description": "Covers target in feathers, cutting Attack."
    },
    {
        "name": "Sky Attack",
        "type": "Wind",
        "power": 140,
        "accuracy": 0.9,
        "category": "Physical",
        "description": "A high-power dive bomb attack."
    },
    {
        "name": "Air Blast",
        "type": "Wind",
        "power": 80,
        "accuracy": 0.95,
        "category": "Special",
        "description": "Fires air blasts."
    },
    {
        "name": "Wind Shield",
        "type": "Wind",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.3},
        "description": "Wind wall shields target."
    },

    # --- Toxic Moves (7) ---
    {
        "name": "Poison Sting",
        "type": "Toxic",
        "power": 15,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Jabs target with toxic stinger."
    },
    {
        "name": "Poison Powder",
        "type": "Toxic",
        "power": 0,
        "accuracy": 0.75,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 0.8},
        "description": "Weakens target with toxic powder."
    },
    {
        "name": "Sludge",
        "type": "Toxic",
        "power": 65,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Throws toxic sludge at target."
    },
    {
        "name": "Sludge Wave",
        "type": "Toxic",
        "power": 95,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Swamps target in a toxic wave."
    },
    {
        "name": "Toxic Spikes",
        "type": "Toxic",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "speed", "mult": 0.8},
        "description": "Scatters toxic spikes to slow target."
    },
    {
        "name": "Acid Armor",
        "type": "Toxic",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.5},
        "description": "Liquefies body in acid to boost Defense."
    },
    {
        "name": "Venom Drip",
        "type": "Toxic",
        "power": 40,
        "accuracy": 1.0,
        "category": "Special",
        "effect": {"stat": "defense", "mult": 0.8},
        "description": "Venom drips on target, corroding defense."
    },

    # --- Mind Moves (6) ---
    {
        "name": "Zen Headbutt",
        "type": "Mind",
        "power": 80,
        "accuracy": 0.9,
        "category": "Physical",
        "description": "Focuses Zen energy in a headbutt."
    },
    {
        "name": "Extrasensory",
        "type": "Mind",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires an odd telekinetic force."
    },
    {
        "name": "Agility",
        "type": "Mind",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "speed", "mult": 1.5},
        "description": "Relaxes body to double Speed."
    },
    {
        "name": "Barrier",
        "type": "Mind",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "defense", "mult": 1.5},
        "description": "Creates a psychic wall, boosting Defense."
    },
    {
        "name": "Future Sight",
        "type": "Mind",
        "power": 120,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Calculates future vectors to hit."
    },
    {
        "name": "Mind Blast",
        "type": "Mind",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Blasts target with telekinetic mind waves."
    },

    # --- Metal Moves (5) ---
    {
        "name": "Bullet Punch",
        "type": "Metal",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Punches fast like a bullet."
    },
    {
        "name": "Gear Grind",
        "type": "Metal",
        "power": 50,
        "accuracy": 0.85,
        "category": "Physical",
        "description": "Grinds target with steel gears."
    },
    {
        "name": "Heavy Slam",
        "type": "Metal",
        "power": 80,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Slams target with a heavy body."
    },
    {
        "name": "Autotomize",
        "type": "Metal",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "speed", "mult": 1.5},
        "description": "Sheds weight to boost Speed."
    },
    {
        "name": "Metal Burst",
        "type": "Metal",
        "power": 100,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Releases metallic shards on contact."
    },

    # --- Light Moves (5) ---
    {
        "name": "Dazzling Gleam",
        "type": "Light",
        "power": 80,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Blinds target with dazzling light."
    },
    {
        "name": "Luster Purge",
        "type": "Light",
        "power": 70,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires a purging blast of light."
    },
    {
        "name": "Tail Glow",
        "type": "Light",
        "power": 0,
        "accuracy": 1.0,
        "category": "Status",
        "effect": {"stat": "attack", "mult": 1.5},
        "description": "Glows tail brightly, boosting Attack."
    },
    {
        "name": "Prism Laser",
        "type": "Light",
        "power": 120,
        "accuracy": 1.0,
        "category": "Special",
        "description": "Fires a rainbow laser from prisms."
    },
    {
        "name": "Mirror Shot",
        "type": "Light",
        "power": 60,
        "accuracy": 0.85,
        "category": "Special",
        "description": "Reflects light flash to damage."
    },

    # --- Shadow Moves (5) ---
    {
        "name": "Bite",
        "type": "Shadow",
        "power": 60,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Bites target with shadow energy."
    },
    {
        "name": "Crunch",
        "type": "Shadow",
        "power": 80,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Crunches target with dark power."
    },
    {
        "name": "Shadow Sneak",
        "type": "Shadow",
        "power": 40,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Attacks from target's shadow."
    },
    {
        "name": "Sucker Punch",
        "type": "Shadow",
        "power": 70,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Hits target while they prepare."
    },
    {
        "name": "Night Slash",
        "type": "Shadow",
        "power": 70,
        "accuracy": 1.0,
        "category": "Physical",
        "description": "Slashes target in the dark."
    }
]

def generate():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "battle_pals", "data", "moves")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating {len(MOVES_DATA)} move JSON files inside: {output_dir}")
    
    for m in MOVES_DATA:
        filename = m["name"].lower().replace(" ", "_").replace("-", "_") + ".json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=4, ensure_ascii=False)
            
    print("Move JSON files generated successfully!")

if __name__ == "__main__":
    generate()
