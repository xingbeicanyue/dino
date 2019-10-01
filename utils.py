"""
基础通用常量及函数
"""

import pygame


class Color:
    """ 颜色 """

    black = (0, 0, 0)  # 黑色
    dimGray = (83, 83, 83)  # 昏灰
    white = (255, 255, 255)  # 白色

    @staticmethod
    def invert(color: tuple) -> tuple:
        """ 反色 """
        return 255 - color[0], 255 - color[1], 255 - color[2]


def divideSurface(surface: pygame.Surface, rowCount: int, colCount: int, count: int = -1) -> list:
    """ 分割图像，根据行列数平均分配，需保证宽高可以被行列数整除
    :param surface: 图像
    :param rowCount: 行数
    :param colCount: 列数
    :param count: 最终的子图像数，顺序从上至下、每行从左至右，多余的子图会被抛弃
    """
    if count < 0:
        count = rowCount * colCount
    width = surface.get_width() // colCount
    height = surface.get_height() // rowCount
    result = []
    for rowId in range(rowCount):
        for colId in range(colCount):
            result.append(surface.subsurface(pygame.Rect((width * colId, height * rowId), (width, height))))
            if len(result) == count:
                return result
    return result


def loadImage(fileName: str, colorkey=None, width=0, convert: bool = True) -> pygame.Surface:
    """ 读取图像，并设置透明色与尺寸
    :param fileName: 文件名
    :param colorkey: 透明色
    :param width: 宽度，=0时不改变尺寸
    :param convert: 是否转变为与display相同的像素格式
    """
    result = pygame.image.load(fileName)
    if convert:
        result = result.convert()
    if colorkey:
        result.set_colorkey(colorkey)
    if width > 0:
        width = round(width)
        height = round(result.get_height() * width / result.get_width())
        result = pygame.transform.scale(result, (width, height))
    return result


def loadImages(fileName: str, rowCount: int, colCount: int, count: int = -1, colorkey=None, width=0,
               convert: bool = True) -> list:
    """ 读取、分割图像，并设置透明色与尺寸
    :param fileName: 文件名
    :param rowCount: 行数
    :param colCount: 列数
    :param count: 最终的子图像数，顺序从上至下、每行从左至右，多余的子图会被抛弃
    :param colorkey: 透明色
    :param width: 宽度，=0时不改变尺寸
    :param convert: 是否转变为与display相同的像素格式
    """
    image = pygame.image.load(fileName)
    if convert:
        image = image.convert()
    if colorkey:
        image.set_colorkey(colorkey)
    result = divideSurface(image, rowCount, colCount, count)
    if width > 0 and result:
        width = round(width)
        height = round(result[0].get_height() * width / result[0].get_width())
        for i in range(len(result)):
            result[i] = pygame.transform.scale(result[i], (width, height))
    return result


def invertSurface(surface: pygame.Surface) -> pygame.Surface:
    """ 返回surface的反色图像 """
    oriColorkey = surface.get_colorkey()
    result = pygame.surfarray.make_surface(255 - pygame.surfarray.array3d(surface))
    result.set_colorkey(Color.invert(oriColorkey))
    return result


def invertSurfaces(surfaces: list) -> list:
    """ 返回surfaces的反色图像列表 """
    return [invertSurface(surface) for surface in surfaces]
