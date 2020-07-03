'''
    百度图片文字识别接口封装
'''

import base64

from .httplib import HEADERS, retry_get, retry_post


class GeneralOcr(object):
    '''通用文字识别，而非精确识别接口'''

    __client_id = 'yIDSsYZD1uk1OcdOmuaSDYsZ'
    __client_secret = '5rqZhYFgs2VQcLXRNMNeQSWIeqexVajc'

    def __init__(self, client_id=None, client_secret=None, access_token=None):
        self.client_id = client_id or self.__client_id
        self.client_secret = client_id or self.__client_secret
        self.access_token = access_token or self.oauth()

    @classmethod
    def oauth(cls, client_id=None, client_secret=None):
        client_id = client_id or cls.__client_id
        client_secret = client_secret or cls.__client_secret
        oauth_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
        oauth_data = retry_get(oauth_url).json()
        return oauth_data['access_token']

    def basic_general(self, image):
        general = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={self.access_token}"
        data = {'image': base64.b64encode(image)}
        HEADERS['Content-Type'] = 'application/x-www-form-urlencoded'
        resp = retry_post(general, data=data, headers=HEADERS)
        return resp.json() if resp else ({'words_result': '请求错误'})

    def basic_ocr(self, addr, sep='\n'):
        if addr.startswith('http'):
            if addr.endswith('png') or addr.endswith('jpg'):
                resp = retry_get(addr)
                image = resp.content if resp else b''
            else:
                pass
        else:
            with open(addr, 'rb') as fp:
                image = fp.read()
        _wds = self.basic_general(image).get('words_result', tuple())
        wds = ''
        for _wd in _wds:
            wds += _wd.get('words', '') + sep
        return wds
