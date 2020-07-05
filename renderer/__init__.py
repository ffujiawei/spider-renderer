'''Building a modular crawler template system based on Jinja2'''

import re
import warnings
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from .utils import (replace_all, replace_ws, retry_get, retry_post, rm_tags,
                    rm_ws)
from .utils.constants import DATETIME_12, WHITESPACE


class ModularLoader(FileSystemLoader):

    def __init__(self, searchpath, encoding="utf-8", followlinks=False):
        if not isinstance(searchpath, (tuple, set, list)):
            searchpath = [searchpath]
        self.searchpath = searchpath
        self.encoding = encoding
        self.followlinks = followlinks
        self.templates = []
        self.flag = False
        self.head, self.body, self.foot = '', '', ''

    def get_source(self, environment, template):
        x, y, z = super().get_source(environment, template)
        if self.flag:
            return x, y, z
        self.flag = True
        return self.head+self.body+x+self.foot, y, z

    def extends(self, templates):
        if not isinstance(templates, (tuple, set, list)):
            templates = (templates,)
        ext = ''
        for template in templates:
            ext += '{% extends "template" %}\n'.replace('template', template)
        self.head = ext + self.head

    def include(self, templates, left=False):
        if not isinstance(templates, (tuple, set, list)):
            templates = (templates,)
        ext = ''
        for template in templates:
            ext += '{% include "template" %}\n'.replace('template', template)
        if left:
            self.body += ext
        else:
            self.foot += ext

    def include_left(self, templates):
        self.include(templates, left=True)

    def add_block(self, block):
        self.body += '{%- block bk -%}\n'.replace('bk', block)
        self.foot = '{%- endblock bk -%}\n'.replace('bk', block) + self.foot

    def reset(self):
        self.flag = False
        self.head, self.body, self.foot = '', '', ''


def render_templatefile(dst, templatefile, **kwargs):
    default_loader = FileSystemLoader(
        kwargs.pop('templates_folder', './templates'))
    env = Environment(loader=kwargs.pop('loader', default_loader))
    template = env.get_template(templatefile)
    with open(dst, 'w', encoding='utf-8') as fp:
        fp.write(template.render(**kwargs))


# 可根据实际需求修改部分代码
def genspider(home_url, templatefile, dst, spider, **kwargs):
    response = retry_get(home_url)
    if not response:
        raise Exception('Request failed, invalid URL or parameter.')

    try:
        string = response.content.decode('utf8')
    except UnicodeDecodeError:
        string = response.content.decode('gbk')

    source = re.findall(r'(?is)<title>(.*?)</title>', string)[0]

    # 清理标题中的干扰字符
    clear_chars = kwargs.pop('clear_chars', WHITESPACE)
    source = re.sub(r'\s', '', replace_all(source, clear_chars + WHITESPACE))

    # 仅供参考，建议自行修改
    kwargs.update({
        'datetime': datetime.now().strftime(DATETIME_12),
        'spider': spider,
        'source': source,
        # 'region': replace_all(source, list(kwargs.get('city', '')))[:3] if spider[5] != '0' else '',
        'home_url': home_url,
        'author': kwargs.pop('author', 'White Turing'),
    })

    spiderfile = f'{dst}/{spider}.py'
    render_templatefile(spiderfile, templatefile, **kwargs)
