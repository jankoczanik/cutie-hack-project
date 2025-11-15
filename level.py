import pygame
from entity import Player, Exit

class Level:

    def __init__(self, x, y, width, height, config):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = config['size']
        self.name = config['name']
        self.player = Player(x + width * config['spawn'][0], y + height * config['spawn'][1], self.size, self.size / 10)
        self.exit = Exit(x + width * config['exit'][0], y + height * config['exit'][1], self.size)

    def draw(self, screen, font):
        temp_surface = pygame.Surface(
            (self.width + self.size, self.height + self.size), pygame.SRCALPHA
        )
        pygame.draw.rect(
            temp_surface,
            (255, 255, 255, 200),
            (0, 0, self.width + self.size, self.height + self.size)
        )
        screen.blit(temp_surface, (self.x - self.size / 2, self.y - self.size / 2))
        self.exit.draw(screen)
        self.player.draw(screen)
        text_surface = font.render(self.name, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))


    def tick(self):
        x, y = pygame.mouse.get_pos()
        self.player.moveTowards(x, y, self.x, self.y, self.x + self.width, self.y + self.height)
        return self.player.touchingExit(self.exit)