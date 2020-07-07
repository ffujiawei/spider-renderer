'''
    常用的 HTTP 请求——封装了发生错误时重试的功能
'''

import logging
from os import makedirs, path
from time import sleep, time

import requests

from .constants import HEADERS, STATUS_CODES, TIMEOUT

# 设置日志
logger = logging.getLogger("httplib")
handler = logging.StreamHandler()
# 日志格式
formatter = logging.Formatter("%(levelname)s %(message)s")
# 日志级别
handler.setLevel(logging.WARNING)
handler.setFormatter(formatter)
logger.addHandler(handler)

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
                logger.warning(f"[{resp.status_code}]: {url}")
                return resp
            retry += 1
        except Exception as error:
            if retry >= retries:
                logger.error(f"{error}: {url}")
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
        logger.info(src)


# 下载文件且以时间戳命名文件
def download_file(src, folder='.'):
    '''Download the file and name the file with a timestamp.'''
    if not path.isdir(folder):
        makedirs(folder)
    ext = path.splitext(src)[-1]
    dst = path.join(folder, f'{int(time())}{ext}')
    download(src, dst)
    return dst


# 将请求数据写入文件
def save_html(response, fn='default.html'):
    if not fn.endswith('.html'):
        fn = '%s.html' % fn
    with open(fn, 'wb') as fp:
        fp.write(response.content)
