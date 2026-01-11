# 3D Assets

This directory contains the 3D assets and scene configurations used by the Omniverse simulation.

## Core Assets

### `ocean_scene.usda`

The primary scene definition file. It configures the environment, lighting, and water surfaces:

* **RTX Fog**: Configured for a smooth "Twilight Zone" transition. The fog absorbs light with depth, creating a natural dark abyss.
* **Lighting**:
  * `DomeLight` (`EnvironmentLight`): Provides the sky background and environmental reflections.
  * `DistantLight` (`SunLight`): A directional light representing the sun, tilted for realistic water penetration.
* **Water Surfaces**:
  * `WaterPlaneAbove`: Optimized for top-down viewing with metallic reflections and sky-blue tint.
  * `WaterPlane` (Below): Optimized for underwater viewing with darker tint and subsurface scattering simulation.
* **World Bounds**: Expanded to a 500km radius with a seafloor at -20km.

## Required Assets (External)

Large binary assets or models under restrictive licenses are not tracked. You must place these files manually in this directory:

| File Name | Description | Source / Attribution |
|-----------|-------------|----------------------|
| `fishing_vessel.usdc` | Fishing vessel asset for scale and context | [Fisher Boat](https://www.cgtrader.com/free-3d-models/watercraft/industrial-watercraft/fisher-boat-96631d80-50ba-4b41-a11d-2bea68e1db64) by seemlyhasan |
| `great_white_shark.glb` | Shark Model | [great_white_shark](https://skfb.ly/pCoJH) by 'not important' (CC-BY) |

## Directory Structure

```text
omniverse/assets/
├── README.md              # Documentation
├── ocean_scene.usda       # Base scene configuration (Tracked)
├── fishing_vessel.usdc    # Vessel model (Tracked)
├── great_white_shark.glb  # Main shark model (Download required)
└── test_model_orientation.usda # Orientation debugging utility
```
