#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/18 11:46
# @Author  : Harvey
# @File    : get_img.py
import requests


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=0, i",
    "referer": "https://www.amazon.com/dp/B0CS28ZLWS",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
cookies = {
    # "csm-sid": "602-5089573-6274975"
}
url = "https://www.amazon.com/errors/validateCaptcha"
params = {
    "amzn": "b+TKPZCS+956d3A6Vjh14g==",
    "amzn-r": "/dp/B08DFLR38F",
    "field-keywords": "jtymlx"
}
proxies = {'http': 'http://613706c5ede9d:kF0C7UslCBzxXdt@121.206.142.66:3328', 'https': 'http://613706c5ede9d:kF0C7UslCBzxXdt@121.206.142.66:3328'}
# 请求成功后会返回302，需要禁用自动跳转，先获取cookie，否则会自动跳转到详情页
response = requests.get(url, headers=headers, cookies=cookies, params=params,proxies=proxies, allow_redirects=False)

# print(response.text)
print(len(response.text))
print(response.cookies)
print(response.headers)
print(response.status_code)
# 当出现302状态说明请求成功

print("======= 重定向  =======")
response = requests.get(url, headers=headers, cookies=cookies, params=params,proxies=proxies)
print(len(response.text))
print(response.cookies)
print(response.headers)
print(response.status_code)