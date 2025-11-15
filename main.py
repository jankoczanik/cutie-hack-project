import pygame
from game import Game

pygame.init()

mygame = Game()

while mygame.running:
    mygame.events()
    mygame.tick()
    if mygame.active:
        mygame.draw()
    mygame.wait()

pygame.quit()
