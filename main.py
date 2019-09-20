import sys
import pygame
from settings import settings
from state import appStates
from startScene import StartScene
from dinosaur import Dinosaur


pygame.init()
pygame.display.set_caption('dino')

appStates.screen = pygame.display.set_mode(settings.initialWindowSize)
startScene = StartScene()
dinosaur = Dinosaur()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if appStates.gameState == 0:
                    appStates.gameState = 1
                    appStates.screen.fill((255, 255, 255))

    if appStates.gameState == 0:
        startScene.show()
    if appStates.gameState == 1:
        appStates.screen.fill(rect=dinosaur.getShowRect(), color=(255, 255, 255))
        dinosaur.show()
    pygame.display.update()
