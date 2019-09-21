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
        # 封面图由两张图组成，尺寸相同，coverImage2为闭眼状态
        self._coverImage = pygame.image.load('src/coverImage.png').convert()
        self._coverImage.set_colorkey(settings.defaultColorKey)
        self._coverImage2 = pygame.image.load('src/coverImage2.png').convert()
        self._coverImage2.set_colorkey(settings.defaultColorKey)

    def show(self):
        """ 绘制 """
        appStates.screen.fill((255, 255, 255))
        left = round((appStates.screen.get_width() - self._coverImage.get_width()) / 2)
        top = round((appStates.screen.get_height() - self._coverImage.get_height()) / 2)
        if 0 <= pygame.time.get_ticks() % 5000 <= 100:
            appStates.screen.blit(self._coverImage2, (left, top))
        else:
            appStates.screen.blit(self._coverImage, (left, top))
