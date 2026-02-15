"""Bird class for Flappy Bird"""

import pygame
from flappy_bird.constants import FLAP_STRENGTH, GRAVITY, SCREEN_HEIGHT, GROUND_HEIGHT, YELLOW, BLACK, ORANGE
from flappy_bird.sounds import flap_sound


class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 15
        self.alive = True
        self.rotation = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH
        flap_sound.play()  # Play flap sound

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Calculate rotation based on velocity
        self.rotation = max(-30, min(self.velocity * 2, 90))

        # Keep bird on screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0
            self.rotation = -30

        if self.y > SCREEN_HEIGHT - GROUND_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.radius
            self.velocity = 0
            self.rotation = -90

    def draw(self, surface):
        # Create a surface for the bird with rotation
        bird_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(bird_surface, YELLOW, (self.radius, self.radius), self.radius)
        # Draw eye
        pygame.draw.circle(bird_surface, BLACK, (self.radius + 8, self.radius - 5), 4)
        # Draw beak
        pygame.draw.polygon(bird_surface, ORANGE, [(self.radius + 10, self.radius),
                                                         (self.radius + 20, self.radius - 5),
                                                         (self.radius + 20, self.radius + 5)])

        # Rotate the bird surface
        rotated_surface = pygame.transform.rotate(bird_surface, -self.rotation)
        rotated_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))

        # Draw the rotated bird
        surface.blit(rotated_surface, rotated_rect.topleft)

    def get_mask(self):
        # Simple circle mask for collision detection
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)