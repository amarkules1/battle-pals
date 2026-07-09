---
name: create-battle-pal-move
description: Guidelines and instructions on how to create, define, and configure custom moves inside the Battle Pals game by writing JSON files in the moves directory. Covers physical, special, status, healing, and stat-altering moves.
---

# Creating a Custom Battle Pal Move

Battle Pals loads all moves dynamically at runtime from formatted JSON files inside the `battle_pals/data/moves/` directory. This guide describes the schema and process for defining custom moves.

---

## 📁 Location & Naming
* **Directory**: `battle_pals/data/moves/`
* **Filename**: Keep the filename in lowercase snake case matching the move's name (e.g. `volt_tackle.json` for a move named "Volt Tackle").

---

## ⚙️ Move JSON Schema

Every move JSON file must contain the following fields:

| Field | Type | Description |
|---|---|---|
| `name` | `string` | The exact display name of the move. |
| `type` | `string` | The elemental type matching one of the 13 types: `Normal`, `Fire`, `Water`, `Grass`, `Electric`, `Ice`, `Earth`, `Wind`, `Toxic`, `Mind`, `Metal`, `Light`, or `Shadow`. |
| `power` | `integer` | Base damage. Use `0` for status-only moves. |
| `accuracy` | `float` | Hit chance probability, represented as a float between `0.0` (0%) and `1.0` (100%). |
| `category` | `string` | Must be one of: `"Physical"` (contact damage), `"Special"` (ranged/energy damage), or `"Status"` (non-damaging utility/effects). |
| `effect` | `dict` (optional) | Optional dictionary defining status effects (e.g., healing or stat changes). |
| `description` | `string` | Short description displayed in the move info panel during combat. |

---

## 💡 Move Effect Types

If a move includes an `"effect"`, it supports the following formats:

### 1. Healing Effect (`"heal"`)
Heals the user for a percentage of their **maximum HP**. Value is a float representing the fraction (e.g. `0.5` = 50% healing).
* **Format**: `{"heal": float}`
* **Example**: `{"heal": 0.5}`

### 2. Stat Modification (`"stat"` & `"mult"`)
Applies a multiplier to the **target's** stats. Multipliers are clamped between `0.4` and `2.0`.
* **Format**: `{"stat": "attack" | "defense" | "speed", "mult": float}`
* **Example**: `{"stat": "attack", "mult": 0.8}` (Reduces target's Attack by 20%).
* **Example**: `{"stat": "speed", "mult": 1.5}` (Boosts target's Speed by 50%).

---

## 📝 Code Examples

### 1. Physical Attack Move (`metal_claw.json`)
```json
{
    "name": "Metal Claw",
    "type": "Metal",
    "power": 50,
    "accuracy": 0.95,
    "category": "Physical",
    "description": "Strikes target with metallic claws."
}
```

### 2. Special Attack Move (`thunderbolt.json`)
```json
{
    "name": "Thunderbolt",
    "type": "Electric",
    "power": 90,
    "accuracy": 1.0,
    "category": "Special",
    "description": "Fires a powerful electric bolt."
}
```

### 3. Healing Status Move (`synthesize.json`)
```json
{
    "name": "Synthesize",
    "type": "Grass",
    "power": 0,
    "accuracy": 1.0,
    "category": "Status",
    "effect": {
        "heal": 0.5
    },
    "description": "Heals 50% of the user's max HP."
}
```

### 4. Debuffing Status Move (`growl.json`)
```json
{
    "name": "Growl",
    "type": "Normal",
    "power": 0,
    "accuracy": 1.0,
    "category": "Status",
    "effect": {
        "stat": "attack",
        "mult": 0.8
    },
    "description": "Intimidates the target, lowering their Attack."
}
```
