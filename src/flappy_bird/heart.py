"""Heart collectible class for Flappy Bird"""

import pygame
import math
from flappy_bird.constants import SCREEN_HEIGHT, GROUND_HEIGHT


class Heart:
    """A collectible heart that restores health when picked up"""
    
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.radius: int = 12  # Slightly smaller than bird
        self.collected: bool = False
        self.float_offset: float = 0  # For floating animation
        self.float_speed: float = 0.02  # Speed of floating motion
        self.float_amplitude: float = 2  # How far it floats up/down
        
    def update(self, speed: float) -> None:
        """Update heart position and animation"""
        self.x -= speed
        # Floating animation
        self.float_offset = math.sin(pygame.time.get_ticks() * self.float_speed) * self.float_amplitude
        
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the heart with floating animation - same style as health hearts"""
        y = self.y + self.float_offset
        heart_color = (255, 0, 0)  # Red
        
        # Draw heart using the same polygon style as health hearts
        # Left side points
        left_points = [
            (self.x, y + 16),        # Bottom point (center)
            (self.x - 2, y + 12),    # Lower curve left 1
            (self.x - 4, y + 9),     # Lower curve left 2
            (self.x - 6, y + 6),     # Lower left curve
            (self.x - 8, y + 3),     # Left side lower
            (self.x - 9, y + 0),     # Left side
            (self.x - 10, y - 3),    # Left side middle
            (self.x - 10, y - 6),    # Left side upper
            (self.x - 9, y - 9),     # Left bump lower outer
            (self.x - 8, y - 12),    # Left bump outer lower
            (self.x - 6, y - 14),    # Left bump outer
            (self.x - 4, y - 15),    # Left bump top outer
            (self.x - 2, y - 14),    # Left bump top
            (self.x - 1, y - 11),    # Left bump inner
            (self.x, y - 8),         # Left side of center dip
        ]

        # Right side points (mirror of left)
        right_points = [
            (self.x, y - 8),         # Right side of center dip
            (self.x + 1, y - 11),    # Right bump inner
            (self.x + 2, y - 14),    # Right bump top
            (self.x + 4, y - 15),    # Right bump top outer
            (self.x + 6, y - 14),    # Right bump outer
            (self.x + 8, y - 12),    # Right bump outer lower
            (self.x + 9, y - 9),     # Right bump lower outer
            (self.x + 10, y - 6),    # Right side upper
            (self.x + 10, y - 3),    # Right side middle
            (self.x + 9, y + 0),     # Right side
            (self.x + 8, y + 3),     # Right side lower
            (self.x + 6, y + 6),     # Lower right curve
            (self.x + 4, y + 9),     # Lower curve right 2
            (self.x + 2, y + 12),    # Lower curve right 1
        ]

        # Combine all points into one closed polygon
        points = left_points + right_points
        pygame.draw.polygon(surface, heart_color, points)
        
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle for the heart"""
        return pygame.Rect(
            self.x - self.radius,
            self.y + self.float_offset - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def is_off_screen(self) -> bool:
        """Check if heart has moved off the left side of the screen"""
        return self.x < -self.radius * 2
