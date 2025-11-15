import pygame
import math

class Player:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

        self.image = pygame.image.load(r"assets/images/knight.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def moveTowards(self, x, y, left, top, right, bottom):
        distance = math.sqrt(math.pow(self.x - x, 2) + math.pow(self.y - y, 2))
        if distance < self.speed:
            return
        self.x += self.speed * (x - self.x) / distance
        self.x = min(max(left, self.x), right)
        self.y += self.speed * (y - self.y) / distance
        self.y = min(max(top, self.y), bottom)

    def touchingExit(self, exit):
        return abs(self.x - exit.x) < self.size and abs(self.y - exit.y) < self.size

class Exit:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.image = pygame.image.load(r"assets/images/doorway.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)