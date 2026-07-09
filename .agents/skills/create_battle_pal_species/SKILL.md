---
name: create-battle-pal-species
description: Instructions on how to define, configure, and register new Battle Pal species by writing JSON profiles in the species directory. Outlines fields, base stats, learnsets, traits, evolution branches, and 3D rendering configurations.
---

# Creating a Custom Battle Pal Species

Battle Pals loads all species templates dynamically at runtime from JSON files located in the `battle_pals/data/species/` directory. This guide describes the schema and process for defining custom species.

---

## 📁 Location & Naming
* **Directory**: `battle_pals/data/species/`
* **Filename**: Keep the filename in lowercase snake case matching the species name (e.g. `thundermouse.json` for a species named "Thundermouse").

---

## ⚙️ Species JSON Schema

Every species JSON file must contain the following fields:

| Field | Type | Description |
|---|---|---|
| `name` | `string` | The display name of the species. |
| `types` | `list[string]` | A list of 1 or 2 types (e.g., `["Fire"]` or `["Grass", "Wind"]`). |
| `base_stats` | `dict` | Core base stats for scaling. Structure: `{"hp": int, "attack": int, "defense": int, "speed": int}`. |
| `learnset` | `list[dict]` | Moves this species learns. Structure: `[{"level": int, "move": "MoveName"}]`. |
| `trait` | `string` | Battle passive. Supported: `Clear Body`, `Chlorophyll`, `Overgrow`, `Blaze`, `Torrent`, `Volt Absorb`, `Shield Dust`. |
| `evolves_from` | `string \| null` | Name of the pre-evolution species (if any). |
| `evolves_into` | `string \| null` | Name of the post-evolution species (if any). |
| `evolution_level` | `integer \| null` | Level at which this species evolves. |
| `description` | `string` | Brief lore or description. |
| `appearance` | `dict` | 3D visual parameters used by the battle renderer. |

### Appearance Sub-Schema

The `"appearance"` dictionary maps the 3D model properties:

| Property | Value Options | Description |
|---|---|---|
| `base_shape` | `"quadruped" \| "biped" \| "aquatic" \| "bird" \| "blob"` | Governs body structure and limb drawing. |
| `body_color` | `[r, g, b, a]` | Base color of the main body and head. |
| `accent_color`| `[r, g, b, a]` | Color of extremities (paws, ears, tail sprouts). |
| `belly_color` | `[r, g, b, a]` | Chest/belly patch overlay color. |
| `eye_color` | `[r, g, b, a]` | Iris color (defaults to black `[0, 0, 0, 255]`). |
| `ears` | `"leaf" \| "puppy" \| "fins" \| "pointy" \| "none"` | Style of ears attached to the head. |
| `tail` | `"leaf" \| "flame" \| "flipper" \| "spikes" \| "fluffy" \| "none"` | Style of tail attached to the body. |
| `head_sprout` | `boolean` | Renders a small plant sprout on top of the head. |
| `horn` | `"single" \| "dual" \| "none"` | Forehead horns. |
| `wings` | `"feathered" \| "bat" \| "none"` | Wing structures attached to the back. |

---

## 📝 Code Examples

### 1. Leaflet (`leaflet.json`)
```json
{
    "name": "Leaflet",
    "types": ["Grass", "Wind"],
    "base_stats": {"hp": 45, "attack": 49, "defense": 65, "speed": 45},
    "learnset": [
        {"level": 1, "move": "Tackle"},
        {"level": 3, "move": "Gust"},
        {"level": 5, "move": "Razor Leaf"},
        {"level": 8, "move": "Synthesize"}
    ],
    "trait": "Overgrow",
    "evolves_from": null,
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
        "head_sprout": true,
        "horn": "none",
        "wings": "none"
    }
}
```

### 2. Solaris (`solaris.json`)
```json
{
    "name": "Solaris",
    "types": ["Light"],
    "base_stats": {"hp": 55, "attack": 65, "defense": 50, "speed": 80},
    "learnset": [
        {"level": 1, "move": "Tackle"},
        {"level": 4, "move": "Flash"},
        {"level": 14, "move": "Solar Flare"}
    ],
    "trait": "Chlorophyll",
    "evolves_from": null,
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
        "head_sprout": false,
        "horn": "single",
        "wings": "none"
    }
}
```
