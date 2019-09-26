"""
游戏控制及游戏对象
"""

import enum
import random
import sys
import numpy
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
        self._cactusGroup = pygame.sprite.RenderPlain()
        self._birdGroup = pygame.sprite.RenderPlain()
        self._terrian = Terrian()
        self._cloudGroup = pygame.sprite.RenderPlain()
        self._cloudProbability = settings.cloudMaxProbability  # 云出现的概率
        self._enemyProbalility = 0  # 敌人出现的概率
        appStates.curTerrianSpeed = settings.terrianSpeed

    def _updateEnemies(self):
        """ 更新敌人 """
        self._cactusGroup.update()
        for cactus in self._cactusGroup.copy():
            if cactus.rect.right < 0:
                self._cactusGroup.remove(cactus)
        self._birdGroup.update()
        for bird in self._birdGroup.copy():
            if bird.rect.right < 0:
                self._birdGroup.remove(bird)

        if random.randint(0, settings.enemyMaxProbability) < self._enemyProbalility or\
                self._enemyProbalility >= settings.enemyMaxProbability / 2:
            if random.randint(0, 2) <= 1:
                self._cactusGroup.add(Cactus())
            else:
                self._birdGroup.add(Bird())
            self._enemyProbalility = -settings.enemyMinFrameInterval
        else:
            self._enemyProbalility += 1

    def _updateClouds(self):
        """ 更新云群的位置 """
        self._cloudGroup.update()
        for cloud in self._cloudGroup.copy():
            if cloud.rect.right < 0:
                self._cloudGroup.remove(cloud)
        if random.randint(0, settings.cloudMaxProbability) < self._cloudProbability:
            self._cloudGroup.add(Cloud((appStates.screen.get_width(),
                                        random.randint(settings.cloudMaxTop, settings.cloudMinTop))))
            # 一段时间内不再出现云
            self._cloudProbability = -settings.cloudMinInterval / settings.cloudSpeed * settings.cloudProbabilitySpeed
        else:
            self._cloudProbability += settings.cloudProbabilitySpeed

    def _detectCollision(self) -> bool:
        """ 检测碰撞 """
        if pygame.sprite.spritecollide(self._dinosaur, self._cactusGroup, False, pygame.sprite.collide_mask):
            return True
        return False

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
            # 更新状态
            self._terrian.update()
            self._updateEnemies()
            self._updateClouds()
            self._dinosaur.update()
            # 显示
            appStates.screen.fill(rect=appStates.screen.get_rect(), color=(255, 255, 255))
            self._terrian.draw(appStates.screen)
            self._cloudGroup.draw(appStates.screen)
            self._cactusGroup.draw(appStates.screen)
            for bird in self._birdGroup:
                bird.draw(appStates.screen)
            self._dinosaur.show()
            # 碰撞检测
            if self._detectCollision():
                appStates.gameState = 2
        pygame.display.update()


class StartScene:
    """ 开始界面 """

    def __init__(self):
        """ 初始化 """
        # 封面图由两张图组成，尺寸相同，coverImage2为闭眼状态
        coverImage = pygame.image.load('src/coverImage.png').convert()
        coverImage.set_colorkey(settings.defaultColorKey)
        self._coverImages = baseFunc.divideSruface(coverImage, 1, 2)

    def show(self):
        """ 绘制 """
        appStates.screen.fill((255, 255, 255))
        left = round((appStates.screen.get_width() - self._coverImages[0].get_width()) / 2)
        top = round((appStates.screen.get_height() - self._coverImages[0].get_height()) / 2)
        if 0 <= pygame.time.get_ticks() % 5000 <= 100:
            appStates.screen.blit(self._coverImages[1], (left, top))
        else:
            appStates.screen.blit(self._coverImages[0], (left, top))


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

    screenDinoRate = 1 / 15  # 屏幕宽->恐龙宽的倍率（非俯冲状态）
    screenDivingDinoRate = 11 / 120  # 屏幕宽->恐龙宽的倍率（俯冲状态）
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
        self.image = self._runningImgs[0]
        self.rect = self.getShowRect()

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

    def update(self):
        """ 更新位置、状态及图片 """
        if self.__inJumpingStates():
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
        self.image = self.getShowImage()
        self.rect = self.getShowRect()

    def show(self):
        """ 绘制 """
        if self._state == DinosaurState.run:
            appStates.screen.blit(self.getShowImage(), self.getShowRect().topleft)
        elif self._state == DinosaurState.dive:
            appStates.screen.blit(self.getShowImage(), self.getShowRect().topleft)
        elif self.__inJumpingStates():
            appStates.screen.blit(self.getShowImage(), self.getShowRect().topleft)

    def getShowImage(self) -> pygame.Surface:
        if self._state == DinosaurState.run:
            return self._runningImgs[pygame.time.get_ticks() // 100 % 2]
        elif self._state == DinosaurState.dive:
            return self._divingImgs[pygame.time.get_ticks() // 100 % 2]
        elif self.__inJumpingStates():
            return self._jumpingImg
        elif self._state == DinosaurState.die:
            return None
        raise ValueError

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


class Cactus(pygame.sprite.Sprite):
    """ 仙人掌 """

    surfArrays = None

    def __init__(self):
        """ 初始化 """
        super().__init__()
        Cactus.__loadImage()
        self.isLarge = random.randint(0, 1) == 1  # 是否大仙人掌
        self.num = random.randint(1, 4)  # 仙人掌数
        self.__initCactus()
        self.rect = pygame.Rect((appStates.screen.get_width(), settings.cactusBottom - self.image.get_height()),
                                self.image.get_size())

    @staticmethod
    def __loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Cactus.surfArrays:
            image = pygame.image.load('src/cactus.png').convert()
            images = baseFunc.divideSruface(image, 1, 3)
            for i in range(len(images)):
                newImageWidth = round(appStates.screen.get_width() * settings.screenCactusRate)
                newImageHeight = round(images[i].get_height() * newImageWidth / images[i].get_width())
                images[i] = pygame.transform.scale(images[i], (newImageWidth, newImageHeight))
            Cactus.surfArrays = []
            for image in images:
                Cactus.surfArrays.append(pygame.surfarray.array3d(image))

    def __initCactus(self):
        """ 初始化自身仙人掌组信息 """
        imageArray = numpy.zeros((len(Cactus.surfArrays[0]) * self.num, len(Cactus.surfArrays[0][0]), 3))
        for i in range(self.num):
            imageArray[len(Cactus.surfArrays[0])*i:len(Cactus.surfArrays[0])*(i+1), :] =\
                Cactus.surfArrays[random.randint(0, 2)]
        self.image = pygame.surfarray.make_surface(imageArray)
        self.image.set_colorkey(settings.defaultColorKey)
        if not self.isLarge:
            self.image = pygame.transform.scale(self.image, (round(self.image.get_width() * settings.smallCactusRate),
                                                             round(self.image.get_height() * settings.smallCactusRate)))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-appStates.curTerrianSpeed, 0)


class Bird(pygame.sprite.Sprite):
    """ 鸟 """

    images = None

    def __init__(self):
        """ 初始化 """
        super().__init__()
        Bird.__loadImage()
        self.rect = pygame.Rect((appStates.screen.get_width(), settings.birdTops[random.randint(0, 2)]),
                                Bird.images[0].get_size())

    @staticmethod
    def __loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Bird.images:
            image = pygame.image.load('src/bird.png').convert()
            image.set_colorkey(settings.defaultColorKey)
            Bird.images = baseFunc.divideSruface(image, 1, 2)
            for i in range(len(Bird.images)):
                newImageWidth = round(appStates.screen.get_width() * settings.screenBirdRate)
                newImageHeight = round(Bird.images[i].get_height() * newImageWidth / Bird.images[i].get_width())
                Bird.images[i] = pygame.transform.scale(Bird.images[i], (newImageWidth, newImageHeight))

    def update(self):
        self.rect = self.rect.move(-appStates.curTerrianSpeed, 0)

    def draw(self, surface):
        """ 绘制 """
        surface.blit(Bird.images[pygame.time.get_ticks() // 200 % 2], self.rect.topleft)


class Terrian(pygame.sprite.Sprite):
    """ 地形 """

    image = None

    def __init__(self):
        """ 初始化 """
        super().__init__()
        Terrian.__loadImage()
        self.rect = pygame.Rect(settings.terrianTopLeft, Terrian.image.get_size())

    @staticmethod
    def __loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Terrian.image:
            Terrian.image = pygame.image.load('src/terrian.png').convert()
            newImageWidth = round(appStates.screen.get_width() * 2)
            newImageHeight = round(Terrian.image.get_height() * newImageWidth / Terrian.image.get_width())
            Terrian.image = pygame.transform.scale(Terrian.image, (newImageWidth, newImageHeight))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-appStates.curTerrianSpeed, 0)
        if self.rect.right < appStates.screen.get_width():
            self.rect = self.rect.move(appStates.screen.get_width(), 0)

    def draw(self, screen):
        """ 绘制 """
        screen.blit(Terrian.image, self.rect)


class Cloud(pygame.sprite.Sprite):
    """ 云 """

    image = None

    def __init__(self, topLeft):
        """ 初始化 """
        super().__init__()
        Cloud.__loadImage()
        self.rect = pygame.Rect(topLeft, self.image.get_size())

    @staticmethod
    def __loadImage():
        """ 载入图片并根据屏幕窗口调整大小 """
        if not Cloud.image:
            Cloud.image = pygame.image.load('src/cloud.png').convert()
            Cloud.image.set_colorkey(settings.defaultColorKey)
            newImageWidth = round(appStates.screen.get_width() * settings.screenCloudRate)
            newImageHeight = round(Cloud.image.get_height() * newImageWidth / Cloud.image.get_width())
            Cloud.image = pygame.transform.scale(Cloud.image, (newImageWidth, newImageHeight))

    def update(self):
        """ 更新 """
        self.rect = self.rect.move(-settings.cloudSpeed, 0)
