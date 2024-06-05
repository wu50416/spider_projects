#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/18 11:51
# @Author  : Harvey
# @File    : get_detail.py
import requests
from wbh_word.spider.Get_TJ_ip import ip_proxies

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
    # "csm-sid": "713-2299262-7567932",
    "x-amz-captcha-1": "1717480655829841",
    "x-amz-captcha-2": "THz/dORI7f9MPEYpk6zAOQ==",
    "session-id": "145-8954814-3186315",
    "session-id-time": "2082787201l",
    # 上面这部分为核心字段，过了验证码之后就可以得到

    "i18n-prefs": "USD",
    "lc-main": "zh_CN",
    "sp-cdn": "\"L5Z9:CN\"",
    # "ubid-main": "132-1464863-8061124",
    # "session-token": "m4jtyQF+jZJqVW/adslOeUE7aWcay+oPVttMzoTlqWO9R9VCk6M0xNooY5RmGRW9eOBxpsP949PLbSn9eXz1ECwAwFVxwxRSWZtYLjcpY/70/WSGpis0IqQpRZSPI5RmUQgi/1lHq4qB+zIqJoudzKwXxCt7ihAa4fhbjcAOJjVsAO3pxMHfOH7aDjRw3wHt4xDaW53dyRENzIaYNvwh+KCkzK0w5SOxz6fxuY6v9zUsuWLt8pZmtQ75YoU1C3+Okt2scs+5b+jt+1dl/OTQ6oHj7QyAqK5h0MFeVM9jEkXgoubepR1OgB0YWNmMD3wCrb3sB0NtbZThvFJmWxOV3Bri1TQREibq",
    # "csm-hit": "tb:7NNEK8EZX7MDKY0R3SZH+s-7NNEK8EZX7MDKY0R3SZH|1715936997814&t:1715936997814&adb:adblk_no"
}
# url = "https://www.amazon.com/Munchkin%C2%AE-Brica%C2%AE-Stroller-Organizer-Bag/dp/B0BPMQQN6M"
url = "https://www.amazon.com/dp/B08DFLR38F"

proxies = ip_proxies()
# proxies = {'http': 'http://613706c5ede9d:kF0C7UslCBzxXdt@114.239.95.42:3328', 'https': 'http://613706c5ede9d:kF0C7UslCBzxXdt@114.239.95.42:3328'}
response = requests.get(url, headers=headers, cookies=cookies,proxies=proxies)
print(response.text)
print(len(response.text))
print(response.cookies)
print(response.headers)