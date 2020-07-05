'''
    模块化爬虫模板系统简单示例
''' 

import os
import os.path

from renderer import genspider

basepath = os.path.abspath(os.path.dirname(__file__))
dst = os.path.join(basepath, 'spiders')
templates_folder = os.path.join(basepath, 'templates')

if not os.path.isdir(dst):
    os.mkdir(dst)

templatefile = 'parser.tmpl'
spider = 'fonts_spider'

home_url = '''
http://fonts.mobanwang.com/fangzheng/
'''.strip()

page_url = '''
http://fonts.mobanwang.com/fangzheng/List_%d.html
'''.strip()

regex = r'''
href=['"](\S+?html?)['"][^<>]*?title=['"]
'''.strip()


kwargs = {
    'all_page': 20,
    'page_url': page_url,
    'regex': regex,
    'templates_folder': templates_folder,
    'author': 'White Turing',
}

genspider(home_url, templatefile, dst, spider, **kwargs)
