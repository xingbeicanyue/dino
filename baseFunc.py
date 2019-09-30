"""
基础通用常量及函数
"""

import pygame


class Color:
    """ 颜色常量 """
    black = (0, 0, 0)  # 黑色
    dimGray = (83, 83, 83)  # 昏灰
    white = (255, 255, 255)  # 白色

    @staticmethod
    def invert(color: tuple) -> tuple:
        """ 反色 """
        return 255 - color[0], 255 - color[1], 255 - color[2]


def divideSurface(surface: pygame.Surface, rowCount: int, colCount: int, count: int = -1) -> list:
    """ 分割图像，根据行列数平均分配，需保证长宽可以被行列数整除
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


def invertSurface(surface: pygame.Surface) -> pygame.Surface:
    """ 返回surface的反色图像 """
    oriColorkey = surface.get_colorkey()
    result = pygame.surfarray.make_surface(255 - pygame.surfarray.array3d(surface))
    result.set_colorkey(Color.invert(oriColorkey))
    return result


def invertSurfaces(surfaces: list) -> list:
    """ 返回surfaces的反色图像列表 """
    return [invertSurface(surface) for surface in surfaces]
