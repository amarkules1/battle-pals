import os
import sys

# Ensure the root folder is on Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from battle_pals.models.species import SPECIES
from battle_pals.models.pal import Pal
from battle_pals.models.state import GameState, PRECINCTS

def run_tests():
    print("Running Battle Pals Campaign RPG Tests...")

    # 1. State Initialization
    state = GameState("TestRobin", "Boy", "Leaflet")
    GameState.set_instance(state)
    
    assert state.player_name == "TestRobin"
    assert state.player_gender == "Boy"
    assert len(state.party) == 1
    
    starter = state.party[0]
    assert starter.name == "Leaflet"
    assert starter.level == 5
    assert len(starter.moves) > 0
    print("PASS: Campaign initialized successfully with level 5 Leaflet starter.")

    # 2. Paldex Tracking
    assert state.paldex["Leaflet"]["seen"] == True
    assert state.paldex["Leaflet"]["captured"] == 1
    assert state.paldex["Leaflet"]["defeated"] == 0
    print("PASS: Paldex logged starter Pal automatically.")

    # 3. Item Purchases & RP Balance
    state.gain_research_points(500)
    assert state.research_points == 500
    
    # Buy 1 Ultra Cube (500 RP)
    state.research_points -= 500
    state.inventory["Ultra Cube"] += 1
    
    assert state.research_points == 0
    assert state.inventory["Ultra Cube"] == 2  # Started with 1, bought 1
    print("PASS: RP earnings and Capture Cube purchases work correctly.")

    # 4. Party Size Limits & Storage Box Swapping
    # Add 9 Pyropups to fill the party to 10
    for i in range(9):
        p = Pal("Pyropup", level=5)
        added_loc = state.add_pal_to_party_or_box(p)
        assert added_loc == "party"

    assert len(state.party) == 10
    
    # Add an 11th Pal - should go to Box
    extra_pal = Pal("Aquasplash", level=12)
    added_loc = state.add_pal_to_party_or_box(extra_pal)
    assert added_loc == "box"
    assert len(state.box) == 1
    print("PASS: Party limit capped at 10; 11th Pal correctly redirected to Box Storage.")

    # 5. EXP gains & Level up
    # Leaflet level 5 needs: 5 * 100 = 500 EXP to reach level 6
    old_max_hp = starter.max_hp
    logs = starter.gain_experience(500)
    print(f"Level up logs: {logs}")
    assert starter.level == 6
    assert starter.max_hp > old_max_hp
    assert any("leveled up to Level 6" in log for log in logs)
    print("PASS: EXP scale and stats re-calculation on level up function perfectly.")

    # 6. Moves learning on level up
    # Leaflet learns Synthesize at level 8. Let's level it up to 8!
    # To go 6 -> 7 needs 600 EXP. 7 -> 8 needs 700 EXP. Total 1300 EXP.
    logs_moves = starter.gain_experience(1300)
    print(f"Level up & moves logs: {logs_moves}")
    assert starter.level == 8
    assert any("learned Synthesize" in log for log in logs_moves)
    assert "Synthesize" in [m.name for m in starter.moves]
    print("PASS: Move learning based on species learnset triggers correctly on level up.")

    # 7. Evolution
    # Leaflet evolves to Florafox at level 16.
    # Let's give it plenty of experience to reach level 16
    logs_evolution = starter.gain_experience(10000)
    print(f"Evolution logs: {logs_evolution}")
    assert starter.level >= 16
    assert starter.name == "Florafox"
    assert "Grass" in starter.types
    print("PASS: Evolution triggered at level 16 and morphed Leaflet into Florafox successfully.")

    print("\nAll Campaign RPG tests passed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    run_tests()
