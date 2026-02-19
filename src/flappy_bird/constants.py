"""Constants for Flappy Bird"""

from typing import NamedTuple, List, Dict


class Color(NamedTuple):
    """RGB color representation"""
    red: int
    green: int
    blue: int


# Game constants
SCREEN_WIDTH: int = 400
SCREEN_HEIGHT: int = 600
GRAVITY: float = 0.25
FLAP_STRENGTH: int = -5
PIPE_GAP: int = 150
BASE_PIPE_SPEED: int = 3
PIPE_FREQUENCY: int = 1800  # milliseconds
GROUND_HEIGHT: int = 100
DIFFICULTY_INCREMENT: float = 0.2  # Speed increase per 5 points

# Biome constants
BIOME_INTERVAL: int = 10  # Change biome every 10 points
BIOMES: List[Dict[str, Color]] = [
    {  # Day biome (default)
        "sky_color": Color(135, 206, 235),  # Sky blue
        "pipe_color": Color(34, 139, 34),   # Forest green
        "pipe_cap_color": Color(0, 100, 0), # Dark green
        "ground_color": Color(139, 69, 19), # Brown
        "grass_color": Color(50, 205, 50)   # Lime green
    },
    {  # Evening biome
        "sky_color": Color(70, 130, 180),   # Steel blue (evening sky)
        "pipe_color": Color(106, 90, 205),  # Slate blue (more subtle)
        "pipe_cap_color": Color(72, 61, 139), # Dark slate blue
        "ground_color": Color(101, 67, 33), # Dark brown
        "grass_color": Color(34, 139, 34)   # Forest green
    },
    {  # Desert biome
        "sky_color": Color(244, 164, 96),   # Sandy
        "pipe_color": Color(210, 180, 140), # Tan
        "pipe_cap_color": Color(160, 120, 90), # Darker tan
        "ground_color": Color(210, 180, 140), # Tan
        "grass_color": Color(194, 178, 128)  # Light tan
    },
    {  # Snow biome
        "sky_color": Color(176, 196, 222),  # Light steel blue
        "pipe_color": Color(176, 196, 222), # Light steel blue (icy look)
        "pipe_cap_color": Color(100, 149, 237), # Cornflower blue
        "ground_color": Color(245, 245, 245), # White (snow)
        "grass_color": Color(220, 220, 220)  # Light gray (frozen grass)
    }
]

# Colors
WHITE: Color = Color(255, 255, 255)
BLACK: Color = Color(0, 0, 0)
BLUE: Color = Color(135, 206, 235)  # Sky blue (will be replaced by biome)
GREEN: Color = Color(0, 200, 0)     # Will be replaced by biome
DARK_GREEN: Color = Color(0, 150, 0) # Will be replaced by biome
YELLOW: Color = Color(255, 255, 0)
ORANGE: Color = Color(255, 165, 0)
BROWN: Color = Color(139, 69, 19)   # Will be replaced by biome
