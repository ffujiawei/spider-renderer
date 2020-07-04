'''Parsing HTML forms.'''

import re
import warnings

from lxml import html

from .htmlib import rm_ws
from .httplib import retry_get
from .quick import contains


# 判断表格是否包含相关数据
def is_table(tables, within, without):
    '''Determine whether the table contains relevant data.'''
    is_tab, table = False, None
    for table in tables:
        string = re.sub(r'\s', '', table.text_content())
        if contains(string, within, without):
            is_tab = True
            break
    return is_tab, table


# 提取表格全部文本
def extract_string(table) -> str:
    '''Extract all text in the table.'''
    return rm_ws(table.text_content())


# 按行按列提取表格文本放入元组列表
def extract_list(table) -> list:
    '''Extract the table text by row and column and put it into the tuple list.'''
    rows = table.xpath('tr | */tr')
    form = []
    for row in rows:
        cols = row.xpath('td | th')
        res = []
        for col in cols:
            res.append(rm_ws(col.text_content(), ''))
        if res:
            form.append(tuple(res))
    return form


# 打包全部操作
def parse_form(form_url, within, without=tuple(), encoding='utf-8', sep='</t', to_list=False):
    response = retry_get(form_url)
    if not response:
        raise Exception('Request failed, invalid URL or parameter.')

    string = response.content.decode(encoding)
    elements = html.fromstring(string.replace(sep, '\n'+sep))

    tables = elements.xpath('//table')  # 找到全部表格
    is_tab, table = is_table(tables, within, without)
    if is_tab:
        return extract_list(table) if to_list else extract_string(table)

    warnings.warn('Cannot find table with required data.')
    return False
