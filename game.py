import pygame
import json
import time
from level import Level

class Game:
    def __init__(self):

        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.bounds = min(self.screen_width, self.screen_height) * 0.8

        with open("levels.json", "r") as f:
            self.levels = json.load(f)

        self.level_num = 0
        self.level = None
        
        self.game_font = pygame.font.Font("assets/fonts/Firlest-Regular.otf", 48)
        self.timer_font = pygame.font.Font("assets/fonts/JetBrainsMono-SemiBold.ttf", 48)
        self.menu_font = pygame.font.Font("assets/fonts/Firlest-Regular.otf", 72)
        self.button_font = pygame.font.Font("assets/fonts/Firlest-Regular.otf", 56)

        self.start_time = time.time()
        self.elapsed_time = 0.0
        self.final_time = 0.0

        self.bg_image = pygame.image.load("assets\images\dungeon-background.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        self.bg_rect = self.bg_image.get_rect()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.running = True
        self.active = False
        self.menu_active = True
        self.play_button_rect = None

        pygame.display.set_caption("Knight's Quest")

    def draw(self):
        self.screen.fill("black")
        self.screen.blit(self.bg_image, self.bg_rect)
        if self.menu_active:
            self.draw_menu()
        elif self.active:
            self.level.draw(self.screen, self.game_font)
            self.draw_timer()
        else:
            self.draw_completion_screen()
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw the main menu screen with a play button."""
        # Draw title
        title_text = self.menu_font.render("Knight's Quest", True, (255, 255, 255))
        title_rect = title_text.get_rect()
        title_rect.center = (self.screen_width // 2, self.screen_height // 2 - 150)
        
        # Draw semi-transparent background for title
        title_bg = pygame.Surface((title_rect.width + 40, title_rect.height + 20), pygame.SRCALPHA)
        title_bg.fill((0, 0, 0, 180))
        self.screen.blit(title_bg, (title_rect.x - 20, title_rect.y - 10))
        self.screen.blit(title_text, title_rect)
        
        # Draw play button
        button_text = self.button_font.render("Play", True, (255, 255, 255))
        button_rect = button_text.get_rect()
        button_rect.center = (self.screen_width // 2, self.screen_height // 2 + 50)
        
        # Button background
        button_bg_rect = pygame.Rect(button_rect.x - 30, button_rect.y - 15, 
                                    button_rect.width + 60, button_rect.height + 30)
        
        # Check if mouse is over button
        mouse_pos = pygame.mouse.get_pos()
        mouse_over = button_bg_rect.collidepoint(mouse_pos)
        
        # Draw button background with hover effect
        button_color = (100, 150, 200) if mouse_over else (80, 120, 160)
        pygame.draw.rect(self.screen, button_color, button_bg_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), button_bg_rect, width=3, border_radius=10)
        
        # Draw button text
        self.screen.blit(button_text, button_rect)
        
        # Store button rect for click detection
        self.play_button_rect = button_bg_rect
    
    def draw_timer(self):
        # Only update elapsed_time if game is still active
        if self.active:
            self.elapsed_time = time.time() - self.start_time
            time_to_display = self.elapsed_time
        else:
            # Game is complete - use final_time (which should be set when game completes)
            # If final_time is 0, use elapsed_time as fallback (shouldn't happen)
            time_to_display = self.final_time if self.final_time > 0 else self.elapsed_time
        
        time_str = self.format_time(time_to_display)
        
        # Render timer text
        timer_surface = self.timer_font.render(time_str, True, (255, 255, 255))
        timer_rect = timer_surface.get_rect()
        
        # Position at top right with 10 pixels padding from corner
        timer_rect.topright = (self.screen_width - 10, 10)
        
        # Draw semi-transparent background for better visibility
        # Background extends slightly left and down from text, but top-right stays at 10px margin
        bg_padding = 5
        bg_rect = pygame.Rect(timer_rect.left - bg_padding, timer_rect.top, 
                             timer_rect.width + bg_padding, timer_rect.height + bg_padding)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))
        self.screen.blit(bg_surface, bg_rect)
        
        # Draw timer text
        self.screen.blit(timer_surface, timer_rect)
    
    def format_time(self, time_seconds):
        """Format time as HH:MM:SS.mmm or MM:SS.mmm (LiveSplit style)"""
        hours = int(time_seconds // 3600)
        minutes = int((time_seconds % 3600) // 60)
        seconds = int(time_seconds % 60)
        milliseconds = int((time_seconds % 1) * 1000)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        else:
            return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    def draw_completion_screen(self):
        """Draw the final completion time in the center of the screen"""
        # Draw full-screen black background with 50% transparency
        black_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        black_surface.fill((0, 0, 0, 200))  # 128 = 50% of 255
        self.screen.blit(black_surface, (0, 0))
        
        # Format final time
        time_str = self.format_time(self.final_time)
        
        # Render completion text
        completion_font = pygame.font.Font("assets/fonts/Firlest-Regular.otf", 64)
        time_font = pygame.font.Font("assets/fonts/JetBrainsMono-SemiBold.ttf", 72)
        
        completion_text = completion_font.render("Final Time", True, (255, 255, 255))
        time_text = time_font.render(time_str, True, (0, 255, 0))
        
        completion_rect = completion_text.get_rect()
        time_rect = time_text.get_rect()
        
        # Center both texts vertically, with some spacing
        completion_rect.center = (self.screen_width // 2, self.screen_height // 2 - 60)
        time_rect.center = (self.screen_width // 2, self.screen_height // 2 + 40)
        
        # Draw text
        self.screen.blit(completion_text, completion_rect)
        self.screen.blit(time_text, time_rect)

    def start_game(self):
        """Start the game from the first level."""
        self.menu_active = False
        self.active = True
        self.level_num = 0
        self.start_time = time.time()
        self.elapsed_time = 0.0
        self.final_time = 0.0
        self.level = Level(self.screen_width // 2 - self.bounds // 2, 
                          self.screen_height // 2 - self.bounds // 2, 
                          self.bounds, self.bounds, self.levels[self.level_num])

    def tick(self):
        if self.menu_active or not self.active:
            return
        if (self.level.tick()):
            self.level_num += 1
            if self.level_num < len(self.levels):
                self.level = Level(self.screen_width // 2 - self.bounds // 2, self.screen_height // 2 - self.bounds // 2, self.bounds, self.bounds, self.levels[self.level_num])
            else:
                # Stop timer immediately when game is completed
                # Set active to False FIRST to prevent any further timer updates
                self.active = False
                self.final_time = time.time() - self.start_time
                self.elapsed_time = self.final_time


    def wait(self):
        self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.menu_active and self.play_button_rect:
                        if self.play_button_rect.collidepoint(event.pos):
                            self.start_game()