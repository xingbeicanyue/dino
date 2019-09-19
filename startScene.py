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
        self._coverImage = pygame.image.load('src/coverImage.png').convert()
        self._coverImage.set_colorkey((255, 255, 255))
        self.__scaleCoverImage()

    def __scaleCoverImage(self):
        """ 根据屏幕窗口大小更新封面图大小 """
        if appStates.screen.get_width() != self._lastScreenWidth:
            self._lastScreenWidth = appStates.screen.get_width()
            newImageWidth = round(self._lastScreenWidth * settings.screenDinoRate)
            newImageHeight = round(self._coverImage.get_height() * newImageWidth / self._coverImage.get_width())
            self._coverImage = pygame.transform.scale(self._coverImage, (newImageWidth, newImageHeight))

    def show(self):
        """ 绘制开始界面 """
        self.__scaleCoverImage()
        appStates.screen.fill((255, 255, 255))
        left = round((appStates.screen.get_width() - self._coverImage.get_width()) / 2)
        top = round((appStates.screen.get_height() - self._coverImage.get_height()) / 2)
        appStates.screen.blit(self._coverImage, (left, top))
