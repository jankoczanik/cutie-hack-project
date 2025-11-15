import pygame

class Game:
    def __init__(self):
        info = pygame.display.Info()

        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.display.set_caption("The Looker")

    def draw(self):
        self.screen.fill("black")
        pygame.display.flip()

    def tick(self):
        self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False