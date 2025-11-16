import pygame
from game import Game

pygame.init()
# Initialize mixer with better settings for audio playback
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Mixer initialized successfully")
except pygame.error as e:
    print(f"Mixer initialization error: {e}")
    pygame.mixer.init()  # Fallback to default initialization

mygame = Game()

while mygame.running:
    mygame.events()
    mygame.tick()
    mygame.draw()
    mygame.wait()

pygame.quit()
