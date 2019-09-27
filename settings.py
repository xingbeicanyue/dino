"""
常数及用户设置参数
"""


class Settings:
    """ 设置参数 """

    def __init__(self):
        """ 初始化 """
        self.initialWindowSize = (1280, 720)  # 窗口初始尺寸
        self.maxFPS = 60  # 最大帧数
        self.defaultColorKey = (255, 255, 255)  # 默认设为透明的颜色

        self.dinosaurLeft = 100  # 恐龙左侧初始坐标
        self.dinosaurBottom = 430  # 恐龙上侧初始坐标

        self.screenCactusRate = 0.04  # 屏幕宽->大仙人掌宽倍率
        self.smallCactusRate = 0.75  # 小仙人掌相对于大仙人掌的比例
        self.cactusBottom = 432  # 仙人掌下侧坐标

        self.screenBirdRate = 0.07  # 屏幕宽->鸟宽倍率
        self.birdTops = (255, 295, 345)  # 鸟可能的上侧坐标

        self.enemyMaxProbability = 400  # 必然出现敌人的几率数值
        self.enemyMinFrameInterval = 25  # 敌人最小帧数间隔

        self.terrianTopLeft = (0, 405)  # 地形左上角点
        self.terrianSpeed = 720 / self.maxFPS  # 地形初始移动速度

        self.screenCloudRate = 0.075  # 屏幕宽->云宽倍率
        self.cloudSpeed = 3  # 云移动速度
        self.cloudProbabilitySpeed = 1  # 出现云概率增加速度
        self.cloudMaxProbability = 10000  # 必然出现云的几率数值
        self.cloudMinInterval = 150  # 云最小x坐标差
        self.cloudMinTop = 300  # 云上侧最低坐标
        self.cloudMaxTop = 180  # 云上侧最高坐标


settings = Settings()
