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