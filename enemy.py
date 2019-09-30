"""
敌方
"""

import random
import numpy
import pygame
import baseFunc
from settings import Settings


class Cactus(pygame.sprite.Sprite):
    """ 仙人掌 """

    surfArrays = None

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        Cactus._loadImage()
        self._game = game
        self.isLarge = random.randint(0, 1) == 1  # 是否大仙人掌
        self.num = random.randint(1, 4)  # 仙人掌数
        self._initCactus()
        self.image = self._imageDay
        self.rect = pygame.Rect((Settings.initialWindowSize[0], Settings.cactusBottom - self.image.get_height()),
                                self.image.get_size())

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Cactus.surfArrays:
            image = pygame.image.load('src/image/cactus.png').convert()
            images = baseFunc.divideSurface(image, 1, 3)
            for i in range(len(images)):
                newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenCactusRate)
                newImageHeight = round(images[i].get_height() * newImageWidth / images[i].get_width())
                images[i] = pygame.transform.scale(images[i], (newImageWidth, newImageHeight))
            Cactus.surfArrays = []
            for image in images:
                Cactus.surfArrays.append(pygame.surfarray.array3d(image))

    def _initCactus(self):
        """ 初始化自身仙人掌组信息 """
        imageArray = numpy.zeros((len(Cactus.surfArrays[0]) * self.num, len(Cactus.surfArrays[0][0]), 3))
        for i in range(self.num):
            imageArray[len(Cactus.surfArrays[0])*i:len(Cactus.surfArrays[0])*(i+1), :] =\
                Cactus.surfArrays[random.randint(0, 2)]
        self._imageDay = pygame.surfarray.make_surface(imageArray)
        self._imageDay.set_colorkey(Settings.defaultColorKey)
        if not self.isLarge:
            self._imageDay = pygame.transform.scale(self._imageDay,
                                                    (round(self._imageDay.get_width() * Settings.smallCactusRate),
                                                     round(self._imageDay.get_height() * Settings.smallCactusRate)))
        self._imageNight = baseFunc.invertSurface(self._imageDay)

    def update(self):
        """ 更新 """
        if self._game.showNightImage():
            self.image = self._imageNight
        else:
            self.image = self._imageDay
        self.rect = self.rect.move(-self._game.curTerrianSpeed, 0)


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

    @staticmethod
    def _loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Bird.imageDays:
            image = pygame.image.load('src/image/bird.png').convert()
            image.set_colorkey(Settings.defaultColorKey)
            Bird.imageDays = baseFunc.divideSurface(image, 1, 2)
            for i in range(len(Bird.imageDays)):
                newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenBirdRate)
                newImageHeight = round(Bird.imageDays[i].get_height() * newImageWidth / Bird.imageDays[i].get_width())
                Bird.imageDays[i] = pygame.transform.scale(Bird.imageDays[i], (newImageWidth, newImageHeight))
            Bird.imageNights = baseFunc.invertSurfaces(Bird.imageDays)

    def update(self):
        if self._game.showNightImage():
            self.image = Bird.imageNights[pygame.time.get_ticks() // 200 % 2]
        else:
            self.image = Bird.imageDays[pygame.time.get_ticks() // 200 % 2]
        self.rect = self.rect.move(-self._game.curTerrianSpeed, 0)
