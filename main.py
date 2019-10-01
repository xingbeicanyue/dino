import pygame
from settings import Settings
from game import Game


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

pygame.display.set_caption('dino')
iconImage = pygame.image.load('src/image/dinoJumping.png')
iconImage.set_colorkey(Settings.defaultColorKey)
pygame.display.set_icon(iconImage)

game = Game(pygame.display.set_mode(Settings.initialWindowSize))
clock = pygame.time.Clock()
while True:
    game.handleEvents()
    game.updateAndDraw()
    clock.tick(Settings.maxFPS)
