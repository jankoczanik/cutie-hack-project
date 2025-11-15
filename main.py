import pygame
from game import Game

pygame.init()

mygame = Game()

while mygame.running:
    mygame.events()
    mygame.draw()
    mygame.tick()

pygame.quit()
