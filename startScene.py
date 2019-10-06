"""
开始界面
"""

import pygame
import utils
from settings import Settings


class StartScene:
    """ 开始界面 """

    def __init__(self):
        """ 初始化 """
        self._coverImages = utils.loadImages(Settings.coverImagePath, 1, 2)
        self._textImage = utils.loadImage(Settings.coverTextPath)

    def draw(self, screen):
        """ 绘制 """
        screen.fill(utils.Color.white)
        totalWidth = self._textImage.get_width()
        totalHeight = self._coverImages[0].get_height() * 2 + self._textImage.get_height()
        left = round((Settings.initialWindowSize[0] - totalWidth) / 2)
        top = round((Settings.initialWindowSize[1] - totalHeight) / 2)
        screen.blit(self._coverImages[0 <= pygame.time.get_ticks() % 5000 <= 100], (left, top))
        top += self._coverImages[0].get_height() * 2
        screen.blit(self._textImage, (left, top))
