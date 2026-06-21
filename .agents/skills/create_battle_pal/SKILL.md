---
name: create-battle-pal
description: Guidelines and instructions on how to create, configure, and procedurally render new Battle Pals (creatures) in the Battle Pals game. Covers base stats, moves dictionary, factory constructors, and Raylib 3D procedural drawing logic.
---

# Creating a New Battle Pal

This guide describes how to define, configure, and procedurally render a new Battle Pal (creature) in the Battle Pals game.

---

## Step 1: Configure Moves

Before defining the creature's stats, check if it requires new attacks. Moves are defined in the `MOVES` dictionary in [move.py](file:///c:/Users/amarl/dev/games/battle-pals/battle_pals/models/move.py).

### Defining a Custom Move
Add a new entry to the dictionary:
```python
"Spark": Move(
    name="Spark",
    move_type="Electric",          # Type name (e.g. Fire, Water, Grass, Electric, Normal)
    power=40,                      # Base damage power (0 for status moves)
    accuracy=100,                  # Accuracy percentage (0 to 100)
    description="A small jolt of electricity that may stun.",
    stat_modifiers={"speed": -0.1}, # Optional: percentage modifications to stats
    heals=False                    # Set True to heal 50% max HP instead of damage
)
```

---

## Step 2: Define the Pal Stats & Factory

Pals are defined using the `Pal` class in [pal.py](file:///c:/Users/amarl/dev/games/battle-pals/battle_pals/models/pal.py).

### 1. Write the Factory Function
Add a new factory function at the bottom of the file to instantiate your creature with its base stats:
```python
def create_sparky(level=5, is_player=False):
    return Pal(
        name="Sparky",
        pal_type="Electric",       # Core type
        level=level,
        hp=55,                     # Max HP
        attack=60,                 # Base Attack
        defense=45,                # Base Defense
        speed=70,                  # Base Speed
        moves_list=["Tackle", "Growl", "Spark"], # List of move names matching MOVES keys
        is_player=is_player
    )
```

### 2. Register Type Effectiveness (Optional)
If you introduced a new elemental type, register its strengths and weaknesses inside `Pal.get_effectiveness(move_type, target_type)` in [pal.py](file:///c:/Users/amarl/dev/games/battle-pals/battle_pals/models/pal.py):
```python
relations = {
    ("Electric", "Water"): 2.0,   # Super Effective
    ("Electric", "Grass"): 0.5,   # Not Very Effective
    # ...
}
```

---

## Step 3: Implement 3D Graphics

We draw character graphics inside `draw_pal_3d(self, pal)` in [battle_view.py](file:///c:/Users/amarl/dev/games/battle-pals/battle_pals/views/battle_view.py). 

### ⚠️ CRITICAL CONSTRAINTS & RULES
1. **Never use coordinate properties** like `.x`, `.y`, or `.z` on position vectors. On Windows, `pos` evaluates to a standard 1D NumPy array, which will crash with an `AttributeError`. **Always use array indices**: `pos[0]` (X), `pos[1]` (Y), and `pos[2]` (Z).
2. **Support taking-damage flashes**: Always wrap colors of your custom shapes with the `get_color(base_color)` helper.
3. **Respect scale**: Always multiply radii, lengths, and offsets by `scale` to support the smooth fainting scale-down animation.
4. **Respect facing**: Multiply Z-axis offsets by `facing` (`1.0` for player, `-1.0` for opponent) to ensure facial features point towards the battlefield center.

---

### Template for Drawing Procedural 3D Geometry

Add an `elif pal.name == "Sparky":` or `elif pal.type == "Electric":` block inside `draw_pal_3d(self, pal)`:

```python
        elif pal.name == "Sparky":
            color_body = get_color((241, 196, 15, 255))   # Yellow main
            color_accent = get_color((243, 156, 18, 255))  # Orange details
            
            # 1. Split Body and Head
            body_center = Vector3.Create(pos[0], pos[1] - 0.2 * scale, pos[2] + 0.1 * facing * scale)
            head_center = Vector3.Create(pos[0], pos[1] + 0.7 * scale, pos[2] - 0.3 * facing * scale)
            
            AI4Animation.Draw.Sphere(body_center, 0.95 * scale, 12, color_body)
            AI4Animation.Draw.Sphere(head_center, 0.8 * scale, 12, color_body)
            
            # 2. Chest/Belly Patch
            belly_center = Vector3.Create(pos[0], pos[1] - 0.1 * scale, pos[2] - 0.6 * facing * scale)
            AI4Animation.Draw.Sphere(belly_center, 0.4 * scale, 8, color_accent)
            
            # 3. Face Details
            # Eyes (Black base + white glossy highlight)
            eye_y = head_center[1] + 0.15 * scale
            eye_z = head_center[2] - 0.6 * facing * scale
            eye_xl = head_center[0] - 0.28 * scale
            eye_xr = head_center[0] + 0.28 * scale
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xl, eye_y, eye_z), 0.11 * scale, 6, get_color(color_eye_bg))
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xr, eye_y, eye_z), 0.11 * scale, 6, get_color(color_eye_bg))
            
            # Shiny Pupil Highlights
            hl_z = eye_z - 0.07 * facing * scale
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xl + 0.04 * scale, eye_y + 0.04 * scale, hl_z), 0.04 * scale, 4, get_color(color_eye_fg))
            AI4Animation.Draw.Sphere(Vector3.Create(eye_xr + 0.04 * scale, eye_y + 0.04 * scale, hl_z), 0.04 * scale, 4, get_color(color_eye_fg))
            
            # Blushing Cheeks & Mouth
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] - 0.42 * scale, head_center[1] - 0.05 * scale, eye_z), 0.1 * scale, 6, get_color(color_cheek))
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0] + 0.42 * scale, head_center[1] - 0.05 * scale, eye_z), 0.1 * scale, 6, get_color(color_cheek))
            AI4Animation.Draw.Sphere(Vector3.Create(head_center[0], head_center[1] - 0.15 * scale, eye_z - 0.05 * facing * scale), 0.06 * scale, 6, get_color(color_mouth))

            # 4. Pointy Lightning Ears
            # Left Ear
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0] - 0.5 * scale, head_center[1] + 0.3 * scale, head_center[2]),
                Vector3.Create(head_center[0] - 0.9 * scale, head_center[1] + 1.2 * scale, head_center[2] - 0.2 * facing * scale),
                0.14 * scale, 0.02 * scale, 8, color_accent
            )
            # Right Ear
            AI4Animation.Draw.Cylinder(
                Vector3.Create(head_center[0] + 0.5 * scale, head_center[1] + 0.3 * scale, head_center[2]),
                Vector3.Create(head_center[0] + 0.9 * scale, head_center[1] + 1.2 * scale, head_center[2] - 0.2 * facing * scale),
                0.14 * scale, 0.02 * scale, 8, color_accent
            )

            # 5. Stout Legs & paws
            leg_offsets = [
                (-0.35, -0.3, -0.35),
                (0.35, -0.3, -0.35),
                (-0.35, -0.3, 0.35),
                (0.35, -0.3, 0.35)
            ]
            for ox, oy, oz in leg_offsets:
                l_start = Vector3.Create(body_center[0] + ox * scale, body_center[1] + oy * scale, body_center[2] + oz * facing * scale)
                l_end = Vector3.Create(body_center[0] + ox * scale, body_center[1] - 0.85 * scale, body_center[2] + oz * facing * scale)
                AI4Animation.Draw.Cylinder(l_start, l_end, 0.13 * scale, 0.13 * scale, 6, color_body)
                AI4Animation.Draw.Sphere(l_end, 0.18 * scale, 6, color_accent) # paws

            # 6. Lightning Bolt Tail
            tail_base = Vector3.Create(body_center[0], body_center[1] - 0.3 * scale, body_center[2] + 0.65 * facing * scale)
            tail_mid = Vector3.Create(body_center[0] - 0.4 * scale, body_center[1] + 0.1 * scale, body_center[2] + 1.2 * facing * scale)
            tail_tip = Vector3.Create(body_center[0] + 0.3 * scale, body_center[1] + 0.9 * scale, body_center[2] + 1.6 * facing * scale)
            AI4Animation.Draw.Cylinder(tail_base, tail_mid, 0.1 * scale, 0.08 * scale, 6, color_accent)
            AI4Animation.Draw.Cylinder(tail_mid, tail_tip, 0.08 * scale, 0.02 * scale, 6, color_body)
```
