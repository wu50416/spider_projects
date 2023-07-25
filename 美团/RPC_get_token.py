# -*- coding: UTF-8 -*-
'''
@Project ：wbh_pj 
@File ：RPC_Demo.py
@Author ：hao
@Date ：2023/6/30 16:58 
'''
# 使用RPC获取美团token
import requests

def get_token(url):
    js_data = f'''
    var a1 = window.get_token("{url}")
    resolve(abc)
    '''
    params = {
        'group':'ftx-group',
        'action':'executeJs',
        'code':'abc',           # 示例参数，这个参数值放啥都行，仅用于示例
        'js_data':js_data       # 需要执行的 js 代码
    }
    # 使用前记得打开 RPC 端口
    # http://127.0.0.1:6001/business-demo/invoke?group=ftx-group&action=executeJs&code=abc
    RPC_url = "http://127.0.0.1:6001/business-demo/invoke"          # 固定的

    res = requests.get(url = RPC_url,params=params)
    try:
        res_data = res.json()['data']        # 获取cookie数据
        print(res_data)
    except Exception as e:
        print("数据获取失败，响应为： ",res.text)
    return res_data

def run():

    url = "https://gz.meituan.com/meishi/api/poi/getPoiList?cityName=广州&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=2&userId=754270772&uuid=28725e29921749e7a78f.1685590514.1.0.0&platform=1&partner=126&originUrl=https://gz.meituan.com/meishi/pn2/&riskLevel=1&optimusCode=10"
    _token = get_token(url)
    print(_token)


if __name__ == '__main__':
    run()

