import os
import random
from battle_pals.models.species import SPECIES
from battle_pals.models.pal import Pal

PRECINCTS = [
    {
        "name": "Greenvale", 
        "env": "Rural Valleys & Greenhouses", 
        "type": "Grass", 
        "bureaucrat": "Director Vance", 
        "wilds": ["Leaflet", "Breezy", "Windry", "Florafox", "Vinedrake"],
        "boss_team": [("Florafox", 8), ("Vinedrake", 10)]
    },
    {
        "name": "Ironclad", 
        "env": "Deep Mines & Smelters", 
        "type": "Metal", 
        "bureaucrat": "Warden Steel", 
        "wilds": ["Rusty", "Ironclad", "Rocky", "Molehole", "Sandcrawler", "Gigamech"],
        "boss_team": [("Ironclad", 16), ("Gigamech", 18)]
    },
    {
        "name": "Frostbite", 
        "env": "Tundra & Frozen Coastline", 
        "type": "Ice", 
        "bureaucrat": "Inspector Frost", 
        "wilds": ["Frosty", "Snowball", "Glacier", "Icelope", "Aquasplash", "Seashell"],
        "boss_team": [("Glacier", 24), ("Seashell", 26)]
    },
    {
        "name": "Cinder", 
        "env": "Volcanic Slopes & Power Stations", 
        "type": "Fire", 
        "bureaucrat": "Commissioner Pyre", 
        "wilds": ["Pyropup", "Solaris", "Blazecat", "Infernoct", "Luxor"],
        "boss_team": [("Blazecat", 32), ("Infernoct", 35)]
    },
    {
        "name": "Nox", 
        "env": "Smoggy Urban Slums", 
        "type": "Toxic", 
        "bureaucrat": "Director Venom", 
        "wilds": ["Noxious", "Gloop", "Acidbug", "Rattler", "Vipera"],
        "boss_team": [("Acidbug", 42), ("Vipera", 45)]
    },
    {
        "name": "Resonance", 
        "env": "High-Tech Megacity", 
        "type": "Mind", 
        "bureaucrat": "Minister Brain", 
        "wilds": ["Brainy", "Psycat", "Psiwyrm", "Chubby", "Slothfit"],
        "boss_team": [("Psycat", 52), ("Chubby", 55)]
    },
    {
        "name": "Tempest", 
        "env": "Windswept Grasslands & Grids", 
        "type": "Electric", 
        "bureaucrat": "Marshal Gale", 
        "wilds": ["Sparky", "Voltcat", "Thundermouse", "Galehawk", "Stormeagle"],
        "boss_team": [("Thundermouse", 62), ("Stormeagle", 65)]
    },
    {
        "name": "Void", 
        "env": "Ancient Ruins & Canyons", 
        "type": "Shadow", 
        "bureaucrat": "Archon Shade", 
        "wilds": ["Umbra", "Spectre", "Phantasm", "Darkdread", "Gravelord"],
        "boss_team": [("Darkdread", 72), ("Gravelord", 75)]
    },
    {
        "name": "The Citadel", 
        "env": "Imperial Capital District", 
        "type": "All", 
        "bureaucrat": "Grand Chancellor Jin", 
        "wilds": ["Angelix", "Prismite", "Steelwing", "Krakentos", "Alakazam"],
        "boss_team": [("Prismite", 82), ("Steelwing", 85), ("Alakazam", 90)]
    }
]

class GameState:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            # Create a default blank state just in case
            cls._instance = GameState("Default", "Boy", "Leaflet")
        return cls._instance

    @classmethod
    def set_instance(cls, inst):
        cls._instance = inst

    def __init__(self, name, gender, starter_name):
        self.player_name = name
        self.player_gender = gender  # "Boy" or "Girl"
        
        # Game progression lists
        self.party = []       # Active team of Pal specimens (max 10)
        self.box = []         # Reserved Pal specimens
        
        # Paldex logs: {species_name: {"seen": bool, "defeated": int, "captured": int}}
        self.paldex = {}
        for s_name in SPECIES:
            self.paldex[s_name] = {"seen": False, "defeated": 0, "captured": 0}

        # Initialize starter Pal specimen (level 5)
        starter_specimen = Pal(starter_name, level=5, is_player=True)
        self.party.append(starter_specimen)
        self.add_to_paldex(starter_name, "captured")

        # Inventory
        self.inventory = {
            "Basic Cube": 5,
            "Mega Cube": 2,
            "Ultra Cube": 1
        }

        # Campaign indexes
        self.current_precinct = 0
        self.unlocked_precincts = [0]
        self.defeated_bureaucrats = []
        self.research_points = 0

    def add_to_paldex(self, species_name, action):
        """Helper to mark seen/defeated/captured inside Paldex."""
        if species_name in self.paldex:
            self.paldex[species_name]["seen"] = True
            if action == "defeated":
                self.paldex[species_name]["defeated"] += 1
            elif action == "captured":
                self.paldex[species_name]["captured"] += 1

    def add_pal_to_party_or_box(self, pal):
        """Adds a newly caught specimen to the party (capped at 10) or sends to box storage."""
        pal.is_player = True
        # Set base position for player drawing
        from ai4animation import Vector3
        pal.base_position = Vector3.Create(-4.0, 1.5, -2.0)
        pal.position = Vector3.Create(-4.0, 1.5, -2.0)
        
        if len(self.party) < 10:
            self.party.append(pal)
            return "party"
        else:
            self.box.append(pal)
            return "box"

    def heal_all_pals(self):
        """Restores HP of all party members to maximum."""
        for pal in self.party:
            pal.reset_battle_stats(heal=True)

    def gain_research_points(self, amount):
        self.research_points += amount
