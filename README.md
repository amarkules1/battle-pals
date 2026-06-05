# Battle Pals (Pokémon-like Battle Arena MVP)

A Python-based 2D turn-based RPG battle arena built using **Arcade 3.3.3** and **Pyglet**. The project simulates a retro Game Boy-style combat system similar to Pokémon FireRed/Sapphire.

---

## 📁 Project Architecture

The codebase is designed modularly to separate models (game state) from views (rendering and user interaction).

```
battle-pals/
├── battle_pals/
│   ├── __init__.py           # Package entry point
│   ├── constants.py          # Graphics sizing, fonts, and dark theme colors
│   ├── game.py               # Game window initialization and loop runner
│   ├── models/
│   │   ├── __init__.py
│   │   ├── move.py          # Combat Move class & predefined move presets
│   │   └── pal.py           # Pal class, stats, level scaling, and damage formulas
│   └── views/
│       ├── __init__.py
│       ├── starter_view.py   # Starter Pal selection cards (Leaflet, Pyropup, Aquasplash)
│       ├── battle_view.py    # Turn-based battle screen and state machine
│       └── game_over_view.py # Victory / Defeat screen and restart handler
├── main.py                   # Root execution script
└── README.md                 # Project documentation
```

---

## ⚙️ Core Systems & Mechanics

### 1. Combat & Stats Model ([pal.py](file:///C:/Users/amarl/dev/games/battle-pals/battle_pals/models/pal.py))
*   **Stats**: Each Pal has HP, Attack, Defense, and Speed stats. Speed determines turn order.
*   **Type Effectiveness**: Implements standard rock-paper-scissors relationships: `Fire > Grass > Water > Fire`.
    *   Super Effective: `2.0x` damage.
    *   Not Very Effective: `0.5x` damage.
*   **Damage Formula**: A simplified version of standard Pokémon calculations, adding critical hit chances (6.25%) and randomized variance (85%-100%):
    $$\text{Damage} = \text{int}\left( \left( \frac{\frac{2 \times \text{Level}}{5} + 2 \times \text{Move Power} \times \frac{\text{Attack}}{\text{Defense}}}{50} + 2 \right) \times \text{Effectiveness} \times \text{Variance} \times \text{Crit} \right)$$
*   **Status Moves**: Supports stat reductions (like `Growl` reducing attack multiplier) and healing (like `Synthesize` healing 50% max HP).

### 2. Views & State Machine ([battle_view.py](file:///C:/Users/amarl/dev/games/battle-pals/battle_pals/views/battle_view.py))
*   **Dialogue Controller**: Combat messages are stored in a queue. Clicking anywhere on the screen advances the text log.
*   **Combat States**:
    *   `STATE_INTRO`: Introduces the opponent and player Pal.
    *   `STATE_MOVE_SELECT`: Displays a 2x2 grid of buttons. Hovering over a button displays detailed info on the right panel.
    *   `STATE_COMBAT_LOGS`: Runs speed check, executes player/opponent moves, resolves damage/status, and queues logs.

---

## 🛠️ Setup & Running

### Requirements
*   Python 3.10+
*   `uv` (recommended fast package installer) or `pip`

### Virtual Environment Setup
Ensure you are in the parent directory (`C:\Users\amarl\dev\games\`) or within the project directory:

```powershell
# Create environment
uv venv

# Install Arcade
uv pip install arcade
```

### Run the Game
Execute the entrypoint:
```powershell
cd C:\Users\amarl\dev\games\battle-pals
..\.venv\Scripts\python.exe main.py
```

---

## 💡 Notes for Future Devs & AIs

If you are modifying this codebase, please keep the following framework-specific guidelines in mind:

### ⚠️ Arcade 3.3.3 Drawing API Constraints
Arcade 3.3.3 deprecated several traditional shape-drawing methods.
*   **Do NOT use** `arcade.draw_rectangle_filled` or `arcade.draw_rectangle_outline` directly with center coordinates.
*   **Use instead** `arcade.draw_lbwh_rectangle_filled` and `arcade.draw_lbwh_rectangle_outline`.
    *   These take coordinates starting from the **bottom-left** corner: `(left, bottom, width, height, color)`.
    *   To draw from a center coordinate `(cx, cy)`:
        ```python
        arcade.draw_lbwh_rectangle_filled(cx - width/2, cy - height/2, width, height, color)
        ```
*   `arcade.draw_circle_filled` and `arcade.draw_circle_outline` still exist and work normally using center coordinates.

### Modifying Pal/Move Assets
*   Predefined moves are defined in a static dictionary in `models/move.py`.
*   To add new creatures, create a factory function in `models/pal.py` and register it in the `STARTERS` dictionary.
