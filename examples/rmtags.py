from lxml import html
from renderer.utils import retry_get, rm_tags
from w3lib.html import remove_tags

url = 'https://mengso.com/'
response = retry_get(url)
string = response.content.decode('utf-8')

html.fromstring(string).text_content()
remove_tags(string)

rm_tags(string, '\n')
rm_tags(string)
