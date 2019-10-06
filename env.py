"""
场景元素
"""

import random
import pygame
import utils
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

    def update(self):
        """ 更新 """
        self.image = Terrian.imageNight if self._game.showNightImage() else Terrian.imageDay
        self.rect = self.rect.move(-self._game.curTerrianSpeed, 0)
        if self.rect.right < Settings.initialWindowSize[0]:
            self.rect = self.rect.move(Settings.initialWindowSize[0], 0)

    def draw(self, screen):
        """ 绘制 """
        screen.blit(self.image, self.rect)

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Terrian.imageDay:
            Terrian.imageDay = utils.loadImage(Settings.terrianPath, Settings.defaultColorKey,
                                               Settings.initialWindowSize[0] * 2)
            Terrian.imageNight = utils.invertSurface(Terrian.imageDay)


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

    def update(self):
        """ 更新 """
        self.image = Cloud.imageNight if self._game.showNightImage() else Cloud.imageDay
        self.rect = self.rect.move(-Settings.cloudSpeed, 0)

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Cloud.imageDay:
            Cloud.imageDay = utils.loadImage(Settings.cloudPath, Settings.defaultColorKey,
                                             Settings.initialWindowSize[0] * Settings.screenCloudRate)
            Cloud.imageNight = utils.invertSurface(Cloud.imageDay)


class Moon(pygame.sprite.Sprite):
    """ 月亮 """

    images = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Moon._loadImage()
        self._game = game
        self._imageIndex = 0  # 月相下标
        self.image = Moon.images[self._imageIndex]
        self.rect = pygame.Rect((Settings.initialWindowSize[0], Settings.moonTop), self.image.get_size())

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
        self._imageIndex = self._imageIndex + 1 if self._imageIndex < len(Moon.images) - 1 else 0
        self.image = Moon.images[self._imageIndex]

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Moon.images:
            Moon.images = utils.loadImages(Settings.moonPath, 1, 7, -1, Settings.defaultColorKey,
                                           Settings.initialWindowSize[0] * Settings.screenMoonRate)


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

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-Settings.starSpeed, 0)

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Star.images:
            Star.images = utils.loadImages(Settings.starPath, 1, 2, -1, Settings.defaultColorKey,
                                           Settings.initialWindowSize[0] * Settings.screenStarRate)
