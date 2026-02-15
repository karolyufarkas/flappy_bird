"""Constants for Flappy Bird"""

from typing import Tuple, List, Dict, Any

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
BIOMES: List[Dict[str, Tuple[int, int, int]]] = [
    {  # Day biome (default)
        "sky_color": (135, 206, 235),  # Sky blue
        "pipe_color": (34, 139, 34),   # Forest green
        "pipe_cap_color": (0, 100, 0), # Dark green
        "ground_color": (139, 69, 19), # Brown
        "grass_color": (50, 205, 50)   # Lime green
    },
    {  # Evening biome
        "sky_color": (70, 130, 180),   # Steel blue (evening sky)
        "pipe_color": (106, 90, 205),  # Slate blue (more subtle)
        "pipe_cap_color": (72, 61, 139), # Dark slate blue
        "ground_color": (101, 67, 33), # Dark brown
        "grass_color": (34, 139, 34)   # Forest green
    },
    {  # Desert biome
        "sky_color": (244, 164, 96),   # Sandy
        "pipe_color": (210, 180, 140), # Tan
        "pipe_cap_color": (160, 120, 90), # Darker tan
        "ground_color": (210, 180, 140), # Tan
        "grass_color": (194, 178, 128)  # Light tan
    },
    {  # Snow biome
        "sky_color": (176, 196, 222),  # Light steel blue
        "pipe_color": (176, 196, 222), # Light steel blue (icy look)
        "pipe_cap_color": (100, 149, 237), # Cornflower blue
        "ground_color": (245, 245, 245), # White (snow)
        "grass_color": (220, 220, 220)  # Light gray (frozen grass)
    }
]

# Colors
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
BLUE: Tuple[int, int, int] = (135, 206, 235)  # Sky blue (will be replaced by biome)
GREEN: Tuple[int, int, int] = (0, 200, 0)     # Will be replaced by biome
DARK_GREEN: Tuple[int, int, int] = (0, 150, 0) # Will be replaced by biome
YELLOW: Tuple[int, int, int] = (255, 255, 0)
ORANGE: Tuple[int, int, int] = (255, 165, 0)
BROWN: Tuple[int, int, int] = (139, 69, 19)   # Will be replaced by biome