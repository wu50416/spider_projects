#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/22 18:31
# @Author  : Harvey
# @File    : 方案4_http2.py
import httpx
from urllib.parse import urlparse

# proxies = {
#     'http://': 'http://172.23.64.1:8888',
#     'https://': 'http://172.23.64.1:8888',
# }
# # 为代理键添加正确的URL格式
# proxies = {urlparse(k).scheme + '://' + urlparse(k).netloc: v for k, v in proxies.items()}

# client = httpx.Client(http2=True, proxies=proxies, verify=False)
client = httpx.Client(http2=True)

# 之后的使用方式和requests一样

headers = {
    "dpr": "1",
    "referer": "https://www.amazon.com",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-viewport-width": "1912",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "viewport-width": "1912"
}


url = 'https://www.amazon.com/gp/product/ajax/ref=dp_aod_NEW_mbc?asin=B08DFLR38F&m=&qid=&smid=&sourcecustomerorglistid=&sourcecustomerorglistitemid=&sr=&pc=dp&experienceId=aodAjaxMain'
# url2 = '/gp/aag/main?ie=UTF8&amp;seller=A3VQLMMKUUX89G&amp;isAmazonFulfilled=1&amp;asin=B08DFLR38F&amp;ref_=olp_merch_name_2'

result = client.get(url, headers=headers)


print(result.text)
print(result)
