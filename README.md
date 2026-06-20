# Battle Pals (Pokémon-like Battle Arena 3D MVP)

A Python-based turn-based RPG battle arena built using the [ai4animationpy](https://github.com/facebookresearch/ai4animationpy) framework (utilizing its Entity Component System (ECS) architecture and built-in **Raylib** 3D rendering engine). The project simulates a retro combat system similar to Pokémon, rendered in a 2D/pseudo-3D perspective with procedural animations.

---

## 🚀 Setup & Quick Start Guide

Follow these instructions to set up the game from scratch, even if you have no pre-installed programming tools (like Python or Conda).

### Step 1: Install Conda (Miniconda)
Conda is an environment manager that helps you run different versions of Python and packages without conflicts.
1. Download the **Miniconda Installer** for your operating system:
   * **Windows**: [Miniconda Windows 64-bit Installer](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)
   * **macOS**: [Miniconda macOS Apple Silicon M1/M2/M3 Installer](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.pkg) or [Intel Installer](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.pkg)
   * **Linux**: [Miniconda Linux 64-bit Installer](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh)
2. Run the downloaded installer and follow the default installation prompts.
3. Open your terminal:
   * **Windows**: Press the Start key, search for **Anaconda Prompt** (or **Miniconda Prompt**), and open it.
   * **macOS / Linux**: Open your system **Terminal**.

### Step 2: Install Git & Clone the Projects
You need to clone both the `battle-pals` game repository and its dependency framework `ai4animationpy` into the same folder.
1. If you do not have Git installed, install it via Conda:
   ```bash
   conda install git -y
   ```
2. Create a projects folder and clone both repositories side-by-side:
   ```bash
   # Create and enter projects folder
   mkdir battle-pals-project
   cd battle-pals-project

   # Clone the battle-pals game
   git clone https://github.com/amarl/battle-pals.git

   # Clone the ai4animationpy framework
   git clone https://github.com/facebookresearch/ai4animationpy.git
   ```

### Step 3: Create the Python Environment
We will create an isolated environment with Python 3.12:
```bash
# Create a Conda environment named 'ai4animationpy_env'
conda create -n ai4animationpy_env python=3.12 -y

# Activate the environment
conda activate ai4animationpy_env
```

### Step 4: Install Dependencies
Navigate into the `ai4animationpy` framework directory and install it in editable mode. This will automatically download and install PyTorch, Raylib, NumPy, SciPy, and all other package requirements:
```bash
# Enter the framework directory
cd ai4animationpy

# Install framework and its dependencies
pip install -e .
```

### Step 5: Run the Game
Now navigate back and enter the `battle-pals` directory to launch the game:
```bash
# Move to the battle-pals directory
cd ../battle-pals

# Run the game
python main.py
```

---

## 📁 Project Architecture

The codebase is organized modularly to separate models (game state) from views (rendering and interaction):

```
battle-pals-project/
├── ai4animationpy/          # Sibling framework repository
└── battle-pals/             # Game project repository
    ├── battle_pals/
    │   ├── __init__.py      # Package entry point
    │   ├── constants.py     # Graphics scaling, fonts, and dark theme colors
    │   ├── game.py          # Game lifecycle coordinator & ECS scene cleanups
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── move.py      # Combat Move class & predefined move presets
    │   │   └── pal.py       # Pal class, stats, animation states, and damage formulas
    │   └── views/
    │       ├── __init__.py
    │       ├── starter_view.py # Starter Selection screen (Leaflet, Pyropup, Aquasplash)
    │       ├── battle_view.py  # Turn-based 3D scene and 2D overlay GUI view
    │       └── game_over_view.py # Victory / Defeat screen and restart handler
    ├── main.py              # Root execution script
    └── README.md            # Project documentation (This file)
```

---

## ⚙️ Core Systems & Mechanics

### 1. Combat & Stats Model ([pal.py](file:///C:/Users/amarl/dev/games/battle-pals/battle_pals/models/pal.py))
*   **Stats**: Each Pal has HP, Attack, Defense, and Speed stats. Speed determines turn order.
*   **Type Effectiveness**: Implements rock-paper-scissors relationships: `Fire > Grass > Water > Fire`.
    *   Super Effective: `2.0x` damage.
    *   Not Very Effective: `0.5x` damage.
*   **Damage Formula**: Implements critical hit chances (6.25%) and randomized variance (85%-100%):
    $$\text{Damage} = \text{int}\left( \left( \frac{\frac{2 \times \text{Level}}{5} + 2 \times \text{Move Power} \times \frac{\text{Attack}}{\text{Defense}}}{50} + 2 \right) \times \text{Effectiveness} \times \text{Variance} \times \text{Crit} \right)$$
*   **Status Moves**: Supports stat reductions (like `Growl` reducing attack multiplier) and healing (like `Synthesize` healing 50% max HP).

### 2. Rendering Lifecycle ([battle_view.py](file:///C:/Users/amarl/dev/games/battle-pals/battle_pals/views/battle_view.py))
*   **3D Drawing (`on_draw`)**: Manages rendering in 3D camera space. The circular arena floor and player/opponent platforms are drawn using Raylib planes. The character models are drawn procedurally as 3D composite primitives (body spheres, facial details, and type decorations like leafy ears, flame tails, or dorsal fins).
*   **2D GUI (`on_gui`)**: Draws the retro overlay panels, health bars, statistics, move grid buttons, and combat dialogue console text box on top of the 3D scene.

### 3. Procedural Animations
Each Pal manages its real-time animations:
*   **Idle**: A floating sinusoidal breathing bounce.
*   **Attack**: An explosive slide towards the opponent, tracking turn execution.
*   **Damage**: An elastic horizontal shaking and color-flashing feedback effect.
*   **Faint**: A spinning descent below the platform, scaling the Pal down to zero.

---

## 💡 Notes for Future Devs & AIs

If you are modifying this codebase, please keep the following Raylib & `ai4animationpy` guidelines in mind:

### ⚠️ Rendering Lifecycle & Background Wipes
*   **Do NOT call** `rl.ClearBackground(...)` inside your views' `on_gui` methods. The framework processes `on_draw` first and overlays `on_gui` second. Wiping the background in `on_gui` will erase the 3D scene completely.
*   The sky/background clear color is managed directly by the framework's [RenderPipeline.py](file:///c:/Users/amarl/dev/games/ai4animationpy/ai4animation/Standalone/RenderPipeline.py). It has been configured to use the game's dark theme color `(20, 24, 33, 255)` in `RenderLight()` to ensure a consistent atmospheric layout.

### ⚠️ Numpy Array Attribute Constraints (Windows)
*   The `ai4animationpy` framework implements a custom Vector3 tensor backend. On Windows, position vector elements evaluate to standard NumPy 1D arrays.
*   **Do NOT access** coordinate elements via properties (e.g., `pos.x`, `pos.y`, `pos.z`) as this will raise an `AttributeError`.
*   **Use array indexing** instead to access coordinates: `pos[0]` (X), `pos[1]` (Y), and `pos[2]` (Z).
