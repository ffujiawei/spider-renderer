# 解决 Security Verify 参数“云锁”问题

今天又遭遇了一个 JavaScript 设置验证相关参数的问题，这次必须请求三次才能得到最终结果，还挺有意思的，值得记录下来。

示例网址：

```
http://www.xjbl.gov.cn/zdlygk/zfcgztb/zbgg1.htm
```

首次请求，返回主体如下结果：

```js
function stringToHex(str) {
    var val = "";
    for (var i = 0; i < str.length; i++) {
        if (val == "") val = str.charCodeAt(i).toString(16);
        else val += str.charCodeAt(i).toString(16);
    } return val;
}

function YunSuoAutoJump() {
    var width = screen.width;
    var height = screen.height;
    var screendate = width + "," + height;
    var curlocation = window.location.href;
    if (-1 == curlocation.indexOf("security_verify_")) { document.cookie = "srcurl=" + stringToHex(window.location.href) + ";path=/;"; }
    self.location = "/zdlygk/zfcgztb/zbgg1/1.htm?security_verify_data=" + stringToHex(screendate);
}
```

由于这次的函数是固定的，可以直接模拟进行计算：

```python
def string_to_hex(string, val=""):
    for i in range(len(string)):
        val += hex(ord(string[i]))[2:]
    return val

def gen_cookie(url):
    return {"srcurl": string_to_hex(url), "path": "/"}
```

废话不多说了，毕竟正真想理解还是得自己动手尝试，完整的请求流程如下：

```python
import re
import requests
from urllib.parse import urljoin
from renderer.utils.constants import HEADERS

origin = 'http://www.xjbl.gov.cn/zdlygk/zfcgztb/zbgg1.htm'
location = re.compile(r'''location = "(\S+)"''')

session = requests.session()

resp1 = session.get(origin, headers=HEADERS)
loc1 = location.findall(resp1.text)[0]

verify_url = urljoin(origin, loc1 + '313932302c31303830')
session.cookies.update(gen_cookie(origin))

resp2 = session.get(verify_url)
loc2 = location.findall(resp2.text)[0]

resp3 = session.get(urljoin(origin, loc2))
resp3.content.decode('utf-8')
```

OK，搞定！
