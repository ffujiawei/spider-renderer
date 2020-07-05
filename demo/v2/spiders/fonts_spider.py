'''Rendered on 2020-07-05 07:53:10 PM'''

import re
import scrapy

class NewspiderSpider(scrapy.Spider):

    name = 'fonts_spider'
    source = '方正字体下载，免费下载字体，中文字体-模板王字库'
    url = 'http://fonts.mobanwang.com/fangzheng/'
    author = 'White Turing'
    all_page = 20
    
    def start_requests(self):
        url = 'http://fonts.mobanwang.com/fangzheng/List_%d.html'
        all_page = self.all_page or 10
        for page in range(1, all_page):
            yield scrapy.Request(url % page, callback=self.parse)

    def parse(self, response):
        response.string = re.sub('[\r\n\t\v\f]', '', response.text)
        rows = re.findall(r'''href=['"](\S+?html?)['"][^<>]*?title=['"]''', response.string)