# 基于 Jinja2 构建模块化爬虫模板系统

- [模块化爬虫模板系统设想提出的前因后果](doc/blog.md)
- [解析网页表格的两种方法](doc/form.md)
- [破解 MD5 签名参数验证](problems/sign/README.md)
- [移除 HTML 标签获取全部文本的三种方法对比](doc/rmtags.md)
- [解决必须执行 JS 计算 Cookie 的问题](problems/521/README.md)
- [记录一种特别的 POST 请求方式](problems/body/README.md)
- [深入理解 POST 请求数据的处理过程](problems/post/README.md)
- [解决 VIEWSTATE 类型的网站](problems/viewstate/README.md)

本来打算就写写题目所说的，但是后来我还是决定就全放在这个项目里了，于是这个项目就变成了我一个月实习经历的经验总结。我把我很多工作中自己写的辅助用的函数工具都放到了其中，包括网页表格解析函数、文本处理函数等，另外就是记录了遇到的比较特殊的问题的解决方法。

**可实现模板外自由组合的新版本已经发布**，详细说明见 [v2 简明教程](demo/v2/README.md)，这样的话基本实现了我最初的设想，然而开心不起来。。。

- **安装方式**：

```shell
pip install -U spider-renderer
```

- **简单模板文件示例**：

`header.tmpl`

```python
'''Rendered on {{datetime}}'''

import re
import scrapy

class NewspiderSpider(scrapy.Spider):

    name = '{{spider}}'
    source = '{{source}}'
    url = '{{home_url}}'
    author = '{{author}}'
    all_page = {{all_page}}
```

`requests.tmpl`

```python
    def start_requests(self):
        url = '{{page_url}}'
        all_page = self.all_page or 10
        for page in range(1, all_page):
            yield scrapy.Request(url % page, callback=self.parse)
```

`parser.tmpl`

```python
{% include "header.tmpl" %}
{% include "requests.tmpl" %}

    def parse(self, response):
        response.string = re.sub('[\r\n\t\v\f]', '', response.text)
        rows = re.findall(r'''{{regex}}''', response.string)
```

- **渲染生成程序示例**：

```python
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
```

这个示例没有用到稍微复杂的 Jinja2 语法，但实际可以通过加入一些条件判断，让模板的包容性更广一点。
