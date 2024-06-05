#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4 14:16
# @Author  : Harvey
# @File    : demo.py
'''
本案例以抓包软件作为例子，需要打开抓包软件
'''

import requests

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
cookies = {
    # "csm-sid": "885-4772898-7643320",
    # "x-amz-captcha-1": "1717478519134743",
    # "x-amz-captcha-2": "uSp1Hmez5CpG+zhsKIdmTw=="
}
url = "https://www.amazon.com/-/zh/product-reviews/B00M0DWQYI?ie=UTF8&reviewerType=all_reviews&pageNumber=3"

# IP为抓包软件的地址，端口号为软件的监听端口
proxies = {
    'http://': 'http://172.23.64.1:8888',
    'https://': 'http://172.23.64.1:8888',
}
response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)


print(response.text)
print(response)
print(len(response.text))
print(dict(response.cookies))
print(proxies)

