#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
from lxml import html

parameters = sys.argv[1:]
if parameters:
    url = parameters[0]
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
    resp = s.get(url)
    p = html.fromstring(resp.content)
else:
    sys.stderr.write('1st parameter should be valid url!\n')
    exit(1)

