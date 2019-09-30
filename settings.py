"""
参数设置
"""

from baseFunc import Color


class Settings:
    """ 参数设置 """
    initialWindowSize = (1280, 720)  # 窗口初始尺寸
    maxFPS = 60  # 最大帧数
    defaultColorKey = Color.white  # 默认设为透明的颜色

    screenDinoRate = 0.0667  # 屏幕宽->恐龙宽的倍率（非俯冲状态）
    screenDivingDinoRate = 0.0917  # 屏幕宽->恐龙宽的倍率（俯冲状态）
    dinosaurLeft = 100  # 恐龙左侧初始坐标
    dinosaurBottom = 430  # 恐龙上侧初始坐标
    jumpFrame = maxFPS * 0.5  # 大跳持续帧数
    littleJumpFrame = maxFPS * 0.3333  # 小跳持续帧数
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
    cloudProbability = 200  # x，每帧出现云的概率为1/x
    cloudFrameInterval = 50  # 云最小帧数间隔

    moonTop = 160  # 月亮上侧坐标
    screenMoonRate = 0.0667  # 屏幕宽->月亮宽倍率
    moonSpeed = 1  # 月亮移动速度

    screenStarRate = 0.013  # 屏幕宽->星星宽倍率
    starMinTop = 300  # 星星上侧最低坐标
    starMaxTop = 160  # 星星上侧最高坐标
    starSpeed = 2  # 星星移动速度
    starProbability = 150  # x，每帧出现星星的概率为1/x

    dayNightScore = 700  # 一天的分数
    nightScore = 300  # 夜晚的分数
    dayNightChangeFrame = maxFPS * 0.5  # 日夜交替动画帧数
    dayToNightMoonShowFrame = round(dayNightChangeFrame * 0.7)  # 白天转黑夜中月亮（星星）出现在动画中的帧数
    dayToNightChangeColorFrame = round(dayNightChangeFrame * 0.6)  # 白天转黑夜中景色变色在动画中的帧数

    screenRestartImageRate = 0.056  # 屏幕宽->重新开始按钮宽倍率
    restartMinFrameCount = maxFPS * 0.3333  # 重新开始界面最小显示帧数

    scoreRate = 0.012  # 实际分数->显示分数倍率
