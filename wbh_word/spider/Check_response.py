# -*- coding: UTF-8 -*-
'''
@Project ：yj_pj 
@File ：Check_response.py
@Author ：hao
@Date ：2023/3/28 17:01 
'''
import cchardet


def check_response(response):
    encoding = cchardet.detect(response.content)["encoding"]
    print(f"当前响应编码为：{encoding}")
    return encoding