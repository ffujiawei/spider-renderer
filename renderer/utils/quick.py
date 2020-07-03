'''
    常用操作的函数封装
'''

from functools import partial

from .constants import WHITESPACE


# 判断是否包含某些元素且不包含某些元素
def contains(string, within, without=tuple()) -> bool:
    if any(k in string for k in without):
        return False
    if any(k in string for k in within):
        return True
    return False


# 替换一组字符
def replace_all(string, words=tuple()) -> str:
    for w in words:
        string = string.replace(w, '')
    return string


# 替换空白符
replace_ws = partial(replace_all, words=WHITESPACE)
