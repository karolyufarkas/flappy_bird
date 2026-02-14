import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -5
PIPE_GAP = 150
PIPE_SPEED = 3
PIPE_FREQUENCY = 1800  # milliseconds
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('arial', 24)

# Sound effects (using pygame.mixer for sound)
# Since we can't create actual sound files, we'll create dummy sound objects
class DummySound:
    def play(self): pass

flap_sound = DummySound()
hit_sound = DummySound()
point_sound = DummySound()


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


class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)
        self.top_pipe = pygame.Rect(self.x, 0, 60, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, 60, SCREEN_HEIGHT)
        self.passed = False
        self.PIPE_COLOR = GREEN
        
    def update(self):
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x
        
    def draw(self, surface):
        # Draw top pipe
        pygame.draw.rect(surface, self.PIPE_COLOR, self.top_pipe)
        # Draw bottom pipe
        pygame.draw.rect(surface, self.PIPE_COLOR, self.bottom_pipe)
        # Draw pipe caps
        pygame.draw.rect(surface, (0, 180, 0), (self.x - 5, self.height - 20, 70, 20))
        pygame.draw.rect(surface, (0, 180, 0), (self.x - 5, self.height + PIPE_GAP, 70, 20))
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        return bird_mask.colliderect(self.top_pipe) or bird_mask.colliderect(self.bottom_pipe)


def check_collision(bird, pipes):
    # Check collision with ground or ceiling
    if bird.y >= SCREEN_HEIGHT - GROUND_HEIGHT - bird.radius or bird.y <= bird.radius:
        return True
    
    # Check collision with pipes
    for pipe in pipes:
        if pipe.collide(bird):
            return True
    
    return False


def draw_ground(surface):
    pygame.draw.rect(surface, (139, 69, 19), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    # Draw grass on top of ground
    pygame.draw.rect(surface, (0, 200, 0), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, 15))


def draw_start_screen(surface):
    title_font = pygame.font.SysFont('arial', 36)
    title_text = title_font.render("FLAPPY BIRD", True, WHITE)
    instruction_text = font.render("Press SPACE to Start", True, WHITE)
    
    surface.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
    surface.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, SCREEN_HEIGHT//2 + 20))


def draw_game_over_screen(surface, score):
    title_font = pygame.font.SysFont('arial', 36)
    title_text = title_font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    
    surface.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
    surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
    surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 40))


def main():
    bird = Bird()
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()
    passed_pipe_index = 0  # Index of the last pipe that the bird passed
    game_state = "start"  # "start", "playing", "game_over"
    
    running = True
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
                        passed_pipe_index = 0
                        game_state = "playing"
                if event.key == pygame.K_r and game_state == "game_over":
                    # Restart the game
                    bird = Bird()
                    pipes = []
                    score = 0
                    last_pipe = pygame.time.get_ticks()
                    passed_pipe_index = 0
                    game_state = "playing"
        
        # Fill the screen with sky blue
        screen.fill(BLUE)
        
        if game_state == "start":
            # Draw start screen
            draw_start_screen(screen)
            
        elif game_state == "playing":
            # Update bird
            bird.update()
            
            # Generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = time_now
                
            # Update pipes and remove off-screen pipes
            for pipe in pipes[:]:
                pipe.update()
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
                
            draw_ground(screen)
            bird.draw(screen)
            
            # Draw score
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
        elif game_state == "game_over":
            # Draw all pipes and bird for game over state
            for pipe in pipes:
                pipe.draw(screen)
            draw_ground(screen)
            bird.draw(screen)
            
            # Draw game over screen
            draw_game_over_screen(screen, score)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()