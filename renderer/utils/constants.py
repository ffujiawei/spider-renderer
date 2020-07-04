'''
    常量，建议大写
'''

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
}

PROXIES = {
    'http': 'http://127.0.0.1:8118',
    'https': 'https://127.0.0.1:8118',
}

TIMEOUT = 36

# 可处理的状态码
STATUS_CODES = [200, 521]

# 常见的网页空格符号
WHITESPACE = ('\xa0', '\u3000', '\x0c', '&nbsp;', ' ')

# 一般无有效数据的标签
USELESS_TAGS = ('script', 'style', 'input', 'iframe', 'head')

# 格式化时间
DATETIME_12 = r'%Y-%m-%d %I:%M:%S %p'  # 2020-07-02 08:17:54 AM
DATETIME_24 = r'%Y-%m-%d %H:%M:%S'  # 2020-07-02 21:29:33
