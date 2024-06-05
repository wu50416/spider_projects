# -*- coding: UTF-8 -*-
'''
@Project ：wbh_pj 
@File ：123.py
@Author ：hao
@Date ：2023/10/24 14:56 
'''
'''
# 亚马逊所有页面都可以采集，最强的方案
# 目前只有 safari15_5 / safari15_3 指纹可以通过
'''
# import requests
from curl_cffi import requests
from wbh_word.spider.Get_TJ_ip import ip_proxies

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
# 产品详情
# url = "https://www.amazon.com/dp/B0CS28ZLWS"
# 评论区
# url = "https://www.amazon.com/Spatula-Tableware-Serving-Scratch-Eco-friendly/product-reviews/B08DFLR38F/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber=2"
url = "https://www.amazon.com/Spatula-Tableware-Serving-Scratch-Eco-friendly/product-reviews/B08DFLR38F/ref=cm_cr_getr_d_paging_btm_next_3?pageNumber=3"
proxies = ip_proxies()

response = requests.get(url, headers=headers, proxies=proxies, impersonate="safari15_3")

print(response.text)
print(response)


