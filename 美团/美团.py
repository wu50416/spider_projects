# -*- coding: utf-8 -*-
'''
@file    : 美团.py
@Time    : 2022/8/18 15:28
@Author  : hao
'''

import time
import execjs
import json
import requests
import random
import pandas as pd

# 第一页reqUrlAndParams
# "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=754270772&uuid=3bcf687243ae42cf94f2.1660875247.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/&riskLevel=1&optimusCode=10"
# "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=2&userId=754270772&uuid=3bcf687243ae42cf94f2.1660875247.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/pn2/&riskLevel=1&optimusCode=10"
# "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=3&userId=754270772&uuid=3bcf687243ae42cf94f2.1660875247.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/pn3/&riskLevel=1&optimusCode=10"
# ****** 获取token ******
def get_token(url1):
    filename_js = 'token.js'
    with open(filename_js, encoding='utf-8', mode='r') as f:
        token_js = f.read()
        f.close()
    js1 = execjs.compile(token_js)

    # url1 = "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=price_asc&dinnerCountAttrId=&page=1&userId=754270772&uuid=3440f348ca534abea52c.1660792952.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/price_asc/&riskLevel=1&optimusCode=10"
    print('********* 正在生成 -- token *********')
    token = js1.call('token', url1)         # 获取token
    print(token)
    return token



def sleep_time(star,end):
    time.sleep(float(random.randint(star,end)/1000))

# ****** 获取请求头+参数 ******
def get_headers(Cookie,token,page):
    if page == 1:
        page1 = page
    else:
        page1 = page-1
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': Cookie,
        'Host': 'gz.meituan.com',
        'Referer': f'https://gz.meituan.com/meishi/pn{page1}/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }
    params = {
        'cityName': '广州',
        'cateId': '0',          # 分类
        'areaId': '0',          # 区域
        'sort': '',
        'dinnerCountAttrId': '',    # 用餐人数
        'page': page,
        'userId': '754270772',
        'uuid': '3bcf687243ae42cf94f2.1660875247.1.0.0',
        'platform': '1',
        'partner': ' 126',
        'originUrl': f'https://gz.meituan.com/meishi/pn{page}/',  # 类型+地点  11：广州
        'riskLevel': ' 1',
        'optimusCode': '10',
        '_token': token,
    }
    return headers,params



def get_data(Cookie):
    url = 'https://gz.meituan.com/meishi/api/poi/getPoiList'
    dt = {'店铺ID': [], '店铺名称': [], '评分': [], '店铺地址': [], '人均金额': []}
    for page in range(5):
        # 这个url用来获取token，不同的页面后面的参数必须要跟着更新
        url1 = f"https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page={page}&userId=754270772&uuid=3bcf687243ae42cf94f2.1660875247.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/pn{page}/&riskLevel=1&optimusCode=10"
        token = get_token(url1)
        headers,params = get_headers(Cookie,token,page=int(page+1))
        response = requests.get(url=url, headers=headers, params=params).json()
        print(response)
        # sleep_time(2500,5000)
        datas = response['data']['poiInfos']
        for data in datas:
            dt['店铺ID'].append(data['poiId'])
            dt['店铺名称'].append(data['title'])
            dt['评分'].append(data['avgScore'])
            dt['店铺地址'].append(data['address'])
            dt['人均金额'].append(data['avgPrice'])

    print(dt)
    dt = pd.DataFrame(dt)
    print(dt)
    dt.to_excel('美团数据.xlsx', encoding='gbk', index=False)




if __name__ == '__main__':
    Cookie = '_lxsdk_cuid=182a5b9c796c8-0c41b11b1de596-3e604809-1fa400-182a5b9c796c8; iuuid=07BE6F63032CEB165BF169DD7F7C7DD2DCE978161F7A545E150B25E4E5C30A9F; _lxsdk=07BE6F63032CEB165BF169DD7F7C7DD2DCE978161F7A545E150B25E4E5C30A9F; _hc.v=ecc68847-3f20-41bb-aa55-3c0ec1027f24.1660733903; oops=mvYQazboRQpHkJS6Vj5x-GHMFgkAAAAAZRMAANClzE-oLD7F7R2AwN2ap1kZrwhtY1jf8tC0A4z8BoZvnD2xNxPGr4nCoOmDQhRGdg; userId=754270772; ci=20; rvct=20%2C44%2C30; uuid=edd1be2c976845c4aff8.1664438227.1.0.0; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic; mtcdn=K; userTicket=FkekNuvjnuQuWpKZBTkvjLrTCPOcGZkdLceeDuCX; _lxsdk_s=183883fd2fd-11d-a2c-1d2%7C%7C15; _yoda_verify_resp=uz7wFWHfMOUtwstbQ8B7XW%2FNTgDVxhHLS4jdbEGrHffgdKClVYHzyFNiLnvyqL4gCybF1GUatm%2BkXL5jH06IYkCanIyiS%2FrZNGsdKn%2F4RRc%2B%2BbjLoT8DyW%2BC8Yanq5NgCjz4272rOw0O3BkBwq%2Br5QmBnRjCIvnLLN6gBapw8MtKaWeU5m7Srl0c9KgPlaslhyAXtvOyjJWa%2FHHpqWMtn2c6e3kHqhnPdkginHWMlfoToLf177TjR2BF0dYSWg5IYLETCDiTeSqAaVUn1iJT7ECvcRcDTiQQI6sZn6y0FVG373FnDFu5GPUU2%2BOYGyif9fsGFDD5uS7o7AZg5o5MeAmP2F1MVnDgsxyuWVzEYcWyhOrALixiufaW3ICCTjcj; _yoda_verify_rid=15dcecdb72016041; u=754270772; n=%E6%B5%A95452; lt=GCsl6PCUBfaRAYqyKbhoGuXjYr0AAAAACRQAABTh2cgHLDB1IiWHcE8GIyboOZDDwEep-39UBha_VIoECRT6CPnaI_j50i5492tQUA; mt_c_token=GCsl6PCUBfaRAYqyKbhoGuXjYr0AAAAACRQAABTh2cgHLDB1IiWHcE8GIyboOZDDwEep-39UBha_VIoECRT6CPnaI_j50i5492tQUA; token=GCsl6PCUBfaRAYqyKbhoGuXjYr0AAAAACRQAABTh2cgHLDB1IiWHcE8GIyboOZDDwEep-39UBha_VIoECRT6CPnaI_j50i5492tQUA; token2=GCsl6PCUBfaRAYqyKbhoGuXjYr0AAAAACRQAABTh2cgHLDB1IiWHcE8GIyboOZDDwEep-39UBha_VIoECRT6CPnaI_j50i5492tQUA'

    get_data(Cookie)














