"""
敌方
"""

import random
import numpy
import pygame
import utils
from settings import Settings


class Cactus(pygame.sprite.Sprite):
    """ 仙人掌 """

    surfArrays = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Cactus._loadImage()
        self._game = game
        self._isLarge = random.randint(0, 1) == 1  # 是否大仙人掌
        self._num = random.randint(1, 3 if self._game.curShowScore < Settings.maxCactusScore else 4)  # 仙人掌数
        self._initCactus()
        self.image = self._imageDay
        self.rect = pygame.Rect((Settings.initialWindowSize[0], Settings.cactusBottom - self.image.get_height()),
                                self.image.get_size())

    def update(self):
        """ 更新 """
        self.image = self._imageNight if self._game.showNightImage() else self._imageDay
        self.rect = self.rect.move(-self._game.curTerrianSpeed, 0)

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Cactus.surfArrays:
            images = utils.loadImages(Settings.cactusPath, 1, 3, -1, None,
                                      Settings.initialWindowSize[0] * Settings.screenCactusRate)
            Cactus.surfArrays = [pygame.surfarray.array3d(image) for image in images]

    def _initCactus(self):
        """ 初始化自身仙人掌组信息 """
        imageArray = numpy.zeros((len(Cactus.surfArrays[0]) * self._num, len(Cactus.surfArrays[0][0]), 3))
        for i in range(self._num):
            imageArray[len(Cactus.surfArrays[0])*i:len(Cactus.surfArrays[0])*(i+1), :] =\
                Cactus.surfArrays[random.randint(0, 2)]
        self._imageDay = pygame.surfarray.make_surface(imageArray)
        self._imageDay.set_colorkey(Settings.defaultColorKey)
        if not self._isLarge:
            self._imageDay = pygame.transform.scale(self._imageDay,
                                                    (round(self._imageDay.get_width() * Settings.smallCactusRate),
                                                     round(self._imageDay.get_height() * Settings.smallCactusRate)))
        self._imageNight = utils.invertSurface(self._imageDay)


class Bird(pygame.sprite.Sprite):
    """ 鸟 """

    imageDays = None
    imageNights = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Bird._loadImage()
        self._game = game
        self.image = Bird.imageDays[0]
        self.rect = pygame.Rect((Settings.initialWindowSize[0], Settings.birdTops[random.randint(0, 2)]),
                                Bird.imageDays[0].get_size())

    def update(self):
        imgIndex = pygame.time.get_ticks() // 200 % 2
        self.image = Bird.imageNights[imgIndex] if self._game.showNightImage() else Bird.imageDays[imgIndex]
        self.rect = self.rect.move(-self._game.curTerrianSpeed, 0)

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Bird.imageDays:
            Bird.imageDays = utils.loadImages(Settings.birdPath, 1, 2, -1, Settings.defaultColorKey,
                                              Settings.initialWindowSize[0] * Settings.screenBirdRate)
            Bird.imageNights = utils.invertSurfaces(Bird.imageDays)
