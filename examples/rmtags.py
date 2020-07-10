from lxml import html
from renderer.utils import retry_get, rm_tags
from w3lib.html import remove_tags

url = 'https://mengso.com/'
url = 'http://ggzy.wlmq.gov.cn/infopublish.do?method=infoPublishView&infoid=A850B1A55A9643CDE05310C410AC5772'
response = retry_get(url)
string = response.content.decode('utf-8')
string = response.content.decode('gbk')

html.fromstring(string).text_content()
remove_tags(string)

rm_tags(string, '\n')
rm_tags(string)
from renderer.utils import save_html
save_html(response)