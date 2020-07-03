'''
    常用的 HTTP 请求——封装了发生错误时重试的功能
'''

import logging
from time import sleep, time

import requests

from .constants import HEADERS, TIMEOUT

# 设置日志
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s %(message)s'
)

# 禁用SLL证书警告
requests.urllib3.disable_warnings()


# 发生错误时再次请求，默认重试 3 次
def retry_get(url, m=3, headers=HEADERS, proxies=None, timeout=TIMEOUT):
    c = 1
    while True:
        try:
            resp = requests.get(url, headers=headers, proxies=proxies,
                                timeout=timeout, verify=False)
            if resp.status_code == 200:
                return resp
            if c >= m:
                logging.warning(f"[{resp.status_code}]: {url}")
                return False
            c += 1
        except Exception as error:
            if c >= m:
                logging.error(f"{error}: {url}")
                return False
            c += 1
            # 发生延时、最大请求数量等错误时休眠若干秒
            sleep(3)


def retry_post(url, data=None, m=3, headers=HEADERS, proxies=None, timeout=TIMEOUT):
    c = 1
    while True:
        try:
            resp = requests.post(url, data=data, headers=headers, proxies=proxies,
                                 timeout=timeout, verify=False)
            if resp.status_code == 200:
                return resp
            if c >= m:
                logging.warning(f"[{resp.status_code}]: {url}")
                return False
            c += 1
        except Exception as error:
            if c >= m:
                logging.error(f"{error}: {url}")
                return False
            c += 1
            # 发生延时、最大请求数量等错误时休眠若干秒
            sleep(3)


# 下载文件，默认重试 8 次
def download(src, dst, headers=HEADERS, proxies=None, timeout=TIMEOUT):
    resp = retry_get(src, 8, headers, proxies, timeout)
    if resp:
        with open(dst, 'wb') as f:
            f.write(resp.content)
        logging.info(src)


# 将请求数据写入文件，默认将网页标题作为文件名
def save_html(response, fn='default.html'):
    if not fn.endswith('.html'):
        fn = '%s.html' % fn
    with open(fn, 'wb') as fp:
        fp.write(response.content)
