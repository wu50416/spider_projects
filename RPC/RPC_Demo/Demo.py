# -*- coding: UTF-8 -*-
'''
@Project ：wbh_pj 
@File ：RPC_Demo.py
@Author ：hao
@Date ：2023/6/30 16:58 
'''

import requests


js_data = '''
var abc = "abcabc"
resolve(abc)
'''

params = {
    'group':'ftx-group',
    'action':'executeJs',
    'code':'abc',           # 示例参数，这个参数值放啥都行，仅用于示例
    'js_data':js_data        # 需要执行的 js 代码 没有这个参数则默认返回 document.cookie
}
# 使用前记得打开 RPC 端口
# http://127.0.0.1:6001/business-demo/invoke?group=ftx-group&action=executeJs&code=abc
url = "http://127.0.0.1:6001/business-demo/invoke"          # 固定的

res = requests.get(url = url,params=params)
print(res.text)

'''
try:
    cookies = res.json()['data']        # 获取cookie数据
    print(cookies)
except Exception as e:
    print("数据获取失败，响应为： ",res.text)
'''
