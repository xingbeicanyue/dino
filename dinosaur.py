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
    screenDivingDinoRate = 11 / 120  # 屏幕长->恐龙长的倍率（俯冲状态）

    def __init__(self):
        """ 初始化 """
        super().__init__()
        self._state = 0  # 0:普通状态; 1:俯冲; 2:跳跃起步; 3:大跳; 4:小跳; 5.降落; 6.加速降落; 7:死亡
        self._addHeight = 0  # 高度
        self._jumpingFrame = 0  # 跳跃帧数
        self.__loadImage()
        self._lastImgRect = None  # 上一帧图片范围

    def __loadImage(self):
        """ 载入图片并根据屏幕窗口调整大小 """
        # 跑步状态
        runningImg = pygame.image.load('src/dinoRunning.png').convert()
        runningImg.set_colorkey(settings.defaultColorKey)
        self._runningImgs = baseFunc.divideSruface(runningImg, 1, 2)
        newImageWidth = round(appStates.screen.get_width() * self.screenDinoRate)
        newImageHeight = round(self._runningImgs[0].get_height() * newImageWidth / self._runningImgs[0].get_width())
        for i in range(len(self._runningImgs)):
            self._runningImgs[i] = pygame.transform.scale(self._runningImgs[i], (newImageWidth, newImageHeight))

        # 俯冲状态
        divingImg = pygame.image.load('src/dinoDiving.png').convert()
        divingImg.set_colorkey(settings.defaultColorKey)
        self._divingImgs = baseFunc.divideSruface(divingImg, 1, 2)
        newImageWidth = round(appStates.screen.get_width() * self.screenDivingDinoRate)
        newImageHeight = round(self._divingImgs[0].get_height() * newImageWidth / self._divingImgs[0].get_width())
        for i in range(len(self._divingImgs)):
            self._divingImgs[i] = pygame.transform.scale(self._divingImgs[i], (newImageWidth, newImageHeight))

        # 跳跃状态
        self._jumpingImg = pygame.image.load('src/dinoJumping.png').convert()
        self._jumpingImg.set_colorkey(settings.defaultColorKey)
        newImageWidth = round(appStates.screen.get_width() * self.screenDinoRate)
        newImageHeight = round(self._jumpingImg.get_height() * newImageWidth / self._jumpingImg.get_width())
        self._jumpingImg = pygame.transform.scale(self._jumpingImg, (newImageWidth, newImageHeight))

    def updateState(self):
        """ 更新位置及状态 """
        if self._state == 2:
            self._addHeight += (15 - self._jumpingFrame) * 1.7
            self._jumpingFrame += 1
            if self._addHeight <= 0:
                self._state = 0
                self._jumpingFrame = 0
                self._addHeight = 0

    def show(self):
        """ 绘制 """
        if self._lastImgRect:
            appStates.screen.fill(rect=self._lastImgRect, color=(255, 255, 255))

        self._lastImgRect = self.getShowRect()
        if self._state == 0:
            appStates.screen.blit(self._runningImgs[pygame.time.get_ticks() // 100 % 2], self._lastImgRect.topleft)
        elif self._state == 1:
            appStates.screen.blit(self._divingImgs[pygame.time.get_ticks() // 100 % 2], self._lastImgRect.topleft)
        elif self._state == 2:
            appStates.screen.blit(self._jumpingImg, self._lastImgRect.topleft)

    def getShowRect(self) -> pygame.Rect:
        """ 获取图片显示矩形 """
        if self._state == 0:
            return pygame.Rect((settings.dinosaurLeft, settings.dinosaurBottom - self._runningImgs[0].get_height()),
                               self._runningImgs[0].get_size())
        elif self._state == 1:
            return pygame.Rect((settings.dinosaurLeft, settings.dinosaurBottom - self._divingImgs[0].get_height()),
                               self._divingImgs[0].get_size())
        elif self._state == 2:
            return pygame.Rect((settings.dinosaurLeft, settings.dinosaurBottom - self._jumpingImg.get_height() -
                                self._addHeight), self._jumpingImg.get_size())

    def startDown(self):
        """ 开始俯冲按键 """
        if self._state == 0:
            self._state = 1

    def endDown(self):
        """ 结束俯冲按键 """
        if self._state == 1:
            self._state = 0

    def startUp(self):
        """ 开始跳跃按键 """
        if self._state == 0:
            self._state = 2
            self._jumpingFrame = 0

    def endUp(self):
        """ 结束跳跃按键 """
        pass
