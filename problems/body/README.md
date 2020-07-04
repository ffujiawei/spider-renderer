# 记录一种特别的 POST 请求方式

这个问题是很久以前了（其实也就大概三个星期前），当时略被困扰，但很快还是发现了问题所在，然后顺利解决了。之所以今天写下来，是因为这几天我在整理勉强一个月的实习经历中学到的东西和经验的总结。

顺带说一下，我把我很多工作中自己写的辅助用的函数工具打包开源了，包括网页表格解析函数、文本处理函数等。

项目地址：

```
https://github.com/ffujiawei/spider-renderer
```

安装方式：

```powershell
>>> pip install -U spider-renderer
```

言归正传，这种特别的 POST 请求方式在于数据的附带方法，对于 Requests 而言，是看不出区别的，因为源码的处理方法非常好，无论怎么写都是可以的。请求数据可以写成字典传入，或者下面的字符串形式（这个我好像还是从 Requests 导出的，有兴趣自己动手实践一下就知道了，我不想复现了）。

```python
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
```

但是，对于 Scrapy 而言，就有问题了，用 `scrapy.FormRequest` 的方式传入字典结构的数据是错误的，然后用 `scrapy.Request` 的方式将字典传入 `body` 参数也是不行的，最后我的解决方法就是从 Requests 导出上面的字符串，传入 `body` 参数才最终成功了。
