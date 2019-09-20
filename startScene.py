"""
开始界面
"""

import pygame
from settings import settings
from state import appStates


class StartScene:
    """ 开始界面 """

    def __init__(self):
        """ 初始化 """
        self._lastScreenWidth = -1
        self._coverImage = None
        self.__coverImage2 = None

    def __loadCoverImage(self):
        """ 载入封面图并根据屏幕窗口调整大小 """
        # 封面图由两张图组成，尺寸相同，coverImage2为闭眼状态
        if (self._coverImage is None) or (appStates.screen.get_width() != self._lastScreenWidth):
            self._coverImage = pygame.image.load('src/coverImage.png').convert()
            self._coverImage.set_colorkey(settings.defaultColorKey)
            self._coverImage2 = pygame.image.load('src/coverImage2.png').convert()
            self._coverImage2.set_colorkey(settings.defaultColorKey)

            self._lastScreenWidth = appStates.screen.get_width()
            newImageWidth = round(self._lastScreenWidth / 15)
            newImageHeight = round(self._coverImage.get_height() * newImageWidth / self._coverImage.get_width())
            self._coverImage = pygame.transform.scale(self._coverImage, (newImageWidth, newImageHeight))
            self._coverImage2 = pygame.transform.scale(self._coverImage2, (newImageWidth, newImageHeight))

    def show(self):
        """ 绘制开始界面 """
        self.__loadCoverImage()
        appStates.screen.fill((255, 255, 255))
        left = round((appStates.screen.get_width() - self._coverImage.get_width()) / 2)
        top = round((appStates.screen.get_height() - self._coverImage.get_height()) / 2)
        if 0 <= pygame.time.get_ticks() % 5000 <= 100:
            appStates.screen.blit(self._coverImage2, (left, top))
        else:
            appStates.screen.blit(self._coverImage, (left, top))
