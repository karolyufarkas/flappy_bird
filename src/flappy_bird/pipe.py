"""Pipe class for Flappy Bird"""

import pygame
import random
from flappy_bird.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_GAP, GROUND_HEIGHT, BIOMES


class Pipe:
    def __init__(self, biome_colors=None):
        self.x = SCREEN_WIDTH
        self.height = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)
        self.top_pipe = pygame.Rect(self.x, 0, 60, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, 60, SCREEN_HEIGHT)
        self.passed = False
        self.biome_colors = biome_colors or BIOMES[0]  # Default to day biome

    def update(self, pipe_speed):
        self.x -= pipe_speed
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self, surface):
        # Draw top pipe
        pygame.draw.rect(surface, self.biome_colors["pipe_color"], self.top_pipe)
        # Draw bottom pipe
        pygame.draw.rect(surface, self.biome_colors["pipe_color"], self.bottom_pipe)
        # Draw pipe caps
        pygame.draw.rect(surface, self.biome_colors["pipe_cap_color"], (self.x - 5, self.height - 20, 70, 20))
        pygame.draw.rect(surface, self.biome_colors["pipe_cap_color"], (self.x - 5, self.height + PIPE_GAP, 70, 20))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        return bird_mask.colliderect(self.top_pipe) or bird_mask.colliderect(self.bottom_pipe)