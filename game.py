"""
游戏控制及游戏对象
"""

import enum
import random
import sys
import pygame
import baseFunc
from state import appStates
from settings import settings


class Game:
    """ 游戏控制 """

    def __init__(self):
        """ 初始化 """
        self._startScene = StartScene()
        self._dinosaur = Dinosaur()
        self._terrian = Terrian()
        self._cloudGroup = pygame.sprite.RenderPlain()
        self._cloudProbability = settings.cloudMaxProbability  # 云出现的概率

    def _updateClouds(self):
        """ 更新云群的位置 """
        self._cloudGroup.update()
        if random.randint(0, settings.cloudMaxProbability) < self._cloudProbability:
            self._cloudGroup.add(Cloud((appStates.screen.get_width(),
                                        random.randint(settings.cloudMaxTop, settings.cloudMinTop))))
            # 一段时间内不再出现云
            self._cloudProbability = -settings.cloudMinInterval / settings.cloudSpeed * settings.cloudProbabilitySpeed
        else:
            self._cloudProbability += settings.cloudProbabilitySpeed

    def handleEvents(self):
        """ 处理事件 """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if appStates.gameState == 0:
                        appStates.gameState = 1
                        appStates.screen.fill((255, 255, 255))
                    elif appStates.gameState == 1:
                        self._dinosaur.startUp()
                elif event.key == pygame.K_DOWN:
                    if appStates.gameState == 1:
                        self._dinosaur.startDown()
                elif event.key == pygame.K_UP:
                    if appStates.gameState == 1:
                        self._dinosaur.startUp()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    if appStates.gameState == 1:
                        self._dinosaur.endDown()
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    if appStates.gameState == 1:
                        self._dinosaur.endUp()

    def draw(self):
        """ 绘制 """
        if appStates.gameState == 0:
            self._startScene.show()
        elif appStates.gameState == 1:
            self._terrian.update()
            self._updateClouds()
            self._dinosaur.updateState()

            appStates.screen.fill(rect=appStates.screen.get_rect(), color=(255, 255, 255))
            self._terrian.draw(appStates.screen)
            self._cloudGroup.draw(appStates.screen)
            self._dinosaur.show()
        pygame.display.update()


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
        if self._state == DinosaurState.run:
            appStates.screen.blit(self._runningImgs[pygame.time.get_ticks() // 100 % 2], self.getShowRect().topleft)
        elif self._state == DinosaurState.dive:
            appStates.screen.blit(self._divingImgs[pygame.time.get_ticks() // 100 % 2], self.getShowRect().topleft)
        elif self.__inJumpingStates():
            appStates.screen.blit(self._jumpingImg, self.getShowRect().topleft)

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


class Terrian(pygame.sprite.Sprite):
    """ 地形 """

    def __init__(self):
        """ 初始化 """
        super().__init__()
        self.__loadImage()
        self.rect = pygame.Rect(settings.terrianTopLeft, self.image.get_size())
        self.curSpeed = settings.terrianSpeed

    def __loadImage(self):
        """ 载入图片并根据屏幕窗口调整大小 """
        self.image = pygame.image.load('src/terrian.png').convert()
        newImageWidth = round(appStates.screen.get_width() * 2)
        newImageHeight = round(self.image.get_height() * newImageWidth / self.image.get_width())
        self.image = pygame.transform.scale(self.image, (newImageWidth, newImageHeight))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-self.curSpeed, 0)
        if self.rect.right < appStates.screen.get_width():
            self.rect = self.rect.move(appStates.screen.get_width(), 0)

    def draw(self, screen):
        """ 绘制 """
        screen.blit(self.image, self.rect)


class Cloud(pygame.sprite.Sprite):
    """ 云 """

    def __init__(self, topLeft):
        """ 初始化 """
        super().__init__()
        self.image = pygame.image.load('src/cloud.png').convert()
        self.image.set_colorkey(settings.defaultColorKey)
        newImageWidth = round(appStates.screen.get_width() * settings.screenCloudRate)
        newImageHeight = round(self.image.get_height() * newImageWidth / self.image.get_width())
        self.image = pygame.transform.scale(self.image, (newImageWidth, newImageHeight))
        self.rect = pygame.Rect(topLeft, self.image.get_size())

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-settings.cloudSpeed, 0)
