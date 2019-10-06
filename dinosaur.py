"""
恐龙
"""

import enum
import pygame
import utils
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
        self._loadSound()
        self._game = game
        self._state = DinosaurState.run
        self._addHeight = 0  # 高度
        self._jumpingFrame = 0  # 跳跃帧数（用于计算高度位移）
        self._downPressed, self._upPressed = False, False  # 俯冲|跳跃按键是否按下
        self.image = self._runningImageDays[0]
        self.rect = self.getShowRect()

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
                    self._jumpSound.play()
                else:
                    self._state = DinosaurState.run
        self.image = self.getShowImage()
        self.rect = self.getShowRect()

    def draw(self, surface):
        """ 绘制 """
        surface.blit(self.image, self.rect.topleft)

    def getShowImage(self) -> pygame.Surface:
        """ 获取显示的图片 """
        imgIndex = pygame.time.get_ticks() // 100 % 2
        if self._game.showNightImage():
            if self._state == DinosaurState.run:
                return self._runningImageNights[imgIndex]
            elif self._state == DinosaurState.dive:
                return self._divingImageNights[imgIndex]
            elif self._inJumpingStates():
                return self._jumpingImageNight
            else:
                return self._dyingImageNight
        else:
            if self._state == DinosaurState.run:
                return self._runningImageDays[imgIndex]
            elif self._state == DinosaurState.dive:
                return self._divingImageDays[imgIndex]
            elif self._inJumpingStates():
                return self._jumpingImageDay
            else:
                return self._dyingImageDay

    def getShowRect(self) -> pygame.Rect:
        """ 获取图片显示矩形 """
        if self._state == DinosaurState.run:
            return pygame.Rect((Settings.dinosaurLeft, Settings.dinosaurBottom -
                                self._runningImageDays[0].get_height()), self._runningImageDays[0].get_size())
        elif self._state == DinosaurState.dive:
            return pygame.Rect((Settings.dinosaurLeft, Settings.dinosaurBottom -
                                self._divingImageDays[0].get_height()), self._divingImageDays[0].get_size())
        elif self._inJumpingStates():
            return pygame.Rect((Settings.dinosaurLeft, Settings.dinosaurBottom - self._jumpingImageDay.get_height() -
                                self._addHeight), self._jumpingImageDay.get_size())
        else:
            return pygame.Rect((Settings.dinosaurLeft, Settings.dinosaurBottom - self._dyingImageDay.get_height() -
                                self._addHeight), self._dyingImageDay.get_size())

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
            self._jumpSound.play()

    def endUp(self):
        """ 结束跳跃按键 """
        self._upPressed = False
        if self._state == DinosaurState.startJump:
            self._state = DinosaurState.littleJump if self._jumpingFrame < Settings.jumpCommandFrame\
                else DinosaurState.jump

    def die(self):
        """ 进入死亡状态 """
        self._state = DinosaurState.die
        self.update()
        self._dieSound.play()

    def restart(self):
        """ 重置状态 """
        self._state = DinosaurState.run
        self._addHeight = 0
        self._jumpingFrame = 0
        self._downPressed, self._upPressed = False, False
        self.image = self._runningImageNights[0] if self._game.showNightImage() else self._runningImageDays[0]
        self.rect = self.getShowRect()

    def _inJumpingStates(self) -> bool:
        """ 判断是否处于跳跃状态（跳跃起步、大跳、小跳、加速降落） """
        return self._state in (DinosaurState.startJump, DinosaurState.jump,
                               DinosaurState.littleJump, DinosaurState.fall)

    def _loadImage(self):
        """ 载入图片并根据屏幕窗口调整大小 """
        # 跑步状态
        self._runningImageDays = utils.loadImages(Settings.dinoRunningPath, 1, 2, -1, Settings.defaultColorKey,
                                                  Settings.initialWindowSize[0] * Settings.screenDinoRate)
        self._runningImageNights = utils.invertSurfaces(self._runningImageDays)

        # 俯冲状态
        self._divingImageDays = utils.loadImages(Settings.dinoDivingPath, 1, 2, -1, Settings.defaultColorKey,
                                                 Settings.initialWindowSize[0] * Settings.screenDivingDinoRate)
        self._divingImageNights = utils.invertSurfaces(self._divingImageDays)

        # 跳跃状态
        self._jumpingImageDay = utils.loadImage(Settings.dinoJumpingPath, Settings.defaultColorKey,
                                                Settings.initialWindowSize[0] * Settings.screenDinoRate)
        self._jumpingImageNight = utils.invertSurface(self._jumpingImageDay)

        # 死亡状态
        self._dyingImageDay = utils.loadImage(Settings.dinoDyingPath, Settings.defaultColorKey,
                                              Settings.initialWindowSize[0] * Settings.screenDinoRate)
        self._dyingImageNight = utils.invertSurface(self._dyingImageDay)

    def _loadSound(self):
        """ 加载音效 """
        self._jumpSound = pygame.mixer.Sound(Settings.jumpSoundPath)
        self._dieSound = pygame.mixer.Sound(Settings.dieSoundPath)