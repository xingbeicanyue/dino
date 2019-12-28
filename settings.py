"""
参数设置
"""

from utils import Color


class Settings:
    """ 参数设置 """

    # 全局参数
    caption = 'dino'  # 游戏标题
    initialWindowSize = (1280, 720)  # 窗口初始尺寸
    maxFPS = 120  # 最大帧数
    defaultColorKey = Color.white  # 默认设为透明的颜色

    # 动作参数
    jumpFrame = maxFPS * 0.5  # 大跳持续帧数
    littleJumpFrame = maxFPS * 0.3333  # 小跳持续帧数
    frameSpeedRate = 6000 / maxFPS ** 2  # 帧数->跳跃高度变化速度倍率
    fallSpeed = 1600 / maxFPS  # 加速降落速度
    jumpCommandFrame = round(maxFPS * 0.0833)  # 跳跃按键抬起接收帧数（区分大小跳）

    # 小恐龙
    screenDinoRate = 0.0667  # 屏幕宽->恐龙宽的倍率（非俯冲状态）
    screenDivingDinoRate = 0.0917  # 屏幕宽->恐龙宽的倍率（俯冲状态）
    dinosaurLeft = 100  # 恐龙左侧初始坐标
    dinosaurBottom = 430  # 恐龙上侧初始坐标

    # 仙人掌
    screenCactusRate = 0.04  # 屏幕宽->大仙人掌宽倍率
    smallCactusRate = 0.75  # 小仙人掌相对于大仙人掌的比例
    cactusBottom = 432  # 仙人掌下侧坐标

    # 鸟
    screenBirdRate = 0.07  # 屏幕宽->鸟宽倍率
    birdTops = (255, 295, 345)  # 鸟上侧坐标集合

    # 敌人
    enemyInitProbability = 180  # x，每帧出现敌人的初始概率为1/x
    enemyMaxProbability = 60  # x，每帧出现敌人的最大概率为1/x
    enemyInitMinFrameInterval = maxFPS * 0.6  # 敌人初始最小帧数间隔
    enemyMinMinFrameInterval = maxFPS * 0.3  # 敌人最小最小帧数间隔
    birdScore = 500  # 出现鸟的最低分数
    maxCactusScore = 1000  # 出现每组4个仙人掌的最低分数

    # 地形
    terrianTopLeft = (0, 405)  # 地形左上角点
    terrianInitSpeed = 800 / maxFPS  # 地形初始移动速度
    terrianMaxSpeed = 1600 / maxFPS  # 地形最大移动速度

    # 云
    screenCloudRate = 0.075  # 屏幕宽->云宽倍率
    cloudMinTop = 300  # 云上侧最低坐标
    cloudMaxTop = 180  # 云上侧最高坐标
    cloudSpeed = 3  # 云移动速度
    cloudProbability = maxFPS * 3  # x，每帧出现云的概率为1/x
    cloudFrameInterval = 50  # 云最小帧数间隔

    # 月亮
    moonTop = 160  # 月亮上侧坐标
    screenMoonRate = 0.0667  # 屏幕宽->月亮宽倍率
    moonSpeed = 1  # 月亮移动速度

    # 星星
    screenStarRate = 0.013  # 屏幕宽->星星宽倍率
    starMinTop = 250  # 星星上侧最低坐标
    starMaxTop = 150  # 星星上侧最高坐标
    starSpeed = 2  # 星星移动速度
    starProbability = maxFPS * 2  # x，每帧出现星星的概率为1/x

    # 昼夜变化
    dayNightScore = 700  # 一天的分数
    nightScore = 300  # 夜晚的分数
    dayNightChangeFrame = maxFPS * 0.5  # 昼夜变化动画帧数
    dayToNightMoonShowFrame = round(dayNightChangeFrame * 0.7)  # 白天转黑夜中月亮（星星）出现在动画中的帧数
    dayToNightChangeColorFrame = round(dayNightChangeFrame * 0.6)  # 白天转黑夜中景色变色在动画中的帧数

    # 游戏结束场景
    screenRestartImageRate = 0.056  # 屏幕宽->重新开始按钮宽倍率
    restartMinFrameCount = maxFPS * 0.3333  # 重新开始界面最小显示帧数

    # 分数
    scoreRate = 0.012  # 实际分数->显示分数倍率
    maxDifficultyScore = 10000  # 达到最高难度的分数

    # 资源路径
    iconBasePath = 'src/icon'  # 图标资源根路径
    imgBasePath = 'src/image'  # 图片资源根路径
    mainWindowIconPath = iconBasePath + '/mainWindow.png'  # 窗口图标
    coverImagePath = imgBasePath + '/coverImage.png'  # 封面图
    coverTextPath = imgBasePath + '/coverText.png'  # 封面文字
    restartPath = imgBasePath + '/restart.png'  # 重新开始
    dinoRunningPath = imgBasePath + '/dinoRunning.png'  # 恐龙跑步
    dinoJumpingPath = imgBasePath + '/dinoJumping.png'  # 恐龙跳跃
    dinoDivingPath = imgBasePath + '/dinoDiving.png'  # 恐龙俯冲
    dinoDyingPath = imgBasePath + '/dinoDying.png'  # 恐龙死亡
    cactusPath = imgBasePath + '/cactus.png'  # 仙人掌
    birdPath = imgBasePath + '/bird.png'  # 鸟
    terrianPath = imgBasePath + '/terrian.png'  # 地形
    cloudPath = imgBasePath + '/cloud.png'  # 云
    moonPath = imgBasePath + '/moon.png'  # 月亮
    starPath = imgBasePath + '/star.png'  # 星星

    soundBasePath = 'src/sound'  # 音效资源根路径
    jumpSoundPath = soundBasePath + '/jump.wav'  # 跳跃音效
    dieSoundPath = soundBasePath + '/die.wav'  # 死亡音效

    fontBasePath = 'src/font'  # 字体资源根路径
    courierNewBoldFontPath = fontBasePath + '/courbd.ttf'  # courier new 粗体
