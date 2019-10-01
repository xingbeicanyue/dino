"""
游戏结束场景
"""

import pygame
import utils
from utils import Color
from settings import Settings


class GameoverScene:
    """ 游戏结束场景 """

    def __init__(self, game):
        """ 初始化 """
        self._game = game
        self._loadImage()

    def _loadImage(self):
        """ 载入图片并根据屏幕窗口调整大小 """
        self._restartImageDay = utils.loadImage('src/image/restart.png', Settings.defaultColorKey,
                                                Settings.initialWindowSize[0] * Settings.screenRestartImageRate)
        self._restartImageNight = utils.invertSurface(self._restartImageDay)

    def draw(self, screen):
        """ 绘制 """
        topLeft = ((Settings.initialWindowSize[0] - self._restartImageDay.get_width()) / 2,
                   (Settings.initialWindowSize[1] - self._restartImageDay.get_height()) / 2)
        screen.blit(self._restartImageNight if self._game.showNightImage() else self._restartImageDay, topLeft)

        color = Color.invert(Color.dimGray) if self._game.showNightImage() else Color.dimGray
        gameoverImage = pygame.font.Font('src/font/courbd.ttf', 48).render('G A M E    O V E R', True, color)
        topLeft = ((Settings.initialWindowSize[0] - gameoverImage.get_width()) / 2,
                   topLeft[1] - gameoverImage.get_height() * 2)
        screen.blit(gameoverImage, topLeft)
