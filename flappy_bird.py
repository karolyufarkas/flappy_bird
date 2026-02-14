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
BASE_PIPE_SPEED = 3
PIPE_FREQUENCY = 1800  # milliseconds
GROUND_HEIGHT = 100
DIFFICULTY_INCREMENT = 0.2  # Speed increase per 5 points

# Biome constants
BIOME_INTERVAL = 10  # Change biome every 10 points
BIOMES = [
    {  # Day biome (default)
        "sky_color": (135, 206, 235),  # Sky blue
        "pipe_color": (34, 139, 34),   # Forest green
        "pipe_cap_color": (0, 100, 0), # Dark green
        "ground_color": (139, 69, 19), # Brown
        "grass_color": (50, 205, 50)   # Lime green
    },
    {  # Evening biome
        "sky_color": (70, 130, 180),   # Steel blue (evening sky)
        "pipe_color": (106, 90, 205),  # Slate blue (more subtle)
        "pipe_cap_color": (72, 61, 139), # Dark slate blue
        "ground_color": (101, 67, 33), # Dark brown
        "grass_color": (34, 139, 34)   # Forest green
    },
    {  # Desert biome
        "sky_color": (244, 164, 96),   # Sandy
        "pipe_color": (210, 180, 140), # Tan
        "pipe_cap_color": (160, 120, 90), # Darker tan
        "ground_color": (210, 180, 140), # Tan
        "grass_color": (194, 178, 128)  # Light tan
    },
    {  # Snow biome
        "sky_color": (176, 196, 222),  # Light steel blue
        "pipe_color": (176, 196, 222), # Light steel blue (icy look)
        "pipe_cap_color": (100, 149, 237), # Cornflower blue
        "ground_color": (245, 245, 245), # White (snow)
        "grass_color": (220, 220, 220)  # Light gray (frozen grass)
    }
]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue (will be replaced by biome)
GREEN = (0, 200, 0)     # Will be replaced by biome
DARK_GREEN = (0, 150, 0) # Will be replaced by biome
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)   # Will be replaced by biome

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('arial', 24)

# Initialize sound mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Create more complex sound effects programmatically
def create_flap_sound():
    """Create a more complex flap sound effect"""
    sample_rate = 22050
    duration_ms = 120
    n_samples = int(round(duration_ms * sample_rate / 1000.0))
    
    # Generate samples for stereo (2 channels)
    arr = numpy.zeros((n_samples, 2))
    for i in range(n_samples):
        t = float(i) / sample_rate
        
        # Create a combination of frequencies that decrease over time
        freq1 = 523.25 * (1 - t / (duration_ms/1000))  # Decreasing C note
        freq2 = 659.25 * (1 - t / (duration_ms/1000))  # Decreasing E note
        
        # Create a more complex waveform combining multiple harmonics
        val = 0.3 * numpy.sin(2 * numpy.pi * freq1 * t)
        val += 0.2 * numpy.sin(2 * numpy.pi * freq2 * t)
        val += 0.1 * numpy.sin(2 * numpy.pi * freq1 * 2 * t)  # Harmonic
        val += 0.1 * numpy.sin(2 * numpy.pi * freq2 * 1.5 * t)  # Harmonic
        
        # Apply envelope to make it sound more natural
        envelope = 1.0 - (t / (duration_ms/1000)) ** 2  # Quadratic fade
        val *= envelope
        
        val *= 0.3 * 32767.0  # Volume control
        arr[i][0] = val  # Left channel
        arr[i][1] = val  # Right channel
    
    # Convert to int16 and create sound
    arr = arr.astype(numpy.int16)
    sound = pygame.sndarray.make_sound(arr)
    return sound

def create_hit_sound():
    """Create a more complex hit sound effect"""
    sample_rate = 22050
    duration_ms = 400
    n_samples = int(round(duration_ms * sample_rate / 1000.0))
    
    # Generate samples for stereo (2 channels)
    arr = numpy.zeros((n_samples, 2))
    for i in range(n_samples):
        t = float(i) / sample_rate
        
        # Create a noise-like sound with multiple decreasing frequencies
        total_val = 0
        for harmonic in range(1, 5):
            freq = 220.00 / harmonic * (1 - t / (duration_ms/1000))  # Decreasing frequency
            total_val += numpy.sin(2 * numpy.pi * freq * t) / harmonic
        
        # Add some white noise for impact
        noise_factor = numpy.random.uniform(-0.1, 0.1) * (1 - t / (duration_ms/1000))
        total_val += noise_factor
        
        # Apply envelope for realistic decay
        envelope = numpy.exp(-t * 3)  # Exponential decay
        total_val *= envelope
        
        total_val *= 0.5 * 32767.0  # Volume control
        arr[i][0] = total_val  # Left channel
        arr[i][1] = total_val  # Right channel
    
    # Convert to int16 and create sound
    arr = arr.astype(numpy.int16)
    sound = pygame.sndarray.make_sound(arr)
    return sound

def create_point_sound():
    """Create a more complex point sound effect"""
    sample_rate = 22050
    duration_ms = 200
    n_samples = int(round(duration_ms * sample_rate / 1000.0))
    
    # Generate samples for stereo (2 channels)
    arr = numpy.zeros((n_samples, 2))
    for i in range(n_samples):
        t = float(i) / sample_rate
        
        # Create a pleasant arpeggiated sound
        freq1 = 523.25  # C note
        freq2 = 659.25  # E note
        freq3 = 783.99  # G note
        
        # Play notes in sequence
        note_duration = (duration_ms/1000) / 3
        if t < note_duration:
            val = numpy.sin(2 * numpy.pi * freq1 * t)
        elif t < 2 * note_duration:
            val = numpy.sin(2 * numpy.pi * freq2 * t)
        else:
            val = numpy.sin(2 * numpy.pi * freq3 * t)
        
        # Apply envelope for clean attack and decay
        attack_time = 0.02  # 20ms attack
        release_time = 0.1  # 100ms release
        if t < attack_time:
            envelope = t / attack_time  # Linear attack
        elif t > (duration_ms/1000 - release_time):
            envelope = (duration_ms/1000 - t) / release_time  # Linear release
        else:
            envelope = 1.0  # Sustain
        
        val *= envelope
        val *= 0.4 * 32767.0  # Volume control
        arr[i][0] = val  # Left channel
        arr[i][1] = val  # Right channel
    
    # Convert to int16 and create sound
    arr = arr.astype(numpy.int16)
    sound = pygame.sndarray.make_sound(arr)
    return sound

# Since pygame.sndarray might not be available, create a fallback
try:
    import numpy
    if pygame.sndarray.get_arraytype() != 'numpy':
        raise ImportError("sndarray not available")
    flap_sound = create_flap_sound()
    hit_sound = create_hit_sound()
    point_sound = create_point_sound()
except (ImportError, AttributeError):
    # Fallback if numpy or sndarray isn't available
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


def check_collision(bird, pipes):
    # Check collision with ground or ceiling
    if bird.y >= SCREEN_HEIGHT - GROUND_HEIGHT - bird.radius or bird.y <= bird.radius:
        return True
    
    # Check collision with pipes
    for pipe in pipes:
        if pipe.collide(bird):
            return True
    
    return False


def draw_background_elements(surface, biome_colors, score, elapsed_time):
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
        pygame.draw.circle(sun_surf, (255, 255, 0, 50), (30, 30), 30)
        # Inner sun
        pygame.draw.circle(sun_surf, (255, 255, 0), (30, 30), 20)
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


def draw_ground(surface, biome_colors):
    pygame.draw.rect(surface, biome_colors["ground_color"], (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    # Draw grass on top of ground
    pygame.draw.rect(surface, biome_colors["grass_color"], (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, 15))


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


def get_current_biome(score):
    """Get the current biome based on the score"""
    biome_index = (score // BIOME_INTERVAL) % len(BIOMES)
    return BIOMES[biome_index]

def get_current_pipe_speed(score):
    """Calculate the current pipe speed based on the score"""
    # Increase speed every 5 points
    level = score // 5
    return BASE_PIPE_SPEED + (level * DIFFICULTY_INCREMENT)

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
        
        # Fill the screen with current biome's sky color
        current_biome = get_current_biome(score)
        screen.fill(current_biome["sky_color"])
        
        # Draw background elements based on current biome
        draw_background_elements(screen, current_biome, score, pygame.time.get_ticks())
        
        if game_state == "start":
            # Draw start screen
            draw_start_screen(screen)
            
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
            score_text = font.render(f"Score: {score}", True, WHITE)
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
            draw_game_over_screen(screen, score)
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()