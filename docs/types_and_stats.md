# Battle Pals: Types and Stats System

This document explains how stats, species templates, dynamic specimens, and elemental types function in Battle Pals combat.

---

## 🧬 Species vs. Specimens

Battle Pals implements a clean split between **Species** templates and unique **Specimens**:

1. **Species**: A static template defined in a JSON file (e.g., `leaflet.json`). It specifies the base stats (HP, Attack, Defense, Speed), type(s), learnable moves (learnset), battle trait, evolution requirements, and visual 3D appearance configurations.
2. **Specimen**: A unique, dynamic instance of a species generated during gameplay (represented by the `Pal` class). A specimen has a specific level, current HP, status conditions, and randomized **Stat Variations** (analogous to IVs).

---

## 📊 Stats & Level Scaling

Each Pal possesses four core stats that dictate their strength and speed in battle:

1. **HP (Hit Points)**: Dictates how much damage a Pal can sustain before fainting.
2. **Attack**: Modifies the damage dealt by physical or special moves.
3. **Defense**: Reduces the damage taken from incoming attacks.
4. **Speed**: Determines the prioritization of actions. The Pal with the higher Speed stat moves first in a combat round.

### Stat Variations (Individual Values)
When a specimen is generated, it is assigned a random integer between `0` and `15` for each stat (known as its **Stat Variation**). This ensures that two specimens of the same species and level have slightly different stats.

### Stat Calculation Formulas
Stats at a specific level $L$ are calculated from base stats and variations using the following formulas:

$$\text{HP} = \text{int}\left( \frac{(2 \times \text{BaseHP} + \text{HP\_Variation}) \times L}{50} \right) + L + 10$$

$$\text{Other Stat} = \text{int}\left( \frac{(2 \times \text{BaseStat} + \text{Stat\_Variation}) \times L}{50} \right) + 5$$

---

## 🌟 Battle Traits

Species can have unique traits that grant passive bonuses in combat:

* **Clear Body**: Grants complete immunity against status reductions (prevents enemy moves from lowering stats).
* **Chlorophyll**: Boosts the specimen's Speed stat by `1.5x` in battle.
* **Overgrow**: Boosts the power of Grass-type moves by `1.5x` when the specimen's HP falls below 33%.
* **Blaze**: Boosts the power of Fire-type moves by `1.5x` when the specimen's HP falls below 33%.
* **Torrent**: Boosts the power of Water-type moves by `1.5x` when the specimen's HP falls below 33%.


### Leveling & Stat Modifiers
Stats scale as a Pal levels up. Additionally, during combat, certain moves (Status category) can apply modifiers that temporarily increase or decrease a Pal's stats (clamped between a minimum multiplier of `0.4` and a maximum of `2.0`).

### Damage Calculation Formula
When a move hits, damage is computed using a simplified version of the standard RPG formula:

$$\text{Damage} = \text{int}\left( \left( \frac{\frac{2 \times \text{Level}}{5} + 2 \times \text{Move Power} \times \frac{\text{Attack}}{\text{Defense}}}{50} + 2 \right) \times \text{Effectiveness} \times \text{Variance} \times \text{Crit} \right)$$

* **Variance**: A randomized multiplier between `0.85` and `1.0`.
* **Crit**: 6.25% chance of a critical hit, applying a `1.5x` multiplier.
* **Effectiveness**: The calculated type multiplier of the attacking move against the defending Pal's type(s).

---

## ⚡ Elemental Types

Pals have either one primary type, or a combination of a primary and secondary type (e.g. `Grass/Wind`). Move attacks always have exactly one type. There are **12 core types** (plus a default **Normal** type) in the Battle Pals universe:

| Type | Theme / Description |
|---|---|
| **Normal** | Balanced, basic moves with no special type advantages. |
| **Fire** | Hot and expressive. Deals heavy damage to organic and metallic objects. |
| **Water** | Fluid and adaptive. Extinguishes fire and erodes the earth. |
| **Grass** | Growth and nature. Absorbs moisture from the ground and water. |
| **Electric** | Swift electricity. Electrifies water and conducts through metals. |
| **Ice** | Freezing frost. Slows down wind and freezes organic growth. |
| **Earth** | Clay, rocks, and soil. Grounded and heavy; grounds electric currents. |
| **Wind** | Air currents and flight. Evades earthbound attacks easily. |
| **Toxic** | Corrosive poisons and acid. Dissolves plants but cannot corrode metal. |
| **Mind** | Psychic powers and focus. Controls toxic impurities but cannot pierce light. |
| **Metal** | Heavy alloys. Resists elemental attacks but is vulnerable to fire and corrosion. |
| **Light** | Pure energy. dispels shadows and blinds psychic minds. |
| **Shadow** | Dark and phantom power. Envelops light and corrupts minds. |

---

## ⚔️ Type Effectiveness Matrix

Matchups can be **Super Effective** (`2.0x`), **Not Very Effective** (`0.5x`), **Normally Effective** (`1.0x`), or have **No Effect** (`0.0x` / immunity).

### Dual-Type Calculations
If a target Pal has two types, the total effectiveness is the product of the move's effectiveness against each type individually:

$$\text{Effectiveness} = \text{Eff}(\text{Move}, \text{Type 1}) \times \text{Eff}(\text{Move}, \text{Type 2})$$

* **Double Weakness**: E.g. Fire vs a `Grass/Ice` Pal = $2.0 \times 2.0 = 4.0x$ damage.
* **Double Resistance**: E.g. Fire vs a `Fire/Water` Pal = $0.5 \times 0.5 = 0.25x$ damage.
* **Neutralizing**: E.g. Fire vs a `Water/Grass` Pal = $0.5 \times 2.0 = 1.0x$ damage.
* **Immunity Rule**: If any target type is immune to the attacking move ($0.0x$), the entire attack deals $0.0x$ damage, regardless of other type weaknesses.

### Key Matchup Rules (Imunities)
* **Electric vs Earth**: Electric currents are safely grounded by the Earth ($0.0x$).
* **Earth vs Wind**: Earthbound tremors and dust storms cannot reach the high-altitude Wind ($0.0x$).
* **Toxic vs Metal**: Acids and poisons cannot pierce or corrode inorganic Metal alloys ($0.0x$).
* **Mind vs Light**: Pure, unfiltered Light dispels all illusion and mind control ($0.0x$).
