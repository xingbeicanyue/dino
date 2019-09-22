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

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if appStates.gameState == 0:
                    appStates.gameState = 1
                    appStates.screen.fill((255, 255, 255))
                elif appStates.gameState == 1:
                    dinosaur.startUp()
            elif event.key == pygame.K_DOWN:
                if appStates.gameState == 1:
                    dinosaur.startDown()
            elif event.key == pygame.K_UP:
                if appStates.gameState == 1:
                    dinosaur.startUp()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                if appStates.gameState == 1:
                    dinosaur.endDown()
            elif event.key in (pygame.K_SPACE, pygame.K_UP):
                if appStates.gameState == 1:
                    dinosaur.endUp()

    if appStates.gameState == 0:
        startScene.show()
    elif appStates.gameState == 1:
        dinosaur.updateState()
        dinosaur.show()
    pygame.display.update()
    clock.tick(settings.maxFPS)
