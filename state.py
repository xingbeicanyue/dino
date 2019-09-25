"""
程序状态
"""


class AppStates:
    """ 程序状态 """

    def __init__(self):
        """ 初始化 """
        self.screen = None  # 屏幕
        self.gameState = 0  # 0:开始画面; 1:游戏中; 2:游戏结束
        self.curTerrianSpeed = 0  # 当前地形移动速度


appStates = AppStates()
