"""
场景元素
"""

import pygame
from settings import Settings


class Terrian(pygame.sprite.Sprite):
    """ 地形 """

    image = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Terrian._loadImage()
        self._game = game
        self.rect = pygame.Rect(Settings.terrianTopLeft, Terrian.image.get_size())

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Terrian.image:
            Terrian.image = pygame.image.load('src/terrian.png').convert()
            newImageWidth = round(Settings.initialWindowSize[0] * 2)
            newImageHeight = round(Terrian.image.get_height() * newImageWidth / Terrian.image.get_width())
            Terrian.image = pygame.transform.scale(Terrian.image, (newImageWidth, newImageHeight))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-self._game.curTerrianSpeed, 0)
        if self.rect.right < Settings.initialWindowSize[0]:
            self.rect = self.rect.move(Settings.initialWindowSize[0], 0)

    def draw(self, screen):
        """ 绘制 """
        screen.blit(Terrian.image, self.rect)


class Cloud(pygame.sprite.Sprite):
    """ 云 """

    image = None

    def __init__(self, game, topLeft):
        """ 初始化 """
        super().__init__()
        Cloud._loadImage()
        self._game = game
        self.rect = pygame.Rect(topLeft, self.image.get_size())

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Cloud.image:
            Cloud.image = pygame.image.load('src/cloud.png').convert()
            Cloud.image.set_colorkey(Settings.defaultColorKey)
            newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenCloudRate)
            newImageHeight = round(Cloud.image.get_height() * newImageWidth / Cloud.image.get_width())
            Cloud.image = pygame.transform.scale(Cloud.image, (newImageWidth, newImageHeight))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-Settings.cloudSpeed, 0)
