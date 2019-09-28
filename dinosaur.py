"""
恐龙
"""

import enum
import pygame
import baseFunc
from settings import Settings


class DinosaurState(enum.Enum):
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

    def __init__(self, game):
        """ 初始化 """
        super().__init__()
        self._loadImage()
        self._game = game
        self._state = DinosaurState.run
        self._addHeight = 0  # 高度
        self._jumpingFrame = 0  # 跳跃帧数（用于计算高度位移）
        self._downPressed, self._upPressed = False, False  # 俯冲|跳跃按键是否按下
        self.image = self._runningImgs[0]
        self.rect = self.getShowRect()

    def _inJumpingStates(self) -> bool:
        """ 判断是否处于跳跃状态（跳跃起步、大跳、小跳、加速降落） """
        return self._state in (DinosaurState.startJump, DinosaurState.jump,
                               DinosaurState.littleJump, DinosaurState.fall)

    def _loadImage(self):
        """ 载入图片并根据屏幕窗口调整大小 """
        # 跑步状态
        runningImg = pygame.image.load('src/dinoRunning.png').convert()
        runningImg.set_colorkey(Settings.defaultColorKey)
        self._runningImgs = baseFunc.divideSruface(runningImg, 1, 2)
        newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenDinoRate)
        newImageHeight = round(self._runningImgs[0].get_height() * newImageWidth / self._runningImgs[0].get_width())
        for i in range(len(self._runningImgs)):
            self._runningImgs[i] = pygame.transform.scale(self._runningImgs[i], (newImageWidth, newImageHeight))

        # 俯冲状态
        divingImg = pygame.image.load('src/dinoDiving.png').convert()
        divingImg.set_colorkey(Settings.defaultColorKey)
        self._divingImgs = baseFunc.divideSruface(divingImg, 1, 2)
        newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenDivingDinoRate)
        newImageHeight = round(self._divingImgs[0].get_height() * newImageWidth / self._divingImgs[0].get_width())
        for i in range(len(self._divingImgs)):
            self._divingImgs[i] = pygame.transform.scale(self._divingImgs[i], (newImageWidth, newImageHeight))

        # 跳跃状态
        self._jumpingImg = pygame.image.load('src/dinoJumping.png').convert()
        self._jumpingImg.set_colorkey(Settings.defaultColorKey)
        newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenDinoRate)
        newImageHeight = round(self._jumpingImg.get_height() * newImageWidth / self._jumpingImg.get_width())
        self._jumpingImg = pygame.transform.scale(self._jumpingImg, (newImageWidth, newImageHeight))

        # 死亡状态
        self._dyingImg = pygame.image.load('src/dinoDying.png').convert()
        self._dyingImg.set_colorkey(Settings.defaultColorKey)
        newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenDinoRate)
        newImageHeight = round(self._dyingImg.get_height() * newImageWidth / self._dyingImg.get_width())
        self._dyingImg = pygame.transform.scale(self._dyingImg, (newImageWidth, newImageHeight))

    def update(self):
        """ 更新位置、状态及图片 """
        if self._inJumpingStates():
            if self._state in (DinosaurState.startJump, DinosaurState.jump):
                self._addHeight += (Settings.jumpFrame / 2 - self._jumpingFrame) * Settings.frameSpeedRate
            elif self._state == DinosaurState.littleJump:
                self._addHeight += (Settings.littleJumpFrame / 2 - self._jumpingFrame) * Settings.frameSpeedRate
            elif self._state == DinosaurState.fall:
                self._addHeight -= Settings.fallSpeed
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
        self.image = self.getShowImage()
        self.rect = self.getShowRect()

    def draw(self, surface):
        """ 绘制 """
        if self._state == DinosaurState.run:
            surface.blit(self.getShowImage(), self.getShowRect().topleft)
        elif self._state == DinosaurState.dive:
            surface.blit(self.getShowImage(), self.getShowRect().topleft)
        elif self._inJumpingStates():
            surface.blit(self.getShowImage(), self.getShowRect().topleft)
        else:
            surface.blit(self.getShowImage(), self.getShowRect().topleft)

    def getShowImage(self) -> pygame.Surface:
        """ 获取显示的图片 """
        if self._state == DinosaurState.run:
            return self._runningImgs[pygame.time.get_ticks() // 100 % 2]
        elif self._state == DinosaurState.dive:
            return self._divingImgs[pygame.time.get_ticks() // 100 % 2]
        elif self._inJumpingStates():
            return self._jumpingImg
        else:
            return self._dyingImg

    def getShowRect(self) -> pygame.Rect:
        """ 获取图片显示矩形 """
        if self._state == DinosaurState.run:
            return pygame.Rect((Settings.dinosaurLeft, Settings.dinosaurBottom - self._runningImgs[0].get_height()),
                               self._runningImgs[0].get_size())
        elif self._state == DinosaurState.dive:
            return pygame.Rect((Settings.dinosaurLeft, Settings.dinosaurBottom - self._divingImgs[0].get_height()),
                               self._divingImgs[0].get_size())
        elif self._inJumpingStates():
            return pygame.Rect((Settings.dinosaurLeft, Settings.dinosaurBottom - self._jumpingImg.get_height() -
                               self._addHeight), self._jumpingImg.get_size())
        else:
            return pygame.Rect((Settings.dinosaurLeft, Settings.dinosaurBottom - self._dyingImg.get_height() -
                               self._addHeight), self._dyingImg.get_size())

    def startDown(self):
        """ 开始俯冲按键 """
        self._downPressed = True
        if self._state == DinosaurState.run:
            self._state = DinosaurState.dive
        elif self._inJumpingStates():
            self._state = DinosaurState.fall

    def endDown(self):
        """ 结束俯冲按键 """
        self._downPressed = False
        if self._state == DinosaurState.dive:
            self._state = DinosaurState.run

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
            self._state = DinosaurState.littleJump if self._jumpingFrame < Settings.jumpCommandFrame\
                else DinosaurState.jump

    def die(self):
        """ 进入死亡状态 """
        self._state = DinosaurState.die

    def restart(self):
        """ 重置状态 """
        self._state = DinosaurState.run
        self._addHeight = 0
        self._jumpingFrame = 0
        self._downPressed, self._upPressed = False, False
        self.image = self._runningImgs[0]
        self.rect = self.getShowRect()
