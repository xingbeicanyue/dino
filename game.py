"""
游戏管理及控制
"""

import random
import sys
import pygame
from settings import Color, Settings
from startScene import StartScene
from dinosaur import Dinosaur
from enemy import Cactus, Bird
from env import Cloud, Terrian
from score import Score


class Game:
    """ 游戏 """

    def __init__(self, screen):
        """ 初始化 """
        self._screen = screen  # 屏幕
        self._gameState = 0  # 0:开始画面; 1:游戏中; 2:游戏结束
        self._frameCount = 0  # 每个游戏状态的帧数计数
        self._score = Score()  # 分数系统
        self._startScene = StartScene()
        self._dinosaur = Dinosaur(self)
        self._cactusGroup = pygame.sprite.RenderPlain()
        self._birdGroup = pygame.sprite.RenderPlain()
        self._terrian = Terrian(self)
        self._cloudGroup = pygame.sprite.RenderPlain()

        self._lastEnemyFrameCount = 0  # 上一次出现敌人的帧数计数
        self._curEnemeyProbability = Settings.enemyInitProbability  # x，当前每帧敌人出现的概率为1/x
        self._curEnemyMinFrameInterval = Settings.enemyInitMinFrameInterval  # 敌人最小帧数间隔
        self._curTerrianSpeed = Settings.terrianInitSpeed  # 当前地形移动速度
        self._loadRestartImage()

    def _loadRestartImage(self):
        """ 加载重新开始图片并根据屏幕窗口调整大小 """
        self._restartImage = pygame.image.load('src/restart.png').convert()
        self._restartImage.set_colorkey(Settings.defaultColorKey)
        newImageWidth = round(Settings.initialWindowSize[0] * Settings.screenRestartImageRate)
        newImageHeight = round(self._restartImage.get_height() * newImageWidth / self._restartImage.get_width())
        self._restartImage = pygame.transform.scale(self._restartImage, (newImageWidth, newImageHeight))

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

        frameWithoutEnemy = self._frameCount - self._lastEnemyFrameCount
        if frameWithoutEnemy > self._curEnemyMinFrameInterval and\
                (random.randint(0, round(self._curEnemeyProbability)) == 0 or
                 frameWithoutEnemy >= self._curEnemeyProbability):
            if (self._score.curScore * Settings.scoreRate) < Settings.birdScore or random.randint(0, 2) <= 1:
                self._cactusGroup.add(Cactus(self))
            else:
                self._birdGroup.add(Bird(self))
            self._lastEnemyFrameCount = self._frameCount

    def _updateClouds(self):
        """ 更新云群 """
        self._cloudGroup.update()
        for cloud in self._cloudGroup.copy():
            if cloud.rect.right < 0:
                self._cloudGroup.remove(cloud)
        if random.randint(0, Settings.cloudProbability) == 0:
            self._cloudGroup.add(Cloud(self, (self._screen.get_width(),
                                              random.randint(Settings.cloudMaxTop, Settings.cloudMinTop))))

    def _updateDifficulty(self):
        """ 更新难度参数 """
        showScore = self._score.curScore * Settings.scoreRate

        self._curEnemeyProbability = Settings.enemyInitProbability +\
            (Settings.enemyMaxProbability - Settings.enemyInitProbability) / 10000 * showScore
        self._curEnemeyProbability = max(self._curEnemeyProbability, Settings.enemyMaxProbability)

        self._curEnemyMinFrameInterval = Settings.enemyInitMinFrameInterval +\
            (Settings.enemyMinMinFrameInterval - Settings.enemyInitMinFrameInterval) / 10000 * showScore
        self._curEnemyMinFrameInterval = max(self._curEnemyMinFrameInterval, Settings.enemyMinMinFrameInterval)

        self._curTerrianSpeed = Settings.terrianInitSpeed +\
            (Settings.terrianMaxSpeed - Settings.terrianInitSpeed) / 10000 * showScore
        self._curTerrianSpeed = min(self._curTerrianSpeed, Settings.terrianMaxSpeed)

    def _detectCollision(self) -> bool:
        """ 检测碰撞 """
        return pygame.sprite.spritecollide(self._dinosaur, self._cactusGroup, False, pygame.sprite.collide_mask) or\
            pygame.sprite.spritecollide(self._dinosaur, self._birdGroup, False, pygame.sprite.collide_mask)

    def _drawRestartImage(self):
        """ 显示重新开始画面 """
        topLeft = ((Settings.initialWindowSize[0] - self._restartImage.get_width()) / 2,
                   (Settings.initialWindowSize[1] - self._restartImage.get_height()) / 2)
        self._screen.blit(self._restartImage, topLeft)

        gameoverImage = pygame.font.Font('src/courbd.ttf', 48).render('G A M E    O V E R', True, Color.dimGray)
        topLeft = ((Settings.initialWindowSize[0] - gameoverImage.get_width()) / 2,
                   topLeft[1] - gameoverImage.get_height() * 2)
        self._screen.blit(gameoverImage, topLeft)

    def _restart(self):
        """ 重开游戏 """
        self._gameState = 1
        self._frameCount = 0
        self._score.setScore(0)
        self._dinosaur.restart()
        self._cactusGroup.empty()
        self._birdGroup.empty()
        self._lastEnemyFrameCount = 0
        self._curEnemeyProbability = Settings.enemyInitProbability
        self._curEnemyMinFrameInterval = Settings.enemyInitMinFrameInterval
        self._curTerrianSpeed = Settings.terrianInitSpeed

    @property
    def curTerrianSpeed(self):
        """ 获取当前地形移动速度 """
        return self._curTerrianSpeed

    def handleEvents(self):
        """ 处理事件 """
        self._frameCount += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self._gameState == 0:
                        self._gameState = 1
                        self._frameCount = 0
                        self._screen.fill((255, 255, 255))
                    elif self._gameState == 1:
                        self._dinosaur.startUp()
                    elif self._gameState == 2:
                        if self._frameCount >= Settings.restartMinFrameCount:
                            self._restart()
                elif event.key == pygame.K_DOWN:
                    if self._gameState == 1:
                        self._dinosaur.startDown()
                elif event.key == pygame.K_UP:
                    if self._gameState == 1:
                        self._dinosaur.startUp()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    if self._gameState == 1:
                        self._dinosaur.endDown()
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    if self._gameState == 1:
                        self._dinosaur.endUp()

    def updateAndDraw(self):
        """ 更新并绘制 """

        def showGameScene():
            """ 显示当前帧 """
            self._screen.fill(rect=self._screen.get_rect(), color=(255, 255, 255))
            self._terrian.draw(self._screen)
            self._cloudGroup.draw(self._screen)
            self._cactusGroup.draw(self._screen)
            self._birdGroup.draw(self._screen)
            self._dinosaur.draw(self._screen)
            self._score.draw(self._screen)

        if self._gameState == 0:
            self._startScene.draw(self._screen)
        elif self._gameState == 1:
            # 更新状态
            self._terrian.update()
            self._updateClouds()
            self._updateEnemies()
            self._dinosaur.update()
            self._score.addScore(self._curTerrianSpeed)
            self._updateDifficulty()
            # 显示
            showGameScene()
            # 碰撞检测
            if self._detectCollision():
                self._dinosaur.die()
                self._gameState = 2
                self._frameCount = 0
        else:
            showGameScene()
            self._drawRestartImage()
        pygame.display.update()
