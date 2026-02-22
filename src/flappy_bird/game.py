"""Main game module for Flappy Bird"""

import pygame
import sys
from typing import List, Any
from flappy_bird.bird import Bird
from flappy_bird.pipe import Pipe
from flappy_bird.graphics import draw_background_elements, draw_ground, draw_start_screen, draw_game_over_screen
from flappy_bird.sounds import hit_sound, point_sound
from flappy_bird.constants import BIOMES, BIOME_INTERVAL, PIPE_FREQUENCY, BASE_PIPE_SPEED, DIFFICULTY_INCREMENT, SCREEN_WIDTH, GROUND_HEIGHT, SCREEN_HEIGHT


def check_collision(bird: Bird, pipes: List[Pipe]) -> bool:
    # Check collision with ground or ceiling
    if bird.y >= SCREEN_HEIGHT - GROUND_HEIGHT - bird.radius or bird.y <= bird.radius:
        return True

    # Check collision with pipes
    for pipe in pipes:
        if pipe.collide(bird):
            return True

    return False


def draw_lives(surface: pygame.Surface, lives: float) -> None:
    """Draw hearts to represent remaining lives (supports half hearts)"""
    heart_color = (255, 0, 0)  # Red color for hearts
    margin = 10
    
    full_hearts = int(lives)
    has_half_heart = lives % 1 >= 0.5
    
    # Draw full hearts with complex symmetrical shape (smaller size)
    for i in range(full_hearts):
        x = SCREEN_WIDTH - margin - 20 - (i * 28)
        y = margin + 10
        
        # Draw complex symmetrical heart - left side points
        left_points = [
            (x, y + 16),        # Bottom point (center)
            (x - 2, y + 12),    # Lower curve left 1
            (x - 4, y + 9),     # Lower curve left 2
            (x - 6, y + 6),     # Lower left curve
            (x - 8, y + 3),     # Left side lower
            (x - 9, y + 0),     # Left side
            (x - 10, y - 3),    # Left side middle
            (x - 10, y - 6),    # Left side upper
            (x - 9, y - 9),     # Left bump lower outer
            (x - 8, y - 12),    # Left bump outer lower
            (x - 6, y - 14),    # Left bump outer
            (x - 4, y - 15),    # Left bump top outer
            (x - 2, y - 14),    # Left bump top
            (x - 1, y - 11),    # Left bump inner
            (x, y - 8),         # Left side of center dip
        ]
        
        # Right side points (mirror of left)
        right_points = [
            (x, y - 8),         # Right side of center dip
            (x + 1, y - 11),    # Right bump inner
            (x + 2, y - 14),    # Right bump top
            (x + 4, y - 15),    # Right bump top outer
            (x + 6, y - 14),    # Right bump outer
            (x + 8, y - 12),    # Right bump outer lower
            (x + 9, y - 9),     # Right bump lower outer
            (x + 10, y - 6),    # Right side upper
            (x + 10, y - 3),    # Right side middle
            (x + 9, y + 0),     # Right side
            (x + 8, y + 3),     # Right side lower
            (x + 6, y + 6),     # Lower right curve
            (x + 4, y + 9),     # Lower curve right 2
            (x + 2, y + 12),    # Lower curve right 1
        ]
        
        # Combine all points into one closed polygon
        points = left_points + right_points
        pygame.draw.polygon(surface, heart_color, points)
    
    # Draw half heart with complex symmetrical left half shape (smaller size)
    if has_half_heart:
        i = full_hearts
        x = SCREEN_WIDTH - margin - 20 - (i * 28)
        y = margin + 10
        
        # Draw left half of complex symmetrical heart (scaled down)
        points = [
            (x, y + 16),        # Bottom point (center line)
            (x - 2, y + 12),    # Lower curve left 1
            (x - 4, y + 9),     # Lower curve left 2
            (x - 6, y + 6),     # Lower left curve
            (x - 8, y + 3),     # Left side lower
            (x - 9, y + 0),     # Left side
            (x - 10, y - 3),    # Left side middle
            (x - 10, y - 6),    # Left side upper
            (x - 9, y - 9),     # Left bump lower outer
            (x - 8, y - 12),    # Left bump outer lower
            (x - 6, y - 14),    # Left bump outer
            (x - 4, y - 15),    # Left bump top outer
            (x - 2, y - 14),    # Left bump top
            (x - 1, y - 11),    # Left bump inner
            (x, y - 8),         # Center dip (on cut line)
        ]
        pygame.draw.polygon(surface, heart_color, points)


def get_current_biome(score: int):
    """Get the current biome based on the score"""
    biome_index = (score // BIOME_INTERVAL) % len(BIOMES)
    return BIOMES[biome_index]


def get_current_pipe_speed(score: int) -> float:
    """Calculate the current pipe speed based on the score"""
    # Increase speed every 5 points
    level = score // 5
    return BASE_PIPE_SPEED + (level * DIFFICULTY_INCREMENT)


def main() -> None:
    # Initialize pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    # Font - with fallback for systems where font module is not available
    font: Any
    try:
        font = pygame.font.SysFont('arial', 24)
    except (pygame.error, NotImplementedError):
        # If font module is not available, try loading a default font
        font = pygame.font.Font(None, 24)  # Use default font

    # Sound mixer is handled in the sounds module
    bird = Bird()
    pipes: List[Pipe] = []
    score: int = 0
    lives: float = 3.0  # Player starts with 3 lives (supports half hearts)
    last_pipe: int = pygame.time.get_ticks()
    game_state: str = "start"  # "start", "playing", "game_over"
    invincible: bool = False  # Invincibility flag after getting hit
    invincible_timer: int = 0  # Timer for invincibility (in milliseconds)
    INVINCIBILITY_DURATION: int = 2000  # 2 seconds of invincibility
    
    # Fall damage system
    max_height: float = SCREEN_HEIGHT // 2  # Track the highest point before falling
    FALL_DAMAGE_THRESHOLD: float = 100  # Minimum fall distance to take damage
    MAX_FALL_DAMAGE: float = 3.0  # Maximum damage from a single fall

    running: bool = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_state == "start":
                        game_state = "playing"
                    elif game_state == "playing":
                        bird.flap()
                    elif game_state == "game_over":
                        # Restart the game
                        bird = Bird()
                        pipes = []
                        score = 0
                        lives = 3.0  # Reset lives
                        max_height = SCREEN_HEIGHT // 2  # Reset max height tracking
                        last_pipe = pygame.time.get_ticks()
                        invincible = False
                        invincible_timer = 0
                        game_state = "playing"
                if event.key == pygame.K_r and game_state == "game_over":
                    # Restart the game
                    bird = Bird()
                    pipes = []
                    score = 0
                    lives = 3.0  # Reset lives
                    max_height = SCREEN_HEIGHT // 2  # Reset max height tracking
                    last_pipe = pygame.time.get_ticks()
                    invincible = False
                    invincible_timer = 0
                    game_state = "playing"

        # Fill the screen with current biome's sky color
        current_biome = get_current_biome(score)
        screen.fill(current_biome["sky_color"])

        # Draw background elements based on current biome
        draw_background_elements(screen, current_biome, score, pygame.time.get_ticks())

        if game_state == "start":
            # Draw start screen
            draw_start_screen(screen, font)

        elif game_state == "playing":
            # Update bird and track maximum height
            bird.update()
            
            # Track the highest point (lowest y value) before falling
            if bird.y < max_height:
                max_height = bird.y

            # Calculate current pipe speed and biome based on score
            current_pipe_speed = get_current_pipe_speed(score)
            current_biome = get_current_biome(score)

            # Generate new pipes with current biome colors
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe(biome_colors=current_biome))
                last_pipe = time_now

            # Update pipes and remove off-screen pipes
            for pipe in pipes[:]:
                pipe.update(current_pipe_speed)
                if pipe.x < -60:  # Pipe is off screen
                    pipes.remove(pipe)

            # Check for collisions (only if not invincible)
            if not invincible and check_collision(bird, pipes):
                hit_sound.play()  # Play hit sound
                
                # Calculate fall damage
                fall_distance = bird.y - max_height
                if fall_distance > FALL_DAMAGE_THRESHOLD:
                    # Calculate damage based on fall distance (0.5 hearts per 100 pixels fallen, max 3)
                    damage = min(int(fall_distance / 100) * 0.5 + 0.5, MAX_FALL_DAMAGE)
                else:
                    damage = 0.5  # Minimum 0.5 damage for any collision
                
                lives -= damage  # Lose lives based on damage
                if lives <= 0:
                    game_state = "game_over"  # Game over when no lives left
                else:
                    # Become invincible for a short period
                    invincible = True
                    invincible_timer = pygame.time.get_ticks()
                    # Reset bird position
                    bird.y = SCREEN_HEIGHT // 2
                    bird.velocity = 0
                    # Reset max height tracking
                    max_height = bird.y

            # Update invincibility timer
            if invincible:
                time_now = pygame.time.get_ticks()
                if time_now - invincible_timer > INVINCIBILITY_DURATION:
                    invincible = False

            # Calculate score
            for i, pipe in enumerate(pipes):
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1
                    point_sound.play()  # Play point sound

            # Draw everything
            for pipe in pipes:
                pipe.draw(screen)

            draw_ground(screen, current_biome)
            bird.draw(screen, invincible)  # Pass invincible flag for visual feedback

            # Draw score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            
            # Draw lives
            draw_lives(screen, lives)

        elif game_state == "game_over":
            # Draw all pipes and bird for game over state
            current_biome = get_current_biome(score)  # Use final score's biome
            # Draw background elements even in game over
            draw_background_elements(screen, current_biome, score, pygame.time.get_ticks())
            for pipe in pipes:
                pipe.draw(screen)
            draw_ground(screen, current_biome)
            bird.draw(screen)

            # Draw game over screen
            draw_game_over_screen(screen, score, font)

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()