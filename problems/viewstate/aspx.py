import json
import re
from urllib.parse import unquote

from lxml import html
from renderer.utils import retry_get, retry_post

# 转义后的网址
url = r'http://ggzyjy.cqspb.gov.cn/LBv3/n_newslist_zz_item.aspx?ILWHBNjF4cnt57FZxA1uhw=%3d'
resp = retry_get(url)
response = html.fromstring(resp.text)
__VIEWSTATE = response.xpath('//input[@id="__VIEWSTATE"]/@value')[0]

# 还原字符
unquote(r'%3d')

# 还原后的网址
url = r'http://ggzyjy.cqspb.gov.cn/LBv3/n_newslist_zz_item.aspx?ILWHBNjF4cnt57FZxA1uhw=='
resp = retry_get(url)
response = html.fromstring(resp.content.decode('utf-8'))
__VIEWSTATE = response.xpath('//input[@id="__VIEWSTATE"]/@value')[0]
__EVENTVALIDATION = response.xpath('//input[@id="__EVENTVALIDATION"]/@value')[0]

post_url = 'http://ggzyjy.cqspb.gov.cn/LBv3/n_newslist_zz_item.aspx?ILWHBNjF4cnt57FZxA1uhw=='

formdata = {
    '__VIEWSTATE': __VIEWSTATE,
    '__EVENTVALIDATION': __EVENTVALIDATION,
    'ctl00$n_search1$searchBox': '',
    'ctl00$ContentPlaceHolder2$F3': '下一页',
}

resp = retry_post(post_url, data=formdata)
