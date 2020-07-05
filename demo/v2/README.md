# 模块化爬虫模板系统 v2 简明教程

未必有人看，就写简单点吧。

```python
import os
from renderer import ModularLoader, genspider

basepath = os.path.abspath(os.path.dirname(__file__))
dst = os.path.join(basepath, 'spiders')
templates_folder = os.path.join(basepath, 'templates')

loader = ModularLoader(templates_folder)

# 这里请特别注意：基模板不可以被继承或包含
# 否则将导致循环引用错误
templatefile = 'requests.tmpl'  # 基模板

# 模板的自由组合
loader.include_left('header.tmpl')  # 加在基模板内容之前
loader.include('parser.tmpl')  # 加在基模板内容之后

spider = 'spider'
home_url = '''
http://fonts.mobanwang.com/fangzheng/
'''.strip()

kwargs = {
    'loader': loader,
    'templates_folder': templates_folder,
    'author': 'White Turing',
}

genspider(home_url, templatefile, dst, spider, **kwargs)
```

支持 Jinja2 语法的 `extends` 和 `include`。
