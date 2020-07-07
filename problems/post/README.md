# 深入理解 POST 请求数据的处理过程

之前遇到过类似的问题，但当时还是一知半解。今天再次阅读了 Requests 和 Scrapy 有关 POST 请求数据的处理源码，才终于彻底明白了。

示例网址：

```
http://ggzy.xjyl.gov.cn:83/jyxx/tradelist.html
```

该网站请求时必须带 `Authorization` 参数，而且几分钟就过期，必须再次获取该参数。这让我困扰了一会儿，最后发现了解决方法，就是等它过期，找到过期后请求的网址。

```python
>>> token = 'http://ggzy.xjyl.gov.cn:83/EpointWebBuilder/rest/getOauthInfoAction/getNoUserAccessToken'
>>> data = retry_post(token).json()['custom']
>>> access_token = data['access_token']
>>> access_token
'31abbd15f40e749fa401a4ac51121ca2'
```

另一个问题就是这个网站 POST 请求带的数据是一个嵌套的字典，虽然知道处理方法，但觉得不够优雅而且不理解为什么该这样，所以我决定好好做一下实验，读一读相关源码。

原始请求数据：

```python
formdata = {"params": {"siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a", "title": "", "categorynum": "001001", "diqu": "654001", "xmlx": "", "cgfs": "", "pageIndex": 1, "pageSize": 20}}
```

## 方法一：传入词典

试试进行 URL 编码处理：

```python
>>> from urllib.parse import urlencode
>>> urlencode(formdata)
'params=%7B%27siteGuid%27%3A+%277eb5f7f1-9041-43ad-8e13-8fcb82ea831a%27%2C+%27title%27%3A+%27%27%2C+%27categorynum%27%3A+%27001001%27%2C+%27diqu%27%3A+%27654001%27%2C+%27xmlx%27%3A+%27%27%2C+%27cgfs%27%3A+%27%27%2C+%27pageIndex%27%3A+1%2C+%27pageSize%27%3A+20%7D'
```

而实际上，Requests 和 Scrapy 内部实现的 URL 编码是这样的：

```python
>>> urlencode(formdata, doseq=True)
'params=siteGuid&params=title&params=categorynum&params=diqu&params=xmlx&params=cgfs&params=pageIndex&params=pageSize'
```

这造成了严重的问题，导致直接传入嵌套字典进行 POST 请求是错误。

因此，必须将嵌套的字典放入引号中，即：

```python
>>> formdata = {"params": '{"siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a", "title": "", "categorynum": "001001", "diqu": "654001", "xmlx": "", "cgfs": "", "pageIndex": 1, "pageSize": 20}'}
>>> urlencode(formdata, doseq=True)
'params=%7B%22siteGuid%22%3A+%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C+%22title%22%3A+%22%22%2C+%22categorynum%22%3A+%22001001%22%2C+%22diqu%22%3A+%22654001%22%2C+%22xmlx%22%3A+%22%22%2C+%22cgfs%22%3A+%22%22%2C+%22pageIndex%22%3A+1%2C+%22pageSize%22%3A+20%7D'
```

如此才得到了正确的结果。

在这种方法中，由于 Requests 和 Scrapy 判断出是表单数据，默认设置了 `Content-Type` 参数，就不会发生下面介绍的两种方法会发生的错误。

然而，这种方法问题在于翻页处理变得不够优雅了，因为页数设置在嵌套的字典里。

## 方法二：传入字符串

修改原始字典数据为下面的形式：

```python
data = 'params={"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","title":"","categorynum":"001001","diqu":"654001","xmlx":"","cgfs":"","pageIndex":1,"pageSize":20}'
```

然后直接传入 Requests 的 `data` 参数或 Scrapy 的 `body` 参数，通过阅读源码，我发现两者对于字符串数据都未做任何转义编码处理，传入什么就是什么。这种方法，必须手动设置 `Content-Type` 参数：

```python
headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
```

否则服务器不会返回正确数据。

## 方法三：传入转义后的字符串

通过 Postman 、浏览器或者上文中的 `urlencode` 函数对嵌套字典编码，就可以直接取得该字符串，一般就是这样的：

```python
data = 'params=%20%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22title%22%3A%22%22%2C%22categorynum%22%3A%22001001%22%2C%22diqu%22%3A%22654001%22%2C%22xmlx%22%3A%22%22%2C%22cgfs%22%3A%22%22%2C%22pageIndex%22%3A1%2C%22pageSize%22%3A20%7D'
```

问题在于可读性差了点，其实与传入字符串方法无异，同样必须手动设置 `Content-Type` 参数。

​Requests 和 Scrapy 在 POST 的数据处理上，Scrapy 分成了 FromRequest 和 Request 方法，而 Requests 不作特别的区分，两者仅在传入 JSON 数据时有区别，Scrapy 没有针对 JSON 作特殊处理，而 Requests 有专门的 `json` 参数，请求数据是字符串时，Scrapy 传入 `body` 参数即可，这种情况下特别注意 `Content-Type` 参数是必须的，[之前的文章](../body/README.md)，就是这种情况，当时不甚理解。
