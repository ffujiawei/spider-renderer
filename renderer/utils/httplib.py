'''
    常用的 HTTP 请求——封装了发生错误时重试的功能
'''

import logging
from time import sleep, time

import requests

from .constants import HEADERS, STATUS_CODES, TIMEOUT

# 设置日志
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s %(message)s'
)

# 禁用SLL证书警告
requests.urllib3.disable_warnings()


# 发生错误时再次请求
def retry_request(method, url, retries=3, **kwargs):
    retry = 1
    kwargs.update({
        'headers': kwargs.get('headers', HEADERS),
        'timeout': kwargs.get('timeout', TIMEOUT),
        'verify': kwargs.get('verify', False),
    })
    while True:
        try:
            resp = requests.request(method, url, **kwargs)
            if resp.status_code in STATUS_CODES:
                return resp
            if retry >= retries:
                logging.warning(f"[{resp.status_code}]: {url}")
                return False
            retry += 1
        except Exception as error:
            if retry >= retries:
                logging.error(f"{error}: {url}")
                return False
            retry += 1
            sleep(3)  # 发生错误时休眠若干秒


def retry_get(url, retries=3, **kwargs):
    return retry_request('GET', url, retries=retries, **kwargs)


def retry_post(url, data=None, retries=3, **kwargs):
    return retry_request('POST', url, data=data, retries=retries, **kwargs)


# 下载文件
def download(src, dst, retries=8, **kwargs):
    resp = retry_get(src, retries, **kwargs)
    if resp:
        with open(dst, 'wb') as f:
            f.write(resp.content)
        logging.info(src)


# 将请求数据写入文件
def save_html(response, fn='default.html'):
    if not fn.endswith('.html'):
        fn = '%s.html' % fn
    with open(fn, 'wb') as fp:
        fp.write(response.content)
