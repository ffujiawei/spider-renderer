'''常用操作的函数封装'''

from functools import partial

from .constants import WHITESPACE


# 判断是否包含某些元素且不包含某些元素
def contains(string, within, without=tuple()) -> bool:
    '''Determine if it contains certain elements
       and does not contain certain elements.'''
    if any(k in string for k in without):
        return False
    if any(k in string for k in within):
        return True
    return False


# 替换一组字符
def replace_all(string, words=tuple(), char='') -> str:
    '''Replace a set of characters.'''
    for w in words:
        string = string.replace(w, char)
    return string


# 清除空格符号
replace_ws = partial(replace_all, words=WHITESPACE)


# 将路径分割为上一级路径、文件名和扩展名
def split_path(path):
    '''Split the path/url into upper-level path/url, file name, and extension.'''
    import os.path
    ph, filext = os.path.split(path)  # 分割为上一级路径和包含后缀的文件名
    fil, ext = os.path.splitext(filext)  # 分割为文件名和后缀
    return ph, fil, ext
