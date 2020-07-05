'''
    常用正则表达式收藏
'''
import re


# 全部中文字符
CHINESE_CHARS = re.compile(r'[\u4e00-\u9fa5]')

# 正常格式的日期
DATE = re.compile(r'(20\d{2}[-\./年]\d{1,2}[-\./月]\d{1,2}日?)')

# 提取属性
A = re.compile(r'''href=['"](\S+?)['"]''')

# 价格
M = re.compile(r'''[1-9][\d,]+\.?\d{0,2}''')
