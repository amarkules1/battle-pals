import os
import json

# Define the 50 species data list
SPECIES_DATA = [
    # --- Starters & Evolutions (9) ---
    {
        "name": "Leaflet",
        "types": ["Grass", "Wind"],
        "base_stats": {"hp": 45, "attack": 49, "defense": 65, "speed": 45},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 1, "move": "Growl"},
            {"level": 3, "move": "Gust"},
            {"level": 5, "move": "Razor Leaf"},
            {"level": 8, "move": "Synthesize"},
            {"level": 12, "move": "Mega Drain"}
        ],
        "trait": "Overgrow",
        "evolves_from": None,
        "evolves_into": "Florafox",
        "evolution_level": 16,
        "description": "A small grassy seedling that floats gracefully on wind currents.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [115, 198, 80, 255],
            "accent_color": [46, 204, 113, 255],
            "belly_color": [215, 235, 150, 255],
            "ears": "leaf",
            "tail": "leaf",
            "head_sprout": True,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Florafox",
        "types": ["Grass", "Wind"],
        "base_stats": {"hp": 60, "attack": 62, "defense": 80, "speed": 60},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 1, "move": "Growl"},
            {"level": 3, "move": "Gust"},
            {"level": 5, "move": "Razor Leaf"},
            {"level": 8, "move": "Synthesize"},
            {"level": 16, "move": "Air Cutter"},
            {"level": 20, "move": "Leaf Blade"}
        ],
        "trait": "Overgrow",
        "evolves_from": "Leaflet",
        "evolves_into": "Vinedrake",
        "evolution_level": 32,
        "description": "An elegant fox-like Pal adorned with blooming leaf decorations.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [90, 180, 70, 255],
            "accent_color": [39, 174, 96, 255],
            "belly_color": [220, 240, 170, 255],
            "ears": "pointy",
            "tail": "leaf",
            "head_sprout": True,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Vinedrake",
        "types": ["Grass", "Dragon"],
        "base_stats": {"hp": 80, "attack": 85, "defense": 95, "speed": 80},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 1, "move": "Growl"},
            {"level": 5, "move": "Razor Leaf"},
            {"level": 16, "move": "Air Cutter"},
            {"level": 20, "move": "Leaf Blade"},
            {"level": 32, "move": "Solar Beam"},
            {"level": 40, "move": "Wood Hammer"}
        ],
        "trait": "Overgrow",
        "evolves_from": "Florafox",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A magnificent forest dragon that summons thick vines and gales.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [46, 204, 113, 255],
            "accent_color": [26, 188, 156, 255],
            "belly_color": [241, 250, 218, 255],
            "ears": "pointy",
            "tail": "leaf",
            "head_sprout": True,
            "horn": "dual",
            "wings": "feathered"
        }
    },
    {
        "name": "Pyropup",
        "types": ["Fire"],
        "base_stats": {"hp": 39, "attack": 52, "defense": 43, "speed": 65},
        "learnset": [
            {"level": 1, "move": "Scratch"},
            {"level": 1, "move": "Growl"},
            {"level": 4, "move": "Ember"},
            {"level": 9, "move": "Tail Whip"},
            {"level": 12, "move": "Flame Wheel"}
        ],
        "trait": "Blaze",
        "evolves_from": None,
        "evolves_into": "Blazecat",
        "evolution_level": 16,
        "description": "A warm-blooded puppy Pal. Its tail burns brighter when excited.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [235, 94, 85, 255],
            "accent_color": [243, 156, 18, 255],
            "belly_color": [253, 224, 71, 255],
            "ears": "puppy",
            "tail": "flame",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Blazecat",
        "types": ["Fire", "Shadow"],
        "base_stats": {"hp": 58, "attack": 64, "defense": 58, "speed": 80},
        "learnset": [
            {"level": 1, "move": "Scratch"},
            {"level": 1, "move": "Growl"},
            {"level": 4, "move": "Ember"},
            {"level": 12, "move": "Flame Wheel"},
            {"level": 16, "move": "Bite"},
            {"level": 22, "move": "Flamethrower"}
        ],
        "trait": "Blaze",
        "evolves_from": "Pyropup",
        "evolves_into": "Infernoct",
        "evolution_level": 32,
        "description": "A stealthy feline Pal that stalks in the dark and breathes flames.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [192, 57, 43, 255],
            "accent_color": [142, 68, 173, 255],
            "belly_color": [241, 196, 15, 255],
            "ears": "pointy",
            "tail": "flame",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Infernoct",
        "types": ["Fire", "Shadow"],
        "base_stats": {"hp": 78, "attack": 84, "defense": 78, "speed": 100},
        "learnset": [
            {"level": 1, "move": "Scratch"},
            {"level": 4, "move": "Ember"},
            {"level": 16, "move": "Bite"},
            {"level": 22, "move": "Flamethrower"},
            {"level": 32, "move": "Fire Blast"},
            {"level": 40, "move": "Dark Pulse"}
        ],
        "trait": "Blaze",
        "evolves_from": "Blazecat",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A feared demon Pal with wings made of pure ash and dark fire.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [44, 62, 80, 255],
            "accent_color": [231, 76, 60, 255],
            "belly_color": [155, 89, 182, 255],
            "ears": "pointy",
            "tail": "flame",
            "head_sprout": False,
            "horn": "dual",
            "wings": "bat"
        }
    },
    {
        "name": "Aquasplash",
        "types": ["Water", "Ice"],
        "base_stats": {"hp": 44, "attack": 48, "defense": 65, "speed": 43},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 1, "move": "Tail Whip"},
            {"level": 3, "move": "Ice Shard"},
            {"level": 6, "move": "Water Gun"},
            {"level": 9, "move": "Bubble"},
            {"level": 14, "move": "Water Pulse"}
        ],
        "trait": "Torrent",
        "evolves_from": None,
        "evolves_into": "Seashell",
        "evolution_level": 16,
        "description": "A playful otter Pal. It produces icy bubbles to defend itself.",
        "appearance": {
            "base_shape": "aquatic",
            "body_color": [74, 144, 226, 255],
            "accent_color": [52, 152, 219, 255],
            "belly_color": [236, 240, 241, 255],
            "ears": "fins",
            "tail": "flipper",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Seashell",
        "types": ["Water", "Ice"],
        "base_stats": {"hp": 59, "attack": 63, "defense": 80, "speed": 58},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 1, "move": "Tail Whip"},
            {"level": 3, "move": "Ice Shard"},
            {"level": 6, "move": "Water Gun"},
            {"level": 14, "move": "Water Pulse"},
            {"level": 18, "move": "Ice Beam"},
            {"level": 22, "move": "Surf"}
        ],
        "trait": "Torrent",
        "evolves_from": "Aquasplash",
        "evolves_into": "Krakentos",
        "evolution_level": 32,
        "description": "Carries a thick frozen shell that absorbs massive heavy blows.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [41, 128, 185, 255],
            "accent_color": [116, 215, 238, 255],
            "belly_color": [253, 254, 220, 255],
            "ears": "fins",
            "tail": "flipper",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Krakentos",
        "types": ["Water", "Toxic"],
        "base_stats": {"hp": 79, "attack": 83, "defense": 100, "speed": 78},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 6, "move": "Water Gun"},
            {"level": 14, "move": "Water Pulse"},
            {"level": 22, "move": "Surf"},
            {"level": 32, "move": "Hydro Pump"},
            {"level": 36, "move": "Sludge Bomb"}
        ],
        "trait": "Torrent",
        "evolves_from": "Seashell",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A deep sea monster that floods shores and leaks corrosive ink.",
        "appearance": {
            "base_shape": "aquatic",
            "body_color": [22, 160, 133, 255],
            "accent_color": [142, 68, 173, 255],
            "belly_color": [26, 188, 156, 255],
            "ears": "fins",
            "tail": "flipper",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },

    # --- Normal Wild Pals (5) ---
    {
        "name": "Chubby",
        "types": ["Normal"],
        "base_stats": {"hp": 90, "attack": 40, "defense": 40, "speed": 20},
        "learnset": [
            {"level": 1, "move": "Pound"},
            {"level": 1, "move": "Growl"},
            {"level": 5, "move": "Double Slap"},
            {"level": 10, "move": "Harden"},
            {"level": 15, "move": "Recover"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": "Grizzo",
        "evolution_level": 20,
        "description": "A round, chubby blob that rolls around sleeping and eating.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [220, 220, 220, 255],
            "accent_color": [180, 180, 180, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "puppy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Grizzo",
        "types": ["Normal"],
        "base_stats": {"hp": 120, "attack": 80, "defense": 70, "speed": 40},
        "learnset": [
            {"level": 1, "move": "Pound"},
            {"level": 1, "move": "Growl"},
            {"level": 5, "move": "Double Slap"},
            {"level": 20, "move": "Slam"},
            {"level": 25, "move": "Body Slam"},
            {"level": 30, "move": "Hyper Beam"}
        ],
        "trait": "Clear Body",
        "evolves_from": "Chubby",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A giant grizzly bear-like Pal that defends its territory fiercely.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [139, 69, 19, 255],
            "accent_color": [160, 82, 45, 255],
            "belly_color": [222, 184, 135, 255],
            "ears": "puppy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Swiftwing",
        "types": ["Normal", "Wind"],
        "base_stats": {"hp": 40, "attack": 45, "defense": 35, "speed": 75},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 3, "move": "Gust"},
            {"level": 8, "move": "Quick Attack"},
            {"level": 12, "move": "Wing Attack"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": "Galehawk",
        "evolution_level": 18,
        "description": "A tiny bird Pal that flies at supersonic speeds.",
        "appearance": {
            "base_shape": "bird",
            "body_color": [245, 222, 179, 255],
            "accent_color": [210, 180, 140, 255],
            "belly_color": [255, 250, 240, 255],
            "ears": "none",
            "tail": "none",
            "head_sprout": False,
            "horn": "none",
            "wings": "feathered"
        }
    },
    {
        "name": "Galehawk",
        "types": ["Wind", "Light"],
        "base_stats": {"hp": 65, "attack": 75, "defense": 60, "speed": 105},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 3, "move": "Gust"},
            {"level": 12, "move": "Wing Attack"},
            {"level": 18, "move": "Air Cutter"},
            {"level": 24, "move": "Tailwind"},
            {"level": 30, "move": "Hurricane"}
        ],
        "trait": "Clear Body",
        "evolves_from": "Swiftwing",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A golden bird of prey that shoots rays of sun from its feathers.",
        "appearance": {
            "base_shape": "bird",
            "body_color": [241, 196, 15, 255],
            "accent_color": [230, 126, 34, 255],
            "belly_color": [253, 254, 220, 255],
            "ears": "none",
            "tail": "none",
            "head_sprout": False,
            "horn": "single",
            "wings": "feathered"
        }
    },
    {
        "name": "Rattler",
        "types": ["Normal"],
        "base_stats": {"hp": 30, "attack": 56, "defense": 35, "speed": 72},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 1, "move": "Growl"},
            {"level": 4, "move": "Quick Attack"},
            {"level": 7, "move": "Bite"},
            {"level": 10, "move": "Tail Whip"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A quick rat Pal that lives in tall grass fields.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [155, 89, 182, 255],
            "accent_color": [142, 68, 173, 255],
            "belly_color": [241, 240, 230, 255],
            "ears": "pointy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },

    # --- Electric Wild Pals (4) ---
    {
        "name": "Sparky",
        "types": ["Electric"],
        "base_stats": {"hp": 35, "attack": 55, "defense": 30, "speed": 90},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Thunder Shock"},
            {"level": 8, "move": "Spark"},
            {"level": 12, "move": "Thunder Wave"}
        ],
        "trait": "Volt Absorb",
        "evolves_from": None,
        "evolves_into": "Thundermouse",
        "evolution_level": 15,
        "description": "A small yellow rodent that stores electrical static in its cheeks.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [241, 196, 15, 255],
            "accent_color": [243, 156, 18, 255],
            "belly_color": [253, 254, 220, 255],
            "ears": "pointy",
            "tail": "flame",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Thundermouse",
        "types": ["Electric"],
        "base_stats": {"hp": 60, "attack": 75, "defense": 50, "speed": 110},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Thunder Shock"},
            {"level": 8, "move": "Spark"},
            {"level": 15, "move": "Thunderbolt"},
            {"level": 22, "move": "Volt Tackle"}
        ],
        "trait": "Volt Absorb",
        "evolves_from": "Sparky",
        "evolves_into": None,
        "evolution_level": None,
        "description": "Fires high-voltage beams from its lightning-bolt tail.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [243, 156, 18, 255],
            "accent_color": [230, 126, 34, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "pointy",
            "tail": "flame",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Voltcat",
        "types": ["Electric"],
        "base_stats": {"hp": 65, "attack": 90, "defense": 60, "speed": 95},
        "learnset": [
            {"level": 1, "move": "Scratch"},
            {"level": 5, "move": "Spark"},
            {"level": 12, "move": "Volt Charge"},
            {"level": 18, "move": "Thunderbolt"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A lightning fast cheetah Pal that crackles with electricity.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [241, 196, 15, 255],
            "accent_color": [44, 62, 80, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "pointy",
            "tail": "flame",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Stormeagle",
        "types": ["Electric", "Wind"],
        "base_stats": {"hp": 70, "attack": 80, "defense": 65, "speed": 100},
        "learnset": [
            {"level": 1, "move": "Gust"},
            {"level": 6, "move": "Spark"},
            {"level": 14, "move": "Wing Attack"},
            {"level": 20, "move": "Thunderbolt"},
            {"level": 28, "move": "Hurricane"}
        ],
        "trait": "Volt Absorb",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "An eagle that nestles in storm clouds, calling down lightning.",
        "appearance": {
            "base_shape": "bird",
            "body_color": [52, 152, 219, 255],
            "accent_color": [241, 196, 15, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "none",
            "tail": "none",
            "head_sprout": False,
            "horn": "single",
            "wings": "feathered"
        }
    },

    # --- Ice Wild Pals (4) ---
    {
        "name": "Frosty",
        "types": ["Ice"],
        "base_stats": {"hp": 45, "attack": 35, "defense": 55, "speed": 40},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Powder Snow"},
            {"level": 8, "move": "Ice Shard"},
            {"level": 12, "move": "Haze"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": "Snowball",
        "evolution_level": 15,
        "description": "A floating frost cloud that freezes water on contact.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [224, 247, 250, 255],
            "accent_color": [128, 222, 234, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "fins",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Snowball",
        "types": ["Ice"],
        "base_stats": {"hp": 75, "attack": 65, "defense": 85, "speed": 60},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Powder Snow"},
            {"level": 8, "move": "Ice Shard"},
            {"level": 15, "move": "Ice Beam"},
            {"level": 22, "move": "Blizzard"}
        ],
        "trait": "Clear Body",
        "evolves_from": "Frosty",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A rolling snowball monster that grows larger in snowstorms.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [240, 255, 255, 255],
            "accent_color": [176, 224, 230, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "none",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Icelope",
        "types": ["Ice", "Earth"],
        "base_stats": {"hp": 70, "attack": 85, "defense": 70, "speed": 85},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 5, "move": "Ice Shard"},
            {"level": 10, "move": "Rock Throw"},
            {"level": 16, "move": "Ice Beam"},
            {"level": 22, "move": "Icicle Crash"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "An antelope Pal with horns made of raw glacial ice crystals.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [224, 255, 255, 255],
            "accent_color": [0, 206, 209, 255],
            "belly_color": [240, 248, 255, 255],
            "ears": "pointy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "dual",
            "wings": "none"
        }
    },
    {
        "name": "Glacier",
        "types": ["Ice", "Metal"],
        "base_stats": {"hp": 90, "attack": 90, "defense": 120, "speed": 40},
        "learnset": [
            {"level": 1, "move": "Harden"},
            {"level": 4, "move": "Ice Shard"},
            {"level": 12, "move": "Bullet Punch"},
            {"level": 18, "move": "Icicle Crash"},
            {"level": 26, "move": "Blizzard"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A massive golem covered in sheet metal and unmelting ice armor.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [189, 195, 199, 255],
            "accent_color": [116, 215, 238, 255],
            "belly_color": [236, 240, 241, 255],
            "ears": "none",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },

    # --- Earth Wild Pals (4) ---
    {
        "name": "Rocky",
        "types": ["Earth"],
        "base_stats": {"hp": 50, "attack": 65, "defense": 85, "speed": 35},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 1, "move": "Harden"},
            {"level": 5, "move": "Rock Throw"},
            {"level": 10, "move": "Mud Shot"},
            {"level": 14, "move": "Rock Slide"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": "Gravelord",
        "evolution_level": 20,
        "description": "A small rock spirit that bounds along canyons and gravel paths.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [121, 85, 72, 255],
            "accent_color": [184, 134, 11, 255],
            "belly_color": [215, 204, 200, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },
    {
        "name": "Gravelord",
        "types": ["Earth", "Metal"],
        "base_stats": {"hp": 85, "attack": 100, "defense": 125, "speed": 55},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 5, "move": "Rock Throw"},
            {"level": 14, "move": "Rock Slide"},
            {"level": 20, "move": "Iron Head"},
            {"level": 28, "move": "Earthquake"}
        ],
        "trait": "Clear Body",
        "evolves_from": "Rocky",
        "evolves_into": None,
        "evolution_level": None,
        "description": "An armored lord of tectonic plates that crushes iron structures.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [78, 52, 46, 255],
            "accent_color": [120, 144, 156, 255],
            "belly_color": [141, 110, 99, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "dual",
            "wings": "none"
        }
    },
    {
        "name": "Molehole",
        "types": ["Earth"],
        "base_stats": {"hp": 55, "attack": 75, "defense": 60, "speed": 60},
        "learnset": [
            {"level": 1, "move": "Scratch"},
            {"level": 4, "move": "Mud Slap"},
            {"level": 8, "move": "Rock Throw"},
            {"level": 14, "move": "Earth Power"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A mole Pal that digs deep underground caverns at high speed.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [109, 76, 65, 255],
            "accent_color": [244, 143, 177, 255],
            "belly_color": [215, 204, 200, 255],
            "ears": "puppy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Sandcrawler",
        "types": ["Earth"],
        "base_stats": {"hp": 60, "attack": 80, "defense": 80, "speed": 55},
        "learnset": [
            {"level": 1, "move": "Scratch"},
            {"level": 5, "move": "Sandstorm"},
            {"level": 10, "move": "Mud Shot"},
            {"level": 16, "move": "Earth Power"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "An insectoid crawler that triggers dust and sandstorms.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [210, 180, 140, 255],
            "accent_color": [139, 128, 0, 255],
            "belly_color": [245, 222, 179, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },

    # --- Wind Wild Pals (2) ---
    {
        "name": "Windry",
        "types": ["Wind"],
        "base_stats": {"hp": 45, "attack": 50, "defense": 40, "speed": 85},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 3, "move": "Gust"},
            {"level": 8, "move": "Tailwind"},
            {"level": 14, "move": "Air Slash"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A bird Pal that flies silently using glider-like feathers.",
        "appearance": {
            "base_shape": "bird",
            "body_color": [135, 206, 235, 255],
            "accent_color": [255, 255, 255, 255],
            "belly_color": [224, 247, 250, 255],
            "ears": "none",
            "tail": "none",
            "head_sprout": False,
            "horn": "none",
            "wings": "feathered"
        }
    },
    {
        "name": "Breezy",
        "types": ["Wind"],
        "base_stats": {"hp": 55, "attack": 40, "defense": 45, "speed": 75},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 3, "move": "Gust"},
            {"level": 8, "move": "Tailwind"},
            {"level": 12, "move": "Swift"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A cute wind sprite that drifts with seasonal drafts.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [224, 242, 241, 255],
            "accent_color": [178, 223, 219, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "none",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "feathered"
        }
    },

    # --- Toxic Wild Pals (4) ---
    {
        "name": "Gloop",
        "types": ["Toxic"],
        "base_stats": {"hp": 65, "attack": 45, "defense": 50, "speed": 35},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Acid"},
            {"level": 8, "move": "Toxic"},
            {"level": 12, "move": "Sludge"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": "Vipera",
        "evolution_level": 18,
        "description": "A toxic jelly Pal that dissolves trash and metals.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [155, 89, 182, 255],
            "accent_color": [142, 68, 173, 255],
            "belly_color": [241, 230, 250, 255],
            "ears": "none",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Vipera",
        "types": ["Toxic"],
        "base_stats": {"hp": 85, "attack": 75, "defense": 70, "speed": 65},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Acid"},
            {"level": 8, "move": "Toxic"},
            {"level": 18, "move": "Poison Fang"},
            {"level": 24, "move": "Sludge Bomb"}
        ],
        "trait": "Clear Body",
        "evolves_from": "Gloop",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A venomous snake-like Pal that spits acid at its prey.",
        "appearance": {
            "base_shape": "aquatic",
            "body_color": [125, 60, 152, 255],
            "accent_color": [46, 204, 113, 255],
            "belly_color": [212, 172, 232, 255],
            "ears": "fins",
            "tail": "flipper",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },
    {
        "name": "Noxious",
        "types": ["Toxic", "Shadow"],
        "base_stats": {"hp": 65, "attack": 85, "defense": 65, "speed": 75},
        "learnset": [
            {"level": 1, "move": "Scratch"},
            {"level": 4, "move": "Acid"},
            {"level": 10, "move": "Poison Fang"},
            {"level": 16, "move": "Shadow Claw"},
            {"level": 22, "move": "Sludge Bomb"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A quadruped beast covered in toxic vapor and shadows.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [88, 24, 69, 255],
            "accent_color": [144, 12, 63, 255],
            "belly_color": [218, 247, 166, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Acidbug",
        "types": ["Toxic", "Earth"],
        "base_stats": {"hp": 70, "attack": 65, "defense": 95, "speed": 50},
        "learnset": [
            {"level": 1, "move": "Harden"},
            {"level": 4, "move": "Acid"},
            {"level": 10, "move": "Rock Throw"},
            {"level": 16, "move": "Acid Armor"},
            {"level": 22, "move": "Sludge Bomb"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "An armored insectoid beetle that sprays heavy acid blocks.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [141, 110, 99, 255],
            "accent_color": [156, 39, 176, 255],
            "belly_color": [225, 190, 231, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },

    # --- Mind Wild Pals (4) ---
    {
        "name": "Psiwyrm",
        "types": ["Mind"],
        "base_stats": {"hp": 40, "attack": 60, "defense": 45, "speed": 75},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Confusion"},
            {"level": 9, "move": "Swift"},
            {"level": 12, "move": "Psybeam"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": "Psycat",
        "evolution_level": 22,
        "description": "A floating psychic worm that uses telekinesis to hover.",
        "appearance": {
            "base_shape": "aquatic",
            "body_color": [244, 143, 177, 255],
            "accent_color": [240, 98, 146, 255],
            "belly_color": [252, 228, 236, 255],
            "ears": "fins",
            "tail": "flipper",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },
    {
        "name": "Psycat",
        "types": ["Mind"],
        "base_stats": {"hp": 65, "attack": 85, "defense": 60, "speed": 100},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Confusion"},
            {"level": 12, "move": "Psybeam"},
            {"level": 22, "move": "Psychic"},
            {"level": 28, "move": "Future Sight"}
        ],
        "trait": "Clear Body",
        "evolves_from": "Psiwyrm",
        "evolves_into": None,
        "evolution_level": None,
        "description": "An elegant feline Pal that bends spoons and controls objects.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [233, 30, 99, 255],
            "accent_color": [156, 39, 176, 255],
            "belly_color": [248, 187, 208, 255],
            "ears": "pointy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Brainy",
        "types": ["Mind"],
        "base_stats": {"hp": 60, "attack": 75, "defense": 70, "speed": 55},
        "learnset": [
            {"level": 1, "move": "Growl"},
            {"level": 4, "move": "Confusion"},
            {"level": 10, "move": "Calm Mind"},
            {"level": 16, "move": "Mind Blast"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A floating brain Pal. It reads minds to predict enemy moves.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [248, 187, 208, 255],
            "accent_color": [244, 143, 177, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "none",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Alakazam",
        "types": ["Mind", "Light"],
        "base_stats": {"hp": 60, "attack": 90, "defense": 55, "speed": 110},
        "learnset": [
            {"level": 1, "move": "Confusion"},
            {"level": 5, "move": "Flash"},
            {"level": 12, "move": "Psybeam"},
            {"level": 20, "move": "Psychic"},
            {"level": 30, "move": "Future Sight"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "Its brain cells grow infinitely, giving it godlike memory.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [241, 196, 15, 255],
            "accent_color": [253, 254, 220, 255],
            "belly_color": [245, 222, 179, 255],
            "ears": "pointy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "dual",
            "wings": "none"
        }
    },

    # --- Metal Wild Pals (4) ---
    {
        "name": "Ironclad",
        "types": ["Metal"],
        "base_stats": {"hp": 55, "attack": 70, "defense": 90, "speed": 35},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 1, "move": "Harden"},
            {"level": 5, "move": "Bullet Punch"},
            {"level": 10, "move": "Metal Claw"},
            {"level": 15, "move": "Iron Defense"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": "GigaMech",
        "evolution_level": 25,
        "description": "An armored armadillo clad in scrap steel plates.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [149, 165, 166, 255],
            "accent_color": [127, 140, 141, 255],
            "belly_color": [220, 220, 220, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },
    {
        "name": "GigaMech",
        "types": ["Metal", "Earth"],
        "base_stats": {"hp": 85, "attack": 110, "defense": 130, "speed": 55},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 5, "move": "Bullet Punch"},
            {"level": 10, "move": "Metal Claw"},
            {"level": 15, "move": "Iron Defense"},
            {"level": 25, "move": "Iron Head"},
            {"level": 32, "move": "Earthquake"}
        ],
        "trait": "Clear Body",
        "evolves_from": "Ironclad",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A gigantic steam engine golem built from ancient metal cores.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [52, 73, 94, 255],
            "accent_color": [149, 165, 166, 255],
            "belly_color": [127, 140, 141, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "dual",
            "wings": "none"
        }
    },
    {
        "name": "Steelwing",
        "types": ["Metal", "Wind"],
        "base_stats": {"hp": 65, "attack": 80, "defense": 85, "speed": 90},
        "learnset": [
            {"level": 1, "move": "Gust"},
            {"level": 4, "move": "Metal Claw"},
            {"level": 12, "move": "Wing Attack"},
            {"level": 18, "move": "Iron Head"},
            {"level": 24, "move": "Flash Cannon"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A steel bird that slices clouds using razor-sharp metallic feathers.",
        "appearance": {
            "base_shape": "bird",
            "body_color": [189, 195, 199, 255],
            "accent_color": [52, 73, 94, 255],
            "belly_color": [236, 240, 241, 255],
            "ears": "none",
            "tail": "none",
            "head_sprout": False,
            "horn": "none",
            "wings": "feathered"
        }
    },
    {
        "name": "Rusty",
        "types": ["Metal", "Toxic"],
        "base_stats": {"hp": 60, "attack": 65, "defense": 80, "speed": 50},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Acid"},
            {"level": 10, "move": "Bullet Punch"},
            {"level": 16, "move": "Sludge Bomb"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A discarded machine Pal that leaks heavy acids and rusts over.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [120, 110, 90, 255],
            "accent_color": [211, 84, 0, 255],
            "belly_color": [189, 195, 199, 255],
            "ears": "none",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },

    # --- Light Wild Pals (4) ---
    {
        "name": "Solaris",
        "types": ["Light"],
        "base_stats": {"hp": 55, "attack": 65, "defense": 50, "speed": 80},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Flash"},
            {"level": 9, "move": "Swift"},
            {"level": 14, "move": "Solar Flare"}
        ],
        "trait": "Chlorophyll",
        "evolves_from": None,
        "evolves_into": "Luxor",
        "evolution_level": 24,
        "description": "A sun spirit that absorbs UV rays to output white light bursts.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [254, 249, 195, 255],
            "accent_color": [234, 179, 8, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "pointy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },
    {
        "name": "Luxor",
        "types": ["Light", "Mind"],
        "base_stats": {"hp": 80, "attack": 85, "defense": 70, "speed": 105},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Flash"},
            {"level": 14, "move": "Solar Flare"},
            {"level": 24, "move": "Dazzling Gleam"},
            {"level": 30, "move": "Judgment"}
        ],
        "trait": "Chlorophyll",
        "evolves_from": "Solaris",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A golden guardian that projects telekinetic shields made of light waves.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [253, 224, 71, 255],
            "accent_color": [253, 254, 220, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "pointy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "single",
            "wings": "none"
        }
    },
    {
        "name": "Angelix",
        "types": ["Light", "Wind"],
        "base_stats": {"hp": 70, "attack": 75, "defense": 65, "speed": 95},
        "learnset": [
            {"level": 1, "move": "Gust"},
            {"level": 5, "move": "Flash"},
            {"level": 12, "move": "Air Slash"},
            {"level": 18, "move": "Luster Purge"},
            {"level": 26, "move": "Judgment"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A sacred wind bird that sings comforting hymns to cure allies.",
        "appearance": {
            "base_shape": "bird",
            "body_color": [253, 254, 220, 255],
            "accent_color": [241, 196, 15, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "none",
            "tail": "none",
            "head_sprout": False,
            "horn": "none",
            "wings": "feathered"
        }
    },
    {
        "name": "Prismite",
        "types": ["Light", "Ice"],
        "base_stats": {"hp": 65, "attack": 70, "defense": 85, "speed": 60},
        "learnset": [
            {"level": 1, "move": "Ice Shard"},
            {"level": 4, "move": "Flash"},
            {"level": 10, "move": "Mirror Shot"},
            {"level": 16, "move": "Prism Laser"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A floating glass crystal that breaks light rays into colorful rainbow lasers.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [240, 253, 250, 255],
            "accent_color": [45, 212, 191, 255],
            "belly_color": [255, 255, 255, 255],
            "ears": "none",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },

    # --- Shadow Wild Pals (4) ---
    {
        "name": "Umbra",
        "types": ["Shadow"],
        "base_stats": {"hp": 55, "attack": 65, "defense": 50, "speed": 80},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Bite"},
            {"level": 9, "move": "Swift"},
            {"level": 14, "move": "Shadow Sneak"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": "Phantasm",
        "evolution_level": 20,
        "description": "A feline Pal that dissolves into shadows to stalk silently.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [30, 41, 59, 255],
            "accent_color": [14, 165, 233, 255],
            "belly_color": [241, 245, 249, 255],
            "ears": "pointy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Phantasm",
        "types": ["Shadow", "Mind"],
        "base_stats": {"hp": 80, "attack": 85, "defense": 70, "speed": 105},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Bite"},
            {"level": 14, "move": "Shadow Sneak"},
            {"level": 20, "move": "Shadow Ball"},
            {"level": 30, "move": "Future Sight"}
        ],
        "trait": "Clear Body",
        "evolves_from": "Umbra",
        "evolves_into": None,
        "evolution_level": None,
        "description": "A floating phantom that uses illusions and nightmare energy.",
        "appearance": {
            "base_shape": "blob",
            "body_color": [15, 23, 42, 255],
            "accent_color": [139, 92, 246, 255],
            "belly_color": [30, 41, 59, 255],
            "ears": "none",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "bat"
        }
    },
    {
        "name": "Darkdread",
        "types": ["Shadow", "Metal"],
        "base_stats": {"hp": 75, "attack": 95, "defense": 85, "speed": 85},
        "learnset": [
            {"level": 1, "move": "Scratch"},
            {"level": 5, "move": "Bite"},
            {"level": 12, "move": "Bullet Punch"},
            {"level": 18, "move": "Shadow Claw"},
            {"level": 26, "move": "Dark Pulse"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "An armored predator with razor-sharp metal claws and bat wings.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [30, 30, 36, 255],
            "accent_color": [220, 20, 60, 255],
            "belly_color": [100, 100, 110, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "dual",
            "wings": "bat"
        }
    },
    {
        "name": "Spectre",
        "types": ["Shadow"],
        "base_stats": {"hp": 60, "attack": 75, "defense": 60, "speed": 95},
        "learnset": [
            {"level": 1, "move": "Pound"},
            {"level": 4, "move": "Shadow Sneak"},
            {"level": 10, "move": "Confuse"},
            {"level": 16, "move": "Shadow Ball"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A ghost Pal that fades in and out of phase, spooking wanderers.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [74, 85, 104, 200], # Translucent dark slate
            "accent_color": [113, 128, 150, 200],
            "belly_color": [45, 55, 72, 200],
            "ears": "pointy",
            "tail": "fluffy",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },

    # --- Extra Normal Pals (3) ---
    {
        "name": "Slothfit",
        "types": ["Normal"],
        "base_stats": {"hp": 80, "attack": 65, "defense": 65, "speed": 30},
        "learnset": [
            {"level": 1, "move": "Pound"},
            {"level": 4, "move": "Growl"},
            {"level": 10, "move": "Scratch"},
            {"level": 16, "move": "Slam"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A very lazy sloth Pal that values relaxation above all else.",
        "appearance": {
            "base_shape": "biped",
            "body_color": [188, 170, 150, 255],
            "accent_color": [140, 120, 100, 255],
            "belly_color": [240, 230, 220, 255],
            "ears": "puppy",
            "tail": "none",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    },
    {
        "name": "Spikytail",
        "types": ["Normal", "Earth"],
        "base_stats": {"hp": 65, "attack": 75, "defense": 70, "speed": 65},
        "learnset": [
            {"level": 1, "move": "Tackle"},
            {"level": 4, "move": "Growl"},
            {"level": 8, "move": "Rock Throw"},
            {"level": 14, "move": "Slam"}
        ],
        "trait": "Clear Body",
        "evolves_from": None,
        "evolves_into": None,
        "evolution_level": None,
        "description": "A small mammalian Pal with rocky spikes lining its tail shaft.",
        "appearance": {
            "base_shape": "quadruped",
            "body_color": [205, 133, 63, 255],
            "accent_color": [139, 69, 19, 255],
            "belly_color": [245, 222, 179, 255],
            "ears": "pointy",
            "tail": "spikes",
            "head_sprout": False,
            "horn": "none",
            "wings": "none"
        }
    }
]

def generate():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "battle_pals", "data", "species")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating {len(SPECIES_DATA)} species JSON files inside: {output_dir}")
    
    for s in SPECIES_DATA:
        filename = s["name"].lower().replace(" ", "_") + ".json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(s, f, indent=4, ensure_ascii=False)
            
    print("Species JSON files generated successfully!")

if __name__ == "__main__":
    generate()
