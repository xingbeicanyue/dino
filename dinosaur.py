"""
主角恐龙
"""

from enum import Enum
import pygame
import baseFunc
from settings import settings
from state import appStates


class DinosaurState(Enum):
    """ 恐龙状态 """
    run = 0  # 跑步
    dive = 1  # 俯冲
    startJump = 2  # 跳跃起步
    jump = 3  # 大跳
    littleJump = 4  # 小跳
    fall = 5  # 加速降落
    die = 6  # 死亡


class Dinosaur(pygame.sprite.Sprite):
    """ 主角恐龙 """

    screenDinoRate = 1 / 15  # 屏幕长->恐龙长的倍率（非俯冲状态）
    screenDivingDinoRate = 11 / 120  # 屏幕长->恐龙长的倍率（俯冲状态）
    jumpFrame = 30  # 大跳持续帧数
    littleJumpFrame = 20  # 小跳持续帧数
    fallSpeed = 25  # 加速降落速度
    jumpCommandFrame = 5  # 跳跃按键抬起接收帧数（区分大小跳）

    def __init__(self):
        """ 初始化 """
        super().__init__()
        self._state = DinosaurState.run
        self._addHeight = 0  # 高度
        self._jumpingFrame = 0  # 跳跃帧数（用于计算高度位移）
        self._downPressed, self._upPressed = False, False  # 俯冲|跳跃按键是否按下
        self._lastImgRect = None  # 上一帧图片范围
        self.__loadImage()

    def __inJumpingStates(self) -> bool:
        """ 判断是否处于跳跃状态（跳跃起步、大跳、小跳、加速降落） """
        return self._state in (DinosaurState.startJump, DinosaurState.jump,
                               DinosaurState.littleJump, DinosaurState.fall)

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
        if not self.__inJumpingStates():
            return
        if self._state in (DinosaurState.startJump, DinosaurState.jump):
            self._addHeight += (self.jumpFrame / 2 - self._jumpingFrame) * 1.7
        elif self._state == DinosaurState.littleJump:
            self._addHeight += (self.littleJumpFrame / 2 - self._jumpingFrame) * 1.7
        elif self._state == DinosaurState.fall:
            self._addHeight -= self.fallSpeed
        self._jumpingFrame += 1
        if self._addHeight <= 0:
            self._jumpingFrame = 0
            self._addHeight = 0
            if self._downPressed:
                self._state = DinosaurState.dive
            elif self._upPressed:
                self._state = DinosaurState.startJump
            else:
                self._state = DinosaurState.run

    def show(self):
        """ 绘制 """
        if self._lastImgRect:
            appStates.screen.fill(rect=self._lastImgRect, color=(255, 255, 255))

        self._lastImgRect = self.getShowRect()
        if self._state == DinosaurState.run:
            appStates.screen.blit(self._runningImgs[pygame.time.get_ticks() // 100 % 2], self._lastImgRect.topleft)
        elif self._state == DinosaurState.dive:
            appStates.screen.blit(self._divingImgs[pygame.time.get_ticks() // 100 % 2], self._lastImgRect.topleft)
        elif self.__inJumpingStates():
            appStates.screen.blit(self._jumpingImg, self._lastImgRect.topleft)

    def getShowRect(self) -> pygame.Rect:
        """ 获取图片显示矩形 """
        if self._state == DinosaurState.run:
            return pygame.Rect((settings.dinosaurLeft, settings.dinosaurBottom - self._runningImgs[0].get_height()),
                               self._runningImgs[0].get_size())
        elif self._state == DinosaurState.dive:
            return pygame.Rect((settings.dinosaurLeft, settings.dinosaurBottom - self._divingImgs[0].get_height()),
                               self._divingImgs[0].get_size())
        elif self.__inJumpingStates():
            return pygame.Rect((settings.dinosaurLeft, settings.dinosaurBottom - self._jumpingImg.get_height() -
                                self._addHeight), self._jumpingImg.get_size())

    def startDown(self):
        """ 开始俯冲按键 """
        self._downPressed = True
        if self._state == DinosaurState.run:
            self._state = DinosaurState.dive
        elif self.__inJumpingStates():
            self._state = DinosaurState.fall

    def endDown(self):
        """ 结束俯冲按键 """
        self._downPressed = False
        if self._state == DinosaurState.dive:
            self._state = DinosaurState.run
        elif self._state == DinosaurState.fall:
            self._state = DinosaurState.jump
            self._jumpingFrame = self.jumpFrame / 2

    def startUp(self):
        """ 开始跳跃按键 """
        self._upPressed = True
        if (not self._downPressed) and (self._state == DinosaurState.run):
            self._state = DinosaurState.startJump
            self._jumpingFrame = 0

    def endUp(self):
        """ 结束跳跃按键 """
        self._upPressed = False
        if self._state == DinosaurState.startJump:
            self._state = DinosaurState.littleJump if self._jumpingFrame < self.jumpCommandFrame else DinosaurState.jump
