#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/2/6 17:15
# @Author  : Harvey
# @File    : ja3_demo.py

# 使用ja3魔改库
from curl_cffi import requests
a = requests.get("https://www.globalspec.com/productfinder/data_acquisition_signal_conditioning", impersonate="chrome101")
print(a.text)

print("\n=====================\n")
# 使用原生的request
import requests
b = requests.get("https://www.globalspec.com/productfinder/data_acquisition_signal_conditioning")
print(b.text)

