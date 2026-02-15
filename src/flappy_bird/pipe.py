"""Pipe class for Flappy Bird"""

import pygame
import random
from typing import Dict, Tuple, Optional, TYPE_CHECKING
from flappy_bird.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_GAP, GROUND_HEIGHT, BIOMES

if TYPE_CHECKING:
    from flappy_bird.bird import Bird


class Pipe:
    def __init__(self, biome_colors: Optional[Dict[str, Tuple[int, int, int]]] = None) -> None:
        self.x: float = float(SCREEN_WIDTH)
        self.height: int = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)
        self.top_pipe: pygame.Rect = pygame.Rect(int(self.x), 0, 60, self.height)
        self.bottom_pipe: pygame.Rect = pygame.Rect(int(self.x), self.height + PIPE_GAP, 60, SCREEN_HEIGHT)
        self.passed: bool = False
        self.biome_colors: Dict[str, Tuple[int, int, int]] = biome_colors or BIOMES[0]  # Default to day biome

    def update(self, pipe_speed: float) -> None:
        self.x -= pipe_speed
        self.top_pipe.x = int(self.x)
        self.bottom_pipe.x = int(self.x)

    def draw(self, surface: pygame.Surface) -> None:
        # Draw top pipe
        pygame.draw.rect(surface, self.biome_colors["pipe_color"], self.top_pipe)
        # Draw bottom pipe
        pygame.draw.rect(surface, self.biome_colors["pipe_color"], self.bottom_pipe)
        # Draw pipe caps
        pygame.draw.rect(surface, self.biome_colors["pipe_cap_color"], (self.x - 5, self.height - 20, 70, 20))
        pygame.draw.rect(surface, self.biome_colors["pipe_cap_color"], (self.x - 5, self.height + PIPE_GAP, 70, 20))

    def collide(self, bird: 'Bird') -> bool:
        bird_mask = bird.get_mask()
        return bird_mask.colliderect(self.top_pipe) or bird_mask.colliderect(self.bottom_pipe)