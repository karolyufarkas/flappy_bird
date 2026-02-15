"""Pygame setup for Flappy Bird"""

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('arial', 24)

# Initialize sound mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)