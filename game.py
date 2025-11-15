import pygame
import json
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
        self.level = Level(self.screen_width // 2 - self.bounds // 2, self.screen_height // 2 - self.bounds // 2, self.bounds, self.bounds, self.levels[self.level_num])
        
        self.game_font = pygame.font.Font("assets/fonts/Firlest-Regular.otf", 48)

        self.bg_image = pygame.image.load("assets\images\dungeon-background.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        self.bg_rect = self.bg_image.get_rect()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.running = True
        self.active = True

        pygame.display.set_caption("The Looker")

    def draw(self):
        self.screen.fill("black")
        self.screen.blit(self.bg_image, self.bg_rect)
        self.level.draw(self.screen, self.game_font)
        pygame.display.flip()

    def tick(self):
        if (self.level.tick()):
            self.level_num += 1
            if self.level_num < len(self.levels):
                self.level = Level(self.screen_width // 2 - self.bounds // 2, self.screen_height // 2 - self.bounds // 2, self.bounds, self.bounds, self.levels[self.level_num])
            else:
                self.active = False


    def wait(self):
        self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False