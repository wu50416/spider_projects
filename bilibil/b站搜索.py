# -*- coding: utf-8 -*-
'''
@file    : b站搜索.py
@Time    : 2022/9/28 17:30
@Author  : hao
'''

import json
import random
import re
import time
import requests
import pandas as pd

class MaxPageError(Exception):
    pass


def request(method, url, **kwargs):
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 30
    if 'headers' not in kwargs:
        kwargs['headers'] = ''
    for i in range(1, 1000):
        try:
            res = requests.request(method, url, **kwargs)
            if res.json()['code'] != 0:
                time.sleep(random.uniform(5, 10))
                # kwargs['headers']['cookie'] = get_cookies_from_chrome('bilibili.com')
                kwargs['headers']['cookie'] = "buvid3=8C8BDF41-A391-4AE5-A7CE-51C000DB405834778infoc; rpdid=|(J|~kY|~lYR0J'uYkk)um)~Y; LIVE_BUVID=AUTO5516362001845149; video_page_version=v_old_home; sid=hscy9fe8; CURRENT_BLACKGAP=0; blackside_state=0; buvid4=80EE32CA-B5DC-9B57-D618-A9C7E04FCC4D36092-022020421-c8mC4VtaIp+rOgDqzSenjQ%3D%3D; nostalgia_conf=-1; PVID=1; CURRENT_QUALITY=80; _uuid=7C6EA578-3FDD-BA10B-9E21-3C4E95C10DA9B39876infoc; i-wanna-go-back=-1; b_ut=7; fingerprint=c354324b9742cca891bedbd6a06592cb; buvid_fp_plain=undefined; buvid_fp=c354324b9742cca891bedbd6a06592cb; CURRENT_FNVAL=80; innersign=0; b_nut=100; b_lsid=6A1E2632_183873787F2; bsource=search_360"
                continue
            return res
        except Exception as e:
            print(f'请求失败，重试{i}：{e}')
            time.sleep(random.uniform(5, 10))
    else:
        return None




def search(keyword, page, search_type):
    global df_search
    api = 'https://api.bilibili.com/x/web-interface/search/type'
    params = {
        "search_type": search_type,
        "page": page,
        "keyword": keyword,
        "__refresh__": "true",
        "highlight": "1",
        "single_column": "0",
        "jsonp": "jsonp",
        # "callback": "__jp11"
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'referer': 'https://search.bilibili.com/all',
    }
    res = request('get', api, params=params, headers=headers, verify=False)
    datas = json.loads(re.findall(r'\{.*\}', res.text)[0])
    max_page = datas['data']['numPages']
    items = []
    if search_type == 'video':
        for data in datas['data']['result']:
            item = {}
            item['keyword'] = keyword
            item['id'] = str(data.get('id'))
            item['type'] = data.get('type')
            item['mid'] = str(data.get('mid'))
            item['author'] = data.get('author')
            item['typename'] = data.get('typename')
            item['title'] = data.get('title')
            item['description'] = data.get('description')
            item['play'] = data.get('play')
            item['video_review'] = data.get('video_review')
            item['review'] = data.get('review')
            item['favorites'] = data.get('favorites')
            item['tag'] = data.get('tag')
            item['duration'] = data.get('duration')
            item['url'] = data.get('arcurl')
            item['pubdate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get('pubdate')))
            items.append(item)
            print(item)
    elif search_type == 'article':
        for data in datas['data']['result']:
            item = {}
            item['keyword'] = keyword
            item['id'] = str(data.get('id'))
            item['type'] = data.get('type')
            item['mid'] = str(data.get('mid'))
            item['author'] = data.get('author')
            item['typename'] = data.get('category_name')
            item['title'] = data.get('title')
            item['description'] = data.get('desc')
            item['play'] = data.get('view')
            item['发表时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get('pub_time')))
            items.append(item)
            print(item)
    if items:
        df_search = df_search.append(items)
    if page >= max_page:
        raise MaxPageError


if __name__ == '__main__':
    # 根据搜索词获取搜索结果 [ '气味图书馆','祖玛珑','冰希黎','蓝风铃香水','英国梨与小苍兰','忍冬和印蒿','鎏金香水','流沙金香水','流金沙香水','金字塔香水','咖啡黑玫','上海玉兰']
    keywords = ['python']   # 搜索词
    df_search = pd.DataFrame()
    for keyword in keywords:
        for search_type in ['article']:
            for page in range(1, 5):
                try:
                    search(keyword=keyword, page=page, search_type=search_type)
                except MaxPageError:
                    break
                print('page：', page)
                time.sleep(random.uniform(1, 2))
            df_search.to_excel('data/search1.xlsx')



