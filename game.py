"""
游戏管理及控制
"""

import enum
import random
import sys
import pygame
from settings import Settings
from startScene import StartScene
from gameoverScene import GameoverScene
from dinosaur import Dinosaur
from enemy import Cactus, Bird
from env import Cloud, Moon, Star, Terrian
from score import Score


class GameState(enum.Enum):
    """ 游戏状态 """
    start = 0  # 开始界面
    running = 1  # 游戏进行中
    gameover = 2  # 游戏结束


class Game:
    """ 游戏 """

    def __init__(self, screen):
        """ 初始化 """
        self._screen = screen  # 屏幕画面
        self._gameState = GameState.start  # 游戏状态 0:开始画面; 1:游戏中; 2:游戏结束
        self._frameCount = 0  # 每个游戏状态的帧数计数
        self._score = Score(self)  # 分数系统

        # 游戏元素
        self._startScene = StartScene()
        self._gameoverScene = GameoverScene(self)
        self._dinosaur = Dinosaur(self)
        self._cactusGroup = pygame.sprite.RenderPlain()
        self._birdGroup = pygame.sprite.RenderPlain()
        self._terrian = Terrian(self)
        self._cloudGroup = pygame.sprite.RenderPlain()
        self._moon = Moon(self)
        self._starGroup = pygame.sprite.RenderPlain()

        # 控制难度的变量
        self._lastEnemyFrameCount = 0  # 上一次出现敌人的帧数计数
        self._curEnemeyProbability = Settings.enemyInitProbability  # x，当前每帧敌人出现的概率为1/x
        self._curEnemyMinFrameInterval = Settings.enemyInitMinFrameInterval  # 当前敌人最小帧数间隔
        self._curTerrianSpeed = Settings.terrianInitSpeed  # 当前地形移动速度

        # 控制环境的变量
        self._lastCloudFrameCount = Settings.cloudFrameInterval  # 上一次出现云的帧数计数
        self._isDay = True  # 是否白天
        self._dayNightFrame = Settings.dayNightChangeFrame  # 自从白天/黑夜开始的帧数，初始值不为0，因为开始无需昼夜交替

    @property
    def curShowScore(self):
        """ 获取当前展示分数 """
        return self._score.curShowScore

    @property
    def curTerrianSpeed(self):
        """ 获取当前地形移动速度 """
        return self._curTerrianSpeed

    def showNightImage(self):
        """ 是否显示夜晚图像 """
        if self._isDay:
            return self._dayNightFrame < Settings.dayNightChangeFrame - Settings.dayToNightChangeColorFrame
        return self._dayNightFrame >= Settings.dayToNightChangeColorFrame

    def handleEvents(self):
        """ 处理事件 """
        self._frameCount += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self._gameState == GameState.start:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self._gameState = GameState.running
                    self._frameCount = 0
            elif self._gameState == GameState.running:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._dinosaur.startUp()
                    elif event.key == pygame.K_DOWN:
                        self._dinosaur.startDown()
                    elif event.key == pygame.K_UP:
                        self._dinosaur.startUp()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self._dinosaur.endDown()
                    elif event.key in (pygame.K_SPACE, pygame.K_UP):
                        self._dinosaur.endUp()
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self._frameCount >= Settings.restartMinFrameCount:
                        self._restart()

    def updateAndDraw(self):
        """ 更新并绘制 """

        def update():
            """ 更新游戏元素和状态 """
            self._terrian.update()
            self._updateClouds()
            self._moon.update()
            self._updateStars()
            self._updateEnemies()
            self._dinosaur.update()
            self._score.addScore(self._curTerrianSpeed)
            self._updateDayNight()
            self._updateDifficulty()

        def showGameScene():
            """ 显示当前帧 """
            colorValue = round(255 * min(self._dayNightFrame / Settings.dayNightChangeFrame, 1))
            if not self._isDay:
                colorValue = 255 - colorValue
            self._screen.fill(rect=self._screen.get_rect(), color=(colorValue, colorValue, colorValue))

            if not self._isDay and self._dayNightFrame > Settings.dayToNightMoonShowFrame:
                self._starGroup.draw(self._screen)
                self._moon.draw(self._screen)
            self._terrian.draw(self._screen)
            self._cloudGroup.draw(self._screen)
            self._cactusGroup.draw(self._screen)
            self._birdGroup.draw(self._screen)
            self._dinosaur.draw(self._screen)
            self._score.draw(self._screen)

        def handleCollision():
            """ 处理碰撞 """
            if self._detectCollision():
                self._dinosaur.die()
                self._gameState = GameState.gameover
                self._frameCount = 0

        if self._gameState == GameState.start:
            self._startScene.draw(self._screen)
        elif self._gameState == GameState.running:
            update()
            showGameScene()
            handleCollision()
        else:
            if self._frameCount <= 1:  # 只需显示一次
                showGameScene()
                self._gameoverScene.draw(self._screen)
        pygame.display.update()

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

        self._lastEnemyFrameCount += 1
        if self._lastEnemyFrameCount > self._curEnemyMinFrameInterval and\
                (random.randint(0, round(self._curEnemeyProbability)) == 0 or
                 self._lastEnemyFrameCount >= self._curEnemeyProbability):
            if self.curShowScore < Settings.birdScore or random.randint(0, 2) <= 1:
                self._cactusGroup.add(Cactus(self))
            else:
                self._birdGroup.add(Bird(self))
            self._lastEnemyFrameCount = 0

    def _updateClouds(self):
        """ 更新云群 """
        self._cloudGroup.update()
        for cloud in self._cloudGroup.copy():
            if cloud.rect.right < 0:
                self._cloudGroup.remove(cloud)

        self._lastCloudFrameCount += 1
        if self._lastCloudFrameCount > Settings.cloudFrameInterval and\
                random.randint(0, Settings.cloudProbability) == 0:
            self._cloudGroup.add(Cloud(self))
            self._lastCloudFrameCount = 0

    def _updateStars(self):
        """ 更新星群 """
        self._starGroup.update()
        for star in self._starGroup.copy():
            if star.rect.right < 0:
                self._starGroup.remove(star)

        if random.randint(0, Settings.starProbability) == 0:
            self._starGroup.add(Star(self))

    def _updateDayNight(self):
        """ 更新日夜状态 """
        curIsDay = (self.curShowScore < Settings.dayNightScore) or\
                   (self.curShowScore % Settings.dayNightScore > Settings.nightScore)
        if curIsDay == self._isDay:
            self._dayNightFrame += 1
        else:
            self._isDay = curIsDay
            self._dayNightFrame = max(Settings.dayNightChangeFrame - self._dayNightFrame, 0)
            if curIsDay:
                self._moon.nextPhase()

    def _updateDifficulty(self):
        """ 更新难度参数 """
        self._curEnemeyProbability = Settings.enemyInitProbability +\
            (Settings.enemyMaxProbability - Settings.enemyInitProbability) /\
            Settings.maxDifficultyScore * self.curShowScore
        self._curEnemeyProbability = max(self._curEnemeyProbability, Settings.enemyMaxProbability)

        self._curEnemyMinFrameInterval = Settings.enemyInitMinFrameInterval +\
            (Settings.enemyMinMinFrameInterval - Settings.enemyInitMinFrameInterval) /\
            Settings.maxDifficultyScore * self.curShowScore
        self._curEnemyMinFrameInterval = max(self._curEnemyMinFrameInterval, Settings.enemyMinMinFrameInterval)

        self._curTerrianSpeed = Settings.terrianInitSpeed +\
            (Settings.terrianMaxSpeed - Settings.terrianInitSpeed) / Settings.maxDifficultyScore * self.curShowScore
        self._curTerrianSpeed = min(self._curTerrianSpeed, Settings.terrianMaxSpeed)

    def _detectCollision(self) -> bool:
        """ 检测碰撞 """
        return pygame.sprite.spritecollide(self._dinosaur, self._cactusGroup, False, pygame.sprite.collide_mask) or\
            pygame.sprite.spritecollide(self._dinosaur, self._birdGroup, False, pygame.sprite.collide_mask)

    def _restart(self):
        """ 重开游戏 """
        self._gameState = GameState.running
        self._frameCount = 0
        self._score.setScore(0)
        self._dinosaur.restart()
        self._cactusGroup.empty()
        self._birdGroup.empty()
        self._lastEnemyFrameCount = 0
        self._curEnemeyProbability = Settings.enemyInitProbability
        self._curEnemyMinFrameInterval = Settings.enemyInitMinFrameInterval
        self._curTerrianSpeed = Settings.terrianInitSpeed
