'''HTML parsing helper function.'''

import re

from .constants import USELESS_TAGS
from .quick import replace_ws


# 清除空格符号，然后替换连续的空白符号
def rm_ws(string, char='\n'):
    '''Clear a space character, then 
    replace the continuous blank symbols.'''
    return re.sub(r'\s+', char, replace_ws(string))


# 移除指定标签及其内容，默认同时移除其他标签
# 但保留其内容，最后清除或替换多余空白符
def rm_tags(html, char='', tags=USELESS_TAGS, default=True):
    '''Remove the specified label and its content, 
    while removing other labels but retaining their content.'''
    regex = '|'.join([r'<%s\b.*?</%s>|<%s\s*/>' %
                      (tag, tag, tag) for tag in tags])
    if default:
        regex += r'|</?([^ >/]+).*?>'
    retags = re.compile(regex, re.DOTALL | re.IGNORECASE)
    string = retags.sub('', html)
    return rm_ws(string, char)
