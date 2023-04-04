# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj
@File ：Get_response.py
@Author ：hao
@Date ：2022/12/8 10:57 
'''
# 111
from wbh_word.spider import Get_ip
import requests
import time
import random

def get_html_response(url,headers=None, params=None,data=None, proxies=None,cookies=None,timeout=5,time_sleep=(0,1)):      # time_sleep=(0.5,1.5)
    try:
        response = requests.get(url=url, headers=headers, params=params,data=data,
                                proxies=proxies,cookies=cookies, timeout=timeout)
        if time_sleep != (0, 0):
            time.sleep(float(random.randint(time_sleep[0]*1000, time_sleep[1]*1000)) / 1000)    # 随机暂停1~2秒
        if response.status_code != 200:
            print(f"response状态码: {response.status_code}  不为200！重新请求")
            raise
    except Exception as e:
        print(f"访问失败 e: {e}  重新请求")
        if proxies:     # 判断是否需要携带ip
            proxies = Get_ip.ip_proxies()
        response, proxies = get_html_response(url,headers, params,data=data,
                                              proxies=proxies,cookies=cookies,timeout=timeout,time_sleep=time_sleep)
    return response, proxies

# 这里是post请求
def post_html_response(url,headers=None, params=None,data=None, proxies=None,cookies=None,timeout=5,time_sleep=(0,1)):
    try:
        response = requests.post(url=url, headers=headers, params=params,data=data,
                                 proxies=proxies,cookies=cookies, timeout=timeout)
        if time_sleep != (0, 0):
            time.sleep(float(random.randint(time_sleep[0]*1000, time_sleep[1]*1000)) / 1000)    # 随机暂停1~2秒
        if response.status_code != 200:     # html只能通过状态来判断
            print(f"response状态码: {response.status_code}  不为200！重新请求")
            raise
    except Exception as e:
        print(f"访问失败 e: {e}  重新请求")
        if proxies:     # 判断是否需要携带ip
            proxies = Get_ip.ip_proxies()
        response, proxies = post_html_response(url,headers, params,data=data,
                                               proxies=proxies,cookies=cookies,timeout=timeout,time_sleep=time_sleep)
    return response, proxies


def get_json_response(url,headers=None, params=None,data=None, proxies=None,cookies=None,timeout=5,time_sleep=(0,1)):
    try:
        response = requests.get(url=url, params=params, headers=headers,data=data,
                                proxies=proxies,cookies=cookies,timeout=timeout).json()
        if time_sleep != (0, 0):
            time.sleep(float(random.randint(time_sleep[0]*1000, time_sleep[1]*1000)) / 1000)    # 随机暂停1~2秒
    except Exception as e:
        print(f"访问失败 e: {e}  重新请求")
        if proxies:     # 判断是否需要携带ip
            proxies = Get_ip.ip_proxies()
        response, proxies = get_json_response(url,headers, params,data=data,
                                              proxies=proxies,cookies=cookies,timeout=timeout,time_sleep=time_sleep)
    return response, proxies

def post_json_response(url,headers=None, params=None,data=None, proxies=None,cookies=None,timeout=5,time_sleep=(0,1)):
    try:
        response = requests.post(url=url, params=params, headers=headers,data=data,
                                 proxies=proxies,cookies=cookies,timeout=timeout).json()
        if time_sleep != (0,0):
            time.sleep(float(random.randint(time_sleep[0]*1000, time_sleep[1]*1000)) / 1000)    # 随机暂停1~2秒
    except Exception as e:
        print(f"访问失败 e: {e}  重新请求")
        if proxies:     # 判断是否需要携带ip
            proxies = Get_ip.ip_proxies()
        response, proxies = post_json_response(url,headers, params,data=data,
                                               proxies=proxies,cookies=cookies,timeout=timeout,time_sleep=time_sleep)
    return response, proxies


if __name__ == '__main__':
    pass




