'''图片文字识别示例'''

import re
from urllib.parse import urljoin

from renderer.utils import GeneralOcr, retry_get

url = 'http://www.snqindu.gov.cn/html/zwgk/xxgkml/xzzf/xzcf/202006/44820.html'
resp = retry_get(url)
string = resp.content.decode('utf-8')
imgs = re.findall(r'''src=['"](/uploadfile\S+(jpg|png))['"]''', string)
img, _ = imgs[0]
ocr = GeneralOcr()
ocr.basic_ocr(urljoin(url, img))

url = 'http://ztb.panan.gov.cn/fileserver/down?md5=B6B1765B3732F55D48C7449F6D4CEAA3&bucket=2'
ocr = GeneralOcr()
ocr.basic_ocr(url, certain=True)
