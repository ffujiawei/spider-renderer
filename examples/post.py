import base64

from renderer import retry_get, retry_post

post_url = 'http://www.wszf.gov.cn/xjcms/openapi/t/info/list.do'
formdata = {
    'channelid': 'MTI2Ng==',
    'pagesize': 'MTU=',
}
pageno = str(1).encode('utf-8')
formdata['pageno'] = base64.b64encode(pageno)
response = retry_post(post_url, data=formdata)

post_url = 'http://www.wszf.gov.cn/xjcms/openapi/t/info/list.do'
response = retry_post(post_url)
