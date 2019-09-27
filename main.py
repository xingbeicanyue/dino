import pygame
from settings import Settings
from game import Game


pygame.init()
pygame.display.set_caption('dino')
game = Game(pygame.display.set_mode(Settings.initialWindowSize))
clock = pygame.time.Clock()
while True:
    game.handleEvents()
    game.draw()
    clock.tick(Settings.maxFPS)
