# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：333.py
@Author ：hao
@Date ：2023/6/5 11:17 
'''
# 网站：https://www.fxbaogao.com

import execjs
import requests
import time

headers = {
    'authority': 'api.fxbaogao.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'content-type': 'application/json; charset=UTF-8',
    'origin': 'https://www.fxbaogao.com',
    'referer': 'https://www.fxbaogao.com/',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'user-id': '0',
    'user-token': 'QQ',
}

def get_pas_word(e_dic,this_time):
    filename_js = 'get_pw.js'
    with open(filename_js, encoding='utf-8', mode='r') as f:
        pw_js = f.read()
        f.close()
    js1 = execjs.compile(pw_js)

    print('********* 正在生成 -- pas_word *********')
    pas_word = js1.call('get_pas_word', e_dic,this_time)         # 获取token
    print(pas_word)
    return pas_word

def login():
    this_time = int(time.time())
    e_dic = {
        "mobile": "17688688515",
        "password": "123wu123123"
    }
    pas_word = get_pas_word(e_dic,this_time)

    json_data = {
        'mobile': '17688688515',
        'data': pas_word,
        'time': this_time,
    }
    #
    session = requests.session()
    # response = requests.post('https://api.fxbaogao.com/mofoun/user/login/byPhoneNumber', headers=headers,
    #                          json=json_data)
    response1 = session.post('https://api.fxbaogao.com/mofoun/user/login/byPhoneNumber', headers=headers,json=json_data)
    print(response1.text)

if __name__ == '__main__':
    login()


