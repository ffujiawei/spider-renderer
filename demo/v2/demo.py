import os

from renderer import ModularLoader, genspider

basepath = os.path.abspath(os.path.dirname(__file__))
dst = os.path.join(basepath, 'spiders')
templates_folder = os.path.join(basepath, 'templates')
loader = ModularLoader(templates_folder)

if not os.path.isdir(dst):
    os.mkdir(dst)

# 这里请特别注意：基模板不可以被继承或包含
# 否则将导致循环引用错误
templatefile = 'requests.tmpl'  # 基模板

# 模板的自由组合
loader.include_left('header.tmpl')  # 加在基模板内容之前
loader.include('parser.tmpl')  # 加在基模板内容之后

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
    'loader': loader,
    'all_page': 20,
    'page_url': page_url,
    'regex': regex,
    'templates_folder': templates_folder,
    'author': 'White Turing',
}

genspider(home_url, templatefile, dst, spider, **kwargs)
