import sys
import pygame
from settings import settings
from state import appStates
from startScene import StartScene


pygame.init()
pygame.display.set_caption('dino')

appStates.screen = pygame.display.set_mode(settings.initialWindowSize, flags=pygame.RESIZABLE)
startScene = StartScene()

while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()
        if event.type in (pygame.VIDEORESIZE,):
            appStates.screen = pygame.display.set_mode((event.w, event.h), flags=pygame.RESIZABLE)

    startScene.show()
    pygame.display.update()
