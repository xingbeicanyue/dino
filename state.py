"""
程序状态
"""


class AppStates:
    """ 程序状态 """

    def __init__(self):
        """ 初始化 """
        self.screen = None  # 屏幕
        self.gameState = 0  # 0:开始画面; 1:游戏中; 2:游戏结束

        self.dinoState = 0  # 0:普通状态; 1:跳跃起步; 2:大跳; 3:小跳; 4.降落; 5.加速降落; 6:俯冲; 7:死亡


appStates = AppStates()
