"""Pipe class for Flappy Bird"""

import pygame
import random
import math
from typing import Dict, Optional, TYPE_CHECKING
from flappy_bird.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_GAP, GROUND_HEIGHT, BIOMES, Color

if TYPE_CHECKING:
    from flappy_bird.bird import Bird


class Pipe:
    def __init__(self, biome_colors: Optional[Dict[str, Color]] = None, moving: bool = False) -> None:
        self.x: float = float(SCREEN_WIDTH)
        self.height: int = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)
        self.base_height: int = self.height  # Store original height for moving pipes
        self.top_pipe: pygame.Rect = pygame.Rect(int(self.x), 0, 60, self.height)
        self.bottom_pipe: pygame.Rect = pygame.Rect(int(self.x), self.height + PIPE_GAP, 60, SCREEN_HEIGHT)
        self.passed: bool = False
        self.biome_colors: Dict[str, Color] = biome_colors or BIOMES[0]  # Default to day biome
        self.moving: bool = moving  # Whether this pipe moves up and down
        self.move_offset: float = 0  # Current vertical offset for moving pipes
        self.move_speed: float = 0.03  # Speed of vertical movement
        self.move_amplitude: int = 40  # How far the pipe moves up/down
        # Random starting phase for varied movement patterns
        self.move_phase: float = random.uniform(0, math.pi * 2)

    def update(self, pipe_speed: float) -> None:
        self.x -= pipe_speed
        self.top_pipe.x = int(self.x)
        self.bottom_pipe.x = int(self.x)

        # Update vertical position for moving pipes
        if self.moving:
            self.move_phase += self.move_speed
            self.move_offset = math.sin(self.move_phase) * self.move_amplitude

            # Update pipe positions with offset
            self.top_pipe.height = int(self.base_height + self.move_offset)
            self.bottom_pipe.y = int(self.base_height + PIPE_GAP + self.move_offset)

    def draw(self, surface: pygame.Surface) -> None:
        # Draw top pipe
        pygame.draw.rect(surface, self.biome_colors["pipe_color"], self.top_pipe)
        # Draw bottom pipe
        pygame.draw.rect(surface, self.biome_colors["pipe_color"], self.bottom_pipe)
        # Draw pipe caps (positioned at the end of top pipe and start of bottom pipe)
        pygame.draw.rect(surface, self.biome_colors["pipe_cap_color"],
                        (self.x - 5, self.top_pipe.height - 20, 70, 20))
        pygame.draw.rect(surface, self.biome_colors["pipe_cap_color"],
                        (self.x - 5, self.bottom_pipe.y, 70, 20))

        # Visual indicator for moving pipes (small arrows)
        if self.moving:
            arrow_color = (255, 255, 0)  # Yellow arrows
            # Draw small arrows on the sides to indicate movement
            arrow_x = int(self.x + 30)  # Center of pipe
            # Up arrow on top pipe
            up_arrow_y = int(self.top_pipe.height - 30)
            pygame.draw.polygon(surface, arrow_color, [
                (arrow_x - 5, up_arrow_y + 8),
                (arrow_x, up_arrow_y),
                (arrow_x + 5, up_arrow_y + 8)
            ])
            # Down arrow on bottom pipe
            down_arrow_y = int(self.bottom_pipe.y + 20)
            pygame.draw.polygon(surface, arrow_color, [
                (arrow_x - 5, down_arrow_y),
                (arrow_x, down_arrow_y + 8),
                (arrow_x + 5, down_arrow_y)
            ])

    def collide(self, bird: 'Bird') -> bool:
        bird_mask = bird.get_mask()
        return bird_mask.colliderect(self.top_pipe) or bird_mask.colliderect(self.bottom_pipe)


class HalfPipe:
    """A single pipe obstacle (either top or bottom) that doesn't give score"""

    TOP = "top"
    BOTTOM = "bottom"

    def __init__(self, biome_colors: Optional[Dict[str, Color]] = None,
                 position: str = TOP, height: Optional[int] = None,
                 x_position: Optional[float] = None) -> None:
        self.x: float = float(SCREEN_WIDTH) if x_position is None else x_position
        self.position: str = position  # TOP or BOTTOM
        self.biome_colors: Dict[str, Color] = biome_colors or BIOMES[0]

        # Height for the pipe (how far it extends from top/bottom)
        if height is None:
            # Random height between 200 and 400 pixels
            self.height: int = random.randint(200, 400)
        else:
            # Ensure height is within valid range
            self.height: int = max(50, min(height, 450))

        # Create the pipe rect based on position
        if self.position == self.TOP:
            # Top pipe extends from top of screen downward
            self.pipe_rect: pygame.Rect = pygame.Rect(int(self.x), 0, 60, self.height)
        else:
            # Bottom pipe extends from ground upward
            ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
            self.pipe_rect: pygame.Rect = pygame.Rect(
                int(self.x), ground_y - self.height, 60, self.height
            )

        # Moving pipe properties
        self.moving: bool = False
        self.move_offset: float = 0
        self.move_speed: float = 0.03
        self.move_amplitude: int = 30
        self.move_phase: float = random.uniform(0, math.pi * 2)
        self.base_height: int = self.height

    def update(self, pipe_speed: float) -> None:
        self.x -= pipe_speed
        self.pipe_rect.x = int(self.x)

        # Update vertical position for moving half pipes
        if self.moving:
            self.move_phase += self.move_speed
            self.move_offset = math.sin(self.move_phase) * self.move_amplitude

            if self.position == self.TOP:
                new_height = int(self.base_height + self.move_offset)
                self.pipe_rect.height = max(50, new_height)  # Ensure minimum height
            else:
                ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
                new_y = int(ground_y - self.base_height + self.move_offset)
                # Ensure pipe stays within bounds
                self.pipe_rect.y = max(0, min(new_y, ground_y - 50))
                self.pipe_rect.height = max(50, ground_y - self.pipe_rect.y)

    def draw(self, surface: pygame.Surface) -> None:
        # Draw the pipe
        pygame.draw.rect(surface, self.biome_colors["pipe_color"], self.pipe_rect)
        
        # Draw pipe cap
        if self.position == self.TOP:
            cap_y = self.pipe_rect.height - 20
        else:
            cap_y = self.pipe_rect.y
        
        pygame.draw.rect(surface, self.biome_colors["pipe_cap_color"],
                        (self.x - 5, cap_y, 70, 20))
        
        # Visual indicator for moving pipes
        if self.moving:
            arrow_color = (255, 255, 0)
            arrow_x = int(self.x + 30)
            
            if self.position == self.TOP:
                # Down arrow for top pipe
                arrow_y = int(self.pipe_rect.height - 30)
                pygame.draw.polygon(surface, arrow_color, [
                    (arrow_x - 5, arrow_y),
                    (arrow_x, arrow_y + 8),
                    (arrow_x + 5, arrow_y)
                ])
            else:
                # Up arrow for bottom pipe
                arrow_y = int(self.pipe_rect.y + 20)
                pygame.draw.polygon(surface, arrow_color, [
                    (arrow_x - 5, arrow_y + 8),
                    (arrow_x, arrow_y),
                    (arrow_x + 5, arrow_y + 8)
                ])

    def collide(self, bird: 'Bird') -> bool:
        bird_mask = bird.get_mask()
        return bird_mask.colliderect(self.pipe_rect)

    def is_off_screen(self) -> bool:
        return self.x < -60
