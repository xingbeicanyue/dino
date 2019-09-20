"""
主角恐龙
"""

import pygame
import baseFunc
from settings import settings
from state import appStates


class Dinosaur(pygame.sprite.Sprite):
    """ 主角恐龙 """

    screenDinoRate = 1 / 15  # 屏幕长->恐龙长的倍率（非俯冲状态）
    screenDashDinoRate = 11 / 120  # 屏幕长->恐龙长的倍率（俯冲状态）

    def __init__(self):
        """ 初始化 """
        self._state = 0  # 0:普通状态; 1:跳跃起步; 2:大跳; 3:小跳; 4.降落; 5.加速降落; 6:俯冲; 7:死亡
        self._lastScreenWidth = -1
        self._runningImgs = None  # [跑步图]
        self._dashingImgs = None  # [冲刺图]
        self._jumpingImg = None  # 跳跃图
        self._dyingImg = None  # 死亡图
        self._imgLeftRight = 0.1  # 屏幕宽度 -> 图片左侧坐标

    def _loadImage(self):
        """ 载入图片并根据屏幕窗口调整大小 """
        if (self._runningImgs is None) or (appStates.screen.get_width() != self._lastScreenWidth):
            self._lastScreenWidth = appStates.screen.get_width()

            runningImg = pygame.image.load('src/dinoRunning.png').convert()
            runningImg.set_colorkey(settings.defaultColorKey)
            self._runningImgs = baseFunc.divideSruface(runningImg, 1, 2)
            newImageWidth = round(self._lastScreenWidth * self.screenDinoRate)
            newImageHeight = round(self._runningImgs[0].get_height() * newImageWidth / self._runningImgs[0].get_width())
            for i in range(len(self._runningImgs)):
                self._runningImgs[i] = pygame.transform.scale(self._runningImgs[i], (newImageWidth, newImageHeight))

    def show(self):
        """ 绘制开始界面 """
        self._loadImage()
        appStates.screen.blit(self._runningImgs[pygame.time.get_ticks() // 100 % 2], self.getShowRect().topleft)

    def getShowRect(self) -> pygame.Rect:
        """ 获取图片显示矩形 """
        if self._state == 0:
            return pygame.Rect((settings.dinosaurLeft, settings.dinosaurTop), (128, 138))
