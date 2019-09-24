import pygame
from settings import settings
from state import appStates
from game import Game


pygame.init()
pygame.display.set_caption('dino')

appStates.screen = pygame.display.set_mode(settings.initialWindowSize)
game = Game()

clock = pygame.time.Clock()
while True:
    game.handleEvents()
    game.draw()
    clock.tick(settings.maxFPS)
