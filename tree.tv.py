#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
from lxml import html

class TreeTv:

    def __init__(self):
        self.url = 'http://m.tree.tv'
        self.s = requests.Session()
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'

    def getCont(self, postfix=''):
        res = None
        if postfix:
            if not postfix.startswith('/'):
                postfix = '/' + postfix
        resp = self.s.get(self.url + postfix)
        if resp.status_code == 200:
            res = html.fromstring(resp.content)
        return res

    def getItems(self, page=''):
        if page:
            content = self.getCont('/page/' + str(page))
        else:
            content = self.getCont()
        items = []
        if content:
            title = content.xpath('//div[@class="preview"]/a/img/@alt')
            year = content.xpath('//div[@class="preview"]/div[@class="year"]/a/text()')
            genre = content.xpath('//div[@class="preview"]/div[@class="genre"]/a/text()')
            quality = content.xpath('//div[@class="preview"]/div[@class="quality"]/a/text()')
            img = content.xpath('//div[@class="preview"]/a/img/@src')
            url = content.xpath('//div[@class="item_content"]/h4/a/@href')
            for i in range(0, len(title)-1):
                items.append({
                    'title': title[i],
                    'year': year[i],
                    'genre': genre[i],
                    'quality': quality[i],
                    'img': img[i],
                    'url': url[i]
                })
        return items


tt = TreeTv()
test = tt.getItems()
print test