"""
常量及用户设置参数
"""


class Color:
    """ 颜色常量 """
    white = (255, 255, 255)  # 白色
    dimGray = (83, 83, 83)  # 昏灰


class Settings:
    """ 设置参数 """
    initialWindowSize = (1280, 720)  # 窗口初始尺寸
    maxFPS = 60  # 最大帧数
    defaultColorKey = Color.white  # 默认设为透明的颜色

    screenDinoRate = 1 / 15  # 屏幕宽->恐龙宽的倍率（非俯冲状态）
    screenDivingDinoRate = 11 / 120  # 屏幕宽->恐龙宽的倍率（俯冲状态）
    dinosaurLeft = 100  # 恐龙左侧初始坐标
    dinosaurBottom = 430  # 恐龙上侧初始坐标
    jumpFrame = maxFPS / 2  # 大跳持续帧数
    littleJumpFrame = maxFPS / 3  # 小跳持续帧数
    frameSpeedRate = 6000 / maxFPS ** 2  # 帧数->跳跃高度变化速度倍率
    fallSpeed = 1500 / maxFPS  # 加速降落速度
    jumpCommandFrame = 5  # 跳跃按键抬起接收帧数（区分大小跳）

    screenCactusRate = 0.04  # 屏幕宽->大仙人掌宽倍率
    smallCactusRate = 0.75  # 小仙人掌相对于大仙人掌的比例
    cactusBottom = 432  # 仙人掌下侧坐标

    screenBirdRate = 0.07  # 屏幕宽->鸟宽倍率
    birdTops = (255, 295, 345)  # 鸟可能的上侧坐标

    enemyInitProbability = 100  # x，每帧出现敌人的初始概率为1/x
    enemyMaxProbability = 20  # x，每帧出现敌人的最大概率为1/x
    enemyInitMinFrameInterval = maxFPS * 0.5  # 敌人初始最小帧数间隔
    enemyMinMinFrameInterval = maxFPS * 0.35  # 敌人最小最小帧数间隔
    birdScore = 500  # 出现鸟的最低分数

    terrianTopLeft = (0, 405)  # 地形左上角点
    terrianInitSpeed = 800 / maxFPS  # 地形初始移动速度
    terrianMaxSpeed = 2400 / maxFPS  # 地形最大移动速度

    screenCloudRate = 0.075  # 屏幕宽->云宽倍率
    cloudMinTop = 300  # 云上侧最低坐标
    cloudMaxTop = 180  # 云上侧最高坐标
    cloudSpeed = 3  # 云移动速度
    cloudProbability = 200  # x，每帧出现云的初始概率为1/x

    screenRestartImageRate = 0.056  # 屏幕宽->重新开始按钮宽倍率
    restartMinFrameCount = maxFPS / 3  # 重新开始界面最小显示帧数

    scoreRate = 0.012  # 实际分数->显示分数倍率
