"""
开始界面
"""

import pygame
import baseFunc
from settings import Settings


class StartScene:
    """ 开始界面 """

    def __init__(self):
        """ 初始化 """
        # 封面图由两张图组成，尺寸相同，coverImage2为闭眼状态
        coverImage = pygame.image.load('src/coverImage.png').convert()
        coverImage.set_colorkey(Settings.defaultColorKey)
        self._coverImages = baseFunc.divideSruface(coverImage, 1, 2)

    def draw(self, screen):
        """ 绘制 """
        screen.fill((255, 255, 255))
        left = round((Settings.initialWindowSize[0] - self._coverImages[0].get_width()) / 2)
        top = round((Settings.initialWindowSize[1] - self._coverImages[0].get_height()) / 2)
        if 0 <= pygame.time.get_ticks() % 5000 <= 100:
            screen.blit(self._coverImages[1], (left, top))
        else:
            screen.blit(self._coverImages[0], (left, top))
