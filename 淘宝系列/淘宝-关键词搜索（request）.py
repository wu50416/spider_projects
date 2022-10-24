# -*- coding: utf-8 -*-
'''
@file    : test.py
@Time    : 2022/10/24 17:16
@Author  : hao
'''


import json
import os

import requests
import pandas as pd
from urllib.parse import urljoin, urlencode

class TargetReader:
    def __init__(self):
        pass

    @staticmethod
    def read_target(target, keychain: tuple, default: any = None):
        if type(target) is dict:
            return TargetReader.read_dictionary(target, keychain, default)
        elif type(target) is list or type(target) is tuple:
            return TargetReader.read_array(target, keychain, default)
        else:
            return default

    @staticmethod
    def read_dictionary(dictionary: dict, keychain: tuple, default: any = None):
        if len(keychain) <= 0:
            return default
        elif len(keychain) == 1:
            return dictionary.get(keychain[0], default)
        else:
            current_key = keychain[0]
            if dictionary.keys().__contains__(current_key):
                sub_dictionary = dictionary.get(current_key, None)
                if type(sub_dictionary) is dict:
                    return TargetReader.read_dictionary(sub_dictionary, keychain[1:], default)
                elif type(sub_dictionary) is tuple or type(sub_dictionary) is list:
                    return TargetReader.read_array(sub_dictionary, keychain[1:], default)
                else:
                    return default
            else:
                return default

    @staticmethod
    def read_array(array: tuple, keychain: tuple, default: any = None):
        if len(keychain) <= 0:
            return default
        elif len(keychain) == 1:
            current_key = int(keychain[0])
            if len(array) > current_key:
                return array[int(keychain[0])]
            else:
                return default
        else:
            current_key = int(keychain[0])
            if len(array) > current_key:
                sub_array = array[current_key]
                if type(sub_array) is tuple or type(sub_array) is list:
                    return TargetReader.read_array(sub_array, keychain[1:], default)
                elif type(sub_array) is dict:
                    return TargetReader.read_dictionary(sub_array, keychain[1:], default)
                else:
                    return default
            else:
                return default

    @staticmethod
    def write_dictionary(target_dict: dict, keychain: tuple, value: any):
        if len(keychain) <= 0:
            # not modify anything if keychain is empty
            return target_dict
        if len(keychain) == 1:
            target_dict[keychain[0]] = value
            return target_dict

        current_key = keychain[0]
        if target_dict.get(current_key) is None:
            target_dict[current_key] = {}
        return TargetReader.write_dictionary(target_dict[current_key], keychain[1:], value)





class TaoBao(object):
    def __init__(self, cookie):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'cookie': cookie
        }
        category_file = os.path.join(os.path.dirname(__file__), 'taobao_category.json')
        with open(category_file, 'r', encoding='utf-8') as file:
            self.taobao_category = json.load(file)

    def search_goods(self, keyword, page, sort='sale-desc'):
        """
        发起请求
        :param keyword: 搜索词
        :param page: 当前页数
        :params sort: 排序方式
        :return:
        """
        api = 'https://s.taobao.com/search'
        params = {
            "ajax": "true",
            "_ksTS": "1602748916997_1531",
            "q": keyword,
            "js": "1",
            'sort': 'sale-desc',        # !!!!销量从大到小
            "stats_click": "search_radio_all:1",
            "ie": "utf8",
            'cps': 'yes',
            'cat':'50008056',
            # "sort": "sale-desc",# 第一页没有这个参数
            # "data-key": "s",    # 第一页为sort，第二页为s，第三页为s，第四页为s，第四页回到第一页为s,ps，第一页到第三页为s，第三页回到第一页为s,ps
            # "data-value": 176,  # 第一页为sale-desc，第二页为44，第三页为88，第四页为132，第四页回到第一页为0,1，第一页到第三页为88，第三页回到第一页为0,1
            # "bcoffset": "0",    # 第一页没有这个参数，第二页为0，第三页为0，第四页为0，第四页回到第一页为0，第一页到第四页为0，第三页回到第一页为0
            # "p4ppushleft": ",44", # 第一页没有这个参数，第二页为,44，第三页为,44，第四页为,44，第四页回到第一页为,44，第一页到第三页为,44，第三页回到第一页为,44
            # "s": 44,    # 第一二页没这个参数，第三页为44，第四页为88，第四页回到第一页为132，第一页到第三页为0，第三页回到第一页为88
        }

        # 根据页数构造URL参数
        if page == 1:
            params.update({'data-key': 'sort', 'data-value': sort})
        elif page == 2:
            params.update({'sort': sort, 'data-key': 's', 'data-value': 44*(page-1), 'bcoffset': 0, 'p4ppushleft': ',44'})
        else:
            params.update({'sort': sort, 'data-key': 's', 'data-value': 44*(page - 1), 'bcoffset': 0, 'p4ppushleft': ',44', 's': 44*(page-2)})
        self.session.headers['referer'] = urljoin(api, urlencode(params))
        res = self.session.get(api, params=params, verify=False)
        datas = json.loads(res.text)
        if datas:
            result = []
            search_word = TargetReader.read_target(datas, ('mods', 'itemlist', 'data', 'query'))
            goods_list = TargetReader.read_target(datas, ('mods', 'itemlist', 'data', 'auctions'), [])
            detail_list = TargetReader.read_target(datas, ('mainInfo', 'traceInfo', 'traceData'), [])
            for i in range(len(goods_list)):
                item = {}
                item['搜索词'] = search_word
                item['page'] = page
                item['商品标题'] = TargetReader.read_target(goods_list, (i, 'raw_title'))
                item['商品ID'] = TargetReader.read_target(goods_list, (i, 'nid'))
                item['价格'] = TargetReader.read_target(goods_list, (i, 'view_price'))
                item['销量'] = TargetReader.read_target(goods_list, (i, 'view_sales'))
                item['近30天销量'] = TargetReader.read_target(detail_list, ('allOldBiz30Day', i))
                item['评价数'] = TargetReader.read_target(goods_list, (i, 'comment_count'))
                item['店铺名'] = TargetReader.read_target(goods_list, (i, 'nick'))
                item['店铺ID'] = TargetReader.read_target(goods_list, (i, 'user_id'))
                item['商品详情URL'] = 'https:' + TargetReader.read_target(goods_list, (i, 'detail_url'))

                item['主图URL'] = 'https:' + TargetReader.read_target(goods_list, (i, 'pic_url'))
                item['类目ID'] = TargetReader.read_target(goods_list, (i, 'category'))
                item['类目'] = self.taobao_category.get(TargetReader.read_target(goods_list, (i, 'category')))
                result.append(item)
            return result


if __name__ == '__main__':
    max_page = 50
    keywords = ['雅客']
    output_file = 'data/雅客.xlsx'
    columns = ['搜索词', 'page', '商品标题', '商品ID', '价格', '销量', '近30天销量', '评价数', '店铺名', '店铺ID', '商品详情URL', '主图URL', '类目ID', '类目']
    df = pd.DataFrame(columns=columns)
    # cookie = get_cookies_from_chrome()
    cookie = "thw=cn; UM_distinctid=1805f8af6b563-0a4153d317f94b-6b3e555b-1fa400-1805f8af6b697d; CNZZDATA1277371679=1154409539-1650868523-https%253A%252F%252Fwww.taobao.com%252F%7C1650868523; enc=346k%2FFonwgcBn2R%2FvkjUuUwItk%2BxNeoHaGtjiCoctewAEqT%2Fc4cuqyI1ycxxbyo6WSx6ZzSqiEJISh%2FUWZZpXIfWd3rfceVnBKxIIDWvZyE%3D; Hm_lvt_96bc309cbb9c6a6b838dd38a00162b96=1665736270; _samesite_flag_=true; cookie2=14c941389e7c3bee2cb7bc66523c3624; t=df1d41ad2adcb8dcef51ce9bcbdaa415; _tb_token_=813566433ba5; xlly_s=1; sgcookie=E1005AY2mACgwQd3mLrARQY48r1ZRy7jH8uTmEi6eoDt9rd6olmFTg9KCnC0niBcn6MN65dgH7p8n32vWUZohKJScyjGww5G%2F1oHR89BECk1dHg%3D; alitrackid=www.taobao.com; _m_h5_tk=1d7ede9e9e39b69a3621729460326dba_1666259368589; _m_h5_tk_enc=ea672862232f971dbc45fbfcf68cd58a; lastalitrackid=mrmeat.tmall.com; JSESSIONID=82BFA0CD43B7EE3215D85E9A654E5565; mt=ci=0_0; tracknick=; cna=/1UfGzxF8zUCAT2M7wWEugou; l=eBx7hYycTskiJw22BO5aourza77TiIdbzsPzaNbMiInca6Ll1e9YrNCUh7n2RdtjgtfYne-zv3EoxdEy8WU38xGjL77kRs5mpz99-; tfstk=c1MVBR_tEKp4uZo9J82ZU9wPOxZACiimjTrQiepk5oapXTLY8m5DNNEk0sZzfg7gi; isg=BLW1ZQlLOiW2OV6G7H84BQB9xDFvMmlEIm4ZlDfb_Sx1DtcA_IPgFenMXNI4ToH8"
    taobao = TaoBao(cookie=cookie)
    for keyword in keywords:
        for page in range(1, max_page+1):
            goods_list = taobao.search_goods(keyword=keyword, page=page, sort='sale-desc')
            if goods_list:
                df = df.append(goods_list)
                df.to_excel(output_file, index=False)
            print(f'keyword: {keyword}, page: {page}, {goods_list}')


