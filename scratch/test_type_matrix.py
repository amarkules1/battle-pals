import sys
import os

# Set python path to find battle_pals
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from battle_pals.models.pal import Pal, TYPE_MATRIX, load_type_matrix

def run_tests():
    print("Running Type Matrix Effectiveness Tests...")
    print(f"Loaded matrix entries count: {len(TYPE_MATRIX)}")
    
    # Test cases: (move_type, target_types, expected_effectiveness)
    test_cases = [
        # Basic Single Type
        ("Fire", "Grass", 2.0),
        ("Fire", "Water", 0.5),
        ("Normal", "Fire", 1.0),
        
        # Dual Type Multiplications
        ("Fire", "Grass/Ice", 4.0),       # 2.0 * 2.0
        ("Water", "Fire/Water", 1.0),     # 2.0 * 0.5
        ("Water", "Grass/Water", 0.25),   # 0.5 * 0.5
        
        # Immunities (0.0 effect)
        ("Electric", "Earth", 0.0),       # Electric vs Earth
        ("Earth", "Wind", 0.0),           # Earth vs Wind
        ("Toxic", "Metal", 0.0),          # Toxic vs Metal
        ("Mind", "Light", 0.0),           # Mind vs Light
        
        # Immunity overriding weaknesses (Immunity should make it 0.0)
        ("Electric", "Water/Earth", 0.0), # Electric is super effective vs Water (2.0) but immune vs Earth (0.0) -> 2.0 * 0.0 = 0.0
    ]
    
    failed = False
    for move_type, target_types, expected in test_cases:
        actual = Pal.get_effectiveness(move_type, target_types)
        if abs(actual - expected) < 1e-5:
            print(f"PASS: {move_type} vs {target_types} = {actual} (Expected: {expected})")
        else:
            print(f"FAIL: {move_type} vs {target_types} = {actual} (Expected: {expected})")
            failed = True
            
    if failed:
        print("\nSome tests FAILED.")
        sys.exit(1)
    else:
        print("\nAll tests PASSED successfully!")
        sys.exit(0)

if __name__ == "__main__":
    run_tests()
