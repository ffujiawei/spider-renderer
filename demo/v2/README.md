# 模块化爬虫模板系统 v2 简明教程

模块化爬虫模板系统，我的设想是将爬虫程序拆分到最小粒度，即拆分为基本信息、请求翻页解析、详情页解析等功能模块，然后编写基本模板，比如表格解析、文本解析和图片解析等方法的模板，遇到类似网页时只需选取已有的模板进行自由组合即可，今后遇到新的页面形式，只需编写新的解析模块。

这个星期日，我在阅读了 Jinja2 的部分源码后终于实现了自由组合模板的功能，在这之前，模板的组合从模板写成之时就固定了，除非修改模板，否则无法自由组合。

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

支持 Jinja2 语法的 `block`、`extends` 和 `include`，不过模板间的自由组合真的特别考验一个人的逻辑思维。

比如，我现在用的模板构建组合流，容易绕晕，逻辑差的还得打打草稿：

```python
loader.include_left('head.tmpl')  # 头部
​
# --------------------组合--------------------
​
# 翻页请求
loader.include_left('start.tmpl')  # 普通翻页请求
# loader.include_left('start_aspx.tmpl')  # ASPX 类型翻页请求
​
# 详情页请求
loader.include_left('parse.tmpl')  # 普通详情页请求
​
# 详情页解析
loader.include_left('parse2.tmpl')  # 详情页解析公共头部
​
# --------------------基模板--------------------
​
# 表格解析
templatefile = 'parse2_fm1.tmpl'  # 基模板
# templatefile = 'parse2_fm2.tmpl'  # 基模板
​
# 文本解析
# templatefile = 'parse2_wd_head.tmpl'  # 基模板
​
# 图片解析
# templatefile = 'parse2_img.tmpl'  # 基模板
​
if 'fm' in templatefile:
    # 表格解析
    # loader.include_left('parse2_img.tmpl')  # 添加图片解析部分
    loader.include_left('parse2_wd_head.tmpl')  # 文字解析头部
    loader.include_left('parse2_fm.tmpl')  # 表格解析公共头部
elif 'img' in templatefile:
    # 图片解析
    loader.include('parse2_wd_head.tmpl')  # 文字解析头部
​
loader.include('parse2_wd_foot.tmpl')  # 文字解析尾部
```

`block` 和 `extends` 相对难理解，不推荐用了。
