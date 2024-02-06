#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/17 18:53
# @Author  : Harvey
# @File    : run_new.py
# -*- coding: UTF-8 -*-
import datetime
import json
from urllib.parse import urlencode
import requests
import execjs
import pandas as pd

'''
反爬更新说明：
    2024-02-06：
    1、不登陆时，cookie新增了ttwid参数，由原先的检测s_v_web_id，现在更新为检测ttwid
    2、未登录不允许翻页
    3、登陆后有携带sessionid与sessionid_ss，可以不用X-Bogus
'''

def get_xb_data(urlform):
    filename_js = 'get_XBogus2.js'
    with open(filename_js,  mode='r') as f:
        pw_js = f.read()
        f.close()
    js1 = execjs.compile(pw_js)
    print('********* 正在生成 -- XBogus *********')
    xb_data = js1.call('get_xb', urlform)         # 获取token
    print(xb_data)
    return xb_data


def get_headers():
    # 20240117更新：之前是检测s_v_web_id，现在更新为检测ttwid
    # 未登录的cookie
    # cookies = {
    #     "ttwid": "1%7CvSGoO5ZPPEgIIWpNoRr0YCmMrWzQACoN1hNhqxBsexQ%7C1705490555%7C9d5ecaae8cae4fc1ef856f7de5f31a991a4d9a459b738888c7525070d1e806d0",
    #     # "s_v_web_id": "verify_lqw9zg13_3aUMuPsb_dPTm_4QA0_8Msc_wKAv0zy96U0j",
    # }
    # 登陆后的cookie：
    cookies = {
        "sessionid": "xxxxxxxxxxxx",
        "sessionid_ss": "xxxxxxxxxxxx",
    }
    headers = {
        "referer": "https://www.douyin.com/",
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    return cookies,headers


def get_cursor(page):
    '''
    :param page: 从第 1 页开始，
    :return: cursor 为评论开始的位置（起始为0），count为一次读取多少个评论（最高50）
    '''
    count = 20
    cursor = (page-1) * count       # (1-1)*50 = 0
    return cursor, count


def dispose_params(params_data):
    '''
    将 "X-Bogus" 插入 params 中，同时获取 url
    :param params_data:
    :return:
    '''
    params_ = urlencode(params_data).replace('%3D', '=')  # 转换完后有部分格式问题需要修改
    xb_data = get_xb_data(params_)
    params = params_ + '&X-Bogus=' + xb_data
    url = 'https://www.douyin.com/aweme/v1/web/comment/list/?' + params
    return url


def get_url(page,aweme_id):
    '''
    "aweme_id": "7284507907465481512",  # 视频id
    "cursor": "0",                      # 起始评论位置
    "count": "50",                      # 一次获取的条数，最多50条
    msToken : 固定值
    "X-Bogus" ： 根据不带"X-Bogus"的params数据加密生成
    :return: params(无xb参数的params)
    '''
    cursor,count = get_cursor(page)
    params_data = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "aweme_id": aweme_id,
        "cursor": cursor,
        "count": count,
        "item_type": "0",
        "insert_ids": "",
        "whale_cut_token": "",
        "cut_version": "1",
        "rcFT": "",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1920",
        "screen_height": "1080",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "120.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "120.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "6",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "50",
        "webid": "7325026101045102121",
        "msToken": "",
        # "X-Bogus": "DFSzswVLhOJANcLLti0PqvB9Piz9"
    }
    url = dispose_params(params_data)
    print(url)
    return url


def dispose_comments(comments,data_list):
    for comment_one in comments:
        # ============ 用户个人信息部分 ===========
        nickname = comment_one['user']['nickname']  # 用户名
        user_id = comment_one['user']['short_id']  # 用户id
        signature = comment_one['user']['signature']  # 用户个性签名
        head_image = comment_one['user']['avatar_medium']['url_list'][0]  # 中等大小的头像
        user_url_ = comment_one['user']['sec_uid']
        user_url = 'https://www.douyin.com/user/' + user_url_
        # ============ 用户个人信息部分 ===========
        pinlun_cid = comment_one['cid']  # 后续展开回复评论的请求id（comment_id）

        text_data = comment_one['text']  # 评论内容
        digg_count = comment_one['digg_count']  # 点赞数
        reply_comment_total = comment_one['reply_comment_total']  # 评论数
        create_time_str = comment_one['create_time']  # 评论时间
        create_time = datetime.datetime.fromtimestamp(create_time_str)
        try:
            ip_label = comment_one['ip_label']
        except:
            ip_label = "未知ip"

        print(f"用户名：{nickname} 用户id : {user_id} , ip地址 : {ip_label} , 评论 : {text_data} , "
              f"回复数：{reply_comment_total}  , 点赞数：{digg_count}  , 回复时间：{create_time}")
        data_one_dict = {"用户id":user_id,"用户名":nickname,"用户链接":user_url,"用户头像":head_image,"ip地址":ip_label,
                         "评论":text_data,"回复数":reply_comment_total,"点赞数":digg_count,"个性签名":signature,"回复时间":create_time}

        PL_image_bool = comment_one['image_list']  # 判断评论是否有图片
        if PL_image_bool:
            PL_image = PL_image_bool[0]['origin_url']['url_list'][0]
            data_one_dict['PL_image']=PL_image
        data_list.append(data_one_dict)
    return data_list


def run():
    aweme_id_list = ["7306459845480254754"]
    for aweme_id in aweme_id_list:
        file_name = 'data/' + aweme_id + 'asda.xlsx'
        cookies,headers = get_headers()
        max_page = 5  # 获取100页数据（100*50=5000）条评论
        data_list = []
        for page in range(1,max_page+1):
            print(f"============= 正在获取第 {page} 页数据 =============")
            url = get_url(page,aweme_id)
            response = requests.get(url, headers=headers, cookies=cookies)
            print(response.text)
            if response.json().get("status_msg",None) == "blocked":
                break
            comments = response.json()['comments']
            if comments:
                print(f"当前有 {len(response.json()['comments'])} 条数据")
                data_list = dispose_comments(comments,data_list)
            else:
                break

        df_data = pd.DataFrame.from_dict(data_list)         # 字典列表转pandas
        print(df_data)
        df_data.to_excel(file_name,index=False)


if __name__ == '__main__':
    run()



