# 解决 VIEWSTATE 类型的网站

> 前几天帮同事研究一个特别的网站，不是很复杂，是常见的 ASPX 类型网站，但是又有一定程度的特殊性，就顺手记录一下 VIEWSTATE 类型网站的解决方案。

示例网站：

```
http://ggzyjy.cqspb.gov.cn/LBv3/n_newslist_zz_item.aspx?ILWHBNjF4cnt57FZxA1uhw=%3d
```

同事遇到的问题是永远只能请求到首页，而无法请求到下一页的数据，当时我随便看了一下请求过程，该网页很特别，无法跳转到指定页数，而只能循环传入“下一页”这个参数。

那么只能按这种方法进行了，但在实际调试过程中，我发现了请求这同一个网址，分别用 Postman/浏览器和 Requests，得到的结果源代码居然不一样，Requests 无法获取正确的 VIEWSTATE 值。

```powershell
>>> from renderer.utils import retry_get, retry_post
>>> url = r'http://ggzyjy.cqspb.gov.cn/LBv3/n_newslist_zz_item.aspx?ILWHBNjF4cnt57FZxA1uhw=%3d'       
>>> resp = retry_get(url)
>>> response = html.fromstring(resp.text)
>>> __VIEWSTATE = response.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
>>> __VIEWSTATE
'/wEPDwULLTEyNTI0OTk5NTBkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBRZuX3NlYXJjaDEkc2VhcmNoQnV0dG9ulHABVGSM/zsAVDdj/ajVVSLpXtEo/tSE9fdWEPkJCwI='
```

明显过短了，是错误的。

我知道 Requests 和 Scrapy 在处理 URL 时，结果并不总是一致的，那么与浏览器的处理逻辑也未必相同，于是我开始怀疑是 URL 的问题。直觉告诉我 `%3d` 这个字符很可能有问题，因为它是已经被转义过了，极有可能 Requests 处理时进行了再次转义（仅是猜测，不过我最终还是懒得验证了）。

```powershell
>>> from urllib.parse import unquote
>>> unquote('%3d')
'='
```

那么就将这个字符还原，再次请求尝试：

```powershell
>>> url = r'http://ggzyjy.cqspb.gov.cn/LBv3/n_newslist_zz_item.aspx?ILWHBNjF4cnt57FZxA1uhw=='       
>>> resp = retry_get(url)
>>> response = html.fromstring(resp.text)
>>> __VIEWSTATE = response.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
>>> __VIEWSTATE
'/wEPDwUKMTAzMjQ5MzEyNw9kFgJmD2QD......'
```

得到了很长的一段字符串，这回是对的，之后也得到了正确的数据，问题就这样迎刃而解了。

再顺手写一下  VIEWSTATE 类型的网站的解决办法吧。

```python
__VIEWSTATE = response.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
__EVENTVALIDATION = response.xpath('//input[@id="__EVENTVALIDATION"]/@value')[0]
formdata = {
    '__VIEWSTATE': __VIEWSTATE,
    '__EVENTVALIDATION': __EVENTVALIDATION,
    'ctl00$n_search1$searchBox': '',
    'ctl00$ContentPlaceHolder2$F3': '下一页',
}
resp = retry_post(url, data=formdata)
```

这一类型的网站基本都是这样处理的，而这个示例网址估计已经是最特殊的了，每次请求下一页都必须获取当前页的 VIEWSTATE，而一般情况下取首页的即可。

我是一个既渴望被关注，又害怕被关注的人。我总是小心翼翼地隐藏着自己，生怕别人发现了我的存在，却又偷偷在某个角落尽情展示自己，希望引来他人的欣赏。这样的我，无法在职场上生存，无法在社会上生存。再过几天我就必须离开现在的公司，继续去痛苦地寻找工作了，我不是千里马，我不奢求伯乐，我知道我所面临的人生低谷恐怕还在路上。
