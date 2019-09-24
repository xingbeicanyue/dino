"""
常数及用户设置
"""


class Settings:
    """ 设置 """

    def __init__(self):
        """ 初始化 """
        self.initialWindowSize = (1280, 720)  # 窗口初始尺寸
        self.maxFPS = 60  # 最大帧数
        self.defaultColorKey = (255, 255, 255)  # 默认设为透明的颜色

        self.dinosaurLeft = 100  # 恐龙左侧初始像素
        self.dinosaurBottom = 430  # 恐龙上侧初始像素

        self.terrianTopLeft = (0, 405)  # 地形左上角点
        self.terrianSpeed = 10  # 地形初始移动速度

        self.screenCloudRate = 0.075  # 屏幕长->云宽倍率
        self.cloudSpeed = 3  # 云移动速度
        self.cloudProbabilitySpeed = 1  # 出现云概率增加速度
        self.cloudMaxProbability = 10000  # 必然出现云的几率数值
        self.cloudMinInterval = 150  # 云最小x坐标差
        self.cloudMinTop = 300  # 云顶部最低坐标
        self.cloudMaxTop = 180  # 云顶部最高坐标


settings = Settings()
