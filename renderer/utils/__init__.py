'''
    网络请求、解析等方法的工具库
'''

from .constants import DATETIME_12, DATETIME_24, HEADERS, WHITESPACE
from .formlib import extract_list, extract_string, is_table, parse_form
from .httplib import download, retry_get, retry_post, save_html
from .money import chinese_to_arabic
from .ocrlib import GeneralOcr
from .quick import contains, replace_all, replace_ws
