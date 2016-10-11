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
        if content is not None:
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

    def getItem(self, postfix):
        item = {}
        if postfix:
            content = self.getCont(postfix)
            if content is not None:
                item['title'] = content.xpath('//h1[@id="film_name"]/text()')[0]
                item['quality'] = content.xpath('//span[contains(@class, "film_q_img")]/text()')[0]
                item['genre'] = content.xpath('//a[contains(@href, "/genres/")]/text()')[0]
                item['length'] = content.xpath('//dl[@class="dl-horizontal"]/dd/text()')[-1].strip()
                item['folders'] = {}
                for f in content.xpath('//div[@class="panel panel-default"]'):
                    tmp = html.fromstring(html.tostring(f))
                    fname = tmp.xpath('//h4/text()')[1].strip() # Folder name
                    item['folders'][fname] = {}
                    labels = tmp.xpath('//a/text()')
                    urls = tmp.xpath('//a/@href')
                    for s in xrange(len(labels)):
                        item['folders'][fname][labels[s][1:]] = urls[s]
        return item

    def getStreamUrl(self, postfix):
        playlist = {}
        if postfix:
            content = self.getCont(postfix)
            if content is not None:
                url = ''
                findex = postfix.split('/')[2]
                for f in content.xpath('//iframe/@src'):
                    if f.find('file=' + findex):
                        url = f
                self.s.get(url.replace('/?','/list/?'))
                playlist_url = 'http://player.3tv.im/m3u8/%s.m3u8' % findex
                playlist_content = self.s.get(playlist_url)
                if playlist_content is not None and playlist_content.ok:
                    for l in playlist_content.content.split('\n'):
                        if l.startswith('http'):
                            playlist[l.split('/')[-2:-1][0].split('_')[0]] = l

        return playlist


tt = TreeTv()

test = tt.getStreamUrl('/player/167394/1')
print test
