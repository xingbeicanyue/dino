"""
场景元素
"""

import random
import pygame
import baseFunc
from settings import Settings


class Terrian(pygame.sprite.Sprite):
    """ 地形 """

    imageDay = None
    imageNight = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Terrian._loadImage()
        self._game = game
        self.image = Terrian.imageDay
        self.rect = pygame.Rect(Settings.terrianTopLeft, Terrian.imageDay.get_size())

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Terrian.imageDay:
            Terrian.imageDay = pygame.image.load('src/image/terrian.png').convert()
            Terrian.imageDay.set_colorkey(Settings.defaultColorKey)
            newImageWidth = round(Settings.initialWindowSize[0] * 2)
            newImageHeight = round(Terrian.imageDay.get_height() * newImageWidth / Terrian.imageDay.get_width())
            Terrian.imageDay = pygame.transform.scale(Terrian.imageDay, (newImageWidth, newImageHeight))
            Terrian.imageNight = baseFunc.invertSurface(Terrian.imageDay)

    def update(self):
        """ 更新 """
        if self._game.showNightImage():
            self.image = Terrian.imageNight
        else:
            self.image = Terrian.imageDay
        self.rect = self.rect.move(-self._game.curTerrianSpeed, 0)
        if self.rect.right < Settings.initialWindowSize[0]:
            self.rect = self.rect.move(Settings.initialWindowSize[0], 0)

    def draw(self, screen):
        """ 绘制 """
        screen.blit(self.image, self.rect)


class Cloud(pygame.sprite.Sprite):
    """ 云 """

    imageDay = None
    imageNight = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Cloud._loadImage()
        self._game = game
        self.image = Cloud.imageDay
        self.rect = pygame.Rect((Settings.initialWindowSize[0],
                                 random.randint(Settings.cloudMaxTop, Settings.cloudMinTop)), self.image.get_size())

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Cloud.imageDay:
            Cloud.imageDay = pygame.image.load('src/image/cloud.png').convert()
            Cloud.imageDay.set_colorkey(Settings.defaultColorKey)
            newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenCloudRate)
            newImageHeight = round(Cloud.imageDay.get_height() * newImageWidth / Cloud.imageDay.get_width())
            Cloud.imageDay = pygame.transform.scale(Cloud.imageDay, (newImageWidth, newImageHeight))
            Cloud.imageNight = baseFunc.invertSurface(Cloud.imageDay)

    def update(self):
        """ 更新 """
        if self._game.showNightImage():
            self.image = Cloud.imageNight
        else:
            self.image = Cloud.imageDay
        self.rect = self.rect.move(-Settings.cloudSpeed, 0)


class Moon(pygame.sprite.Sprite):
    """ 月亮 """

    images = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Moon._loadImage()
        self._game = game
        self._imageIndex = 0
        self.image = Moon.images[self._imageIndex]
        self.rect = pygame.Rect((Settings.initialWindowSize[0], Settings.moonTop), self.image.get_size())

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Moon.images:
            image = pygame.image.load('src/image/moon.png').convert()
            image.set_colorkey(Settings.defaultColorKey)
            Moon.images = baseFunc.divideSurface(image, 1, 7)
            for i in range(len(Moon.images)):
                newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenMoonRate)
                newImageHeight = round(Moon.images[i].get_height() * newImageWidth / Moon.images[i].get_width())
                Moon.images[i] = pygame.transform.scale(Moon.images[i], (newImageWidth, newImageHeight))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-Settings.moonSpeed, 0)
        if self.rect.right <= 0:
            self.rect = pygame.Rect((Settings.initialWindowSize[0], Settings.moonTop), self.image.get_size())

    def draw(self, screen):
        """ 绘制 """
        screen.blit(self.image, self.rect)

    def nextPhase(self):
        """ 变换成下一个月相 """
        self._imageIndex = self._imageIndex + 1 if self._imageIndex <= 5 else 0
        self.image = Moon.images[self._imageIndex]


class Star(pygame.sprite.Sprite):
    """ 星星 """

    images = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Star._loadImage()
        self._game = game
        self.image = Star.images[random.randint(0, 1)]
        self.rect = pygame.Rect((Settings.initialWindowSize[0],
                                 random.randint(Settings.starMaxTop, Settings.starMinTop)), self.image.get_size())

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Star.images:
            image = pygame.image.load('src/image/star.png').convert()
            image.set_colorkey(Settings.defaultColorKey)
            Star.images = baseFunc.divideSurface(image, 1, 2)
            for i in range(len(Star.images)):
                newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenStarRate)
                newImageHeight = round(Star.images[i].get_height() * newImageWidth / Star.images[i].get_width())
                Star.images[i] = pygame.transform.scale(Star.images[i], (newImageWidth, newImageHeight))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-Settings.starSpeed, 0)
