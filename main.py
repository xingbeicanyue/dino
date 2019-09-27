import pygame
from settings import settings
from game import Game


pygame.init()
pygame.display.set_caption('dino')
game = Game(pygame.display.set_mode(settings.initialWindowSize))
clock = pygame.time.Clock()
while True:
    game.handleEvents()
    game.draw()
    clock.tick(settings.maxFPS)
