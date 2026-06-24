import pygame
import random
import math

# Initialize Pygame
pygame.init()

# CONFIGURABLE STARTING NUMBERS
NUM_ROCKS = 20
NUM_PAPERS = 20
NUM_SCISSORS = 20

# Constants
INFO = pygame.display.Info()
WIDTH, HEIGHT = INFO.current_w, INFO.current_h
FPS = 60
SPRITE_SIZE = 32
ENTITY_RADIUS = SPRITE_SIZE // 2
GRID_SIZE = 64  # Spatial partitioning grid size

# Colors
BG_COLOR = (20, 20, 40)

def create_rock_sprite():
    """Create detailed pixel art rock sprite"""
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    # 16x16 pixel art
    pixels = [
        "    ▓▓▓▓▓▓▓▓    ",
        "  ▓▓████████▓▓  ",
        " ▓▓██░░████░░██▓ ",
        "▓▓██░░██████░░██▓",
        "▓██████████████▓▓",
        "▓██░░████████░░██▓",
        "▓████████████████▓",
        "▓██████▓▓████████▓",
        "▓████▓▓░░▓▓██████▓",
        "▓██████▓▓████████▓",
        " ▓████████████▓▓ ",
        " ▓▓████████████▓ ",
        "  ▓▓██████████▓  ",
        "   ▓▓████████▓   ",
        "    ▓▓▓▓▓▓▓▓     ",
        "                 "
    ]
    colors = {
        '█': (90, 90, 95),      # dark gray
        '▓': (60, 60, 65),      # darker gray
        '░': (130, 130, 140)    # light gray highlight
    }
    for y, row in enumerate(pixels):
        for x, char in enumerate(row):
            if char in colors:
                pygame.draw.rect(surf, colors[char], (x * 2, y * 2, 2, 2))
    return surf

def create_paper_sprite():
    """Create detailed pixel art paper sprite"""
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    # 16x16 pixel art
    pixels = [
        "  ████████████  ",
        " ██░░░░░░░░░░██ ",
        " █░░░░░░░░░░░░█ ",
        " █░▓▓▓▓▓▓▓▓▓░░█ ",
        " █░░░░░░░░░░░░█ ",
        " █░░░░░░░░░░░░█ ",
        " █░▓▓▓▓▓▓▓▓▓░░█ ",
        " █░░░░░░░░░░░░█ ",
        " █░░░░░░░░░░░░█ ",
        " █░▓▓▓▓▓▓▓▓▓░░█ ",
        " █░░░░░░░░░░░░█ ",
        " █░░░░░░░░░░░░█ ",
        " █░▓▓▓▓▓▓▓▓▓░░█ ",
        " █░░░░░░░░░░░░█ ",
        " ██░░░░░░░░░░██ ",
        "  ████████████  "
    ]
    colors = {
        '█': (245, 245, 235),   # white/cream border
        '░': (255, 255, 250),   # bright white
        '▓': (180, 180, 170)    # gray lines
    }
    for y, row in enumerate(pixels):
        for x, char in enumerate(row):
            if char in colors:
                pygame.draw.rect(surf, colors[char], (x * 2, y * 2, 2, 2))
    return surf

def create_scissors_sprite():
    """Create detailed pixel art scissors sprite"""
    surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    # 16x16 pixel art - scissors with two blades
    pixels = [
        "██            ██",
        "████        ████",
        " ████      ████ ",
        "  ████    ████  ",
        "   ████  ████   ",
        "    ████████    ",
        "     ██░░██     ",
        "      ░░░░      ",
        "      ░░░░      ",
        "     ██░░██     ",
        "    ████████    ",
        "   ████  ████   ",
        "  ████    ████  ",
        " ████      ████ ",
        "▓▓▓▓        ▓▓▓▓",
        "▓▓            ▓▓"
    ]
    colors = {
        '█': (200, 200, 210),   # silver blades
        '░': (160, 160, 170),   # darker metal center
        '▓': (220, 60, 60)      # red handles
    }
    for y, row in enumerate(pixels):
        for x, char in enumerate(row):
            if char in colors:
                pygame.draw.rect(surf, colors[char], (x * 2, y * 2, 2, 2))
    return surf

class Entity:
    def __init__(self, x, y, entity_type, sprites):
        self.x = x
        self.y = y
        self.type = entity_type
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.radius = ENTITY_RADIUS
        self.sprites = sprites
        self.grid_x = 0
        self.grid_y = 0
        self.conversion_count = 0  # Track how many times this entity has been converted
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -1
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy *= -1
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
        
        # Update grid position
        self.grid_x = int(self.x // GRID_SIZE)
        self.grid_y = int(self.y // GRID_SIZE)
    
    def draw(self, screen):
        sprite = self.sprites[self.type]
        screen.blit(sprite, (int(self.x - SPRITE_SIZE // 2), int(self.y - SPRITE_SIZE // 2)))
        
    def distance_squared(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy
    
    def collides_with(self, other):
        collision_dist = (self.radius + other.radius) ** 2
        return self.distance_squared(other) < collision_dist

class DVDLogo:
    def __init__(self):
        # Load DVD logo image
        try:
            self.original_image = pygame.image.load('DVD-logo.jpg').convert_alpha()
            # Scale to reasonable size
            self.width = 150
            self.height = int(self.original_image.get_height() * (self.width / self.original_image.get_width()))
            self.original_image = pygame.transform.scale(self.original_image, (self.width, self.height))
        except:
            # Fallback if image not found
            self.width = 120
            self.height = 60
            self.original_image = None

        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(0, HEIGHT - self.height)
        self.vx = random.choice([-6, 6])
        self.vy = random.choice([-6, 6])

        # Use original image as the main image
        self.image = self.original_image

    def update(self):
        """Move and bounce off screen edges"""
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH - self.width:
            self.vx *= -1
            self.x = max(0, min(WIDTH - self.width, self.x))
        if self.y <= 0 or self.y >= HEIGHT - self.height:
            self.vy *= -1
            self.y = max(0, min(HEIGHT - self.height, self.y))

    def draw(self, screen):
        """Draw DVD logo or fallback"""
        if self.image:
            screen.blit(self.image, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
            font = pygame.font.Font(None, 40)
            text = font.render("DVD", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text, text_rect)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides_with_entity(self, entity):
        entity_rect = pygame.Rect(
            entity.x - entity.radius, 
            entity.y - entity.radius, 
            entity.radius * 2, 
            entity.radius * 2
        )
        # 1 in 4 chance to kill on collision
        if self.get_rect().colliderect(entity_rect):
            return random.randint(1, 4) == 1
        return False

class Thanos:
    def __init__(self):
        # Load Thanos image
        try:
            self.image = pygame.image.load('Thanos.png').convert_alpha()
            # Scale to smaller size
            self.width = 120
            self.height = int(self.image.get_height() * (self.width / self.image.get_width()))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            self.image = None
            self.width = 100
            self.height = 100
        
        # Position in bottom right corner
        self.x = WIDTH - self.width - 20
        self.y = HEIGHT - self.height - 20
        self.snap_timer = 0
        self.snap_check_interval = 60  # Check once per second at 60 FPS
        
    def update(self):
        """Check if it's time to snap (once per second)"""
        self.snap_timer += 1
        
        # Only check every second (60 frames)
        if self.snap_timer >= self.snap_check_interval:
            self.snap_timer = 0
            # 1 in 25 chance to snap (4% chance per second)
            if random.randint(1, 25) == 1:
                return True  # Snap!
        return False
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (int(self.x), int(self.y)))
        else:
            # Fallback
            pygame.draw.rect(screen, (100, 50, 150), (self.x, self.y, self.width, self.height))
            font = pygame.font.Font(None, 40)
            text = font.render("THANOS", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text, text_rect)


def check_winner(type1, type2):
    """Returns True if type1 beats type2"""
    if type1 == 'rock' and type2 == 'scissors':
        return True
    if type1 == 'paper' and type2 == 'rock':
        return True
    if type1 == 'scissors' and type2 == 'paper':
        return True
    return False

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        self.handle_radius = height // 2 + 2
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
            handle_y = self.rect.y + self.rect.height // 2
            dist = math.sqrt((mouse_pos[0] - handle_x) ** 2 + (mouse_pos[1] - handle_y) ** 2)
            if dist <= self.handle_radius:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            relative_x = max(0, min(self.rect.width, mouse_x - self.rect.x))
            self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
    
    def draw(self, screen, label=""):
        # Draw track
        pygame.draw.rect(screen, (60, 60, 70), self.rect, border_radius=self.rect.height // 2)
        
        # Draw filled portion
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, handle_x - self.rect.x, self.rect.height)
        pygame.draw.rect(screen, (100, 150, 255), filled_rect, border_radius=self.rect.height // 2)
        
        # Draw handle
        handle_y = self.rect.y + self.rect.height // 2
        pygame.draw.circle(screen, (255, 255, 255), (int(handle_x), handle_y), self.handle_radius)
        pygame.draw.circle(screen, (200, 200, 200), (int(handle_x), handle_y), self.handle_radius, 2)
        
        # Draw label
        if label:
            font = pygame.font.Font(None, 32)
            label_text = font.render(label, True, (255, 255, 255))
            screen.blit(label_text, (self.rect.x, self.rect.y - 30))
            
            # Draw value
            value_text = font.render(f"{self.value:.1f}x", True, (255, 255, 255))
            screen.blit(value_text, (self.rect.x + self.rect.width + 10, self.rect.y - 5))

def ease_out_cubic(t):
    """Easing function for smooth animation"""
    return 1 - pow(1 - t, 3)

def draw_victory_animation(screen, winner_type, sprites, animation_progress):
    """Draw victory animation with rising podiums"""
    # Apply easing to animation progress for smoother motion
    eased_progress = ease_out_cubic(animation_progress)
    
    # Determine 2nd and 3rd place based on winner
    # 2nd place = what the winner beats (they lasted longer)
    # 3rd place = what beats the winner (they were eliminated first)
    if winner_type == 'rock':
        second_place = 'scissors'  # rock beats scissors (scissors lasted longer)
        third_place = 'paper'  # paper beats rock (paper was eliminated first)
    elif winner_type == 'paper':
        second_place = 'rock'  # paper beats rock (rock lasted longer)
        third_place = 'scissors'  # scissors beats paper (scissors was eliminated first)
    else:  # scissors
        second_place = 'paper'  # scissors beats paper (paper lasted longer)
        third_place = 'rock'  # rock beats scissors (rock was eliminated first)
    
    # Animation progress goes from 0 to 1
    max_gold_height = 350
    max_silver_height = 250
    max_bronze_height = 180
    
    # Use eased progress for smooth podium rise
    podium_height = int(max_gold_height * eased_progress)
    silver_height = int(max_silver_height * eased_progress)
    bronze_height = int(max_bronze_height * eased_progress)
    
    # Center positions for three podiums
    center_x = WIDTH // 2
    baseline_y = HEIGHT - 150  # Bottom of screen
    
    podium_width = 150
    spacing = 50
    sprite_scale = 4
    
    # Gold podium (winner) - center, tallest
    gold_color = (255, 215, 0)
    gold_x = center_x - podium_width // 2
    gold_y = baseline_y - podium_height
    if podium_height > 0:
        pygame.draw.rect(screen, gold_color, (gold_x, gold_y, podium_width, podium_height))
        pygame.draw.rect(screen, (200, 170, 0), (gold_x, gold_y, podium_width, podium_height), 5)
    
    # Silver podium (2nd place) - left, medium
    silver_color = (192, 192, 192)
    silver_x = gold_x - podium_width - spacing
    silver_y = baseline_y - silver_height
    if silver_height > 0:
        pygame.draw.rect(screen, silver_color, (silver_x, silver_y, podium_width, silver_height))
        pygame.draw.rect(screen, (150, 150, 150), (silver_x, silver_y, podium_width, silver_height), 5)
    
    # Bronze podium (3rd place) - right, shortest
    bronze_color = (205, 127, 50)
    bronze_x = gold_x + podium_width + spacing
    bronze_y = baseline_y - bronze_height
    if bronze_height > 0:
        pygame.draw.rect(screen, bronze_color, (bronze_x, bronze_y, podium_width, bronze_height))
        pygame.draw.rect(screen, (160, 100, 40), (bronze_x, bronze_y, podium_width, bronze_height), 5)
    
    # Draw sprites on podiums
    if podium_height > 50:
        # 1st place sprite
        sprite = sprites[winner_type]
        scaled_sprite = pygame.transform.scale(sprite, (SPRITE_SIZE * sprite_scale, SPRITE_SIZE * sprite_scale))
        sprite_x = gold_x + podium_width // 2 - (SPRITE_SIZE * sprite_scale) // 2
        sprite_y = gold_y - (SPRITE_SIZE * sprite_scale) - 20
        screen.blit(scaled_sprite, (sprite_x, sprite_y))
    
    if silver_height > 50:
        # 2nd place sprite
        sprite = sprites[second_place]
        scaled_sprite = pygame.transform.scale(sprite, (SPRITE_SIZE * sprite_scale, SPRITE_SIZE * sprite_scale))
        sprite_x = silver_x + podium_width // 2 - (SPRITE_SIZE * sprite_scale) // 2
        sprite_y = silver_y - (SPRITE_SIZE * sprite_scale) - 20
        screen.blit(scaled_sprite, (sprite_x, sprite_y))
    
    if bronze_height > 50:
        # 3rd place sprite
        sprite = sprites[third_place]
        scaled_sprite = pygame.transform.scale(sprite, (SPRITE_SIZE * sprite_scale, SPRITE_SIZE * sprite_scale))
        sprite_x = bronze_x + podium_width // 2 - (SPRITE_SIZE * sprite_scale) // 2
        sprite_y = bronze_y - (SPRITE_SIZE * sprite_scale) - 20
        screen.blit(scaled_sprite, (sprite_x, sprite_y))
    
    # Draw text labels
    if animation_progress > 0.3:
        big_font = pygame.font.Font(None, 140)
        small_font = pygame.font.Font(None, 70)
        
        winner_text = big_font.render(f"{winner_type.upper()} WINS!", True, (255, 255, 255))
        text_rect = winner_text.get_rect(center=(center_x, 150))
        
        # Draw text shadow
        shadow_text = big_font.render(f"{winner_type.upper()} WINS!", True, (0, 0, 0))
        screen.blit(shadow_text, (text_rect.x + 5, text_rect.y + 5))
        screen.blit(winner_text, text_rect)
        
        # Draw place numbers on podiums with darker shades of podium colors
        if podium_height > 100:
            gold_text_color = (200, 170, 0)  # Darker gold
            place_text = small_font.render("1st", True, gold_text_color)
            place_rect = place_text.get_rect(center=(gold_x + podium_width // 2, gold_y + 50))
            screen.blit(place_text, place_rect)
        if silver_height > 80:
            silver_text_color = (120, 120, 120)  # Darker silver
            place_text = small_font.render("2nd", True, silver_text_color)
            place_rect = place_text.get_rect(center=(silver_x + podium_width // 2, silver_y + 40))
            screen.blit(place_text, place_rect)
        if bronze_height > 60:
            bronze_text_color = (140, 85, 30)  # Darker bronze
            place_text = small_font.render("3rd", True, bronze_text_color)
            place_rect = place_text.get_rect(center=(bronze_x + podium_width // 2, bronze_y + 30))
            screen.blit(place_text, place_rect)

def show_main_menu(screen, sprites):
    """Display main menu with Start and Settings buttons"""
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Buttons
    button_width = 400
    button_height = 80
    start_button = pygame.Rect(center_x - button_width // 2, center_y - 50, button_width, button_height)
    settings_button = pygame.Rect(center_x - button_width // 2, center_y + 60, button_width, button_height)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return 'start'
                if settings_button.collidepoint(event.pos):
                    return 'settings'
        
        screen.fill(BG_COLOR)
        
        # Title
        title_font = pygame.font.Font(None, 120)
        title_text = title_font.render("ROCK PAPER SCISSORS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(center_x, center_y - 250))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 50)
        subtitle_text = subtitle_font.render("Battle Simulation", True, (180, 180, 180))
        subtitle_rect = subtitle_text.get_rect(center=(center_x, center_y - 170))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        button_font = pygame.font.Font(None, 70)
        
        # Start button
        start_hover = start_button.collidepoint(mouse_pos)
        start_color = (100, 200, 100) if start_hover else (70, 150, 70)
        pygame.draw.rect(screen, start_color, start_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), start_button, 3, border_radius=10)
        start_text = button_font.render("START", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)
        
        # Settings button
        settings_hover = settings_button.collidepoint(mouse_pos)
        settings_color = (100, 150, 200) if settings_hover else (70, 100, 150)
        pygame.draw.rect(screen, settings_color, settings_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), settings_button, 3, border_radius=10)
        settings_text = button_font.render("SETTINGS", True, (255, 255, 255))
        settings_text_rect = settings_text.get_rect(center=settings_button.center)
        screen.blit(settings_text, settings_text_rect)
        
        # Instructions
        inst_font = pygame.font.Font(None, 30)
        inst_text = inst_font.render("Press ESC to quit", True, (150, 150, 150))
        inst_rect = inst_text.get_rect(center=(center_x, HEIGHT - 50))
        screen.blit(inst_text, inst_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

def show_settings_menu(screen, sprites, settings):
    """Display settings menu"""
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Left side - Entity counts
    left_x = center_x - 420
    slider_width = 300
    spacing = 70
    rock_slider = Slider(left_x, center_y - 90, slider_width, 25, 10, 1000, settings['num_rocks'])
    paper_slider = Slider(left_x, center_y - 90 + spacing, slider_width, 25, 10, 1000, settings['num_papers'])
    scissors_slider = Slider(left_x, center_y - 90 + spacing * 2, slider_width, 25, 10, 1000, settings['num_scissors'])
    
    # Right side - Game options
    right_x = center_x + 100
    death_slider = Slider(right_x, center_y + 20, slider_width, 25, 1, 10, settings['conversions_to_death'])
    
    # Buttons
    button_width = 200
    button_height = 60
    back_button = pygame.Rect(center_x - button_width - 20, HEIGHT - 120, button_width, button_height)
    save_button = pygame.Rect(center_x + 20, HEIGHT - 120, button_width, button_height)
    
    # Toggle buttons
    toggle_width = 70
    toggle_height = 36
    takeover_toggle = pygame.Rect(right_x + 200, center_y - 135, toggle_width, toggle_height)
    dvd_toggle = pygame.Rect(right_x + 200, center_y + 145, toggle_width, toggle_height)
    thanos_toggle = pygame.Rect(right_x + 200, center_y + 215, toggle_width, toggle_height)
    
    takeover_enabled = settings['takeover_mode']
    dvd_enabled = settings.get('dvd_logo', False)
    thanos_enabled = settings.get('thanos_mode', False)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return settings
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return settings
                if save_button.collidepoint(event.pos):
                    settings['num_rocks'] = int(rock_slider.value)
                    settings['num_papers'] = int(paper_slider.value)
                    settings['num_scissors'] = int(scissors_slider.value)
                    settings['conversions_to_death'] = int(death_slider.value)
                    settings['takeover_mode'] = takeover_enabled
                    settings['dvd_logo'] = dvd_enabled
                    settings['thanos_mode'] = thanos_enabled
                    return settings
                if takeover_toggle.collidepoint(event.pos):
                    takeover_enabled = not takeover_enabled
                if dvd_toggle.collidepoint(event.pos):
                    dvd_enabled = not dvd_enabled
                if thanos_toggle.collidepoint(event.pos):
                    thanos_enabled = not thanos_enabled
            
            rock_slider.handle_event(event)
            paper_slider.handle_event(event)
            scissors_slider.handle_event(event)
            death_slider.handle_event(event)
        
        screen.fill(BG_COLOR)
        
        # Title
        title_font = pygame.font.Font(None, 90)
        title_text = title_font.render("SETTINGS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(center_x, center_y - 300))
        screen.blit(title_text, title_rect)
        
        # Fonts
        section_font = pygame.font.Font(None, 50)
        label_font = pygame.font.Font(None, 32)
        value_font = pygame.font.Font(None, 28)
        toggle_font = pygame.font.Font(None, 26)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # LEFT SIDE - Entity Counts
        left_section = section_font.render("Entity Counts", True, (180, 200, 255))
        screen.blit(left_section, (left_x, center_y - 180))
        
        # Rock slider
        rock_sprite = pygame.transform.scale(sprites['rock'], (36, 36))
        screen.blit(rock_sprite, (left_x - 48, center_y - 105))
        rock_label = label_font.render("Rocks:", True, (255, 255, 255))
        screen.blit(rock_label, (left_x, center_y - 118))
        rock_slider.draw(screen, "")
        rock_value = value_font.render(str(int(rock_slider.value)), True, (180, 180, 180))
        screen.blit(rock_value, (left_x + slider_width + 15, center_y - 95))
        
        # Paper slider
        paper_sprite = pygame.transform.scale(sprites['paper'], (36, 36))
        screen.blit(paper_sprite, (left_x - 48, center_y - 105 + spacing))
        paper_label = label_font.render("Papers:", True, (255, 255, 255))
        screen.blit(paper_label, (left_x, center_y - 118 + spacing))
        paper_slider.draw(screen, "")
        paper_value = value_font.render(str(int(paper_slider.value)), True, (180, 180, 180))
        screen.blit(paper_value, (left_x + slider_width + 15, center_y - 95 + spacing))
        
        # Scissors slider
        scissors_sprite = pygame.transform.scale(sprites['scissors'], (36, 36))
        screen.blit(scissors_sprite, (left_x - 48, center_y - 105 + spacing * 2))
        scissors_label = label_font.render("Scissors:", True, (255, 255, 255))
        screen.blit(scissors_label, (left_x, center_y - 118 + spacing * 2))
        scissors_slider.draw(screen, "")
        scissors_value = value_font.render(str(int(scissors_slider.value)), True, (180, 180, 180))
        screen.blit(scissors_value, (left_x + slider_width + 15, center_y - 95 + spacing * 2))
        
        # RIGHT SIDE - Game Options
        right_section = section_font.render("Game Options", True, (180, 200, 255))
        screen.blit(right_section, (right_x, center_y - 180))
        
        # Takeover mode
        takeover_label = label_font.render("Takeover Mode:", True, (255, 255, 255))
        screen.blit(takeover_label, (right_x, center_y - 130))
        
        takeover_hover = takeover_toggle.collidepoint(mouse_pos)
        if takeover_enabled:
            takeover_color = (130, 230, 130) if takeover_hover else (100, 200, 100)
        else:
            takeover_color = (220, 80, 80) if takeover_hover else (180, 60, 60)
        pygame.draw.rect(screen, takeover_color, takeover_toggle, border_radius=17)
        pygame.draw.rect(screen, (255, 255, 255), takeover_toggle, 3, border_radius=17)
        takeover_text = toggle_font.render("ON" if takeover_enabled else "OFF", True, (255, 255, 255))
        screen.blit(takeover_text, takeover_text.get_rect(center=takeover_toggle.center))
        
        # Conversions to death (only if takeover enabled)
        if takeover_enabled:
            death_label = label_font.render("Conversions to Death:", True, (255, 255, 255))
            screen.blit(death_label, (right_x, center_y - 8))
            death_slider.draw(screen, "")
            death_value = value_font.render(str(int(death_slider.value)), True, (180, 180, 180))
            screen.blit(death_value, (right_x + slider_width + 15, center_y + 15))
        
        # EXTRAS section
        extras_section = section_font.render("Extras", True, (255, 200, 180))
        screen.blit(extras_section, (right_x, center_y + 80))
        
        # DVD Logo option
        dvd_label = label_font.render("DVD Logo Killer:", True, (255, 255, 255))
        screen.blit(dvd_label, (right_x, center_y + 130))
        
        dvd_hover = dvd_toggle.collidepoint(mouse_pos)
        if dvd_enabled:
            dvd_color = (130, 230, 130) if dvd_hover else (100, 200, 100)
        else:
            dvd_color = (220, 80, 80) if dvd_hover else (180, 60, 60)
        pygame.draw.rect(screen, dvd_color, dvd_toggle, border_radius=17)
        pygame.draw.rect(screen, (255, 255, 255), dvd_toggle, 3, border_radius=17)
        dvd_text = toggle_font.render("ON" if dvd_enabled else "OFF", True, (255, 255, 255))
        screen.blit(dvd_text, dvd_text.get_rect(center=dvd_toggle.center))
        
        # Thanos Mode option
        thanos_label = label_font.render("Thanos Mode:", True, (255, 255, 255))
        screen.blit(thanos_label, (right_x, center_y + 200))
        
        thanos_hover = thanos_toggle.collidepoint(mouse_pos)
        if thanos_enabled:
            thanos_color = (130, 230, 130) if thanos_hover else (100, 200, 100)
        else:
            thanos_color = (220, 80, 80) if thanos_hover else (180, 60, 60)
        pygame.draw.rect(screen, thanos_color, thanos_toggle, border_radius=17)
        pygame.draw.rect(screen, (255, 255, 255), thanos_toggle, 3, border_radius=17)
        thanos_text = toggle_font.render("ON" if thanos_enabled else "OFF", True, (255, 255, 255))
        screen.blit(thanos_text, thanos_text.get_rect(center=thanos_toggle.center))
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        button_font = pygame.font.Font(None, 50)
        
        # Back button
        back_hover = back_button.collidepoint(mouse_pos)
        back_color = (150, 150, 150) if back_hover else (100, 100, 100)
        pygame.draw.rect(screen, back_color, back_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), back_button, 3, border_radius=10)
        back_text = button_font.render("BACK", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)
        
        # Save button
        save_hover = save_button.collidepoint(mouse_pos)
        save_color = (100, 200, 100) if save_hover else (70, 150, 70)
        pygame.draw.rect(screen, save_color, save_button, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), save_button, 3, border_radius=10)
        save_text = button_font.render("SAVE", True, (255, 255, 255))
        save_text_rect = save_text.get_rect(center=save_button.center)
        screen.blit(save_text, save_text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

def run_simulation(screen, sprites, settings):
    """Run the main simulation"""
    clock = pygame.time.Clock()
    
    # Create entities with configured numbers
    entities = []
    
    for _ in range(settings['num_rocks']):
        x = random.randint(ENTITY_RADIUS, WIDTH - ENTITY_RADIUS)
        y = random.randint(ENTITY_RADIUS, HEIGHT - ENTITY_RADIUS)
        entities.append(Entity(x, y, 'rock', sprites))
    
    for _ in range(settings['num_papers']):
        x = random.randint(ENTITY_RADIUS, WIDTH - ENTITY_RADIUS)
        y = random.randint(ENTITY_RADIUS, HEIGHT - ENTITY_RADIUS)
        entities.append(Entity(x, y, 'paper', sprites))
    
    for _ in range(settings['num_scissors']):
        x = random.randint(ENTITY_RADIUS, WIDTH - ENTITY_RADIUS)
        y = random.randint(ENTITY_RADIUS, HEIGHT - ENTITY_RADIUS)
        entities.append(Entity(x, y, 'scissors', sprites))
    
    # Create DVD logo if enabled
    dvd_logo = DVDLogo() if settings.get('dvd_logo', False) else None
    
    # Create Thanos if enabled
    thanos = Thanos() if settings.get('thanos_mode', False) else None
    
    font = pygame.font.Font(None, 48)
    running = True
    game_over = False
    winner = None
    victory_timer = 0
    victory_duration = 90  # frames for victory animation (faster)
    
    # Speed control slider
    speed_slider = Slider(WIDTH - 350, 70, 250, 20, 0.1, 5.0, 1.0)
    simulation_speed = 1.0
    
    # Spatial grid for optimization
    grid_cols = (WIDTH // GRID_SIZE) + 1
    grid_rows = (HEIGHT // GRID_SIZE) + 1
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
            
            # Handle slider events
            speed_slider.handle_event(event)
        
        # Update simulation speed
        simulation_speed = speed_slider.value
        
        # Check for victory condition
        if not game_over and len(entities) > 0:
            types_present = set(e.type for e in entities)
            if len(types_present) == 1:
                game_over = True
                winner = list(types_present)[0]
                victory_timer = 0
        
        if not game_over:
            # Run simulation multiple times based on speed
            updates_this_frame = int(simulation_speed)
            fractional_part = simulation_speed - updates_this_frame
            if random.random() < fractional_part:
                updates_this_frame += 1
            
            for _ in range(updates_this_frame):
                # Update DVD logo
                if dvd_logo:
                    dvd_logo.update()
                    # Check DVD collisions with entities (1 in 4 chance to kill)
                    entities = [e for e in entities if not dvd_logo.collides_with_entity(e)]
                
                # Update Thanos
                if thanos:
                    if thanos.update():  # Snap happened!
                        # Remove half of all entities
                        num_to_remove = len(entities) // 2
                        entities = random.sample(entities, len(entities) - num_to_remove)
                
                # Update entities
                for entity in entities:
                    entity.update()
                
                # Build spatial grid
                grid = {}
                for entity in entities:
                    key = (entity.grid_x, entity.grid_y)
                    if key not in grid:
                        grid[key] = []
                    grid[key].append(entity)
                
                # Check collisions using spatial partitioning
                to_remove = set()
                for cell_entities in grid.values():
                    for i in range(len(cell_entities)):
                        if cell_entities[i] in to_remove:
                            continue
                        for j in range(i + 1, len(cell_entities)):
                            if cell_entities[j] in to_remove:
                                continue
                            if cell_entities[i].collides_with(cell_entities[j]):
                                # Determine winner
                                if cell_entities[i].type != cell_entities[j].type:
                                    if check_winner(cell_entities[i].type, cell_entities[j].type):
                                        # j loses
                                        if settings['takeover_mode']:
                                            cell_entities[j].conversion_count += 1
                                            if cell_entities[j].conversion_count >= settings['conversions_to_death']:
                                                to_remove.add(cell_entities[j])
                                            else:
                                                cell_entities[j].type = cell_entities[i].type
                                        else:
                                            to_remove.add(cell_entities[j])
                                    else:
                                        # i loses
                                        if settings['takeover_mode']:
                                            cell_entities[i].conversion_count += 1
                                            if cell_entities[i].conversion_count >= settings['conversions_to_death']:
                                                to_remove.add(cell_entities[i])
                                            else:
                                                cell_entities[i].type = cell_entities[j].type
                                        else:
                                            to_remove.add(cell_entities[i])
                
                # Remove entities that have been converted 3 times
                entities = [e for e in entities if e not in to_remove]
        
        # Draw
        screen.fill(BG_COLOR)
        
        if game_over:
            # Victory animation
            victory_timer += 1
            animation_progress = min(1.0, victory_timer / victory_duration)
            
            # Draw victory animation (no background entities)
            draw_victory_animation(screen, winner, sprites, animation_progress)
        else:
            # Normal gameplay
            for entity in entities:
                entity.draw(screen)
            
            # Draw Thanos (behind everything)
            if thanos:
                thanos.draw(screen)
            
            # Draw DVD logo
            if dvd_logo:
                dvd_logo.draw(screen)
            
            # Count and display stats
            rock_count = sum(1 for e in entities if e.type == 'rock')
            paper_count = sum(1 for e in entities if e.type == 'paper')
            scissors_count = sum(1 for e in entities if e.type == 'scissors')
            total = len(entities)
            
            stats_text = font.render(f"Rock: {rock_count}  Paper: {paper_count}  Scissors: {scissors_count}  Total: {total}", True, (255, 255, 255))
            screen.blit(stats_text, (10, 10))
            
            # Draw speed slider
            speed_slider.draw(screen, "Speed:")
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return True  # Return to menu

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Rock Paper Scissors Simulation")
    
    # Create sprites
    sprites = {
        'rock': create_rock_sprite(),
        'paper': create_paper_sprite(),
        'scissors': create_scissors_sprite()
    }
    
    # Default settings
    settings = {
        'num_rocks': NUM_ROCKS,
        'num_papers': NUM_PAPERS,
        'num_scissors': NUM_SCISSORS,
        'takeover_mode': True,
        'conversions_to_death': 3,
        'dvd_logo': False,
        'thanos_mode': False
    }
    
    # Main loop - show menu, run simulation, repeat
    while True:
        choice = show_main_menu(screen, sprites)
        if choice is None:
            break
        elif choice == 'settings':
            settings = show_settings_menu(screen, sprites, settings)
            if settings is None:
                break
        elif choice == 'start':
            should_continue = run_simulation(screen, sprites, settings)
            if not should_continue:
                break
    
    pygame.quit()

if __name__ == "__main__":
    main()
