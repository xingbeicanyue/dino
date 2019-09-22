"""
地形
"""

import pygame
from settings import settings
from state import appStates


class Terrian(pygame.sprite.Sprite):
    """ 地形 """

    def __init__(self):
        """ 初始化 """
        self.__loadImage()
        self.rect = pygame.Rect(settings.terrianTopLeft, self.image.get_size())
        self.curSpeed = settings.terrianSpeed

    def __loadImage(self):
        """ 载入图片并根据屏幕窗口调整大小 """
        self.image = pygame.image.load('src/terrian.png').convert()
        newImageWidth = appStates.screen.get_width() * 2
        newImageHeight = round(self.image.get_height() * newImageWidth / self.image.get_width())
        self.image = pygame.transform.scale(self.image, (newImageWidth, newImageHeight))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-self.curSpeed, 0)
        if self.rect.right < appStates.screen.get_width():
            self.rect = self.rect.move(appStates.screen.get_width(), 0)

    def draw(self, screen):
        """ 绘制 """
        screen.blit(self.image, self.rect)
