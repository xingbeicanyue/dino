"""
分数系统
"""

import pygame
from settings import Color, Settings


class Score:
    """ 分数系统 """

    def __init__(self):
        """ 初始化 """
        self._curScore = 0  # 当前分数
        self._highestScore = 0  # 历史最高分
        self._font = pygame.font.Font('src/courbd.ttf', 40)  # 显示分数的字体

    @property
    def curScore(self):
        """ 获取当前分数 """
        return self._curScore

    @property
    def highestScore(self):
        """ 获取历史最高分 """
        return self._highestScore

    def addScore(self, value: float):
        """ 增加分数 """
        self._curScore += value
        self._highestScore = max(self._highestScore, self._curScore)

    def setScore(self, value: float):
        """ 设置分数 """
        self._curScore = value
        self._highestScore = max(self._highestScore, self._curScore)

    def draw(self, screen):
        """ 显示分数 """
        scoreStr = f'HI {round(self._highestScore * Settings.scoreRate):05d} '\
            f'{round(self._curScore * Settings.scoreRate):05d} '
        scoreImage = self._font.render(scoreStr, True, Color.dimGray)
        topLeft = ((Settings.initialWindowSize[0] - scoreImage.get_width()), scoreImage.get_height())
        screen.blit(scoreImage, topLeft)
