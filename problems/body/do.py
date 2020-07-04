import json

from renderer import retry_post
from renderer.utils.constants import HEADERS

# 该参数是必须的
HEADERS['Content-Type'] = 'application/json;charset=UTF-8'

home_url = 'http://jtj.xa.gov.cn'
post_url = 'http://jtj.xa.gov.cn/api/doService'
secret = 'b6ca7329-c5f2-4115-a1bb-d289d3f646d2'

body = '''{\n \"srvId\": \"getPubStatusResService\",\n \"data\": {\n \"id\": \"%s\",\n \"pageIndex\": \"%d\",\n \"pageSize\": 300,\n \"searchWord\": \"\"\n }\n}'''

response = retry_post(post_url, data=body % (secret, 1), headers=HEADERS)
data = response.json()

json.dump(data, open('do.json', 'w', encoding='utf-8'), ensure_ascii=False)
