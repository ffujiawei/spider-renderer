import re
from urllib.parse import urljoin

import requests
from renderer.utils.constants import HEADERS


def string_to_hex(string, val=""):
    for i in range(len(string)):
        val += hex(ord(string[i]))[2:]
    return val


def gen_cookie(url):
    return {"srcurl": string_to_hex(url), "path": "/"}

location = re.compile(r'''location = "(\S+)"''')

origin = 'http://www.xjbl.gov.cn/zdlygk/zfcgztb/zbgg1.htm'
origin = 'http://www.xjbl.gov.cn/zdlygk/zfcgztb/zbgg1/%d.htm' % 2

session = requests.session()
session.headers = HEADERS

# 首次请求
resp1 = session.get(origin)
loc1 = location.findall(resp1.text)[0]
verify_url = urljoin(origin, loc1 + '313932302c31303830')
session.cookies.update(gen_cookie(origin))

# 二次请求
resp2 = session.get(verify_url)
loc2 = location.findall(resp2.text)[0]

# 三次请求
resp3 = session.get(urljoin(origin, loc2))
resp3.content.decode('utf-8')
