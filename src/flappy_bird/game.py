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
    last_pipe: int = pygame.time.get_ticks()
    game_state: str = "start"  # "start", "playing", "game_over"

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
                        last_pipe = pygame.time.get_ticks()
                        game_state = "playing"
                if event.key == pygame.K_r and game_state == "game_over":
                    # Restart the game
                    bird = Bird()
                    pipes = []
                    score = 0
                    last_pipe = pygame.time.get_ticks()
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
            # Update bird
            bird.update()

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

            # Check for collisions
            if check_collision(bird, pipes):
                hit_sound.play()  # Play hit sound
                game_state = "game_over"

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
            bird.draw(screen)

            # Draw score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

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