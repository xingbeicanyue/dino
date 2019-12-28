import pygame
from settings import Settings
from game import Game


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
game = Game(pygame.display.set_mode(Settings.initialWindowSize))

pygame.display.set_caption(Settings.caption)
pygame.display.set_icon(pygame.image.load(Settings.mainWindowIconPath))

clock = pygame.time.Clock()
while True:
    game.handleEvents()
    game.updateAndDraw()
    clock.tick(Settings.maxFPS)
