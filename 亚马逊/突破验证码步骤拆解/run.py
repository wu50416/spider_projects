#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/4 16:51
# @Author  : Harvey
# @File    : run.py
import random
import re

import ddddocr
import requests

from wbh_word.spider.Get_TJ_ip import ip_proxies

# # 目前所有站点的域名和cookie(cookie有存活期)
amazon_site_info = {
    # 20500
    "https://www.amazon.com": ['美国站', 'i18n-prefs=USD; lc-main=en_US; session-id={}-{}-{}; ubid-main={}-{}-{}'],
    # NW1 6XE
    "https://www.amazon.co.uk": ['英国站', 'i18n-prefs=CNY; lc-acbuk=en_GB; session-id={}-{}-{}; ubid-acbuk={}-{}-{}'],
    # K1V 7P8
    "https://www.amazon.ca": ['加拿大站', 'i18n-prefs=CAD; lc-acbca=en_CA; session-id={}-{}-{}; ubid-acbca={}-{}-{}'],
    # 10115
    "https://www.amazon.de": ['德国站', 'lc-acbde=en_GB; i18n-prefs=CNY; session-id={}-{}-{}; ubid-acbde={}-{}-{}'],
    # 1011-1109
    "https://www.amazon.nl": ['荷兰站', 'i18n-prefs=EUR; lc-acbnl=en_GB; session-id={}-{}-{}; ubid-acbnl={}-{}-{}'],
    # 11455
    "https://www.amazon.se": ['瑞典站', 'i18n-prefs=SEK; lc-acbse=en_GB; session-id={}-{}-{}; ubid-acbse={}-{}-{}'],
    # 1930
    "https://www.amazon.com.be": ['比利时站',
                                  'i18n-prefs=EUR; lc-acbbe=en_GB; session-id={}-{}-{}; ubid-acbbe={}-{}-{}'],
    # 789680
    "https://www.amazon.sg": ['新加坡站', 'i18n-prefs=SGD; session-id={}-{}-{}; ubid-acbsg={}-{}-{}'],
    # 11433
    "https://www.amazon.sa": ['阿拉伯站', 'i18n-prefs=SAR; lc-acbsa=en_AE; session-id={}-{}-{}; ubid-acbsa={}-{}-{}'],
    # Dubai
    "https://www.amazon.ae": ['阿联酋站', 'i18n-prefs=USD; lc-acbae=en_AE; session-id={}-{}-{}; ubid-acbae={}-{}-{}'],
    # 999008
    "https://www.amazon.in": ['印度站', 'i18n-prefs=INR; lc-acbin=en_IN; session-id={}-{}-{}; ubid-acbin={}-{}-{}'],
    "https://www.amazon.eg": ['埃及站', 'i18n-prefs=EGP; lc-acbeg=en_AE; session-id={}-{}-{}; ubid-acbeg={}-{}-{}'],
    # 00144
    "https://www.amazon.it": ['意大利站', 'i18n-prefs=EUR; session-id={}-{}-{}; ubid-acbit={}-{}-{}'],
    # 08358
    "https://www.amazon.es": ['西班牙站', 'i18n-prefs=EUR; session-id={}-{}-{}; ubid-acbes={}-{}-{}'],
    # 10115
    "https://www.amazon.pl": ["波兰站", 'i18n-prefs=PLN; session-id={}-{}-{}; ubid-acbpl={}-{}-{}'],
    # 34000
    "https://www.amazon.com.tr": ["土耳其站", 'i18n-prefs=TRY; session-id={}-{}-{}; ubid-acbtr={}-{}-{}'],
    # 83331-000
    "https://www.amazon.com.br": ["巴西站", 'i18n-prefs=BRL; session-id={}-{}-{}; ubid-acbbr={}-{}-{}'],
    # 75020
    "https://www.amazon.fr": ["法国站", 'i18n-prefs=EUR; session-id={}-{}-{}; ubid-acbfr={}-{}-{}'],
    # 01830
    "https://www.amazon.com.mx": ["墨西哥站", 'i18n-prefs=MXN; session-id={}-{}-{}; ubid-acbmx={}-{}-{}'],
    # 2600
    "https://www.amazon.com.a": ["澳大利亚站", 'i18n-prefs=AUD; session-id={}-{}-{}; ubid-acbau={}-{}-{}'],
}


def get_response_type(response):
    type = 9999
    if response.status_code == 404:
        # 判断商品是否过期
        print("[Type]当前页面为-商品过期")
        type = 2
    elif not response or response.status_code < 200 or response.status_code >= 400:
        # 异常响应
        print("[Type]当前页面为-异常响应")
        type = 0
    elif (response.status_code == 302) or ('Sorry! Something went wrong' in response.text) or (
            '请刷新页面并重试' in response.text):
        # 请求错误
        print("[Type]当前页面为-请求错误")
        type = -1
    elif re.search(r'Enter the characters you see below', response.text) or (
            '/errors/validateCaptcha' in response.text):
        # 验证码
        print("[Type]当前页面为-验证码")
        type = -2
    elif len(response.text) > 150000:
        print("[Type]当前页面为-正常响应")
        type = 1
    return type


def random_amazon_headers():
    headers = {
        "dpr": "1",
        "referer": "https://www.amazon.com",
        # "sec-ch-ua": "\"Chromium\";v=\"124 \", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-viewport-width": "1912",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "viewport-width": "1912"
    }
    ua_temple = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.{}.{}"
    headers['user-agent'] = ua_temple.format(random.randint(1000, 9999), random.randint(10, 1000))
    return headers


def updata_cookie(cookie_dict, meta):
    '''
    根据cookie字典来更新cookie
    :param cookie_dict:
    :return:
    '''
    # print('[UPDATA_COOKIE]', cookie_dict)
    cookies = meta.get('cookies', {})
    if cookie_dict.get('x-amz-captcha-1', ''):
        cookies['x-amz-captcha-1'] = cookie_dict['x-amz-captcha-1']
    if cookie_dict.get('x-amz-captcha-2', ''):
        cookies['x-amz-captcha-2'] = cookie_dict['x-amz-captcha-2']
    meta['cookies'] = cookies
    return cookies, meta


def get_img(response):
    '''
    下载并识别图片
    :param response:
    :return:图片ID
    :return:图片识别结果
    '''
    img_id = re.findall(r'name="amzn" value="(.*?)"', response.text)
    img = re.findall(r'<img src="(.*?)">', response.text)
    if img_id and img:
        img_url = img[0]
        img_id = img_id[0]
        r = requests.get(img_url)
        img_path = './image/img.png'
        ocr = ddddocr.DdddOcr()
        with open(img_path, 'wb') as f:
            f.write(r.content)
        img_data = ocr.classification(r.content)
        img_data = img_data.lower()
        return img_id, img_data


def run_verify(response, meta):
    '''
    处理验证码
    :param response:
    :return:
    '''
    verify_url = "https://www.amazon.com/errors/validateCaptcha"
    img_id, img_data = get_img(response)
    if img_id and img_data:
        msg_url = meta.get('msg_url', '')
        url_href = msg_url.split('amazon.com')[-1]
        proxies = meta.get('proxies', '')
        headers = meta.get('headers')
        cookies = meta.get('cookies')
        params = {
            "amzn": img_id,
            "amzn-r": url_href,
            "field-keywords": img_data
        }
        if msg_url and proxies:
            print('[GET]正在请求验证码页, 验证码识别结果为：',img_data)
            response = requests.get(verify_url, headers=headers, params=params, cookies=cookies, proxies=proxies,
                                    allow_redirects=False)
            response_cookie = dict(response.cookies)
            cookies, meta = updata_cookie(response_cookie, meta)
    return meta


def get_product_detail(meta):
    '''
    采集产品详情
    :param meta:
    :return:
    '''
    headers = meta['headers']
    msg_url = meta.get('msg_url', '')
    proxies = meta.get('proxies', '')
    cookies = meta.get('cookies', {})
    response = requests.get(msg_url, headers=headers, cookies=cookies, proxies=proxies)

    print('[GET]正在第 {} 次请求, 响应长度为：'.format(meta['retry_count'] + 1), len(response.text))
    response_type = get_response_type(response)
    if response_type == -2:
        # 出现验证码，判断是否超过最大重试次数
        if meta['retry_count'] < meta['max_retry']:
            meta = run_verify(response, meta)
            retry_count = meta['retry_count']
            meta['retry_count'] = retry_count + 1

            print('[RETRY]重试当前任务：', )
            response, meta = get_product_detail(meta)
        else:
            print('[MAX_RETRY]超过最大重试次数')
            return None
    elif response_type == 1:
        # 正常的响应
        pass
    else:
        print(response.text)
        raise '超出预期的响应'
    return response, meta


def run():
    url_list = [
        # 产品详情
        "https://www.amazon.com/dp/B08DFLR38F",
        "https://www.amazon.com/TAISCAI-USB-Mount%EF%BC%8C18W-Dual-Waterproof/dp/B0CY99S3KN",
        "https://www.amazon.com/Wireless-Charging-Mag-Safe-Foldable-Magnetic/dp/B0CSP7KHD1",
        "https://www.amazon.com/Charger-Hohosb-Adapter-Charging-More-White/dp/B0CZ3WXFX3"
        # 评论区
        "https://www.amazon.com/Spatula-Tableware-Serving-Scratch-Eco-friendly/product-reviews/B08DFLR38F",
    ]
    proxies = ip_proxies()
    # proxies = None
    meta = {
        'headers': random_amazon_headers(),
        'proxies': proxies,
        'max_retry': 3  # 最大重试次数
    }
    for url in url_list:
        meta['msg_url'] = url
        meta['retry_count'] = 0  # 重试次数
        print('[START]',url)
        response, meta = get_product_detail(meta)

        # print(response.text)


if __name__ == '__main__':
    run()
