"""
常数及用户设置
"""


class Settings:
    """ 设置 """

    def __init__(self):
        """ 初始化 """
        self.initialWindowSize = (800, 600)  # 窗口初始尺寸
        self.screenDinoRate = 1 / 15  # 屏幕长->恐龙长的倍率


settings = Settings()
