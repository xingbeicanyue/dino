"""
常数及用户设置
"""


class Settings:
    """ 设置 """

    def __init__(self):
        """ 初始化 """
        self.initialWindowSize = (1280, 720)  # 窗口初始尺寸
        self.maxFPS = 60  # 最大帧数

        self.dinosaurLeft = 100  # 恐龙左侧初始像素
        self.dinosaurBottom = 430  # 恐龙上侧初始像素

        self.defaultColorKey = (255, 255, 255)  # 默认设为透明的颜色


settings = Settings()
