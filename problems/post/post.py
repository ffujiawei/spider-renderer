import json

from renderer import retry_post
from renderer.utils.constants import HEADERS

'http://ggzy.xjyl.gov.cn:83/jyxx/tradelist.html'

token = 'http://ggzy.xjyl.gov.cn:83/EpointWebBuilder/rest/getOauthInfoAction/getNoUserAccessToken'
data = retry_post(token).json()['custom']
access_token = data['access_token']

# 不可缺少，否则真的错哪都不知道
HEADERS['Authorization'] = 'Bearer %s' % access_token
HEADERS['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
HEADERS['Content-Type'] = 'application/json;charset=UTF-8'

post_url = 'http://ggzy.xjyl.gov.cn:83/EpointWebBuilder/rest/GetGgListAction/getZtbGgList'

# POST 请求数据为嵌套字典的情况

# 方法一：传字符串
data = 'params={"siteGuid":"7eb5f7f1-9041-43ad-8e13-8fcb82ea831a","title":"","categorynum":"001001","diqu":"654001","xmlx":"","cgfs":"","pageIndex":1,"pageSize":20}'

response = retry_post(post_url, data=data, headers=HEADERS)
response.request.headers
response.request.body   

# 通过阅读 Requests 和 Scrapy 的源码，
# 我发现两者对字符串数据都未做转义
# 等处理，传入是什么就是什么

# 方法二：字典放入引号中
formdata = {"params": '{"siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a", "title": "", "categorynum": "001001", "diqu": "654001", "xmlx": "", "cgfs": "", "pageIndex": 1, "pageSize": 20}'}

formdata = {"params": {"siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a", "title": "", "categorynum": "001001", "diqu": "654001", "xmlx": "", "cgfs": "", "pageIndex": 1, "pageSize": 20}}
from urllib.parse import urlencode
urlencode(formdata, doseq=True)

response = retry_post(post_url, data=urlencode(formdata), headers=HEADERS)
response = retry_post(post_url, data=formdata, headers=HEADERS)
response.request.headers
response.request.body

# 这样的话翻页就比较难弄了
# Requests 和 Scrapy 都会默认设置 application/x-www-form-urlencoded
# 而传入字符串情况下，必须自行设置该参数

# 方法三：直接取转义后的字符串
urlencode = 'params=%20%7B%22siteGuid%22%3A%227eb5f7f1-9041-43ad-8e13-8fcb82ea831a%22%2C%22title%22%3A%22%22%2C%22categorynum%22%3A%22001001%22%2C%22diqu%22%3A%22654001%22%2C%22xmlx%22%3A%22%22%2C%22cgfs%22%3A%22%22%2C%22pageIndex%22%3A1%2C%22pageSize%22%3A20%7D'

response = retry_post(post_url, data=urlencode, headers=HEADERS)
response.request.headers
response.request.body

# 通过 Postman 或浏览器就可以直接取得该字符串
# 自行转义失败在于相关函数不转义引号
# 唯一的问题是可读性差了点

# 通过这次深入理解，我恍然大悟，之前以为 Requests 和 Scrapy 在 POST 的数据上处理有区别，实际上还是自己了解不够，两者的处理殊途同归，仅在与传入 JSON 数据时有区别，Scrapy 没有针对 JSON 作特殊处理，而 Requests 有专门的 `json` 参数，总之特别注意 `Content-Type` 参数是必须的。

data = response.json()

json.dump(data, open('do.json', 'w', encoding='utf-8'), ensure_ascii=False)
