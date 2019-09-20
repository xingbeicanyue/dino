"""
基础通用函数
"""

import pygame


def divideSruface(surface: pygame.Surface, rowCount: int, colCount: int, count: int = -1) -> list:
    """ 分割图片，根据行列数平均分配，需保证长宽可以被行列数整除
    :param count: 最终的子图片数，顺序从上至下、每行从左至右，多余的子图会被抛弃
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
