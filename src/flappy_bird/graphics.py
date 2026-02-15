"""Graphics functions for Flappy Bird"""

import pygame
from typing import Dict, Tuple
from flappy_bird.constants import BIOMES, BIOME_INTERVAL, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT, WHITE, YELLOW


def draw_background_elements(surface: pygame.Surface, biome_colors: Dict[str, Tuple[int, int, int]], score: int, elapsed_time: int) -> None:
    """Draw background elements based on the current biome"""
    biome_index = (score // BIOME_INTERVAL) % len(BIOMES)

    # Draw sun that gradually sets based on score (day to evening transition)
    # Calculate sun position based on score progression within the day biome
    if biome_index == 0 and score < BIOME_INTERVAL:  # Day biome and score < 10
        # Sun moves from left to right and slightly downward as score increases
        normalized_score = score  # Use actual score instead of time-based movement

        sun_x = 50 + (normalized_score / BIOME_INTERVAL) * (SCREEN_WIDTH - 100)
        sun_y = 80 + (normalized_score / BIOME_INTERVAL) * 100  # Move downward as it "sets"

        # Draw sun with glow effect
        sun_surf = pygame.Surface((60, 60))
        sun_surf.fill((0, 0, 0))  # Fill with black first
        sun_surf.set_colorkey((0, 0, 0))  # Make black transparent
        # Outer glow
        pygame.draw.circle(sun_surf, (YELLOW[0], YELLOW[1], YELLOW[2], 50), (30, 30), 30)
        # Inner sun
        pygame.draw.circle(sun_surf, YELLOW, (30, 30), 20)
        surface.blit(sun_surf, (int(sun_x - 30), int(sun_y - 30)))

    if biome_index == 0:  # Day biome - trees
        # Draw large trees that span the entire screen height with trunks at bottom and canopy at top
        for i in range(10):  # More trees to ensure continuous coverage as they move
            # Calculate tree position with smooth movement based on time
            x_pos = (i * 100 - elapsed_time * 0.05) % (SCREEN_WIDTH + 500) - 100  # Trees move backward based on time, faster movement
            # Only draw trees that are visible on screen
            if -50 <= x_pos <= SCREEN_WIDTH + 50:
                # Very tall tree trunk that spans most of the screen
                trunk_width = 40
                trunk_height = SCREEN_HEIGHT - GROUND_HEIGHT - 50  # Almost to the top
                trunk_surf = pygame.Surface((trunk_width, trunk_height))
                trunk_surf.fill((101, 67, 33))  # Full opacity
                surface.blit(trunk_surf, (int(x_pos), 50))  # Start near the top, cast to int for smooth movement

                # Large canopy at the top of the screen
                canopy_surf = pygame.Surface((150, 150))
                canopy_surf.fill((0, 0, 0))  # Fill with black first
                canopy_surf.set_colorkey((0, 0, 0))  # Make black transparent
                # Create a more organic canopy shape using multiple overlapping circles
                pygame.draw.circle(canopy_surf, (34, 139, 34), (75, 100), 60)  # Center
                pygame.draw.circle(canopy_surf, (34, 150, 34), (40, 70), 50)   # Left
                pygame.draw.circle(canopy_surf, (50, 180, 50), (110, 70), 50)  # Right
                pygame.draw.circle(canopy_surf, (34, 145, 34), (25, 40), 40)   # Far left
                pygame.draw.circle(canopy_surf, (40, 155, 40), (125, 40), 40)  # Far right
                surface.blit(canopy_surf, (int(x_pos - 35), 0))  # Position at top of screen, cast to int for smooth movement

    elif biome_index == 1:  # Evening biome - trees
        # Draw large trees that span the entire screen height with trunks at bottom and canopy at top
        for i in range(10):  # More trees to ensure continuous coverage as they move
            # Calculate tree position with smooth movement based on time
            x_pos = (i * 100 - elapsed_time * 0.05) % (SCREEN_WIDTH + 500) - 100  # Trees move backward based on time, faster movement
            # Only draw trees that are visible on screen
            if -50 <= x_pos <= SCREEN_WIDTH + 50:
                # Very tall tree trunk that spans most of the screen
                trunk_width = 40
                trunk_height = SCREEN_HEIGHT - GROUND_HEIGHT - 50  # Almost to the top
                trunk_surf = pygame.Surface((trunk_width, trunk_height))
                trunk_surf.fill((80, 50, 20))  # Full opacity
                surface.blit(trunk_surf, (int(x_pos), 50))  # Start near the top, cast to int for smooth movement

                # Large canopy at the top of the screen
                canopy_surf = pygame.Surface((150, 150))
                canopy_surf.fill((0, 0, 0))  # Fill with black first
                canopy_surf.set_colorkey((0, 0, 0))  # Make black transparent
                # Create a more organic canopy shape using multiple overlapping circles
                pygame.draw.circle(canopy_surf, (34, 100, 34), (75, 100), 60)  # Center
                pygame.draw.circle(canopy_surf, (34, 90, 34), (40, 70), 50)    # Left
                pygame.draw.circle(canopy_surf, (40, 120, 40), (110, 70), 50)  # Right
                pygame.draw.circle(canopy_surf, (34, 105, 34), (25, 40), 40)   # Far left
                pygame.draw.circle(canopy_surf, (40, 115, 40), (125, 40), 40)  # Far right
                surface.blit(canopy_surf, (int(x_pos - 35), 0))  # Position at top of screen, cast to int for smooth movement

    elif biome_index == 2:  # Desert biome - cacti
        # Draw some cacti in the background with transparency
        for i in range(5):
            x_pos = (i * 100 + score * 0.3) % (SCREEN_WIDTH + 200) - 100  # Slower movement
            # Main cactus trunk with transparency
            trunk_surf = pygame.Surface((15, 50), pygame.SRCALPHA)
            trunk_surf.fill((50, 120, 50, 150))  # Semi-transparent
            surface.blit(trunk_surf, (x_pos, SCREEN_HEIGHT - GROUND_HEIGHT - 50))

            # Cactus arms with transparency
            arm1 = pygame.Surface((25, 8), pygame.SRCALPHA)
            arm1.fill((50, 120, 50, 150))
            surface.blit(arm1, (x_pos - 10, SCREEN_HEIGHT - GROUND_HEIGHT - 40))

            arm2 = pygame.Surface((8, 20), pygame.SRCALPHA)
            arm2.fill((50, 120, 50, 150))
            surface.blit(arm2, (x_pos + 7, SCREEN_HEIGHT - GROUND_HEIGHT - 30))

    elif biome_index == 3:  # Snow biome - mountains
        # Draw some mountain silhouettes in the background with transparency
        for i in range(6):
            x_pos = (i * 80 + score * 0.2) % (SCREEN_WIDTH + 100) - 50  # Even slower movement
            # Mountain triangle with transparency
            mountain_points = [
                (x_pos, SCREEN_HEIGHT - GROUND_HEIGHT),
                (x_pos + 40, SCREEN_HEIGHT - GROUND_HEIGHT - 80),
                (x_pos + 80, SCREEN_HEIGHT - GROUND_HEIGHT)
            ]
            mountain_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.polygon(mountain_surf, (200, 200, 220, 120), [(0, 80), (40, 0), (80, 80)])
            surface.blit(mountain_surf, (x_pos, SCREEN_HEIGHT - GROUND_HEIGHT - 80))

            # Snow cap on mountain with transparency
            snow_points = [
                (x_pos + 30, SCREEN_HEIGHT - GROUND_HEIGHT - 60),
                (x_pos + 40, SCREEN_HEIGHT - GROUND_HEIGHT - 80),
                (x_pos + 50, SCREEN_HEIGHT - GROUND_HEIGHT - 60)
            ]
            snow_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.polygon(snow_surf, (245, 245, 245, 180), [(10, 20), (0, 0), (20, 0)])
            surface.blit(snow_surf, (x_pos + 30, SCREEN_HEIGHT - GROUND_HEIGHT - 80))


def draw_ground(surface: pygame.Surface, biome_colors: Dict[str, Tuple[int, int, int]]) -> None:
    pygame.draw.rect(surface, biome_colors["ground_color"], (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    # Draw grass on top of ground
    pygame.draw.rect(surface, biome_colors["grass_color"], (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, 15))


def draw_start_screen(surface: pygame.Surface, font: pygame.font.Font) -> None:
    title_font = pygame.font.SysFont('arial', 36)
    title_text = title_font.render("FLAPPY BIRD", True, WHITE)
    instruction_text = font.render("Press SPACE to Start", True, WHITE)

    surface.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
    surface.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, SCREEN_HEIGHT//2 + 20))


def draw_game_over_screen(surface: pygame.Surface, score: int, font: pygame.font.Font) -> None:
    title_font = pygame.font.SysFont('arial', 36)
    title_text = title_font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)

    surface.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
    surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
    surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 40))