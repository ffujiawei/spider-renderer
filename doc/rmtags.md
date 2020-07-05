# 移除 HTML 标签获取全部文本的三种方法对比

示例网址：

```powershell
>>> url = 'https://mengso.com/'

>>> from renderer.utils import retry_get
>>> response = retry_get(url)
>>> string = response.content.decode('utf-8')
```

1. 通过 lxml 语法的 string() 函数

```powershell
>>> from lxml import html
>>> html.fromstring(string).text_content()
"\n\n萌搜 为小众而搜\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwindow.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\ngtag('config', 'UA-58427671-26');\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n设为首页\n所有产品\n分享萌搜 SHARE\n服务条款\n关于我们\n不良信息举报\n广告投放\n\n\n\n\n\n皖ICP备18013804号-3\xa0/\xa0公安网备34150102000224\n\n© 2020 萌搜 mengso.com\xa0/\xa0违法举报\n\n\n\n\n$(document).ready(function(){ssl_pre();})\n\n"
```

> 这种方法有时候莫名其妙获取不到一些文本，比如深度嵌套的，遇到这种情况我一般就用下面的方法。

2. 通过 w3lib.html 中的 remove_tags() 函数

```powershell
>>> from w3lib.html import remove_tags
>>> remove_tags(string)
"\n\n\n萌搜 为小众而搜\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwindow.dataLayer = window.dataLayer || [];\nfunction gtag(){dataLayer.push(arguments);}\ngtag('js', new Date());\ngtag('config', 'UA-58427671-26');\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n设为首页\n所有产品\n分享萌搜 SHARE\n服务条款\n关于我们\n不良信息举报\n广告投放\n\n\n\n\n\n皖ICP备18013804号-3&nbsp;/&nbsp;公安网备34150102000224\n\n© 2020 萌搜 mengso.com&nbsp;/&nbsp;违法举报\n\n\n\n\n$(document).ready(function(){ssl_pre();})\n\n\n"
```

> 这种方法基本可以满足需求了，但仍有让人不满意的地方，比如混入了许多 JavaScript 代码，因此我决定自己实现一个函数。

3. 我写的利用正则方式清除标签的方法

```powershell
>>> from renderer.utils import rm_tags
>>> rm_tags(string, '\n')
'\n设为首页\n所有产品\n分享萌搜SHARE\n服务条款\n关于我们\n不良信息举报\n广告投放\n皖ICP备18013804号-3/公安网备34150102000224\n©2020萌搜mengso.com/违法举报\n'

>>> rm_tags(string)
'设为首页所有产品分享萌搜SHARE服务条款关于我们不良信息举报广告投放皖ICP备18013804号-3/公安网备34150102000224©2020萌搜mengso.com/违法举报'
```

> 默认只提取正文内容，'\n' 是自定义的分隔符，如何实现可以看源码，
