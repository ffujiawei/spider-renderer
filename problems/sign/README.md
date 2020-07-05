# 破解 MD5 签名参数验证

示例网址：

```
https://www.yungang.gov.cn/infoDetailIm?typeId=7b1d8ce6354c45e9bc01656c96a1dbac&typeIdDetail=7b1d8ce6354c45e9bc01656c96a1dbac
```

通过观察发现请求网址是这样的：

```
https://www.yungang.gov.cn/yungang-cms-api/manage/scContentItem/dataGrid?page=2&typeId=0105a14a090044b8b6f8cf743f3327fb&limit=10&timestamp=1592028388497&sign=EB8F6C1D222748630922F47267BB5D1A
```

然而模拟发起相同的请求都无法获取数据。

观察请求网址，发现有两个特殊的参数 timestamp 和 sign，其中时间戳参数容易模拟，sign 由于我当时是第一次遇到，不知道是什么。所以，我就先谷歌了这个参数，大概得知了是签名参数，及其生成算法。

但具体实现还是有所区别的，然后我去网页源码里寻找 JS 实现源码，搜索 sign，就可以发现这个函数，源码进行了混淆，不过内容还是可以识别的，此处我进行了还原和注释。

```js
// 密钥
var secret = "77029991-78cc-44ea-9656-5b388ed11795";
function q_dict(formdata) {
    return function (formdata) {
        // 解析传入的请求数据
        var q_dict = {}; q_dict = JSON.parse(formdata);
        // 添加时间戳
        q_dict.timestamp = (new Date).getTime();
        // 新建数组存储字典的键
        var keys = new Array(q_dict.length), s = 0;
        for (var key in q_dict) keys[s] = key, s++;
        // 排序键，然后合并
        for (var o = keys.sort(), c = secret, r = 0; r < o.length; r++) { var string = o[r]; c += string + q_dict[string] }
        return c += secret, q_dict.sign = md5(c), q_dict
    }(key()(formdata))
}
```

根据其实现算法，用 Python 同样实现即可。

```python
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
```
