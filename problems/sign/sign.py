'''
    破解 MD5 签名参数验证
'''
import json
import re
import time

from lxml import html
from renderer import retry_post

# 网站首页
base_url = "https://www.yungang.gov.cn/infoDetailIm?typeId=7b1d8ce6354c45e9bc01656c96a1dbac&typeIdDetail=7b1d8ce6354c45e9bc01656c96a1dbac"

# POST 请求网址
url = "https://www.yungang.gov.cn/yungang-cms-api/manage/scContentItem/dataGrid"

formdata = {"page": "2",
            "typeId": "0105a14a090044b8b6f8cf743f3327fb",
            "limit": "10",
            "timestamp": str(int(time.time()*1000)), }


# 计算 MD5 签名
def sign(formdata):
    import hashlib
    string = "77029991-78cc-44ea-9656-5b388ed11795"
    keys = sorted(formdata.keys())
    for key in keys:
        string += key + formdata[key]
    string += "77029991-78cc-44ea-9656-5b388ed11795"
    h = hashlib.md5()
    h.update(string.encode('utf-8'))
    return h.hexdigest().upper()


# 添加签名字段
formdata['sign'] = sign(formdata)
response = retry_post(url, data=formdata)

# response.request.body
# 'page=2&typeId=0105a14a090044b8b6f8cf743f3327fb&limit=10&timestamp=1592319348420&sign=A35BA765A83FC55DB5E513478A2F88CB'

data = response.json()
json.dump(data, open('sign.json', 'w', encoding='utf-8'), ensure_ascii=False)
