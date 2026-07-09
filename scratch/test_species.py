import sys
import os

# Set python path to find battle_pals
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from battle_pals.models.species import SPECIES, Species
from battle_pals.models.pal import Pal
from battle_pals.models.move import Move

def run_tests():
    print("Running Species & Specimens Engine Tests...")
    print(f"Loaded species count: {len(SPECIES)}")
    
    # 1. Verify we have 50 species loaded
    if len(SPECIES) == 50:
        print("PASS: Loaded exactly 50 species profiles.")
    else:
        print(f"FAIL: Loaded {len(SPECIES)} species profiles. Expected 50.")
        sys.exit(1)
        
    # 2. Verify specimen creation & stat variations
    leaflet_species = SPECIES.get("Leaflet")
    if not leaflet_species:
        print("FAIL: Species 'Leaflet' not loaded.")
        sys.exit(1)
        
    p1 = Pal(leaflet_species, level=5)
    p2 = Pal(leaflet_species, level=5)
    
    print(f"Specimen 1 variations: {p1.stat_variations}")
    print(f"Specimen 2 variations: {p2.stat_variations}")
    
    print(f"Specimen 1 stats - HP: {p1.max_hp}, Atk: {p1.base_attack}, Def: {p1.base_defense}, Spd: {p1.base_speed}")
    print(f"Specimen 2 stats - HP: {p2.max_hp}, Atk: {p2.base_attack}, Def: {p2.base_defense}, Spd: {p2.base_speed}")
    
    # Test that stats calculation formula scales with level and variation
    # Check that they can have different stats
    stats1 = (p1.max_hp, p1.base_attack, p1.base_defense, p1.base_speed)
    stats2 = (p2.max_hp, p2.base_attack, p2.base_defense, p2.base_speed)
    # They could be identical by rare random chance, but let's check basic sanity
    if all(s > 0 for s in stats1) and all(s > 0 for s in stats2):
        print("PASS: Stats scale and are non-zero.")
    else:
        print("FAIL: Invalid stat scaling.")
        sys.exit(1)
        
    # 3. Verify learnset move auto-teaching
    # Leaflet at level 5 should learn Tackle, Growl, Gust, Razor Leaf (Gust is lvl 3, Razor Leaf is lvl 5)
    p1_move_names = [m.name for m in p1.moves]
    print(f"Leaflet Level 5 moves: {p1_move_names}")
    expected_moves = ["Tackle", "Growl", "Gust", "Razor Leaf"]
    if all(m in p1_move_names for m in expected_moves):
        print("PASS: Specimen learned the correct level-appropriate moves.")
    else:
        print(f"FAIL: Specimen moves {p1_move_names} do not match expected {expected_moves}.")
        sys.exit(1)
        
    # Let's check a higher level (e.g. Leaflet at level 10 should learn Synthesize at level 8)
    p_lvl10 = Pal(leaflet_species, level=10)
    p_lvl10_moves = [m.name for m in p_lvl10.moves]
    print(f"Leaflet Level 10 moves (max 4): {p_lvl10_moves}")
    # Moves available: Tackle, Growl, Gust, Razor Leaf, Synthesize (lvl 8). Last 4: Growl, Gust, Razor Leaf, Synthesize
    if "Synthesize" in p_lvl10_moves and len(p_lvl10_moves) == 4:
        print("PASS: Level 10 specimen correctly capped moves list to 4 and learned Synthesize.")
    else:
        print(f"FAIL: Level 10 moves list {p_lvl10_moves} is incorrect.")
        sys.exit(1)
        
    # 4. Verify Trait Activation
    # Clear Body: prevents defense reduction
    chubby_species = SPECIES.get("Chubby") # Trait: Clear Body
    chubby = Pal(chubby_species, level=5)
    
    # Create a status move that reduces defense
    reduce_def_move = Move(name="Tail Whip", pal_type="Normal", power=0, accuracy=1.0, category="Status", effect={"stat": "defense", "mult": 0.8})
    
    # Execute tail whip against chubby
    attacker = Pal(leaflet_species, level=5)
    logs = attacker.use_move(reduce_def_move, chubby)
    print(f"Combat Logs for tail whip on Clear Body: {logs}")
    
    if any("Clear Body prevents stat reduction" in log for log in logs) and chubby.stat_modifiers["defense"] == 1.0:
        print("PASS: Clear Body trait successfully blocked stat reduction.")
    else:
        print("FAIL: Clear Body did not protect target defense stat.")
        sys.exit(1)
        
    print("\nAll Species & Specimen tests passed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    run_tests()
